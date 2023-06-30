# WZRD
WZRD is a virtual spellbook CLI for D&D 5th edition. It allows you to create characters, save learned spells to your spell list, and manage character stats.

## Installation

From the wzrd directory, use the following commands to create a virtual environment and enter the virtual shell

```bash
$ pipenv install
$ pipenv shell
```

This will also install all necessary packages from Pipfile

## Database Setup

Navigate into /lib

```bash
$ cd lib
```
WZRD uses SQLAlchemy and Alembic to create and manage it's database and tables. To initialize the database and populate it with the necessary data, run seed.py

```bash
$ ./seed.py
# => Seeding spell list...
# => Complete!
```

If you run into a permissions error, you may need to run the following then try again:

```bash
$ chmod +x ./seed.py
```

## Usage

To start the program, run ./wzrd.py

Input prompts should be rather straightforward with what to enter.
Menu items presented as numbered lists can be selected by entering the correlating number for the option you want to select and hitting enter.
Yes or No prompts will take inputs of either "y" or "n", respectively.

Create a new user by selecting New User from the main menu. Follow input prompts to create your login. Once logged in, you can create a new character from the following menu. Follow the prompts to do so. When choosing the characters level or gold, enter an integer with no spaces. All other inputs accept any string.

### Viewing Spells in the Spellbook

To view the details of a spell from your spellbook, enter the name of the spell exactly as it appears in the list (case sensitive). 

NOTE: This differs from selecting a spell in the "Add Spell" or "Remove Spell" menus, which will ask you to enter the spell ID as an integer. In these scenarios, spell IDs are displayed in front of the spell information on the list.
