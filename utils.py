import json # global

# Mainly a utility file with the following

# find_Line
# Figure out which line a ship belongs to

# sort_ships
# Sort the dictionary based on a stat

# create_line
# Filter best three for each line and calculate oil cost


# Global dictionaries that UI/Console use for validation
global valid_nations
global valid_rarity
global valid_class
global valid_stats

# Useful lists for filtering and data validation
valid_nations = ['Eagle Union', 'Royal Navy', 'Ironblood', 'Sakura Empire', 'Dragon Empery', 'Sardegna Empire', 'North Union', 'Iris Libre', 'Vichya Dominion']
valid_rarity =  ['Common', 'Rare', 'Elite', 'Super Rare', 'Ultra']
valid_class = {
        "Backline": ['BB', 'BC', 'BM', 'CV', 'CVL', 'AR'],
        "Frontline": ['CL', 'CA', 'CB', 'DD'],
        "Subline": ['SS', 'AM'],
}
valid_stats = [
            "HP",
            "Luck",
            "Armor",
            "Speed",
            "Firepower",
            "Anti-Air",
            "Torpedo",
            "Evasion",
            "Aviation",
            "Cost",
            "Reload",
            "Anti-Submarine",
            "Oxygen",
            "Ammunition",
            "Accuracy",
            ]

valid_armor = ['Heavy', 'Medium', 'Light' ]


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
    for ship in ships_dict:
        if ship['Class'] in valid_class["Backline"]:
            # Matches one of the classes so add it
            backline.append(ship)
        elif ship['Class'] in valid_class["Subline"]:
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
    try:
        valid_stats.index(stat)
    except:
        # Not there so we'll use HP
        stat = "HP"

    if stat == 'Armor':
        order = {key: i for i, key in enumerate(valid_armor)}
        sorted_ship_dict = sorted(ships_dict, key = lambda d: order[d[stat]])
    elif stat == 'Cost':
        sorted_ship_dict = sorted(ships_dict, key = lambda d: d[stat])
    else:
        sorted_ship_dict = sorted(ships_dict, key = lambda d: d[stat], reverse=True)
    return sorted_ship_dict

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
            if UI == False:
                backline_names.append(preset_backline[i]['Name'])
            else:
                backline_names.append(preset_backline[i])
            oil_cost += int(float(preset_backline[i]['Cost']))
        for i in range(len(preset_frontline)):
            # Add the backline ship and cost
            if UI == False:
                frontline_names.append(preset_frontline[i]['Name'])
            else:
                frontline_names.append(preset_frontline[i])
            oil_cost += int(float(preset_frontline[i]['Cost']))
        for i in range(len(preset_subline)):
            # Add the backline ship and cost
            if UI == False:
                subline_names.append(preset_subline[i]['Name'])
            else:
                subline_names.append(preset_subline[i])
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
            if UI == False:
                backline_names.append(backline[i]['Name'])
            else:
                backline_names.append(backline[i])
            oil_cost += int(float(backline[i]['Cost']))
    else:
        for i in range(max_range_back):
            # Add the backline ship and cost
            if UI == False:
                backline_names.append(backline[i]['Name'])
            else:
                backline_names.append(backline[i])
            oil_cost += int(float(backline[i]['Cost']))
    # Frontline 
    if(max_range_front >= 3):
        # Only do the top three
        for i in range(3):
            # Add the frontline ship and cost
            if UI == False:
                frontline_names.append(frontline[i]['Name'])
            else:
                frontline_names.append(frontline[i])
            oil_cost += int(float(frontline[i]['Cost']))
    else:
        for i in range(max_range_front):
            # Add the frontline ship and cost
            if UI == False:
                frontline_names.append(frontline[i]['Name'])
            else:
                frontline_names.append(frontline[i])
            oil_cost += int(float(frontline[i]['Cost']))
    # Subline
    if(max_range_sub >= 3):
        # Only do the top three
        for i in range(3):
            # Add the frontline ship and cost
            if UI == False:
                subline_names.append(subline[i]['Name'])
            else:
                subline_names.append(subline[i])
            suboil_cost += int(float(subline[i]['Cost']))
    else:
        for i in range(max_range_sub):
            # Add the frontline ship and cost
            if UI == False:
                subline_names.append(subline[i]['Name'])
            else:
                subline_names.append(subline[i])
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


# TODO merge with normal filter
def filter_ships_ui(ships_dict, name_filter, filters):
    """ Filter the ship dictionary based on Nation or Rarity """
    new_ship_dict = []
    # Structure of filters
    #    0        |         1
    #   Name      |    Conditional

    if(filters[1][name_filter] == '='):
        for ship in ships_dict:
            if(ship[name_filter] == filters[0][name_filter]):
                new_ship_dict.append(ship)
    elif(filters[1][name_filter] == '!='):
        for ship in ships_dict:
            if(ship[name_filter] != filters[0][name_filter]):
                new_ship_dict.append(ship)
    else:
        print("TODO: implement filter of " + filters[1][i])
        return ships_dict

    return new_ship_dict
