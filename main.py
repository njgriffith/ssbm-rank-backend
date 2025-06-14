import scrape
import update_rankings

def update_ssbm_rank(event_name, event_category):
    scrape.scrape(event_name)
    update_rankings.update_rankings(event_name, event_category)


events_2025 = [
    ('genesis-x2', 'super_major'),
    ('battle-of-bc-7-6', 'super_major'),
    ('nouns-bowl-2025', 'super_major'),
    ('full-house-2025', 'super_invitational'),
    ('tipped-off-16-safari', 'super_major')
]

for event in events_2025:
    update_ssbm_rank(event[0], event[1])
