#!/usr/bin/env python
from termcolor import colored
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import declarative_base, sessionmaker
from models import Spell, User, Character, character_spell
import os
import time

# creates initial login screen
def initialize():
    clear_terminal()
    print('''
        1) Login
        2) New User
        0) Exit
    ''' )
    start_option = int(input('Choose Option: '))

    if start_option == 1:
        choose_user()            
    elif start_option == 2:
        new_user()
    elif start_option == 0:
        exit()
    else: # if input not on list
        print(colored('Not a valid input','red'))
        pauser = input('Press Enter to Continue')
        initialize()


#  clears terminal and prints header
# use at the beginning of each menu function 
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(colored('''
         _    _  ____________ ______
        | |  | ||___  /| ___ \|  _  \ 
        | |  | |   / / | |_/ /| | | |
        | |/\| |  / /  |    / | | | |
        \  /\  /./ /___| |\ \ | |/ /
         \/  \/ \_____/\_| \_||___/

    ''', 'light_red'))
    

# lists all current users from 'users' table
# allows selection based on user id
def choose_user():
    clear_terminal()
    print('     Users:')
    user_list = session.query(User).all()
    valid_user_ids = []
    for user in user_list:
        valid_user_ids.append(user.user_id) # creates a list of all valid ID selections
        print(f'            {user.user_id}) {user.username}')
    print('            0) Exit')
    if valid_user_ids == []: # checks to see if any User objects exist
        print('     No users exist')
        print('     1) Create New User')
        print('     0) Exit')
        choice = int(input('Choose option: '))
        if choice == 1:
            new_user()
        else:
            initialize()
    else: # if there are users in the user database
        user_select = int(input('Select User: '))
        if user_select == 0:
            initialize()
        elif user_select in valid_user_ids: # makes sure input is a valid option for login
            password = input('Enter Password >>> ')
            user = session.query(User).filter(User.user_id == user_select).first()
            if password == user.password: # validates user password
                current_user_id = user_select
                user_menu(current_user_id)
            else: # if entered password doesn't match user.password
                clear_terminal()
                print(colored('     Incorrect password', 'red'))
                pauser = input('Press Enter to continue')
                choose_user() # return to menu
        else: # if input not a valid user id
            print(colored('     Invalid input', 'red'))
            choice = input('Exit? (y/n): ')
            if choice == 'y':
                initialize() # exits to main menu
            else:
                choose_user() # returns to list of users
    
def new_user():
    clear_terminal()
    existing_users = session.query(User.username).all()
    username = str(input('Enter your name >>> '))
    pass1 = str(input('Enter your new password >>> '))
    pass2 = str(input('Re-enter your password >>> '))
    if (username,) not in existing_users: # makes sure username does not already exist
        if pass1 == pass2:  # validates that both password inputs were identical
            user = User(username = username, password = pass1)
            session.add(user)
            session.commit()
            query = session.query(User).filter(User.username == username).first()
            current_id = query.user_id
            user_menu(current_id) # logs in with created user

        else: # if password inputs are not identical
            print(colored('     Passwords do not match', 'red'))
            choice = input ('Exit? (y/n): ')
            if choice == 'y':
                initialize() # exits to main menu
            else: # choice == 'n'
                new_user()  # returns to start of user creation
            
    else: # if username already exists
        print(colored('     username already taken', 'red'))
        choice = input ('Exit? (y/n): ')
        if choice == 'y':
            initialize() # returns to main menu
        else: # choice == 'n'
            new_user() # returns to start of user creation



