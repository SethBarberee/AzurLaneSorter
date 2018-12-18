import json
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
    # These are the classes that go in the backline
    backline_set = {'BB', 'BC', 'CV', 'CVL', 'AR', 'CM'}
    for ship in ships_dict:
        if ship['Class'] in backline_set:
            # Matches one of the classes so add it
            backline.append(ship['Name'])
        else:
            # Doesn't match so it's in the front
            frontline.append(ship['Name'])
    # Return which line they are in respectively
    return (backline, frontline)

# TODO: only sorts by one stat... make it do more
def sort_ships(ships_dict, stat='HP'):
    """ Sort the ship dictionary given a certain stat """
    if stat == 'Armor':
        # Armor only has three values
        keyorder = ['Heavy', 'Medium', 'Light' ]
    else:
        # Assign a ranking to each letter
        keyorder = ['S', 'A', 'B', 'C', 'D', 'E' ]
    order = {key: i for i, key in enumerate(keyorder)}
    ship_dict = sorted(ships_dict, key = lambda d: order[d[stat]])
    return ship_dict

def main():
    (ship_dict) = parse_data()
    # TODO find a way to filter based on Nation if desired
    # This is the stat we wish to sort by
    stat = input('Enter the stat you would like to sort by: ')
    print("Sorting by " + stat)
    ship_sorted = sort_ships(ship_dict, stat)
    #print(ship_sorted)
    (backline, frontline) = find_line(ship_sorted)
    # Print the top 3 for each line
    print("Backline:")
    print(backline[0:3])
    print("Frontline:")
    print(frontline[0:3])


if __name__ == "__main__":
    main()

