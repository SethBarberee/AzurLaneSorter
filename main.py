import json, sys, os, copy
ship_dict = [] # global dictionary for all the ships
menu_actions = {}

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
    name = input("Name: ")
    clas = input("Class: ")
    nation = input("Nation: ")
    hp = input("HP: ")
    firepower = input("Firepower: ")
    aa = input("Anti-Air: ")
    armor = input("Armor: ")
    torpedo = input("Torpedo: ")
    aviation = input("Aviation: ")
    evasion = input("Evasion: ")
    cost = input("Cost: ")
    print("Adding " + name + " to the list")
    # Create the dictionary for the new ship
    new_ship = {
            "Name": name,
            "Class": clas,
            "Nation": nation,
            "HP": hp,
            "Firepower": firepower,
            "Anti-Air": aa,
            "Armor": armor,
            "Torpedo": torpedo,
            "Aviation": aviation,
            "Evasion": evasion,
            "Cost": cost
    }
    # Add it to the list
    ships_dict.append(new_ship)
    # write to a json datafile
    # TODO find a way to let user change this
    with open("data_export.json", "w+") as write_file:
        # Dump the data in a nice fashion
        json.dump(ships_dict, write_file, indent = 4, separators=(',',': '))
    return ships_dict

def find_line(ships_dict):
    """ Given the dictionary, parse frontline and backline """
    backline = []
    frontline = []
    # These are the classes that go in the backline
    backline_set = {'BB', 'BC', 'CV', 'CVL', 'AR', 'CM'}
    for ship in ships_dict:
        if ship['Class'] in backline_set:
            # Matches one of the classes so add it
            backline.append(ship)
        else:
            # Doesn't match so it's in the front
            frontline.append(ship)
    # Return which line they are in respectively
    return (backline, frontline)

# TODO: only sorts by one stat... make it do more
def sort_ships(ships_dict, stat='HP'):
    """ Sort the ship dictionary given a certain stat """
    # First, check if the stat is in the dictionary
    if stat in ships_dict[0]:
        if stat == 'Armor':
            # Armor only has three values
            keyorder = ['Heavy', 'Medium', 'Light' ]
        else:
            # Assign a ranking to each letter
            keyorder = ['S', 'A', 'B', 'C', 'D', 'E' ]
        order = {key: i for i, key in enumerate(keyorder)}
        sorted_ship_dict = sorted(ships_dict, key = lambda d: order[d[stat]])
        return sorted_ship_dict
    else:
        print("Key doesn't exist so returing the dictionary that was passed in")
        return ships_dict

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
    # TODO find a way to filter based on Nation if desired
    # TODO What if we want certain ships in our lineup??
    global ship_dict
    stat = input('Enter the stat you would like to sort by: ')
    print("Sorting by " + stat)
    # Split dictionary into backline and frontline
    (backline, frontline) = find_line(ship_dict)
    # Sort both by respective stat
    new_backline = sort_ships(backline, stat)
    new_frontline = sort_ships(frontline, stat)
    # Create a list of names for each line
    frontline_names = []
    backline_names = []
    oil_cost = 0
    # Only do the top three
    for i in range(3):
        # Add the backline ship and cost
        backline_names.append(new_backline[i]['Name'])
        oil_cost += int(float(new_backline[i]['Cost']))
        # Add the frontline ship and cost
        frontline_names.append(new_frontline[i]['Name'])
        oil_cost += int(float(new_frontline[i]['Cost']))

    # Print each line
    print("Backline:")
    print(backline_names)
    print("Frontline:")
    print(frontline_names)
    print("Cost: ")
    print(oil_cost)
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

