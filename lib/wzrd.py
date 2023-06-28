#!/usr/bin/env python

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from models import Spell, User, Character, Base
import os
import time


def initialize():
    clear_terminal()
    print('''
                1) Login
                2) New User
                0) Exit
    ''' )
    start_option = int(input('Choose Option: '))

    while start_option != 0:
        if start_option == 1:
            choose_user()            
            

        if start_option == 2:
            new_user()



def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('''
         _    _  ____________ ______
        | |  | ||___  /| ___ \|  _  \ 
        | |  | |   / / | |_/ /| | | |
        | |/\| |  / /  |    / | | | |
        \  /\  /./ /___| |\ \ | |/ /
         \/  \/ \_____/\_| \_||___/



    ''')
    


def choose_user():
    clear_terminal()
    print('             Users:')
    user_list = session.query(User).all()
    valid_user_ids = []
    for user in user_list:
        valid_user_ids.append(user.user_id)
        print(f'            {user.user_id}) {user.username}')
    if valid_user_ids == []:
        print('No users exist')
        print('1) Create New User')
        print('2) Exit')
        choice = int(input('Choose option: '))
        if choice == 1:
            new_user()
        else:
            exit()
    else:
        user_select = int(input('Select User: '))
        if user_select in valid_user_ids:
            current_user_id = user_select
            user_menu(current_user_id)
        else:
            print('Invalid input')
            choice = input('Exit? (y/n): ')
            if choice == 'y':
                exit()
            else:
                choose_user()
    

def new_user():
    clear_terminal()
    existing_users = session.query(User.username).all()
    username = str(input('Enter your name >>> '))
    pass1 = str(input('Enter your new password >>> '))
    pass2 = str(input('Re-enter your password >>> '))
    if (username,) not in existing_users:
        if pass1 == pass2:
            user = User(username = username, password = pass1)
            session.add(user)
            session.commit()
            query = session.query(User).filter(User.username == username).first()
            current_id = query.user_id
            user_menu(current_id)

        else:
            print('Passwords do not match')
            choice = input ('Exit? (y/n): ')
            if choice == 'y':
                exit()
            else:
                new_user()
            
    else:
        print('user already exists')
        choice = input ('Exit? (y/n): ')
        if choice == 'y':
            exit()
        else:
            new_user()

def user_menu(current_user_id):
    clear_terminal()

    current_user = session.query(User).filter(User.user_id == int(current_user_id)).first()
    print(f'''
                Welcome, {current_user.username}!

               Choose a character:
    ''')
    character_query = session.query(Character).filter(Character.owner == current_user_id).all()
    valid_char_choices = []
    for character in character_query:
        valid_char_choices.append(character.character_id)
        print(f"{character.character_id}) {character.name}")
    if valid_char_choices != []:
        print('''
        -or-
    ''')
    print('0) Create New Character')  
    choice = int(input ('Choose Character: '))
    if choice == 0:
        create_character(current_user_id)
        user_menu(current_user_id)
    elif choice in valid_char_choices:
        character_menu(choice, current_user_id)
    else:
        print('Not a valid response.')


def character_menu(char_id, current_user_id):
    clear_terminal()

    character = session.query(Character).filter(Character.character_id == char_id).first()
    print(f"""
          Character: {character.name}
          --------------------------------
          Level {character.level} | {character.gold} gp

                    1) View Spellbook
                    2) Manage Spellbook
                    3) Manage Gold
                    4) Manage Level



                    0) Delete Character
    """)
    
    choice = input("Choose Option: ")
    if choice == '3':
        print(f'''
              {character.name}

              Current Gold: {character.gold} gp

              1) Add
              2) Remove


              
        ''')
        change = input("Choose Option: ")
        if change == '1':
            new_gp = int(character.gold) + int(input('Gold to add >>> '))
            character.gold = new_gp
            session.commit()
            character_menu(char_id, current_user_id)
        if change == '2':
            new_gp = int(character.gold) - int(input('Gold to Remove >>> '))
            if new_gp >= 0:
                character.gold = new_gp
                session.commit()
                character_menu(char_id, current_user_id)
            else:
                print('Insufficient funds')
                time.sleep(2)
                character_menu(char_id, current_user_id)

    if choice == '0':
        selected_character = session.query(Character).filter(Character.character_id == char_id)
        confirm = input(f'{selected_character[0].name} will be deleted. (type DELETE to confirm): ')
        if confirm == 'DELETE':
            selected_character.delete()
            session.commit()
            user_menu(current_user_id)

def create_character(user_id):
    new_name = str(input('Name Your Character >>> '))
    starting_level = int(input('What is your character\'s current level? >>> '))
    starting_gold = int(input('How much gold do your character have? >>> '))
    print(f'''
        name: {new_name}
        level: {starting_level}
        gold: {starting_gold}
    '''
    )
    confirm = input('Confirm? (y/n): ')
    if confirm == 'y':
        new_character = Character(
            owner = user_id,
            name = new_name,
            level = starting_level,
            gold = starting_gold
        )
        session.add(new_character)
        session.commit()
    else:
        exit()
    



if __name__ == '__main__':
    engine=create_engine('sqlite:///program.db')
    Session= sessionmaker(bind=engine)
    session = Session()
    current_user_id = None

    initialize()