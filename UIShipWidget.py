from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap

import requests
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
