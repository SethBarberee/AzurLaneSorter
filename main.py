import json, sys, os, copy
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

def find_line(ships_dict):
    """ Given the dictionary, parse frontline and backline """
    backline = []
    frontline = []
    subline = []
    # These are the classes that go in the backline
    backline_set = {'BB', 'BC', 'CV', 'CVL', 'AR', 'CM'}
    subline_set = {'SS'}
    for ship in ships_dict:
        if ship['Class'] in backline_set:
            # Matches one of the classes so add it
            backline.append(ship)
        elif ship['Class'] in subline_set:
            # Found a submarine
            subline.append(ship)
        else:
            # Doesn't match so it's in the front
            frontline.append(ship)
    # Return which line they are in respectively
    return (backline, frontline, subline)

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


# TODO: only sorts by one stat... make it do more
def sort_ships(ships_dict, stat='HP'):
    """ Sort the ship dictionary given a certain stat """
    # First, check if the stat is in the dictionary
    try:
        if stat in ships_dict[0]:
            if stat == 'Armor':
                # Armor only has three values
                keyorder = ['Heavy', 'Medium', 'Light' ]
                order = {key: i for i, key in enumerate(keyorder)}
                sorted_ship_dict = sorted(ships_dict, key = lambda d: order[d[stat]])
            else:
                sorted_ship_dict = sorted(ships_dict, key = lambda d: d[stat], reverse=True)
            return sorted_ship_dict
        else:
            print("Key doesn't exist")
            return
    except:
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
    (backline, frontline, subline) = find_line(ship_dict)
    # TODO make it optional to filter instead of the force-filtering
    # Sort both by respective stat
    new_backline = sort_ships(backline, stat)
    print("filter the backline")
    new_backline = filter_ships(new_backline)

    new_frontline = sort_ships(frontline, stat)
    print("filter the frontline")
    new_frontline = filter_ships(new_frontline)

    new_subline = sort_ships(subline, stat)
    print("Filter the subs")
    new_subline = filter_ships(new_subline)
 
    if new_backline == None or new_frontline == None:
        print("Load ships please")
        # TODO maybe a delay
        menu_actions['main']()

    # Create a list of names for each line
    frontline_names = []
    backline_names = []
    subline_names = []
    oil_cost = 0
    suboil_cost = 0 # subs are separate oil
    # See how many ships we have in each lineup
    max_range_back = len(new_backline)
    max_range_front = len(new_frontline)
    max_range_sub = len(new_subline)
    # Backline
    if(max_range_back >= 3):
        # Only do the top three
        for i in range(3):
            # Add the backline ship and cost
            backline_names.append(new_backline[i]['Name'])
            oil_cost += int(float(new_backline[i]['Cost']))
    else:
        print(max_range_back)
        for i in range(max_range_back):
            # Add the backline ship and cost
            backline_names.append(new_backline[i]['Name'])
            oil_cost += int(float(new_backline[i]['Cost']))
    # Frontline 
    if(max_range_front >= 3):
        # Only do the top three
        for i in range(3):
            # Add the frontline ship and cost
            frontline_names.append(new_frontline[i]['Name'])
            oil_cost += int(float(new_frontline[i]['Cost']))
    else:
        for i in range(max_range_front):
            # Add the frontline ship and cost
            frontline_names.append(new_frontline[i]['Name'])
            oil_cost += int(float(new_frontline[i]['Cost']))

    if(max_range_sub >= 3):
        # Only do the top three
        for i in range(3):
            # Add the frontline ship and cost
            subline_names.append(new_subline[i]['Name'])
            suboil_cost += int(float(new_subline[i]['Cost']))
    else:
        for i in range(max_range_sub):
            # Add the frontline ship and cost
            frontline_names.append(new_subline[i]['Name'])
            suboil_cost += int(float(new_subline[i]['Cost']))


    # Print each line
    print("Backline:")
    print(backline_names)
    print("Frontline:")
    print(frontline_names)
    print("Cost: ")
    print(oil_cost)
    print("Subs:")
    print(subline_names)
    print("Sub Cost: ")
    print(suboil_cost)
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

