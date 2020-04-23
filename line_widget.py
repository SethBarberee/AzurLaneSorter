from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap

import os.path
from os import path

import utils

import requests
import urllib

import threading

class UIShipWidget(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent=parent)
        self.Label = QLabel('Ship')
        self.Picture = QLabel('N/A')
        layout = QVBoxLayout(self) # Horizontal box layout
        layout.addWidget(self.Picture)
        layout.addWidget(self.Label)

    def update_image(self, image, label):
        self.Label.setText(label)
        # TODO check if pic storage exists and if pic already exists
        image_dir = "picStorage"
        name_image = label.replace(" (Retrofit)", "Kai")
        image_path = image_dir + "/" + name_image + "Icon.png"

        # Create requests session to get the image
        # Taken from MediaWiki API page:
        # https://www.mediawiki.org/wiki/API:Allimages

        S = requests.Session()

        URL = "https://azurlane.koumakan.jp/w/api.php" # Base URL for Azur Lane Wiki

        PARAMS = {
            "action": "query",
            "format": "json",
            "list": "allimages",
            "aifrom": name_image + "Icon", # Azur Wiki follows a simple format for icons
            "ailimit": "1" # We only need the top result
        }

        R = S.get(url=URL, params=PARAMS)
        DATA = R.json()

        IMAGES = DATA["query"]["allimages"]

        image_download = IMAGES[0]["url"] # we have the right URL so let's download

        # Download and set
        urllib.request.urlretrieve(image_download, image_path)
        # All good so set the image
        self.Picture.setPixmap(QPixmap(image_path))

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

class UILineWidget(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent=parent)
        self.Label1 = UIShipWidget()
        self.Label2 = UIShipWidget()
        self.Label3 = UIShipWidget()
        self.SortList = UISortList()
        self.FilterList = UIFilterList()
        self.TitleLabel = QLabel('Frontline')

        layout = QHBoxLayout(self) # Horizontal box layout
        layout.addWidget(self.TitleLabel)
        layout.addWidget(self.Label1)
        layout.addWidget(self.Label2)
        layout.addWidget(self.Label3)
        layout.addWidget(self.SortList)
        layout.addWidget(self.FilterList)

    def set_label(self, new_label):
        self.TitleLabel.setText(new_label)

    def update_pics(self, image_list, name_list):
        # Do a batch update of the images
        # TODO/BUG handle case when list < 3
        if len(image_list) == 0 or len(name_list) == 0:
            return
        t1 = threading.Thread(target=self.Label1.update_image, args=(image_list[0],name_list[0])) 
        t2 = threading.Thread(target=self.Label2.update_image, args=(image_list[1],name_list[1])) 
        t3 = threading.Thread(target=self.Label3.update_image, args=(image_list[2],name_list[2])) 
        t1.start()
        t2.start()
        t3.start()
        t1.join()
        t2.join()
        t3.join()
