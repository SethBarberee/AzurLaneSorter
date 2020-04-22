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

class UIRadioList(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent=parent)
        layout = QVBoxLayout(self)

        # Loop through all the valid stats and add a radio button
        for item in utils.valid_stats:
            self.new_button = QRadioButton(item)
            layout.addWidget(self.new_button)
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
        self.SortList = UIRadioList()
        self.TitleLabel = QLabel('Frontline')

        layout = QHBoxLayout(self) # Horizontal box layout
        layout.addWidget(self.TitleLabel)
        layout.addWidget(self.Label1)
        layout.addWidget(self.Label2)
        layout.addWidget(self.Label3)
        layout.addWidget(self.SortList)

    def set_label(self, new_label):
        self.TitleLabel.setText(new_label)

    def update_pics(self, image_list, name_list):
        # Do a batch update of the images
        t1 = threading.Thread(target=self.Label1.update_image, args=(image_list[0],name_list[0])) 
        t2 = threading.Thread(target=self.Label2.update_image, args=(image_list[1],name_list[1])) 
        t3 = threading.Thread(target=self.Label3.update_image, args=(image_list[2],name_list[2])) 
        t1.start()
        t2.start()
        t3.start()
        t1.join()
        t2.join()
        t3.join()
