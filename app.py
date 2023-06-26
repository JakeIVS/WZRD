#!/usr/bin/env python

import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from classes.models import Spell, User, Base


if __name__ == '__main__':
    print('''
         _    _  ____________ ______
        | |  | ||___  /| ___ \|  _  \ 
        | |  | |   / / | |_/ /| | | |
        | |/\| |  / /  |    / | | | |
        \  /\  /./ /___| |\ \ | |/ /
         \/  \/ \_____/\_| \_||___/


                1) Login
                2) New User
                0) Exit
    ''' )

    engine = create_engine('sqlite:///users.db')
    start_option = int(input('Choose Option: '))
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    while start_option != 0:
        if start_option is 1:
            print('Choose User:')
            user_list = session.query(User).all()
            for user in user_list:
                print(f'{user.id}) {user.username}')
            user_select = input("Select User: ")


        if start_option is 2:

            username = str(input('Enter your name >>> '))
            pass1 = str(input('Enter your new password >>> '))
            pass2 = str(input('Re-enter your password >>> '))
            if pass1 == pass2:
                user = User(username = username, password = pass1)
                session.add(user)
                session.commit()