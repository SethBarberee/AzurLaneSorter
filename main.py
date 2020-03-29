import json, sys, os, copy # global

import utils #local

ship_dict = [] # global dictionary for all the ships
menu_actions = {}
valid_nations = ['Eagle Union', 'Royal Navy', 'Ironblood', 'Sakura Empire', 'Dragon Empery', 'Sardegna Empire', 'Northern Parliament', 'Iris Libre', 'Vichya Dominion']
valid_rarity =  ['Common', 'Rare', 'Elite', 'Super Rare', 'Ultra']
# Execute menu
def exec_menu(choice):
    os.system('clear')
    ch = choice.lower()
    if ch == '':
        menu_actions['main']()
    else:
        try:
            menu_actions[ch]()
        except KeyError:
            print("Invalid selection, please try again.")
            menu_actions['main']()
    return

def exit():
    sys.exit()

def parse_data(filename='data.json'):
    """ Pass in a JSON file of ships and return a python dictionary """

    # Open the data file for reading
    # loop through line by line
    with open(filename, 'r') as f:
        ships_dict = json.load(f)
    return ships_dict

def new_ship_data(ships_dict):
    """ Add a new ship dictionary and return the updated list"""
    # Prompt each stat
    _id = input("ID: ")
    name = input("Name: ")
    # TODO check nation
    rarity = input("Rarity: ")
    nation = input("Nation: ")
    clas = input("Class: ")
    luck = int(input("Luck: "))
    armor = input("Armor: ")
    speed = int(input("Speed: "))
    hp = int(input("HP: "))
    firepower = int(input("Firepower: "))
    aa = int(input("Anti-Air: "))
    torpedo = int(input("Torpedo: "))
    evasion = int(input("Evasion: "))
    aviation = int(input("Aviation: "))
    cost = int(input("Cost: "))
    reloa = int(input("Reload: "))
    anti_sub = int(input("Anti-Sub: "))
    oxygen  = int(input("Oxygen: "))
    ammo = int(input("Ammunition: "))
    acc = int(input("Accuracy: "))
    print("Adding " + name + " to the list")
    # Create the dictionary for the new ship
    new_ship = {
            "ID": _id,
            "Name": name,
            "Rarity": rarity,
            "Nation": nation,
            "Class": clas,
            "Luck": luck,
            "Armor": armor,
            "Speed": speed,
            "HP": hp,
            "Firepower": firepower,
            "Anti-Air": aa,
            "Torpedo": torpedo,
            "Evasion": evasion,
            "Aviation": aviation,
            "Cost": cost,
            "Reload": reloa,
            "Anti-Submarine": anti_sub,
            "Oxygen": oxygen,
            "Ammunition": ammo,
            "Accuracy": acc
    }
    # Add it to the list
    ships_dict.append(new_ship)
    # write to a json datafile
    # TODO find a way to let user change this
    with open("data_export.json", "w+") as write_file:
        # Dump the data in a nice fashion
        json.dump(ships_dict, write_file, indent = 4, separators=(',',': '))
    return ships_dict

def filter_ships(ships_dict, filter_name='Nation'):
    """ Filter the ship dictionary based on Nation or Rarity """
    new_ship_dict = []
    if filter_name == "Nation":
        # TODO check if it is a valid nation
        nation = input('Enter the desired nation: ')
        print("Filtering by " + nation)
        for ship in ships_dict:
            if(ship["Nation"] == nation):
                new_ship_dict.append(ship)
        return new_ship_dict
            
    elif filter_name == "Rarity":
        # TODO check if it's valid rarity
        rarity = input('Enter the desired rarity: ')
        print("Filtering by " + rarity)
        for ship in ships_dict:
            if(ship["Rarity"] == rarity):
                new_ship_dict.append(ship)
        return new_ship_dict
    else:
        return

def menu1():
    """ Menu that will import the ship data """
    # Declare we are using the global to add the JSON data to it
    global ship_dict
    (ship_dict) = parse_data()
    choice = input("Enter 0 to exit or main for main menu: ")
    exec_menu(choice)
    return 


def menu2():
    """ Menu that sorts our data however we like to our top 3 for front and back"""
    # TODO What if we want certain ships in our lineup??
    global ship_dict
    stat = input('Enter the stat you would like to sort by: ')
    print("Sorting by " + stat)

    # Split dictionary into backline and frontline
    (backline, frontline, subline) = utils.find_line(ship_dict)
    # TODO make it optional to filter instead of the force-filtering
    # Sort both by respective stat
    new_backline = utils.sort_ships(backline, stat)
    print("filter the backline")
    new_backline = filter_ships(new_backline)

    new_frontline = utils.sort_ships(frontline, stat)
    print("filter the frontline")
    new_frontline = filter_ships(new_frontline)

    new_subline = utils.sort_ships(subline, stat)
    print("Filter the subs")
    new_subline = filter_ships(new_subline)
 
    if new_backline == None or new_frontline == None:
        print("Load ships please")
        # TODO maybe a delay
        menu_actions['main']()
    
    utils.create_line(new_backline, new_frontline, new_subline)

    choice = input("Enter 0 to exit or main for main menu: ")
    exec_menu(choice)
    return 

def menu3():
    # Declare we are using the global so we can add the new ship to it
    global ship_dict
    new_ship_dict = new_ship_data(ship_dict)
    ship_dict = new_ship_dict
    choice = input("Enter 0 to exit or main for main menu: ")
    exec_menu(choice)
    return

def main():
    os.system('clear')
    print("Welcome to Azur Lane Sorter")
    print("Enter your selection:")
    print("1. Import Ships")
    print("2. Sort Ships")
    print("3. Add new ship to database")
    print("0. Quit")
    choice = input(" >>  ")
    exec_menu(choice)

# Dictionary of each menu
menu_actions = {
    'main': main,
    '1': menu1,
    '2': menu2,
    '3': menu3,
    '0': exit,
}

if __name__ == "__main__":
    main()

