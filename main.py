from os import system, remove, path
from random import randint

class Player:
    name = ""
    pclass = ""
    max_health = 0
    current_health = 0
    attack = 0
    speed = 10
    pos_x = 0
    pos_y = 0
    gold = 100
    level = 1
    experience = 0
    inventory = ["Health potion"]

class Warrior:
    name = "Warrior"
    max_health = 100
    attack = 50
    def info():
        print(f"Health: {Warrior.health}\nAttack: {Warrior.attack}\n Speed: {Warrior.speed}")

class Wizard:
    name = "Wizard"
    max_health = 50
    attack = 100
    def info():
        print(f"Health: {Wizard.health}\nAttack: {Wizard.attack}\nSpeed: {Wizard.speed}")
    def current_position():
        print(f"Your current position:\nx: {Wizard.pos_x}, y: {Wizard.pos_y}")

class Location:
    pos_x = 0
    pos_y = 0

City = Location()
City.pos_x = -80
City.pos_y = 40

Dungeon = Location()
Dungeon.pos_x = 80
Dungeon.pos_y = -50

Forest = Location()
Forest.pos_x = -60
Forest.pos_y = 10

class Item:
    id = 0
    name = ""
    description = ""

HealthPotion = Item()
HealthPotion.id = 1
HealthPotion.name = "Health potion"
HealthPotion.description = "A glass flask with some mysterious red liquid. Drinking it restores +25 HP"

OldRing = Item()
OldRing.id = 2
OldRing.name = "Old ring"
OldRing.description = "An old ring found in the small box next to the old man's corpse. It might be worth something."

def menu():
    print("Welcome to the TERPGMINAL!")
    print("1 - New game")
    print("2 - Load game")
    print("3 - Exit")
    print("---------------------------")
    choice = input("Select option: ")
    match choice:
        case '1':
            system('clear')
            new_game()
        case '2':
            system('clear')
            load_game()
        case '3':
            exit()
        case _:
            print("Invalid choice!")

def new_game():
    global player
    player = Player()
    character_data = open("character_data.txt", "w")
    player.name = input(("What's your name?: "))
    system('clear')
    print("1 - Warrior")
    print("2 - Wizard")
    choice = input("Choose your class: ")
    match choice:
        case '1':
            player.pclass = "Warrior"
            player.attack = Warrior.attack
            player.max_health = Warrior.max_health
            player.current_health = player.max_health
        case '2':
            player.pclass = "Wizard"
            player.attack = Wizard.attack
            player.max_health = Wizard.max_health
            player.current_health = player.max_health
        case _:
            print("Invalid choice!")
    character_data.close()
    system('clear')
    print("Your adventure has begun!\n")
    main()

def load_game():
    global player
    player = Player()
    try:
        character_data = open("character_data.txt", 'r')
        character_inventory = open("character_inventory.txt", 'r')
    except FileNotFoundError:
        print("Character not found!")
        return menu()
    data = character_data.read().split(';')
    data_inventory = character_inventory.read().split('\n')
    player.name = data[0]
    player.pclass = data[1]
    player.current_health = int(data[2])
    player.max_health = int(data[3])
    player.attack = int(data[4])
    player.speed = int(data[5])
    player.pos_x = int(data[6])
    player.pos_y = int(data[7])
    player.gold = int(data[8])
    player.level = int(data[9])
    player.experience = int(data[10])
    player.inventory = data_inventory
    character_data.close()
    character_inventory.close()
    print("Welcome back, adventurer!\n")
    main()

def events(n:int):
    match n:
        case 1:
            return event1()

def level_up(lvl:int, exp:int, ch:int, mh:int, a:int):
    print(f"Congratulations! You've reached {lvl + 1} level!")
    print(f"+10 Health!\n+5 Attack!\n")
    return lvl + 1, exp - (100 + (10 * lvl)), mh + 10, mh + 10, a + 5

def game_over():
    print("You died! Game over!\n")
    remove("character_data.txt")
    exit()

