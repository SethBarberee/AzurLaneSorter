from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import math
import utils

class UISortList(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent=parent)

        layout = QVBoxLayout(self)
        num_rows = 3

        numItemsInColumn = math.floor(len(utils.valid_stats) / num_rows)


        for row in range(num_rows):
            nestLayout = QHBoxLayout()
            for col in range(numItemsInColumn):
                nestLayout.addWidget(QRadioButton(utils.valid_stats[row + col]))
            layout.addLayout(nestLayout)
        # Set first one as default
        self.findChildren(QRadioButton)[0].setChecked(True)

    # This goes through all the RadioButtons and finds which one is selected
    # This is helpful when we figure out how to sort each line
    def get_selected(self):
        selected = ""
        for radio in self.findChildren(QRadioButton):
            if radio.isChecked():
                selected = radio.text()
                break # we found it so let's end for now
        return selected
