from PyQt5.QtWidgets import *
import data_scrape, utils
from line_widget import UILineWidget

ship_dict = [] # global dictionary for all the ships

def scrape_wiki(checkbox):
    # check whether we need to import only the list or all of them
    if checkbox.isChecked() == True:
        data_scrape.scrape(100, True) # Set to True when we went them all
    else:
        data_scrape.scrape(100, False) # Set to True when we went them all
    alert = QMessageBox()
    alert.setText('Stats have been updated in data_export.json')
    alert.exec_()

def load_ships(list_widget):
    global ship_dict
    ship_dict = utils.parse_data()
    list_widget.clear()
    # Add all ships to the list
    for item in ship_dict:
        list_widget.addItem(item['Name'])
    alert = QMessageBox()
    alert.setText('Ships have been loaded from data.json')
    alert.exec_()

def sort_ships(front_list, back_list, sub_list):
    global ship_dict
    # TODO make someway to override this
    ship_dict = utils.sort_ships(ship_dict, 'HP')
    # Filter the lines
    (backline, frontline, subline) = utils.find_line(ship_dict)
    # Create the top 3 and calculate oil
    # TODO make way to get preset names
    (back, front, oil, sub, suboil) = utils.create_line(backline, frontline, subline, [], True)
    # Add names to the list
    back_images = []
    back_names = []
    for i in range(len(back)):
        back_images.append(back[i]['Image'])
        back_names.append(back[i]['Name'])
    back_list.update_pics(back_images, back_names)

    front_images = []
    front_names = []
    for i in range(len(back)):
        front_images.append(front[i]['Image'])
        front_names.append(front[i]['Name'])
    front_list.update_pics(front_images, front_names)

    sub_images = []
    sub_names = []
    for i in range(len(back)):
        sub_images.append(sub[i]['Image'])
        sub_names.append(sub[i]['Name'])
    sub_list.update_pics(sub_images, sub_names)

def clear_boxes(front_list, back_list, sub_list):
    front_list.clear()
    back_list.clear()
    sub_list.clear()

def main():
    app = QApplication([])
    window = QWidget()
    layout = QVBoxLayout() # Vertical box layout
    total = QHBoxLayout() # Horizontal box layout
    front = QHBoxLayout() # Horizontal box layout
    back = QHBoxLayout() # Horizontal box layout
    sub = QHBoxLayout() # Horizontal box layout

    checkbox1 = QCheckBox("Toggle Import All")
    checkbox1.setChecked(False)

    # Set button labels
    button1 = QPushButton('Import Ships')
    button2 = QPushButton('Sort Ships')
    button3 = QPushButton('Add new ships to database')
    button4 = QPushButton('Update stats from AL wiki')
    button5 = QPushButton('Clear Lines')

    # Set labels for list widgets
    label_total = QLabel('All Ships')
    label_back = QLabel('Backline')
    label_front = QLabel('Frontline')
    label_sub = QLabel('Submarines')

    total_list_widget = QListWidget()
    front_list_widget = UILineWidget()
    back_list_widget = UILineWidget()
    sub_list_widget = UILineWidget()

    # Connect buttons to functions
    button1.clicked.connect(lambda:load_ships(total_list_widget))
    button2.clicked.connect(lambda:sort_ships(front_list_widget, back_list_widget, sub_list_widget))
    button4.clicked.connect(lambda:scrape_wiki(checkbox1))
    button5.clicked.connect(lambda:clear_boxes(front_list_widget, back_list_widget, sub_list_widget))

    # Add menu buttons
    layout.addWidget(button1)
    layout.addWidget(button2)
    layout.addWidget(button3)
    layout.addWidget(button4)
    layout.addWidget(button5)
    layout.addWidget(checkbox1)

    # Add list widgets and labels to respective layouts
    total.addWidget(label_total)
    total.addWidget(total_list_widget)
    #back.addWidget(label_back)
    back.addWidget(back_list_widget)
    #front.addWidget(label_front)
    front.addWidget(front_list_widget)
    #sub.addWidget(label_sub)
    sub.addWidget(sub_list_widget)

    # Nest the layouts in the main layout
    layout.addLayout(total)
    layout.addLayout(back)
    layout.addLayout(front)
    layout.addLayout(sub)

    window.setLayout(layout)
    window.show()
    window.setWindowTitle("Azur Lane Sorter")

    app.exec_()
if __name__ == '__main__':
    main()
