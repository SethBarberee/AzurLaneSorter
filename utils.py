# Mainly a utility file with the following

# find_Line
# Figure out which line a ship belongs to

# sort_ships
# Sort the dictionary based on a stat

# create_line
# Filter best three for each line and calculate oil cost

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

def create_line(backline, frontline, subline):
    # Create a list of names for each line
    frontline_names = []
    backline_names = []
    subline_names = []
    oil_cost = 0
    suboil_cost = 0 # subs are separate oil
    # See how many ships we have in each lineup
    max_range_back = len(backline)
    max_range_front = len(frontline)
    max_range_sub = len(subline)
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

