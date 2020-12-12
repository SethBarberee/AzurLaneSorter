from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
import data_scrape, utils

class UIAddShip(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self, parent=parent)
        self.setModal(True)
        self.dialog_layout = QFormLayout() # Vertical box layout

        for item in ["ID", "Name", "Rarity", "Nation" "Class"]:
            label = QLabel(item)
            label_test= QLineEdit()
            self.dialog_layout.addRow(label, label_test)

        for item in utils.valid_stats:
            label = QLabel(item)
            label_test= QLineEdit()
            self.dialog_layout.addRow(label, label_test)

        save_button = QPushButton("Save")
        quit_button = QPushButton("Quit")
        save_button.clicked.connect(lambda:self.get_data())
        self.dialog_layout.addRow(save_button, quit_button)
        self.setLayout(self.dialog_layout)
        self.setWindowTitle("Azur Lane Sorter")
        self.setWindowIcon(QIcon("icon.jpg"))
    def get_data(self):
        num = self.dialog_layout.count()
        for item in range(num):
            # TODO get data from each row
            print(self.dialog_layout.itemAt(item))


