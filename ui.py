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
    # Add all ships to the list
    list_widget.clear()
    for item in ship_dict:
        list_widget.addItem(item['Name'])
    alert = QMessageBox()
    alert.setText('Ships have been loaded from data.json')
    alert.exec_()

def sort_ships(front_list, back_list, sub_list):
    global ship_dict
    front_list.clear()
    back_list.clear()
    sub_list.clear()
    ship_dict = utils.sort_ships(ship_dict, 'HP')
    (backline, frontline, subline) = utils.find_line(ship_dict)
    (back, front, oil, sub, suboil) = utils.create_line(backline, frontline, subline, [], True)
    back_list.addItems(back)
    front_list.addItems(front)
    sub_list.addItems(sub)

def main():
    app = QApplication([])
    window = QWidget()
    layout = QVBoxLayout() # Vertical box layout
    total = QHBoxLayout() # Vertical box layout
    front = QHBoxLayout() # Vertical box layout
    back = QHBoxLayout() # Vertical box layout
    sub = QHBoxLayout() # Vertical box layout

    button1 = QPushButton('Import Ships')
    button2 = QPushButton('Sort Ships')
    button3 = QPushButton('Add new ships to database')
    button4 = QPushButton('Update stats from AL wiki')

    label_total = QLabel('All Ships')
    label_back = QLabel('Backline')
    label_front = QLabel('Frontline')
    label_sub = QLabel('Submarines')

    total_list_widget = QListWidget()
    front_list_widget = QListWidget()
    back_list_widget = QListWidget()
    sub_list_widget = QListWidget()
    button1.clicked.connect(lambda:load_ships(total_list_widget))
    button2.clicked.connect(lambda:sort_ships(front_list_widget, back_list_widget, sub_list_widget))
    button4.clicked.connect(scrape_wiki)

    layout.addWidget(button1)
    layout.addWidget(button2)
    layout.addWidget(button3)
    layout.addWidget(button4)

    total.addWidget(label_total)
    total.addWidget(total_list_widget)
    back.addWidget(label_back)
    back.addWidget(back_list_widget)
    front.addWidget(label_front)
    front.addWidget(front_list_widget)
    sub.addWidget(label_sub)
    sub.addWidget(sub_list_widget)

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
