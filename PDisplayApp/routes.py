from flask import render_template

from PDisplayApp import app
import requests
import os


class Config:
    uid = ""
    qrcode = ""
    product = ""
    price = ""

    def __init__(self, uid=None, qrcode=None, product=None, price=None):
        self.uid = uid
        self.qrcode = qrcode
        self.product = product
        self.price = price

    def write_to_file(self):
        with open(CONFIGPATH, "w") as f:
            f.write(self.uid)
            f.write(self.qrcode)
            f.write(self.product)
            f.write(self.price)
            f.close()

    def read_from_file(self):
        with open(CONFIGPATH, "r") as f:
            self.uid = f.readline()
            self.qrcode = f.readline()
            self.product = f.readline()
            self.price = f.readline()
            f.close()


CONFIGPATH = "config.cfg"
URL = "https://m0eses.pythonanywhere.com/PriceDisplay/"
CONFIGINSTANCE = Config()


def create_config():
    response = requests.post(URL)
    CONFIGINSTANCE = Config(response.json()["uid"], response.json()["qr_code_img"], "Brak produktu", "0")
    CONFIGINSTANCE.write_to_file()


def read_config():
    CONFIGINSTANCE.read_from_file()


def check_config():
    if not os.path.isfile(CONFIGPATH):
        create_config()
    else:
        read_config()


@app.route('/')
def main():
    check_config()
    return render_template("index.html", config=CONFIGINSTANCE)
