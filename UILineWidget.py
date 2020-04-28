from PyQt5.QtWidgets import *

import os.path
from os import path

import utils
from UIShipWidget import UIShipWidget
from UIFilterList import UIFilterList
from UISortList import UISortList

import threading

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
        print(name_list)
        if len(image_list) == 0 or len(name_list) == 0:
            return
        if len(name_list) == 2:
            t1 = threading.Thread(target=self.Label1.update_image, args=(image_list[0],name_list[0])) 
            t2 = threading.Thread(target=self.Label2.update_image, args=(image_list[1],name_list[1])) 
            t1.start()
            t2.start()
            t1.join()
            t2.join()
        elif len(name_list) == 1:
            t1 = threading.Thread(target=self.Label1.update_image, args=(image_list[0],name_list[0])) 
            t1.start()
            t1.join()
        else:
            t1 = threading.Thread(target=self.Label1.update_image, args=(image_list[0],name_list[0])) 
            t2 = threading.Thread(target=self.Label2.update_image, args=(image_list[1],name_list[1])) 
            t3 = threading.Thread(target=self.Label3.update_image, args=(image_list[2],name_list[2])) 
            t1.start()
            t2.start()
            t3.start()
            t1.join()
            t2.join()
            t3.join()
