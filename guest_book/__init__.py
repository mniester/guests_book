from flask import Flask
import json

app = Flask('guest_book')
app.config.from_file("config.json", load=json.load)

