#!/usr/bin/env python
from termcolor import colored
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import declarative_base, sessionmaker
from models import Spell, User, Character, character_spell
import os
import time

# creates initial login screen
# 
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
    print(colored('''
         _    _  ____________ ______
        | |  | ||___  /| ___ \|  _  \ 
        | |  | |   / / | |_/ /| | | |
        | |/\| |  / /  |    / | | | |
        \  /\  /./ /___| |\ \ | |/ /
         \/  \/ \_____/\_| \_||___/

    ''', 'blue'))
    


def choose_user():
    clear_terminal()
    print('     Users:')
    user_list = session.query(User).all()
    valid_user_ids = []
    for user in user_list:
        valid_user_ids.append(user.user_id)
        print(f'            {user.user_id}) {user.username}')
    if valid_user_ids == []:
        print('     No users exist')
        print('     1) Create New User')
        print('     0) Exit')
        choice = int(input('Choose option: '))
        if choice == 1:
            new_user()
        else:
            initialize()
    else:
        user_select = int(input('Select User: '))
        if user_select in valid_user_ids:
            password = input('Enter Password >>> ')
            user = session.query(User).filter(User.user_id == user_select).first()
            if password == user.password:
                current_user_id = user_select
                user_menu(current_user_id)
            else:
                clear_terminal()
                print(colored('     Incorrect password', 'red'))
                time.sleep(1)
                choose_user()
        else:
            print(colored('     Invalid input', 'red'))
            choice = input('Exit? (y/n): ')
            if choice == 'y':
                initialize()
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
            print(colored('     Passwords do not match', 'red'))
            choice = input ('Exit? (y/n): ')
            if choice == 'y':
                initialize()
            else:
                new_user()
            
    else:
        print(colored('     user already exists', 'red'))
        choice = input ('Exit? (y/n): ')
        if choice == 'y':
            initialize()
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
        print(f"        {character.character_id}) {character.name}")
    if valid_char_choices != []:
        print('''
                 -or-

        NEW) Create New Character
        0) Logout
    ''')
    choice = input ('Choose Character: ')
    if choice == 'NEW':
        create_character(current_user_id)
        user_menu(current_user_id)
    elif choice == '0':
        initialize()
    elif int(choice) in valid_char_choices:
        character_menu(int(choice), character.owner)
    else:
        print(colored('     Not a valid response.', 'red'))



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
        user_menu(current_user_id)



def character_menu(char_id, current_user_id):
    clear_terminal()

    character = session.query(Character).filter(Character.character_id == char_id).first()
    print(f"""
        Character: {character.name}
        --------------------------------
        Level {character.level} | {character.gold} gp
        Max Spell Level: {round((character.level+0.5) / 2)}
        Owner id: {character.owner}
        
        1) View Spellbook
        2) Manage Spellbook
        3) Manage Gold
        4) Manage Level

        
        DELETE) Delete Character

        0) Back
    """)
    
    choice = input("Choose Option: ")
    if choice == '1':
        spellbook(character)
    if choice == '2':
        spellbook_manager(character)
    elif choice == '3':
        manage_gold(character)
    elif choice == '4':
        manage_level(character)
    elif choice == 'DELETE':
        selected_character = session.query(Character).filter(Character.character_id == char_id)
        confirm = input(f'{selected_character[0].name} will be deleted. (type DELETE to confirm): ')
        if confirm == 'DELETE':
            selected_character.delete()
            session.commit()
            user_menu(current_user_id)
    elif choice == '0':
        user_menu(current_user_id)


def spellbook(character):
    clear_terminal()
    highest_level_tuple = session.query(Spell.level).filter(Spell.characters.any(character_id=character.character_id)).order_by(desc(Spell.level)).first()
    highest_level, = highest_level_tuple
    all_spells = []
    for level in range(1,highest_level+1):
        spellbook_segment(level, character, all_spells)

    choice = input('Choose Spell or 0) Back >>> ')
    if choice == '0':
        character_menu(character.character_id, character.owner)
    else:
        clear_terminal()
        selected_spell = session.query(Spell).filter(Spell.name == choice).first()
        print(selected_spell)
        back = input('1) Back to Spellbook 0) Back to Menu: ')
        if back == '1':
            spellbook(character)
        elif back == '0':
            character_menu(character.character_id, character.owner)

    

