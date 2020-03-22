import requests, json

from bs4 import BeautifulSoup

ships_dict = []

def main():
    page = requests.get("https://azurlane.koumakan.jp/List_of_Ships_by_Stats#Level_120")
    soup = BeautifulSoup(page.content, 'html.parser')

    # TODO How do I select each table to go through...
    for i in range(0, len(soup.find_all('div', title = "Level 120"))): # Title
        table = soup.find_all('div', title = "Level 120")[i] # Title

        # Iterate in groups of 20 (since that's one row)
        for x in range(0, len(table.find_all('td')), 20):
            ID = table.find_all('td')[x].get_text() # ID
            name = table.find_all('td')[x + 1].get_text() # name
            rarity = table.find_all('td')[x + 2].get_text() # rarity
            nation = table.find_all('td')[x + 3].get_text() # nation
            _type = table.find_all('td')[x + 4].get_text() # type
            luck = table.find_all('td')[x + 5].get_text() # luck
            armor = table.find_all('td')[x + 6].get_text() # armor
            speed = table.find_all('td')[x + 7].get_text() # speed
            hp = table.find_all('td')[x + 8].get_text() # Title
            firepower = table.find_all('td')[x + 9].get_text() # Title
            aa = table.find_all('td')[x + 10].get_text() # Title
            torpedo = table.find_all('td')[x + 11].get_text() # Title
            evasion = table.find_all('td')[x + 12].get_text() # Title
            aviation = table.find_all('td')[x + 13].get_text() # Title
            cost = table.find_all('td')[x + 14].get_text() # Title
            reloa = table.find_all('td')[x + 15].get_text() # Title
            anti_sub = table.find_all('td')[x + 16].get_text() # Title
            oxygen = table.find_all('td')[x + 17].get_text() # Title
            ammo = table.find_all('td')[x + 18].get_text() # Title
            acc = table.find_all('td')[x + 19].get_text() # Title

            # TODO export to JSON
            new_ship = {
                    "ID": ID,
                    "Name": name,
                    "Rarity": rarity,
                    "Nation": nation,
                    "Class": _type,
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
            # Add to the dictionary
            ships_dict.append(new_ship)

    # All ready to export to JSON
    with open("data_export.json", "w+") as write_file:
        # Dump the data in a nice fashion
        json.dump(ships_dict, write_file, indent = 4, separators=(',',': '))
    return ships_dict

            

if __name__ == "__main__":
    main()