def event1(g:int, ch:int, inv:list[str]):
    print("On your way you encounter a lying, unconscious old man. You approach him to see if he is okay. It turns out that he is dead. Next to him lies a small, old box.")
    choice = input("Do you want to open it? [y/n]: ")
    choice = choice.lower()
    ending = randint(1, 5)
    match choice:
        case 'n':
            print("You figured you wouldn't find anything of value in such a small box anyway. You decided to leave it by the old man's body and walk away.")
            return g, ch, inv       
        case 'y':
            match ending:
                case 1:
                    print("You decided to open the box. Inside you found 25 pieces of gold!\n")
                    return g + 25, ch, inv
                case 2:
                    print("You decided to open the box. Unfortunately, there was nothing inside.\n")
                    return g, ch, inv
                case 3:
                    print("You decided to open the box. A bat flew out from inside and wounded you in the head! You lose -5 HP!\n")
                    return g, ch -5, inv
                case 4:
                    print("You decided to open the box. While opening it, you were attacked from behind by a bandit and lost consciousness. After waking up, you realized that you had been robbed!\nYou lose all the gold coins and lose -15 HP!\n")
                    return g - g, ch - 15, inv
                case 5:
                    print("You decided to open the box. Inside you found an old ring. Who knows, maybe it is worth something?\n")
                    inv.append("Old ring")
                    return g, ch, inv 
        case _:
            print("Invalid choice!\n")
            event1(g, ch)

def move(choice, speed, x, y, gold, chealth):
    match choice:
        case "north":
            if y + player.speed > 50:
                print("You've reached the border of the map! Turn back!")
                return x, y
            else:
                event = randint(1, 2)
                if event == 1:
                    player.gold, player.current_health, player.inventory = event1(player.gold, player.current_health, player.inventory)
                    return x, y + player.speed
                else:
                    return x, y + player.speed
        case "south":
            if y - player.speed < -50:
                print("You've reached the border of the map! Turn back!")
                return x, y
            else:
                event = randint(1, 2)
                if event == 1:
                    player.gold, player.current_health, player.inventory = event1(player.gold, player.current_health, player.inventory)
                    return x, y - player.speed
                else:
                    return x, y - player.speed
        case "east":
            if x + player.speed > 110:
                print("You've reached the border of the map! Turn back!")
                return x, y
            else:
                event = randint(1, 2)
                if event == 1:
                    player.gold, player.current_health, player.inventory = event1(player.gold, player.current_health, player.inventory)
                    return x + player.speed, y
                else:
                    return x + player.speed, y
        case "west":
            if x - player.speed < -110:
                print("You've reached the border of the map! Turn back!")
                return x, y
            else:
                event = randint(1, 2)
                if event == 1:
                    player.gold, player.current_health, player.inventory = event1(player.gold, player.current_health, player.inventory)
                    return x - player.speed, y
                else:
                    return x - player.speed, y
        case _:
            print("Invalid direction!\n")
            return main()
        
def check_stats(ch, mh, a, s, g, l, exp):
    print("+---------STATS---------+")
    print(f"Health: {ch}/{mh}")
    print(f"Attack: {a}")
    print(f"Speed: {s}")
    print(f"Gold: {g}")
    print(f"Level: {l}({exp}/{100 + (l * 10)})")
    print("+-----------------------+\n")

def use_potion(hp:int):
    print("You've used health potion! +25 HP!")
    return hp + 25


#Function that allows players to manage their inventory
def manage_inventory(inv:list):
    print("+---------INVENTORY---------+")
    for i in range(len(inv)):
        print(f"{i + 1}: {inv[i]}")
    print("+---------------------------+\n")
    print("1 - USE AN ITEM")
    print("2 - DROP AND ITEM")
    print("3 - DISPLAY ITEM INFO")
    print("4 - QUIT")
    choice = input("What do you want to do?: ")
    match choice:
        case '1':
            chosen_item = int(input("Select an item: "))
            chosen_item -= 1
            match player.inventory[chosen_item]:
                case HealthPotion.name:
                    player.current_health = use_potion(player.current_health)
                    player.inventory[chosen_item] = None
        case '2':
            chosen_item = int(input("Select an item: "))
            chosen_item -= 1
            decision = input(f"Are you sure you want to drop {player.inventory[chosen_item]}? [y/n]: ")
            decision = decision.lower()
            match decision:
                case 'y':
                    print(f"{player.inventory[chosen_item]} has been dropped!\n")
                    player.inventory[chosen_item] = None
                case 'n':
                    return main()
                case _:
                    print("Invalid choice!\n")
                    return main()
        case '3':
            chosen_item = int(input("Select an item: "))
            chosen_item -= 1
            match player.inventory[chosen_item]:
                case HealthPotion.name:
                    item = HealthPotion
                    print("+--------------------------------------------------------------------------------------------------------------------+")
                    print(item.description)
                    print("+--------------------------------------------------------------------------------------------------------------------+")
                case OldRing.name:
                    item = OldRing
                    print("+--------------------------------------------------------------------------------------------------------------------+")
                    print(item.description)
                    print("+--------------------------------------------------------------------------------------------------------------------+")
        case '4':
            system('clear')
            return main()     
        case _:
            print("There is no item in this slot!")
                    