def spellbook_segment(level, character, all_spells):
    if level == 1:
        level_string = '1st'
    elif level == 2:
        level_string = '2nd'
    elif level == 3:
        level_string = '3rd'
    else:
        level_string = f'{level}th'
    level_spells = session.query(Spell).filter(Spell.characters.any(character_id=character.character_id), Spell.level == level).all()
    print(f'''
         ------- {level_string} Level -------''')
    for spell in level_spells:
        all_spells.append(spell)
        print(f'''
        >   {spell.name}
            Cast time: {spell.casting_time} | Range: {spell.range} | Duration: {spell.duration}''')

def spellbook_manager(character):
    clear_terminal()
    print('''
        Manage Spellbook:
        1) Add Spell to Spellbook
        2) Remove Spell from Spellbook
        3) Add Cantrip

        0) Back
    ''')
    choice = input('Choose Option: ')
    if choice == '0':
        character_menu(character.character_id, character.owner)
    elif choice == '1':
        add_spell(character)
    elif choice == '2':
        remove_spell(character)
    elif choice == '3':
        add_cantrip(character)

def add_cantrip(character):
    pass
    clear_terminal()
    spell_list = []
    cantrips = session.query(Spell).filter(Spell.level == 0).all()
    print(f'''
    0) Back
        
    Cantrips:

    ''')
    for spell in cantrips:
        spell_list.append(spell)
        print(f'ID: {spell.spell_id}) {spell.name} ({spell.casting_time})')
    spell_select = input('Select cantrip by ID (0: Back) >>> ')
    if spell_select == '0':
        add_cantrip(character)
    else:
        clear_terminal()
        selected_spell = session.query(Spell).filter(Spell.spell_id == int(spell_select)).first()
        print(f'''
    Cantrip to Add:

    {selected_spell} 

        ''')
        confirm_spell = input('Confirm? (y/n): ')
        if confirm_spell == 'y':
            character.spells.append(selected_spell)
            session.add(character)
            session.commit()
            clear_terminal()
            print(f'''      {selected_spell.name} added to your Spellbook.
                
            ''')
            keep_going = input('Add More? (y/n): ')
            if keep_going == 'y':
                add_cantrip(character)
            else:
                character_menu(character.character_id, character.owner)
        else:
            add_cantrip(character)


def add_spell(character):
    clear_terminal()
    print('''
        Choose Spell to Add:
        1) Sort by level
        2) Search by name
        0) Back
    ''')
    choice = input('Choose Option: ')
    if choice == '0':
        spellbook_manager(character)
    elif  choice == '1':
        level_search = input("Level of Spell >>> ")
        if int(level_search) <= round((character.level+0.5) / 2):
            cost = int(level_search) * 50
            clear_terminal()
            spell_list = []
            spells_at_level = session.query(Spell).filter(Spell.level == int(level_search)).all()
            print(f'''
            0) Back
                
            Level {level_search} Spells:

            ''')
            for spell in spells_at_level:
                spell_list.append(spell)
                print(f'ID: {spell.spell_id}) {spell.name} ({spell.casting_time})')
            spell_select = input('Select spell by ID (0: Back) >>> ')
            if spell_select == '0':
                add_spell(character)
            else:
                clear_terminal()
                selected_spell = session.query(Spell).filter(Spell.spell_id == int(spell_select)).first()
                print(f'''
            Spell to Add (Cost: {cost}gp):

            {selected_spell} 

                ''')
                confirm_spell = input('Confirm? (y/n): ')
                if confirm_spell == 'y':
                    if character.gold - cost >= 0:
                        character.spells.append(selected_spell)
                        character.gold = character.gold - cost
                        session.add(character)
                        session.commit()
                        clear_terminal()
                        print(f'''      {selected_spell.name} added to your Spellbook.
                            
                        ''')
                        keep_going = input('Add More? (y/n): ')
                        if keep_going == 'y':
                            add_spell(character)
                        else:
                            character_menu(character.character_id, character.owner)
                    else:
                        clear_terminal()
                        print(colored(f'''
            Insufficient funds (Cost: {cost}gp)
            ''', 'red'))
                        time.sleep(3)
                        add_spell(character)
                else:
                    add_spell(character)
        else:
            clear_terminal()
            print(colored(f'''
        Spell level too high for current character (max spell level: {round((character.level+0.5) / 2)})  
                  ''', 'red'))
            time.sleep(3)
            add_spell(character)
        
    elif choice == '2':
        spell_search = input("Search for a spell by name >>> ")
        clear_terminal
        search_results = session.query(Spell).filter(Spell.name.like(f'%{spell_search}')).all()
        for spell in search_results:
            if spell.level <= round((character.level+0.5) / 2):
                print(f'        ID: {spell.spell_id}) {spell.name} ({spell.casting_time}) | Level {spell.level} Spell')
            else:
                print(colored(f'        ID: {spell.spell_id}) {spell.name} ({spell.casting_time}) | Level {spell.level} Spell', 'dark_grey'))

        spell_select = input('Select spell by ID (0: Back) >>> ')
        if spell_select == '0':
            add_spell(character)
        else:
            clear_terminal()
            selected_spell = session.query(Spell).filter(Spell.spell_id == int(spell_select)).first()
            cost = selected_spell.level * 50
            print(f'''
        Spell to Add (Cost: {cost}gp):

        {selected_spell} 

            ''')
            confirm_spell = input('Confirm? (y/n): ')
            if confirm_spell == 'y':
                if selected_spell.level <= round((character.level+0.5) / 2):
                    if character.gold - cost >= 0:
                        character.spells.append(selected_spell)
                        character.gold = character.gold - cost
                        session.add(character)
                        session.commit()
                        clear_terminal()
                        print(f'''
                {selected_spell.name} added to your Spellbook.
                            
                ''')
                        keep_going = input('Add More? (y/n): ')
                        if keep_going == 'y':
                            add_spell(character)
                        else:
                            character_menu(character.character_id, character.owner)
                    else:
                        clear_terminal()
                        print(colored(f'''
            Insufficient funds (Cost: {cost}gp)
            ''', 'red'))
                        time.sleep(3)
                        add_spell(character)
                else:
                    clear_terminal()
                    print(colored(f'''
                Spell level too high for current character (max spell level: {round((character.level+0.5) / 2)})  
                        ''', 'red'))
                    time.sleep(3)
                    add_spell(character)
            else:
                add_spell(character)
        
    elif choice == '0':
        spellbook_manager(character)
    else:
        character_menu(character.character_id, character.owner)

