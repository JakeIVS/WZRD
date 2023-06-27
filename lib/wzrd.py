#!/usr/bin/env python

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from models import Spell, User, Character, Base
import os



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
    print('Users:')
    user_list = session.query(User).all()
    valid_user_ids = []
    for user in user_list:
        valid_user_ids.append(user.id)
        print(f'{user.id}) {user.username}')
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
            current_id = query.id
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

def user_menu(current_id):
    clear_terminal()

    current_user = session.query(User).filter(User.id == int(current_id)).first()
    print(f'''
        Welcome, {current_user.username}!


    ''')
    character_query = session.query(Character).filter(Character.owner == current_id).all()
    valid_char_choices = []
    print('1) Create new Character')
    for character in character_query:
        char_choice = character.id + 1
        valid_char_choices.append(char_choice)
        print(f"{char_choice}) {character.name}")
    choice = int(input ('Choose Character: '))
    print(type(choice))
    if choice == 1:
        create_character(current_id)
        user_menu(current_id)
    elif type(choice) == int:
        char_id = choice -1
        character_menu(char_id)


def character_menu(id):
    clear_terminal()

    character = session.query(Character).filter(Character.id == id).first()
    print(f"Now showing {character.name}")
    choice = input("Exit? (y/n)")
    if choice == 'y':
        exit()

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

    clear_terminal()
    print('''
                1) Login
                2) New User
                0) Exit
    ''' )
    current_user_id = None
    start_option = int(input('Choose Option: '))

    while start_option != 0:
        if start_option == 1:
            choose_user()            
            

        if start_option == 2:
            new_user()
