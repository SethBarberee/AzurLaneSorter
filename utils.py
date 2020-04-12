import json # global

# Mainly a utility file with the following

# find_Line
# Figure out which line a ship belongs to

# sort_ships
# Sort the dictionary based on a stat

# create_line
# Filter best three for each line and calculate oil cost

# Useful lists for filtering and data validation
valid_nations = ['Eagle Union', 'Royal Navy', 'Ironblood', 'Sakura Empire', 'Dragon Empery', 'Sardegna Empire', 'Northern Parliament', 'Iris Libre', 'Vichya Dominion']
valid_rarity =  ['Common', 'Rare', 'Elite', 'Super Rare', 'Ultra']
valid_class =  ['BB', 'BC', 'BM', 'CV', 'CVL', 'CL', 'CA', 'CB', 'DD', 'SS', 'AR'] 


def parse_data(filename='data.json'):
    """ Pass in a JSON file of ships and return a python dictionary """

    # Open the data file for reading
    # loop through line by line
    with open(filename, 'r') as f:
        ships_dict = json.load(f)
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

def sort_ships(ships_dict, stat='HP'):
    """ Sort the ship dictionary given a certain stat """
    # First, check if the stat is in the dictionary
    if stat == "":
        print("Setting to HP")
        stat = "HP"
        
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

def create_line(backline, frontline, subline, preset_names, UI=False):
    # Create a list of names for each line
    frontline_names = []
    backline_names = []
    subline_names = []
    oil_cost = 0
    suboil_cost = 0 # subs are separate oil

    preset_subline = []
    preset_frontline = []
    preset_backline = []
    if len(preset_names) > 0:
        # we've got some to add by default so figure out the lines first
        (preset_backline, preset_frontline, preset_subline) = find_line(preset_names)
        for i in range(len(preset_backline)):
            # Add the backline ship and cost
            backline_names.append(preset_backline[i]['Name'])
            oil_cost += int(float(preset_backline[i]['Cost']))
        for i in range(len(preset_frontline)):
            # Add the backline ship and cost
            frontline_names.append(preset_frontline[i]['Name'])
            oil_cost += int(float(preset_frontline[i]['Cost']))
        for i in range(len(preset_subline)):
            # Add the backline ship and cost
            subline_names.append(preset_subline[i]['Name'])
            suboil_cost += int(float(preset_subline[i]['Cost']))

    # See how many ships we have in each lineup accounting for presets
    max_range_back = min(len(backline), 3 - len(preset_backline))
    max_range_front = min(len(frontline), 3 - len(preset_frontline))
    max_range_sub = min(len(subline), 3 - len(preset_subline))

    # Backline
    if(max_range_back >= 3):
        # Only do the top three
        for i in range(3):
            # Add the backline ship and cost
            backline_names.append(backline[i]['Name'])
            oil_cost += int(float(backline[i]['Cost']))
    else:
        print(max_range_back)
        for i in range(max_range_back):
            # Add the backline ship and cost
            backline_names.append(backline[i]['Name'])
            oil_cost += int(float(backline[i]['Cost']))
    # Frontline 
    if(max_range_front >= 3):
        # Only do the top three
        for i in range(3):
            # Add the frontline ship and cost
            frontline_names.append(frontline[i]['Name'])
            oil_cost += int(float(frontline[i]['Cost']))
    else:
        for i in range(max_range_front):
            # Add the frontline ship and cost
            frontline_names.append(frontline[i]['Name'])
            oil_cost += int(float(frontline[i]['Cost']))
    # Subline
    if(max_range_sub >= 3):
        # Only do the top three
        for i in range(3):
            # Add the frontline ship and cost
            subline_names.append(subline[i]['Name'])
            suboil_cost += int(float(subline[i]['Cost']))
    else:
        for i in range(max_range_sub):
            # Add the frontline ship and cost
            frontline_names.append(subline[i]['Name'])
            suboil_cost += int(float(subline[i]['Cost']))

    if UI == False:
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
        return    
    else:
        # Return all the data
        return(backline_names, frontline_names, oil_cost, subline_names, suboil_cost)

def filter_ships(ships_dict, filter_name="Nation"):
    """ Filter the ship dictionary based on Nation or Rarity """
    new_ship_dict = []
    filter_input = input("Enter the desired " + filter_name + ": ")
    try:
        if filter_name == "Nation": 
            valid_nations.index(filter_input)
        elif filter_name == "Rarity":
            valid_rarity.index(filter_input)
        elif filter_name == "Class":
            valid_class.index(filter_input)
        else:
            print("Error: Filter not supported")
            return ships_dict
    except:
        print("Error: No Filter Applied")
        return ships_dict

    print("Filtering by " + filter_input)
    for ship in ships_dict:
        if(ship[filter_name] == filter_input):
            new_ship_dict.append(ship)
    return new_ship_dict
