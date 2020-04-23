from PyQt5.QtWidgets import *

import utils

class UISortList(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent=parent)
        layout = QGridLayout(self)

        divider = len(utils.valid_stats) / 3 # Split into three columns
        # Loop through all the valid stats and add a radio button
        for i in range(len(utils.valid_stats)):
            row = i % divider # figure out the row
            col = i / divider # figure out the column
            self.new_button = QRadioButton(utils.valid_stats[i])
            layout.addWidget(self.new_button, row, col)
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
