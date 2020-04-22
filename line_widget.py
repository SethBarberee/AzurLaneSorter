from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap

import os.path
from os import path

import urllib

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
        # TODO check if pic storage exists
        image_dir = "picStorage"
        name_image = label.replace(" (Retrofit)", "Kai")
        image_download = "https://azurlane.koumakan.jp/File:" + name_image.replace(" ", "_") + "Icon.png"
        image_path = image_dir + "/" + name_image + "Icon.png"

        print("testing path:")
        print(image_path)
        # TODO uncomment when we get downloading the image working versus downloading the page
        #urllib.request.urlretrieve(image_download, image_path)
        # TODO we'll set to just Hood for now
        image_path = image_dir + "/" + "Hood" + "Icon.png"
        self.Picture.setPixmap(QPixmap(image_path))


class UILineWidget(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent=parent)
        self.Label1 = UIShipWidget()
        self.Label2 = UIShipWidget()
        self.Label3 = UIShipWidget()
        self.TitleLabel = QLabel('Frontline') # TODO figure out best way to change this

        layout = QHBoxLayout(self) # Horizontal box layout
        layout.addWidget(self.TitleLabel)
        layout.addWidget(self.Label1)
        layout.addWidget(self.Label2)
        layout.addWidget(self.Label3)

    def set_label(self, new_label):
        self.TitleLabel.setText(new_label)
    
    def update_pics(self, image_list, name_list):
        self.Label1.update_image(image_list[0], name_list[0])
        self.Label2.update_image(image_list[1], name_list[1])
        self.Label3.update_image(image_list[2], name_list[2])