def user_menu(current_user_id): # main menu for user once logged in
    clear_terminal()

    current_user = session.query(User).filter(User.user_id == int(current_user_id)).first() 
    print(f'''
        Welcome, {current_user.username}!

        Choose a character:
    ''')
    character_query = session.query(Character).filter(Character.owner == current_user_id).all()
    valid_char_choices = [] # list of possible character ids to select
    for character in character_query:
        valid_char_choices.append(character.character_id)
        print(f"        {character.character_id}) {character.name}")
    if valid_char_choices != []: # only prints the  "-or-"  if there are list options above it, otherwise will only show the create character option 
        print('''
                 -or-

    ''')
    print('''
        NEW) Create New Character
        0) Logout
        DELETE) Delete User
        ''')
    choice = input ('Choose Character: ') # input character id to select character
    if choice == 'NEW':
        create_character(current_user_id)
        user_menu(current_user_id)
    elif choice == 'DELETE':
        print(f'Delete {current_user.username}?')
        print(colored('WARNING: This change is permanent', 'red'))
        confirm = input('Continue? (y/n)')
        if confirm == 'y':
            get_him_outta_here = session.query(User).filter(User.user_id == current_user.user_id).first()
            session.delete(get_him_outta_here)
            session.commit()
            clear_terminal()
            print('User Deleted')
            pauser = input('Press Enter to Continue')
            initialize()
        else:
            user_menu(current_user_id)
    elif choice == '0':
        initialize() # exits to main menu
    elif int(choice) in valid_char_choices:
        character_menu(int(choice), character.owner) # selects character based on id input
    else:
        print(colored('     Not a valid response.', 'red'))
        pauser = input('Press Enter to continue') # pauses program until any value is entered
        user_menu(current_user.user_id) # returns to menu



def create_character(user_id): # prompt for creating new character
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
    if confirm == 'y': # if yes, creates new Character object with inputted data
        new_character = Character(
            owner = user_id,
            name = new_name,
            level = starting_level,
            gold = starting_gold
        )
        session.add(new_character)
        session.commit()
    else:
        user_menu(user_id)



# menu for the selected character
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
        selected_character = session.query(Character).filter(Character.character_id == char_id).first()
        confirm = input(f'{selected_character.name} will be deleted. (type DELETE to confirm): ')
        if confirm == 'DELETE': # verification to prevent accidental deletion
            session.delete(selected_character)
            session.commit()
            user_menu(current_user_id)
        else:
            clear_terminal()
            print('Delete aborted')
            pauser = input('Press Enter to continue')
            character_menu(character.character_id, current_user_id)
    elif choice == '0':
        user_menu(current_user_id) # return back to menu for selecting character


# displays list of all spells added to selected character's spell list
def spellbook(character): 
    clear_terminal()
    highest_level_tuple = session.query(Spell.level).filter(Spell.characters.any(character_id=character.character_id)).order_by(desc(Spell.level)).first() # data is returned automatically as a tuple with one value
    if not highest_level_tuple:
        print('Spellbook is currently empty')
        pauser = input('Press Enter to continue')
        character_menu(character.character_id, character.owner)
    highest_level, = highest_level_tuple # converts tuple to integer
    all_spells = [] # list of all spells in spellbook
    for level in range(0,highest_level+1):
        spellbook_segment(level, character, all_spells) # prints a segment for each level of spell in ascending order, with a header for the spell level

    choice = input('Choose Spell or 0) Back >>> ') # input must be exact name of spell as it appears on the list, case-sensitive
    if choice == '0':
        character_menu(character.character_id, character.owner) # go back one menu 
    else:
        clear_terminal()
        
        selected_spell = session.query(Spell).filter(Spell.name.like(choice.lower())).first() # find spell with entered name
        if selected_spell: # check if entered spell name exists
            print(type(selected_spell.name))
            print(selected_spell)
            back = input('1) Back to Spellbook 0) Back to Menu: ')
            if back == '1': # back one menu
                spellbook(character)
            elif back == '0': # goes all the way back to character options
                character_menu(character.character_id, character.owner)
        else: # if spell with entered name does not exist
            clear_terminal()
            print(colored(f'''
        Can't find spell by the name of {choice}.  
                  ''','red'))
            pauser = input('Press Enter to continue')
            spellbook(character)

    
# divides spell list into sections based on spell level
def spellbook_segment(level, character, all_spells):
    if level == 0:
        level_string = 'Cantrips'
    elif level == 1:
        level_string = '1st Level'
    elif level == 2:
        level_string = '2nd Level'
    elif level == 3:
        level_string = '3rd Level'
    else:
        level_string = f'{level}th'
    level_spells = session.query(Spell).filter(Spell.characters.any(character_id=character.character_id), Spell.level == level).all()
    print(f'''
         ------- {level_string} -------''') # segment header
    for spell in level_spells:
        all_spells.append(spell)
        print(f'''
        >   {spell.name}
            Cast time: {spell.casting_time} | Range: {spell.range} | Duration: {spell.duration}''') # format each list item




