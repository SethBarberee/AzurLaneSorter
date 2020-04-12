import json, sys, os, copy # global

import utils, data_scrape #local

ship_dict = [] # global dictionary for all the ships
menu_actions = {} # blank definition here but we fill it at the bottom of the file

# Useful lists for filtering and data validation
valid_nations = ['Eagle Union', 'Royal Navy', 'Ironblood', 'Sakura Empire', 'Dragon Empery', 'Sardegna Empire', 'Northern Parliament', 'Iris Libre', 'Vichya Dominion']
valid_rarity =  ['Common', 'Rare', 'Elite', 'Super Rare', 'Ultra']
valid_class =  ['BB', 'BC', 'BM', 'CV', 'CVL', 'CL', 'CA', 'CB', 'SS', 'AR'] 

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

def new_ship_data(ships_dict):
    """ Add a new ship dictionary and return the updated list"""
    # Prompt each stat
    _id = input("ID: ")
    name = input("Name: ")
    try:
        # Check Rarity input
        rarity = input("Rarity: ")
        valid_rarity.index(rarity)
    except:
        rarity = "Common" # We'll set Common as default
    try:
        # Check Nation input
        nation = input("Nation: ")
        valid_nations.index(nation)
    except:
        nation = "Other"
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
    name_image = name.replace(" (Retrofit)", "Kai")
    image = "https://azurlane.koumakan.jp/File:" + name_image.replace(" ", "_") + "Icon.png"
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
            "Accuracy": acc,
            "Image": image
    }
    # Add it to the list
    ships_dict.append(new_ship)
    # write to a json datafile
    # TODO find a way to let user change this
    with open("data_export.json", "w+") as write_file:
        # Dump the data in a nice fashion
        json.dump(ships_dict, write_file, indent = 4, separators=(',',': '))
    return ships_dict

def filter_menu(ship_dict_old):
    """ Menu for filtering ships given a dictionary """
    test = "Y"
    while (test == 'Y'):
        filter_choice = input('Filter by (Nation, Rarity, Class, N/A): ')
        if(filter_choice == 'N/A' or filter_choice == ""):
            # Set the new equal to the old
            ship_dict_new = ship_dict_old
            return ship_dict_new
        else:
            ship_dict_new = utils.filter_ships(ship_dict_old, filter_choice)
            # copy new to old so we can filter again if we want
            ship_dict_old = ship_dict_new
            test = input('Would you like to filter again? (Y/N): ')
    return ship_dict_new

def menu1():
    """ Menu that will import the ship data """
    # Declare we are using the global to add the JSON data to it
    global ship_dict
    (ship_dict) = utils.parse_data()
    choice = input("Enter 0 to exit or main for main menu: ")
    exec_menu(choice)
    return 

def menu2():
    """ Menu that sorts our data however we like to our top 3 for front and back"""
    # TODO What if we want certain ships in our lineup??
    global ship_dict
    # Split dictionary into backline and frontline
    (backline, frontline, subline) = utils.find_line(ship_dict)
    # Sort by respective stat
    stat = input('Enter the stat you would like to sort the backline by: ')
    print("Sorting by " + stat)
    new_backline = utils.sort_ships(backline, stat)
    new_backline = filter_menu(new_backline)

    stat = input('Enter the stat you would like to sort the frontline by: ')
    print("Sorting by " + stat)
    new_frontline = utils.sort_ships(frontline, stat)
    new_frontline = filter_menu(new_frontline)

    stat = input('Enter the stat you would like to sort the subline by: ')
    print("Sorting by " + stat)
    new_subline = utils.sort_ships(subline, stat)
    new_subline = filter_menu(new_subline)
 
    if new_backline == None or new_frontline == None:
        print("Empty line")
        # TODO maybe a delay
        menu_actions['main']()

    # Allow user to add ships if they want to
    preset_names = []
    test = "Y"
    while (test == 'Y'):
        name_choice = input('Name of Ship to add by default to line: ')
        if(name_choice == 'N/A' or name_choice == ""):
            break
        else:
            for ship in ship_dict:
                # check for the name
                if ship["Name"] == name_choice:
                    preset_names.append(ship) 
                    break
            # TODO search ship_dict and add
            test = input('Would you like to add another? (Y/N): ')

    # Pass it all in and create the lineup
    utils.create_line(new_backline, new_frontline, new_subline, preset_names)

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

def menu4():
    # This will scrape the AL Wiki and update the data_export file
    data_scrape.scrape(100, False)
    print("Updated data_export.json")
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
    print("4. Update stats from AL wiki")
    print("0. Quit")
    choice = input(" >>  ")
    exec_menu(choice)

# Dictionary of each menu
# Each choice is a function that is called
menu_actions = {
    'main': main,
    '1': menu1,
    '2': menu2,
    '3': menu3,
    '4': menu4,
    '0': exit,
}

if __name__ == "__main__":
    main()

