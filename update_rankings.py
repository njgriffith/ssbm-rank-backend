import pandas as pd
import json
from datetime import date, datetime
import math

NUM_BEST_EVENTS = 10

def update_rankings(year, event_name, event_classification):
    print(f'\nSTART: Updating rankings for {event_name}')
    df = pd.read_csv(f'assets/results/{year}/{event_name}_standings.csv')
    last_place = max(df['placement'])
    with open('assets/rankings/rank_data.json', 'r') as rank_file:
        rank_data = json.load(rank_file)
    with open('assets/tourney_classes.json') as classification_file:
        classification_data = json.load(classification_file)
    event_id = str(df.loc[0, 'event_id'])
    event_date = str(df.loc[0, 'event_date'])

    # entrant_id, entrant_name, placement
    for _, row in df.iterrows():
        if row['placement'] == last_place and ('INVITATIONAL' not in event_classification):
            print('Outside bounds for point allocation, last place')
            break
        try:
            points = int(classification_data[event_classification][str(row['placement'])])
        except KeyError:
            print('Outside bounds for point allocation')
            break
        new_event = {
            event_id: {
                "event_name": event_name,
                "event_date": event_date,
                "placement": row["placement"],
                "points": points
            }
        }
        # if existing player
        try:
            user_id = str(int(row['user_id']))
        except ValueError:
            print(f'No user ID for {row}, creating new player')
            continue
        
        # null
        if user_id == '8572':
            row['entrant_name'] = 'null'
        # Zain/jmmok alt
        if user_id == '2669494':
            user_id = '2616'
        if user_id == '2636297':
            user_id = '10563'
        if user_id in rank_data:
            update_player_rank(rank_data[user_id], new_event)
            # update gamertag to latest
            rank_data[user_id]['player'] = row['entrant_name']

        # else, new player
        else:
            new_player = {
                "player": row['entrant_name'],
                "points": points,
                "events": new_event,
                "best_events": new_event
            }
            rank_data[user_id] = new_player
    
    print('Preliminary update complete')

    expired_events = remove_expired_events(rank_data, event_date)
    print(f'Removed expired events: {expired_events}')

    sorted_data = dict(sorted(rank_data.items(), key=lambda item: int(item[1]["points"]), reverse=True))
    print('Sorted rankings')

    with open('assets/rankings/rank_data.json', 'w', encoding='utf-8') as rank_file:
        json.dump(sorted_data, rank_file, indent=4)
    with open(f'assets/rankings/{event_date}_rank_data.json', 'w', encoding='utf-8') as rank_file:
        json.dump(sorted_data, rank_file, indent=4)
    print(f'END: Updating rankings for {event_name}\n')


def update_player_rank(player_data, new_event):
    event_id, event_info = next(iter(new_event.items()))    
    player_data.setdefault("events", {})[event_id] = event_info
    new_points = int(event_info["points"])
    best_events = player_data.setdefault("best_events", {})
    
    if len(best_events) < NUM_BEST_EVENTS:
        best_events[event_id] = event_info
        player_data["points"] = int(player_data.get("points", 0)) + new_points
        return

    # Find current lowest scoring event in top 10
    lowest_event_id, lowest_event_info = min(
        best_events.items(), key=lambda item: int(item[1]["points"])
    )

    if new_points > int(lowest_event_info["points"]):
        # Replace lowest scoring event
        del best_events[lowest_event_id]
        best_events[event_id] = event_info

        # Recalculate total points from best events
        player_data["points"] = sum(int(e["points"]) for e in best_events.values())

def remove_expired_events(data, event_date):
    today = date.fromisoformat(event_date)
    try:
        cutoff_date = today.replace(year=today.year - 1)
    except ValueError:
        # Handles February 29 edge case
        cutoff_date = today.replace(month=2, day=28, year=today.year - 1)

    expired_events = set()
    players_to_remove = []
    for player_id, player_data in data.items():
        new_events = {}
        new_best_events = {}
        new_points = 0

        # Filter 'events'
        for event_id, event in player_data.get("events", {}).items():
            event_date = datetime.strptime(event["event_date"], "%Y-%m-%d").date()
            if event_date > cutoff_date:
                new_events[event_id] = event
                new_points += int(event["points"])
            else:
                expired_events.add(event_id)

        # Filter 'best_events' by event_id
        for event_id, event in player_data.get("best_events", {}).items():
            if event_id not in expired_events:
                new_best_events[event_id] = event

        # Update player data
        player_data["events"] = new_events
        player_data["best_events"] = new_best_events
        player_data["points"] = sum(int(event["points"]) for event in new_best_events.values())
        if new_points == 0:
            players_to_remove.append(player_id)
    print(f'Removing {len(players_to_remove)} inactive players')
    for player in players_to_remove:
        del data[player]

    return expired_events