# creates menu for adding and deleting from spellbook
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




# function for adding level 0 spells (cantrips)
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
        selected_spell = session.query(Spell).filter(Spell.spell_id == int(spell_select), Spell.level == 0).first()
        if selected_spell:
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
        else:
            print(colored("Spell not found in search list", 'red'))
            pauser = input('Hit Enter to Continue')
            add_cantrip(character)

    


# create menu for adding spells to the spellbook
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
        if int(level_search) <= round((character.level+0.5) / 2): # validates spell is of a level the current character has access to
            cost = int(level_search) * 50 # cost in gold for transcribing spell (50 gp per spell level)
            clear_terminal()
            spell_list = []
            spells_at_level = session.query(Spell).filter(Spell.level == int(level_search)).all()
            print(f'''
            0) Back
                
            Level {level_search} Spells:

            ''')
            for spell in spells_at_level:
                spell_list.append(spell)
                print(f'ID: {spell.spell_id}) {spell.name} ({spell.casting_time})') # creates list of all spells at given level
            spell_select = input('Select spell by ID (0: Back) >>> ')
            if spell_select == '0':
                add_spell(character)
            else:
                clear_terminal()
                selected_spell = session.query(Spell).filter(Spell.spell_id == int(spell_select), Spell.level == int(level_search)).first() # query spell by selected spell ID
                if selected_spell:
                    print(f'''
                Spell to Add (Cost: {cost}gp):

                {selected_spell} 

                    ''')
                    confirm_spell = input('Confirm? (y/n): ') # confirms spell to prevent accidental addition
                    if confirm_spell == 'y':
                        if character.gold - cost >= 0: # validates character has the required amount of gold
                            character.spells.append(selected_spell) # adds spell to spellbook
                            character.gold = character.gold - cost # automatically removes gold needed to transcribe spell from character (WARNING: will still remove gold if choosing a spell already in the spellbook, although it will not create a duplicate item in the spellbook itself)
                            session.add(character)
                            session.commit()
                            clear_terminal()
                            print(f'''      {selected_spell.name} added to your Spellbook.
                                
                            ''') # confirmation message
                            keep_going = input('Add More? (y/n): ')
                            if keep_going == 'y':
                                add_spell(character)
                            else: # stop adding spells
                                character_menu(character.character_id, character.owner) # returns to character menu
                        else: # if not enough funds
                            clear_terminal()
                            print(colored(f'''
                Insufficient funds (Cost: {cost}gp)
                ''', 'red'))
                            pauser = input('Press Enter to continue')
                            add_spell(character)
                    else: # confirm spell denied
                        add_spell(character)
                else: # id not in current spell level
                    print(colored('Spell ID not found in current search', 'red'))
                    pauser = input('Hit enter to continue')
                    add_spell(character)
        else: # if spell too high of level for chosen character
            clear_terminal()
            print(colored(f'''
        Spell level too high for current character (max spell level: {round((character.level+0.5) / 2)})  
                ''', 'red'))
            pauser = input('Press Enter to continue')
            add_spell(character)
        
    elif choice == '2': # searching spell list by spell name
        spell_search = input("Search for a spell by name >>> ")
        clear_terminal
        search_results = session.query(Spell).filter(Spell.name.like(f'%{spell_search}%')).all()
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
            cost = selected_spell.level * 50 # sets cost to transcribe spell (50 gp per spell level)
            if selected_spell.level <= round((character.level+0.5) / 2):
                print(f'''
            Spell to Add (Cost: {cost}gp):

            {selected_spell} 

                ''')
                confirm_spell = input('Confirm? (y/n): ')
                if confirm_spell == 'y':
                    if selected_spell.level <= round((character.level+0.5) / 2): # validates that character is high enough level to learn selected spell
                        if character.gold - cost >= 0: # validates that character has required amount of gold
                            character.spells.append(selected_spell)
                            character.gold = character.gold - cost # automatically remove cost to transcribe spell from character gold
                            session.add(character)
                            session.commit()
                            clear_terminal()
                            print(f'''
                    {selected_spell.name} added to your Spellbook.
                                
                    ''') # confirmation message
                            keep_going = input('Add More? (y/n): ')
                            if keep_going == 'y':
                                add_spell(character)
                            else:
                                character_menu(character.character_id, character.owner)
                        else: # if character doesn't have required funds
                            clear_terminal()
                            print(colored(f'''
                Insufficient funds (Cost: {cost}gp)
                ''', 'red'))
                            time.sleep(3)
                            add_spell(character) # return to add spell menu
                    else: # if character doesn't have required level
                        clear_terminal()
                        print(colored(f'''
                    Spell level too high for current character (max spell level: {round((character.level+0.5) / 2)})  
                            ''', 'red'))
                        pauser = input('Press Enter to continue')
                        add_spell(character)
                else: # confirmation denied
                    add_spell(character)
            else:
                print(f'''
            Spell Preview:

            {selected_spell} 

                ''')
                print(colored('Spell level above current max. Cannot add to spellbook', 'red'))
                pauser = input('Hit Enter to Continue')
                add_spell(character)

        
    elif choice == '0':
        spellbook_manager(character) # return to menu for changing spellbook
    else: # invalid option selected
        clear_terminal()
        print(colored('invalid selection','red'))
        pauser = input('Press Enter to continue')
        character_menu(character.character_id, character.owner)


