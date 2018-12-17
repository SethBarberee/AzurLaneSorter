import json
def parse_data():
    backline = []
    frontline = []
    # Open the data file for reading
    # loop through line by line
    with open('data.json', 'r') as f:
        ships_dict = json.load(f)
    # For now, print each ship's name from our json file
    for ship in ships_dict:
        # Parse the class for backline/frontline
        if(ship['Class'] != 'BB' and ship['Class'] != 'BC' and ship['Class'] != 'CV' and ship['Class'] != 'CVL'):
            frontline.append(ship['Name'])
        else:
            backline.append(ship['Name'])
    print("Frontline:")
    print(frontline)
    print("Backline:")
    print(backline)

def main():
    parse_data()


if __name__ == "__main__":
    main()

