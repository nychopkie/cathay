#Contains the routings and the view functions
import json
from random import randint

from flask import Flask, render_template

app = Flask(__name__)
# app.config['SESSION_TYPE'] = 'filesystem'

@app.route('/')
@app.route("/home/")
def home():
    return render_template("Home.html")

