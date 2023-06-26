#!/usr/bin/env python 

import requests 
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from classes.models import Spell, Base

engine = create_engine('sqlite:///spells.db')
Base.metadata.create_all(engine)

response = requests.get('https://www.dnd5eapi.co/api/spells').json()
spell_list = response['results']




print('Seeding spell list...')
for spell in spell_list:
    url = spell['url']
    spell_response = requests.get(f'https://www.dnd5eapi.co{url}')
    fetched_spell = spell_response.json()
    if {"index": "wizard", "name": "Wizard", "url": "/api/classes/wizard"} in fetched_spell['classes']:
        Session = sessionmaker(bind=engine)
        session = Session()
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
print('Complete!')
        
