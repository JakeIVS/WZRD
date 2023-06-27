from sqlalchemy import Column, Integer, String, ForeignKey, Table, MetaData
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)


character_spell = Table(
    'character_spell',
    Base.metadata,
    Column('character_id', ForeignKey('characters.id', primary_key=True)),
    Column('spell_id', ForeignKey('users.id', primary_key=True)),
    extend_existing=True,
)

class Spell(Base):
    __tablename__ = 'spells'

    id = Column(Integer(), primary_key=True)
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
            shown_level = '1st'
        elif self.level is 2:
            shown_level = '2nd'
        elif self.level is 3:
            shown_level = '3rd'
        else:
            shown_level = str(self.level + 'th')
        return f'''
            {self.name}:
            {shown_level} level spell
            Range: {self.range} | Cast Time: {self.casting_time} | Duration: {self.duration}
            ---
            {self.description}
            ---
            {self. higher_level}
        '''

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    username = Column(String())
    password = Column(String())
    characters = relationship('Character', backref='users', cascade='all, delete-orphan')

    def __repr__(self):
        return f"User: {self.username}"

    
class Character(Base):
    __tablename__ = 'characters'

    id = Column(Integer(), primary_key=True)
    owner = Column(Integer(), ForeignKey('users.id'))
    name = Column(String())
    level = Column(Integer())
    gold = Column(Integer())

    spells = relationship('Spell', secondary=character_spell, back_populates='characters')

    def __repr__(self):
        return f'''
        {self.name} (Level {self.level})
        {self.gold} Gold
        '''