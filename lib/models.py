from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

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
    characters = relationship('Character', backref='users')

    def __repr__(self):
        return f"User: {self.username}"

    
class Character(Base):
    __tablename__ = 'characters'

    id = Column(Integer(), primary_key=True)
    owner = Column(Integer(), ForeignKey('users.id'))
    name = Column(String())
    level = Column(Integer())
    gold = Column(Integer())

    def __repr__(self):
        return f'''
        {self.name} (Level {self.level})
        {self.gold} Gold
        '''