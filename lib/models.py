from sqlalchemy import Column, Integer, String, ForeignKey, Table, MetaData, create_engine
from sqlalchemy.orm import declarative_base, relationship, backref

engine = create_engine('sqlite:///program.db')

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

character_spell = Table(
    'character_spell',
    Base.metadata,
    Column('character_id', ForeignKey('characters.character_id', primary_key=True)),
    Column('spell_id', ForeignKey('spells.spell_id', primary_key=True)),
    extend_existing=True,
)

class Spell(Base):
    __tablename__ = 'spells'

    spell_id = Column(Integer(), primary_key=True)
    name = Column(String())
    level = Column(Integer())
    range = Column(String())
    casting_time = Column(String())
    duration = Column(String())
    description = Column(String())
    higher_level = Column(String())

    characters = relationship('Character', secondary=character_spell, back_populates='spells')

    def __repr__(self):
        shown_level = None
        if self.level is 0:
            shown_level = 'Cantrip'
        elif self.level is 1:
            shown_level = '1st Level Spell'
        elif self.level is 2:
            shown_level = '2nd Level Spell'
        elif self.level is 3:
            shown_level = '3rd Level Spell'
        else:
            shown_level = str(self.level + 'th Level Spell')
        return f'''
{self.name}:
{shown_level}
Range: {self.range} | Cast Time: {self.casting_time} | Duration: {self.duration}
---
{self.description}
---
{self. higher_level}
        '''

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer(), primary_key=True)
    username = Column(String())
    password = Column(String())
    characters = relationship('Character', backref=backref('users'), cascade='all, delete-orphan')

    def __repr__(self):
        return f"User: {self.username}"

    
class Character(Base):
    __tablename__ = 'characters'

    character_id = Column(Integer(), primary_key=True)
    owner = Column(Integer(), ForeignKey('users.user_id'))
    name = Column(String())
    level = Column(Integer())
    gold = Column(Integer())

    spells = relationship('Spell', secondary=character_spell, back_populates='characters')

    def __repr__(self):
        return f'''
        {self.name} (Level {self.level})
        {self.gold} Gold
        '''