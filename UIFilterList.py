from PyQt5.QtWidgets import *

import utils

class UIFilterList(QWidget):
    def __init__(self, label, parent = None):
        QWidget.__init__(self, parent=parent)
        self.rarity_layout = QHBoxLayout()
        self.rarity = QCheckBox("Rarity")
        self.rarity_cond = QComboBox()
        self.rarity_enter = QComboBox()
        for item in utils.valid_rarity:
            self.rarity_enter.addItem(item)
        for item in ["=", "<", ">", "<=", ">=", "!="]:
            self.rarity_cond.addItem(item)
        self.rarity_layout.addWidget(self.rarity)
        self.rarity_layout.addWidget(self.rarity_cond)
        self.rarity_layout.addWidget(self.rarity_enter)

        self.nation_layout = QHBoxLayout()
        self.nation = QCheckBox("Nation")
        self.nation_cond = QComboBox()
        self.nation_enter = QComboBox()
        for item in utils.valid_nations:
            self.nation_enter.addItem(item)
        for item in ["=", "!="]:
            self.nation_cond.addItem(item)
        self.nation_layout.addWidget(self.nation)
        self.nation_layout.addWidget(self.nation_cond)
        self.nation_layout.addWidget(self.nation_enter)

        self.class_layout = QHBoxLayout()
        self._class = QCheckBox("Class")
        self.class_cond = QComboBox()
        self.class_enter = QComboBox()
        for item in utils.valid_class[label]:
            self.class_enter.addItem(item)
        for item in ["=", "!="]:
            self.class_cond.addItem(item)
        self.class_layout.addWidget(self._class)
        self.class_layout.addWidget(self.class_cond)
        self.class_layout.addWidget(self.class_enter)

        layout = QVBoxLayout(self)
        layout.addLayout(self.rarity_layout)
        layout.addLayout(self.nation_layout)
        layout.addLayout(self.class_layout)

    def get_filters(self):
        # return a list/dictionary of filters
        current_filters = {}
        filter_conditional = {}
        for check in self.findChildren(QCheckBox):
            if(check.isChecked()):
                # get combo box part of checkbox
                checkbox = check.text()
                if checkbox == "Rarity":
                    selected_item = self.rarity_enter.currentText()
                    cond_check = self.rarity_cond.currentText()
                elif checkbox ==  "Nation":
                    selected_item = self.nation_enter.currentText()
                    cond_check = self.nation_cond.currentText()
                else:
                    selected_item = self.class_enter.currentText()
                    cond_check = self.class_cond.currentText()
                current_filters[check.text()] = selected_item
                filter_conditional[check.text()] = cond_check
        return current_filters, filter_conditional
