from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize

import requests
import urllib

from pathlib import Path

class UIShipWidget(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent=parent)
        self.Label = QLabel('Ship')
        self.Picture = QLabel('N/A')
        layout = QVBoxLayout(self) # Horizontal box layout
        layout.addWidget(self.Picture)
        layout.addWidget(self.Label)
        layout.addStretch(0)

    def clear_widget(self):
        self.Label.setText('Ship')
        self.Picture.setText('N/A')

    def update_image(self, image, label):

        # TODO use JoinPaths from pathLib
        self.Label.setText(label)
        image_dir = 'picStorage'
        image_dir_path = Path(image_dir)
        # check if picStorage exits, else create it
        if not image_dir_path.exists():
            image_dir_path.mkdir()

        # Clean up the file name
        name_image = label.replace(' (Retrofit)', 'Kai')
        name_image = name_image.replace(' ', '_')

        image_path = image_dir + '/' + name_image + 'Icon.png'
        image_path_path = Path(image_path)
        # check if image exists, else download it
        if not image_path_path.exists():
            print("Image doesn't exist for: " + image_path)
            # Create requests session to get the image
            # Taken from MediaWiki API page:
            # https://www.mediawiki.org/wiki/API:Allimages

            S = requests.Session()
            S.headers = {'User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36'}

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

            image_download = IMAGES[0]["url"]

            # Add headers so we can retreive the image..
            # https://blog.actorsfit.com/a?ID=00950-bbd34616-a40c-4a26-993b-6e9816acd7ad
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-Agent',
                                  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]

            urllib.request.install_opener(opener)

            # Download and set
            urllib.request.urlretrieve(image_download, image_path)

        # All good so set the image
        self.Picture.setPixmap(QPixmap(image_path))
        self.Picture.setToolTip(name_image)
