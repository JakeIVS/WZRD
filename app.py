#!/usr/bin/env python

import requests
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from classes.models import Spell, User, Base

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
    print('1) Create new Character')
    choice = input ('Exit? (y/n): ')
    if choice == 'y':
        exit()



if __name__ == '__main__':
    clear_terminal()
    print('''
                1) Login
                2) New User
                0) Exit
    ''' )
    current_user_id = None
    engine = create_engine('sqlite:///users.db')
    start_option = int(input('Choose Option: '))
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    while start_option != 0:
        if start_option is 1:
            choose_user()            
            

        if start_option is 2:
            new_user()
