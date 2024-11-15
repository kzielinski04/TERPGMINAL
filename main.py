from os import system

class Warrior:
    health = 100
    attack = 50
    speed = 25

class Wizard:
    health = 50
    attack = 100
    speed = 30

def menu():
    print("Welcome to the TERPGMINAL!")
    print("1 - New game")
    print("2 - Load game")
    print("3 - Exit")
    print("---------------------------")
    choice = input("Select option (1-3): ")
    match choice:
        case '1':
            system('clear')
            new_game()
        case '2':
            print("Load game")
        case '3':
            exit()
        case _:
            print("Invalid choice!")

def new_game():
    character_data = open("character_data.txt", "w+")
    character_name = input(("What's your name?: "))
    character_data.write(character_name + ';')
    system('clear')
    print("1 - Warrior")
    print("2 - Wizard")
    choice = input("Choose your class: ")
    match choice:
        case '1':
            character_class = Warrior
        case '2':
            character_class = Wizard
    character_data.write(character_class + ';')
#menu()