# menu for removing spells from a character's spellbook
def remove_spell(character):
    clear_terminal()
    print("     Remove Spell:")
    current_spells = []
    spell_query = session.query(Spell).filter(Spell.characters.any(character_id=character.character_id)).order_by(Spell.level).all()
    count = 1
    for spell in spell_query:
        current_spells.append(spell) # adds all spells from character's spellbook into a list
        print(f'        {count}) {spell.name} (level {spell.level})')
        count = count + 1 # adds one to the list number for each spell added
    print('     0) Back')
    choice = input("Choose option: ")
    if choice == '0':
        spellbook_manager(character)
    else:
        clear_terminal()
        selected_spell = current_spells[int(choice)-1] # query spell based on position on list
        print(selected_spell)
        delete_confirm = input('Delete Spell? (y/n): ') # confirmation to prevent accidental deletion
        if delete_confirm == 'y':
                character.spells.remove(selected_spell) # removes selected spell from the character spell list
                session.add(character) # updates character object with 
                session.commit()
                print(f'''
        {selected_spell.name} (ID: {selected_spell.spell_id}) removed from Spellbook.
        ''')
                pauser = input('Press Enter to continue')
                remove_spell(character) # returns to spell remove menu
        else: # confirmation denied
            remove_spell(character) # returns to  spell remove menu




# function to modify the characters amount of gold
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
        else: # character does not have enough gold to subtract
            clear_terminal()
            print(colored('Insufficient funds', 'red'))
            pauser = input('Press Enter to continue')
            character_menu(character.character_id, character.owner)
    elif change == '0':
        character_menu(character.character_id, character.owner)
    else: # invalid option inputted
        clear_terminal()
        print(colored('invalid selection','red'))
        manage_gold(character)
  
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
    if choice == '1': # level up by 1 level
        character.level = character.level +1
        session.add(character)
        session.commit()
        clear_terminal()
        print(f'''
        Level up!
        
        You are now Level {character.level}!
        ''')
        pauser = input('Press Enter to continue')
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
        pauser = input('Press Enter to continue')
        character_menu(character.character_id, character.owner)

    elif choice == '0':
        character_menu(character.character_id, character.owner)
    else: # invalid input
        clear_terminal()
        print(colored('invalid option','red'))
        pauser = input('Press Enter to continue')
        manage_level(character)


if __name__ == '__main__':
    engine=create_engine('sqlite:///program.db') # link to database
    Session= sessionmaker(bind=engine)
    session = Session()

    initialize() # print main menu