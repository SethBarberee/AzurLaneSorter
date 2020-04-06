from PyQt5.QtWidgets import *
import data_scrape, utils

ship_dict = [] # global dictionary for all the ships

def scrape_wiki():
    data_scrape.scrape()
    alert = QMessageBox()
    alert.setText('Stats have been updated in data_export.json')
    alert.exec_()

def load_ships():
    ship_dict = utils.parse_data()
    alert = QMessageBox()
    alert.setText('Ships have been loaded from data.json')
    alert.exec_()

app = QApplication([])
window = QWidget()
layout = QVBoxLayout() # Vertical box layout

button1 = QPushButton('Import Ships')
button2 = QPushButton('Sort Ships')
button3 = QPushButton('Add new ships to database')
button4 = QPushButton('Update stats from AL wiki')
button1.clicked.connect(load_ships)
button4.clicked.connect(scrape_wiki)

layout.addWidget(button1)
layout.addWidget(button2)
layout.addWidget(button3)
layout.addWidget(button4)

window.setLayout(layout)
window.show()

app.exec_()
