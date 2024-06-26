from PyQt6.QtWidgets import *
from PyQt6.QtGui import QAction, QIcon
import data_scrape
import utils
from UILineWidget import UILineWidget
from UIAddShip import UIAddShip

import threading
import sys

ship_dict = {} # global dictionary for all the ships

preset_ships = []


def add_preset(total_list_widget, preset_list_widget):
    global preset_ships
    global ship_dict
    for item in total_list_widget.selectedItems():
        for ship in ship_dict:
            try:
                # Check if we have it in our list yet
                preset_ships.index(ship)
            except ValueError:
                # we know it's not so add it now
                if ship["Name"] == item.text():
                    preset_ships.append(ship)
                    preset_list_widget.addItem(item.text())
                    break


def remove_preset(preset_list_widget):
    global preset_ships
    for item in preset_list_widget.selectedItems():
        for ship in ship_dict:
            if ship["Name"] == item.text():
                preset_list_widget.takeItem(preset_list_widget.row(item))
                preset_ships.remove(ship)
                break


# Take the line and prepare the image link and Name
def prepare_for_update(line):
    images = []
    names = []
    for i in range(len(line)):
        images.append(line[i]['Image'])
        names.append(line[i]['Name'])
    return (images, names)


def scrape_wiki(checkbox):
    # check whether we need to import only the list or all of them
    if checkbox.isChecked() is True:
        data_scrape.scrape(100, True)  # Set to True when we went them all
    else:
        data_scrape.scrape(100, False)  # Set to True when we went them all
    alert = QMessageBox()
    alert.setText('Stats have been updated in data_export.json')
    alert.exec()


def load_ships(list_widget):
    global ship_dict
    ship_dict = utils.parse_data()
    list_widget.clear()
    # Add all ships to the list
    for item in ship_dict:
        list_widget.addItem(item['Name'])
    alert = QMessageBox()
    alert.setText('Ships have been loaded from data.json')
    alert.exec()


def sort_ships(front_list, back_list, sub_list, preset_list):
    global ship_dict
    # Filter by line
    clear_boxes(front_list, back_list, sub_list, preset_list, False)
    (backline, frontline, subline) = utils.find_line(ship_dict)

    # Sort by selected stat
    # TODO maybe parallelize
    backline = utils.sort_ships(backline, back_list.SortList.get_selected())
    frontline = utils.sort_ships(frontline, front_list.SortList.get_selected())
    subline = utils.sort_ships(subline, sub_list.SortList.get_selected())

    # Get filters
    back_filters = back_list.FilterList.get_filters()
    front_filters = front_list.FilterList.get_filters()
    sub_filters = sub_list.FilterList.get_filters()

    # loop through filters and apply filters
    for i in back_filters[0].keys():
        backline = utils.filter_ships_ui(backline, i, back_filters)
    for i in front_filters[0].keys():
        frontline = utils.filter_ships_ui(frontline, i, front_filters)
    for i in sub_filters[0].keys():
        subline = utils.filter_ships_ui(subline, i, sub_filters)

    # Create the lists
    (back, front, oil, sub, suboil) = utils.create_line(backline, frontline, subline, preset_ships, True)

    # Add names to the list
    (back_images, back_names) = prepare_for_update(back)
    t1 = threading.Thread(target=back_list.update_pics, args=(back_images, back_names))

    (front_images, front_names) = prepare_for_update(front)
    t2 = threading.Thread(target=front_list.update_pics, args=(front_images, front_names))

    (sub_images, sub_names) = prepare_for_update(sub)
    t3 = threading.Thread(target=sub_list.update_pics, args=(sub_images, sub_names))
    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()


def clear_boxes(front_list, back_list, sub_list, preset_list, clear_preset):
    global preset_ships
    if (clear_preset):
        preset_ships = []
        preset_list.clear()
    front_list.clear_line()
    back_list.clear_line()
    sub_list.clear_line()


def add_ship():
    global dialog
    dialog.show()


def close_window(window):
    window.close()


def main():
    app = QApplication(sys.argv)
    window = QMainWindow()

    global dialog
    dialog = UIAddShip()

    window.statusbar = window.statusBar()
    window.statusbar.showMessage('Ready')

    menubar = window.menuBar()
    FileMenu = menubar.addMenu('File')

    wikiAct = QAction('Update Stats from Wiki', window)
    wikiAct.setStatusTip('Update Wiki Stats')
    FileMenu.addAction(wikiAct)

    newShipAct = QAction('Add new ships to database', window)
    newShipAct.setStatusTip('Add new ship')
    FileMenu.addAction(newShipAct)

    quitAct = QAction('Quit', window)
    quitAct.setStatusTip('Quit')
    FileMenu.addAction(quitAct)

    base_window = QWidget()
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
    button3 = QPushButton('Clear Lines')

    # Set labels for list widgets
    label_total = QLabel('All Ships')
    label_back = QLabel('Backline')
    label_front = QLabel('Frontline')
    label_sub = QLabel('Submarines')
    label_preset = QLabel('Preset Ships')

    # Create the preset layout
    preset_layout = QVBoxLayout()
    AddPreset = QPushButton(">>")
    RemovePreset = QPushButton("<<")
    preset_layout.addWidget(AddPreset)
    preset_layout.addWidget(RemovePreset)

    # Create Preset/Total Layout
    total_list_widget = QListWidget()
    total_list_widget.setSortingEnabled(True)
    preset_list_widget = QListWidget()
    preset_list_widget.setSortingEnabled(True)
    list_layout = QHBoxLayout()
    list_layout.addWidget(total_list_widget)
    list_layout.addLayout(preset_layout)
    list_layout.addWidget(preset_list_widget)
    list_layout.addWidget(label_preset)
    total.addWidget(label_total)
    total.addLayout(list_layout)
    AddPreset.clicked.connect(lambda: add_preset(total_list_widget, preset_list_widget))
    RemovePreset.clicked.connect(lambda: remove_preset(preset_list_widget))

    # Set up the line widgets
    front_list_widget = UILineWidget('Frontline')
    back_list_widget = UILineWidget('Backline')
    sub_list_widget = UILineWidget('Subline')
    back.addWidget(back_list_widget)
    front.addWidget(front_list_widget)
    sub.addWidget(sub_list_widget)
 
    # Connect buttons to functions
    # button1.triggered.connect(lambda:load_ships(total_list_widget))
    button1.clicked.connect(lambda: load_ships(total_list_widget))
    button2.clicked.connect(lambda: sort_ships(front_list_widget, back_list_widget, sub_list_widget, preset_list_widget))
    wikiAct.triggered.connect(lambda: scrape_wiki(checkbox1))
    quitAct.triggered.connect(lambda: close_window(window))
    newShipAct.triggered.connect(lambda: add_ship())
    button3.clicked.connect(lambda: clear_boxes(front_list_widget, back_list_widget, sub_list_widget, preset_list_widget, True))

    # Add menu buttons
    layout.addWidget(button1)
    layout.addWidget(button2)
    layout.addWidget(button3)
    layout.addWidget(checkbox1)

    # Add list widgets and labels to respective layouts
    # Nest the layouts in the main layout
    layout.addLayout(total)
    layout.addLayout(back)
    layout.addLayout(front)
    layout.addLayout(sub)
    layout.addStretch(0)

    base_window.setLayout(layout)

    window.setCentralWidget(base_window)
    window.setWindowTitle("Azur Lane Sorter")
    window.setWindowIcon(QIcon("icon.jpg"))
    window.show()

    app.exec()

if __name__ == '__main__':
    main()
