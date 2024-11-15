def menu():
    print("Welcome to the TERPGMINAL!")
    print("1 - New game")
    print("2 - Load game")
    print("3 - Exit")
    print("---------------------------")
    choice = input("Select option (1-3): ")
    match choice:
        case '1':
            print("Start new game")
        case '2':
            print("Load game")
        case '3':
            exit()
        case _:
            print("Invalid choice!")


menu()