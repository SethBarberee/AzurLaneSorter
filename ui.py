from PyQt5.QtWidgets import *
import data_scrape, utils
from line_widget import UILineWidget

import threading

ship_dict = [] # global dictionary for all the ships

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
    # Filter by line
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

    # TODO loop through filters and apply filters
    for i in back_filters.keys():
        backline = utils.filter_ships_ui(backline, i, back_filters[i])
    for i in front_filters.keys():
        frontline = utils.filter_ships_ui(frontline, i, front_filters[i])
    for i in sub_filters.keys():
        subline = utils.filter_ships_ui(subline, i, sub_filters[i])
    # TODO make way to get preset names
    (back, front, oil, sub, suboil) = utils.create_line(backline, frontline, subline, [], True)

    # Add names to the list
    # TODO I could probably parallelize appending the names/images to respective lists
    (back_images, back_names) = prepare_for_update(back)
    # dispatch thread to update backline
    t1 = threading.Thread(target=back_list.update_pics, args=(back_images,back_names)) 
    t1.start()

    (front_images, front_names) = prepare_for_update(front)
    # dispatch thread to update frontline
    t2 = threading.Thread(target=front_list.update_pics, args=(front_images,front_names)) 
    t2.start()

    (sub_images, sub_names) = prepare_for_update(sub)
    # dispatch thread to update subline
    t3 = threading.Thread(target=sub_list.update_pics, args=(sub_images,sub_names)) 
    t3.start()

    t1.join()
    t2.join()
    t3.join()
    
def clear_boxes(front_list, back_list, sub_list):
    print("TODO: fix this")
    # TODO fix this to clear the widgets

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

    # Set up the line widgets
    front_list_widget = UILineWidget()
    front_list_widget.set_label('Frontline')
    back_list_widget = UILineWidget()
    back_list_widget.set_label('Backline')
    sub_list_widget = UILineWidget()
    sub_list_widget.set_label('Subline')

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
