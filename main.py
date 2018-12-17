import json
def parse_data():
    # Open the data file for reading
    # loop through line by line
    with open('data.json', 'r') as f:
        ships_dict = json.load(f)
    # TODO parse data from text file into respective arrays
    # TODO concatenate into a list of 6 ships
    # For now, print each ship's name from our json file
    for ship in ships_dict:
        print(ship['Name'])

def main():
    parse_data()


if __name__ == "__main__":
    main()

