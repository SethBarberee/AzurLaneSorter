from PyQt5.QtWidgets import *
import data_scrape, utils

ship_dict = [] # global dictionary for all the ships

def scrape_wiki():
    data_scrape.scrape()
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
    # Clear the lists
    front_list.clear()
    back_list.clear()
    sub_list.clear()
    # TODO make someway to override this
    ship_dict = utils.sort_ships(ship_dict, 'HP')
    # Filter the lines
    (backline, frontline, subline) = utils.find_line(ship_dict)
    # Create the top 3 and calculate oil
    # TODO make way to get preset names
    (back, front, oil, sub, suboil) = utils.create_line(backline, frontline, subline, [], True)
    # Add names to the list
    back_list.addItems(back)
    front_list.addItems(front)
    sub_list.addItems(sub)

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
    front_list_widget = QListWidget()
    back_list_widget = QListWidget()
    sub_list_widget = QListWidget()

    # Connect buttons to functions
    button1.clicked.connect(lambda:load_ships(total_list_widget))
    button2.clicked.connect(lambda:sort_ships(front_list_widget, back_list_widget, sub_list_widget))
    button4.clicked.connect(scrape_wiki)
    button5.clicked.connect(lambda:clear_boxes(front_list_widget, back_list_widget, sub_list_widget))

    # Add menu buttons
    layout.addWidget(button1)
    layout.addWidget(button2)
    layout.addWidget(button3)
    layout.addWidget(button4)
    layout.addWidget(button5)

    # Add list widgets and labels to respective layouts
    total.addWidget(label_total)
    total.addWidget(total_list_widget)
    back.addWidget(label_back)
    back.addWidget(back_list_widget)
    front.addWidget(label_front)
    front.addWidget(front_list_widget)
    sub.addWidget(label_sub)
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
