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


events_2025 = [
    ['genesis-x2', 'melee-singles', SUPER_MAJOR],
    ['battle-of-bc-7-6', 'main-event-melee-singles', SUPER_MAJOR],
    ['nouns-bowl-2025', 'melee-singles', SUPER_MAJOR],
    # ['valhalla-v', 'main-melee-singles', MAJOR],
    ['full-house-2025', 'main-bracket', SUPER_INVITATIONAL],
    ['tipped-off-16-safari', 'melee-singles', SUPER_MAJOR]
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


for event in events_2024:
    update_ssbm_rank('2024', event)

for event in events_2025:
    update_ssbm_rank('2025', event)

with open('assets/rankings/rank_data.json', 'r') as rank_file:
    rank_data = json.load(rank_file)
    i=1
    for player in rank_data:
        print(f'{i}. {rank_data[player]['player']} --> {rank_data[player]['points']} pts')
        i += 1
        if player == "80454":
            print(player, i)
            break
        