def remove_spell(character):
    clear_terminal()
    print("     Remove Spell:")
    current_spells = []
    spell_query = session.query(Spell).filter(Spell.characters.any(character_id=character.character_id)).order_by(Spell.level).all()
    count = 1
    for spell in spell_query:
        current_spells.append(spell)
        print(f'        {count}) {spell.name} (level {spell.level})')
        count = count + 1
    print('     0) Back')
    choice = input("Choose option: ")
    if choice == '0':
        spellbook_manager(character)
    else:
        clear_terminal()
        selected_spell = current_spells[int(choice)-1]
        print(selected_spell)
        delete_confirm = input('Delete Spell? (y/n): ')
        if delete_confirm == 'y':
                print(len(character.spells))
                character.spells.remove(selected_spell)
                session.add(character)
                session.commit()
                print(f'''
        {selected_spell.name} (ID: {selected_spell.spell_id}) removed from Spellbook.
        ''')
                time.sleep(3)
                remove_spell(character)
        else:
            remove_spell(character)





def manage_gold(character):
    clear_terminal()
    print(f'''
            {character.name}

            Current Gold: {character.gold} gp

            1) Add
            2) Remove
            0) Back


            
    ''')
    change = input("Choose Option: ")
    if change == '1':
        new_gp = int(character.gold) + int(input('Gold to add >>> '))
        character.gold = new_gp
        session.commit()
        character_menu(character.character_id, character.owner)
    elif change == '2':
        new_gp = int(character.gold) - int(input('Gold to Remove >>> '))
        if new_gp >= 0:
            character.gold = new_gp
            session.commit()
            character_menu(character.character_id, character.owner)
        else:
            clear_terminal()
            print(colored('Insufficient funds', 'red'))
            time.sleep(2)
            character_menu(character.character_id, character.owner)
    elif change == '0':
        character_menu(character.character_id, character.owner)

  
def manage_level(character):
    clear_terminal()
    print(f'''
        {character.name}
            
            Your current level is {character.level}.
            
            Level up to level {character.level +1}?
            1)Level Up
            2)Choose level manually
            0) Back
            ''')
    choice = (input('Choose Option: '))
    if choice == '1':
        character.level = character.level +1
        session.add(character)
        session.commit()
        clear_terminal()
        print(f'''
        Level up!
        
        You are now Level {character.level}!
        ''')
        time.sleep(4)
        character_menu(character.character_id, character.owner)
    elif choice == '2':
        new_level = input('Enter new level >>> ')
        character.level = int(new_level)
        session.add(character)
        session.commit()
        clear_terminal()
        print(f'''
        Character set to Level {character.level}.
              ''')
        time.sleep(3)
        character_menu(character.character_id, character.owner)

    elif choice == '0':
        character_menu(character.character_id, character.owner)


if __name__ == '__main__':
    engine=create_engine('sqlite:///program.db')
    Session= sessionmaker(bind=engine)
    session = Session()

    initialize()