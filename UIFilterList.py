from PyQt5.QtWidgets import *

import utils

class UIFilterList(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent=parent)
        self.rarity_layout = QHBoxLayout()
        self.rarity = QCheckBox("Rarity")
        self.rarity_enter = QComboBox()
        for item in utils.valid_rarity:
            self.rarity_enter.addItem(item)
        self.rarity_layout.addWidget(self.rarity)
        self.rarity_layout.addWidget(self.rarity_enter)

        self.nation_layout = QHBoxLayout()
        self.nation = QCheckBox("Nation")
        self.nation_enter = QComboBox()
        for item in utils.valid_nations:
            self.nation_enter.addItem(item)
        self.nation_layout.addWidget(self.nation)
        self.nation_layout.addWidget(self.nation_enter)

        self.class_layout = QHBoxLayout()
        self._class = QCheckBox("Class")
        self.class_enter = QComboBox()
        for item in utils.valid_class:
            self.class_enter.addItem(item)
        self.class_layout.addWidget(self._class)
        self.class_layout.addWidget(self.class_enter)

        layout = QVBoxLayout(self)
        layout.addLayout(self.rarity_layout)
        layout.addLayout(self.nation_layout)
        layout.addLayout(self.class_layout)

    def get_filters(self):
        # return a list/dictionary of filters
        current_filters = {}
        for check in self.findChildren(QCheckBox):
            if(check.isChecked()):
                # get combo box part of checkbox
                checkbox = check.text()
                if checkbox == "Rarity":
                    selected_item = self.rarity_enter.currentText()
                elif checkbox ==  "Nation":
                    selected_item = self.nation_enter.currentText()
                else:
                    selected_item = self.class_enter.currentText()
                current_filters[check.text()] = selected_item
        return current_filters