def main():
    while True:
        if player.experience >= 100 + (10 * player.level):
            player.level, player.experience, player.current_health, player.max_health, player.attack = level_up(player.level, player.experience, player.current_health, player.max_health, player.attack)
        if player.current_health <= 0:
            game_over()
        if player.current_health > player.max_health:
            player.current_health = player.max_health
        print("What do you want to do, adventurer?")
        print("1 - MOVE")
        print("2 - CHECK MAP")
        print("3 - CHECK YOUR STATS")
        print("4 - MANAGE YOUR INVENTORY")
        print("8 - SAVE & EXIT")
        print("9 - NEXT PAGE")
        choice = input("Choice: ")
        system('clear')
        match choice:
            case '1':
                direction = input("In which direction do you want to go?: ")
                direction = direction.lower()
                player.pos_x, player.pos_y = move(direction, player.speed, player.pos_x, player.pos_y, player.gold, player.current_health)
                print(f"Your current position\nx: {player.pos_x}\ty: {player.pos_y}\n")
                if player.pos_x == City.pos_x and player.pos_y == City.pos_y:
                    print("+------------------------+")
                    print("|You've reached The City!|")
                    print("+------------------------+\n")
                if player.pos_x == Dungeon.pos_x and player.pos_y == Dungeon.pos_y:
                    print("+---------------------------+")
                    print("|You've reached The Dungeon!|")
                    print("+---------------------------+\n")
                if player.pos_x == Forest.pos_x and player.pos_y == Forest.pos_y:
                    print("+--------------------------+")
                    print("|You've reached The Forest!|")
                    print("+--------------------------+\n")    
            case '2':
                check_map(player.pos_x, player.pos_y)
            case '3':
                check_stats(player.current_health, player.max_health, player.attack, player.speed, player.gold, player.level, player.experience)
            case '4':
                manage_inventory(player.inventory)
            case '8':
                character_data = open("character_data.txt", 'w')
                character_invetory = open("character_inventory.txt", "w")
                character_data.write(str(player.name) + ';')
                character_data.write(str(player.pclass) + ';')
                character_data.write(str(player.current_health) + ';')
                character_data.write(str(player.max_health) + ';')
                character_data.write(str(player.attack) + ';')
                character_data.write(str(player.speed) + ';')
                character_data.write(str(player.pos_x) + ';')
                character_data.write(str(player.pos_y) + ';')
                character_data.write(str(player.gold) + ';')
                character_data.write(str(player.level) + ';')
                character_data.write(str(player.experience))
                for i in range(len(player.inventory)):
                    if i == len(player.inventory) - 1:
                        character_invetory.write(str(player.inventory[i]))
                    else:
                        character_invetory.write(str(player.inventory[i]) + '\n')
                character_data.close()
                character_invetory.close()
                system('clear')
                exit()
            case '9':
                print("Not implemented yet!\n")
            case _:
                print("Invalid choice!\n")

def check_map(x, y):
    print("Hmm, let's take a look...")
    print("+---------------------+")
    print("|                     |")
    print("|  * City(-80,40)     |")
    print("|                     |")
    print("|                     |")
    print("|                     |")
    print("|          +          |")
    print("|    * Forest(-60,-10)|")
    print("|                     |")
    print("|                     |")
    print("|                     |")
    print("|  Dungeon(80,-50) *  |")
    print("+---------------------+")
    print("Hint: + symbol is a center of a map (x: 0  y: 0)")
    print(f"\nYour current location\nx: {x}\ty: {y}\n")

    
menu()
