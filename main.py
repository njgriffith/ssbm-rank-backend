import scrape
import update_rankings
import json

def update_ssbm_rank(year, event_data):
    tourney_name_code = event_data[0]
    event_name_code = event_data[1]
    event_category = event_data[2]
    # scrape.scrape(tourney_name_code, event_name_code)
    update_rankings.update_rankings(year, tourney_name_code, event_category)

SUPER_MAJOR = 'super_major'
MAJOR = 'major'
SUPER_INVITATIONAL = 'super_invitational'
SUPER_REGIONAL = 'super-regional'


events_2025 = [
    ['genesis-x2', 'melee-singles', SUPER_MAJOR],
    ['battle-of-bc-7-6', 'main-event-melee-singles', MAJOR],
    ['nouns-bowl-2025', 'melee-singles', MAJOR],
    ['valhalla-v', 'main-melee-singles', SUPER_REGIONAL],
    ['full-house-2025', 'main-bracket', SUPER_INVITATIONAL],
    ['tipped-off-16-safari', 'melee-singles', SUPER_MAJOR],
    ['get-on-my-level-forever-canadian-fighting-game-championships', 'super-smash-bros-melee-singles', SUPER_MAJOR],
    ['supernova-2025', 'melee-1v1-singles', SUPER_MAJOR],
    ['collision-2025-8', 'melee-singles', SUPER_MAJOR],
    ['riptide-2025-4', 'melee-singles', MAJOR],
    ['nounsvitational-2025-tokyo', 'melee-singles', SUPER_INVITATIONAL]
]

events_2024 = [
    ['genesis-x', 'melee-singles', SUPER_MAJOR],
    ['collision-2024-6', 'melee-singles', SUPER_MAJOR],
    ['battle-of-bc-6-7', 'melee-singles', SUPER_MAJOR],
    ['pat-s-house-4-2', 'melee-singles', SUPER_MAJOR],
    ['get-on-my-level-x-canadian-fighting-game-championships', 'super-smash-bros-melee-singles', SUPER_MAJOR],
    ['tipped-off-15-connected-1', 'melee-singles', SUPER_MAJOR],
    ['supernova-2024', 'melee-1v1-singles', SUPER_MAJOR],
    ['eggdog-invitational', 'final-bracket-sunday', SUPER_INVITATIONAL],
    ['riptide-2024-5', 'melee-singles', SUPER_MAJOR],
    ['wavelength-2024', 'melee-singles', SUPER_MAJOR],
    ['luminosity-makes-moves-miami-2024', 'melee-singles', SUPER_MAJOR],
    # ['sapf', 'melee-singles', MAJOR],
    ['don-t-park-on-the-grass-2024', 'melee-singles', SUPER_MAJOR],
    ['nounsvitational-2024', 'melee-singles', SUPER_INVITATIONAL]
]


# for event in events_2024:
#     update_ssbm_rank('2024', event)

# for event in events_2025:
#     update_ssbm_rank('2025', event)

def print_rankings(n):
    with open('assets/rankings/rank_data.json', 'r') as rank_file:
        rank_data = json.load(rank_file)
        i=1
        for player in rank_data:
            print(f'{i}. {rank_data[player]['player']} --> {rank_data[player]['points']} pts ({len(rank_data[player]['events'].keys())} events entered)')

            if i > 90 :
                print('\tDetails:')
                for event in sorted(rank_data[player]['best_events'].values(),
                    key=lambda item: item["points"], reverse=True):
                    print(f'\t\tEvent: {event['event_name']}, Placement: {event['placement']}, Points Awarded: {event['points']}')

            i += 1
            if i > n:
                break

print_rankings(100)