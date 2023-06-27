#!/usr/bin/env python 

import requests 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Spell

if __name__ == '__main__':
    engine = create_engine('sqlite:///program.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    response = requests.get('https://www.dnd5eapi.co/api/spells').json()
    spell_list = response['results']

    # clear old data
    session.query(Spell).delete()
    session.commit()

    # add new data
    print('Seeding spell list...')
    for spell in spell_list:
        spells = []
        url = spell['url']
        spell_response = requests.get(f'https://www.dnd5eapi.co{url}')
        fetched_spell = spell_response.json()
        if {"index": "wizard", "name": "Wizard", "url": "/api/classes/wizard"} in fetched_spell['classes']:
            spell = Spell(
                name = fetched_spell['name'],
                level = fetched_spell['level'],
                range = fetched_spell['range'],
                casting_time = fetched_spell['casting_time'],
                duration = fetched_spell['duration'],
                description = " ".join(fetched_spell['desc']),
                higher_level = " ".join(fetched_spell['higher_level'])
            )
            
            session.add(spell)
            session.commit()

            spells.append(spell)

    print('Complete!')
        
