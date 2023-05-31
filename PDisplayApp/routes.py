from flask import render_template

from PDisplayApp import app
import requests
import os


CONFIGPATH = "config.cfg"
URL = "https://m0eses.pythonanywhere.com/PriceDisplay/"


class Config:
    uid = ""
    qrcode = ""
    product = ""
    price = ""
    url = URL

    def save(self, uid=None, qrcode=None, product=None, price=None):
        self.uid = uid
        self.qrcode = qrcode
        self.product = product
        self.price = price
        self.write_to_file()

    def write_to_file(self):
        with open(CONFIGPATH, "w") as f:
            f.write(self.uid + "\n")
            f.write(self.qrcode + "\n")
            f.write(self.product + "\n")
            f.write(self.price + "\n")
            f.close()

    def read_from_file(self):
        with open(CONFIGPATH, "r") as f:
            self.uid = f.readline()
            self.qrcode = f.readline()
            self.product = f.readline()
            self.price = f.readline()
            f.close()

    def sync_from_server(self):
        url = f"{URL}{self.uid}/".replace("\n", "")
        response = requests.get(f"{url}/")
        self.save(response.json()["uid"],
                  response.json()["qr_code_img"],
                  response.json()["product"]["name"],
                  response.json()["product"]["price"]
                  )


CONFIGINSTANCE = Config()


def check_config():
    if not os.path.isfile(CONFIGPATH):
        response = requests.post(URL)
        CONFIGINSTANCE.save(response.json()["uid"], response.json()["qr_code_img"], "Brak produktu", "0")
        CONFIGINSTANCE.write_to_file()
    else:
        CONFIGINSTANCE.read_from_file()
        CONFIGINSTANCE.sync_from_server()


@app.route('/')
def main():
    check_config()
    return render_template("index.html", config=CONFIGINSTANCE)
