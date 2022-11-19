#Contains the routings and the view functions
import json

from flask import Flask, render_template, flash, redirect, url_for, request

app = Flask(__name__)
# app.config['SESSION_TYPE'] = 'filesystem'

@app.route('/')
@app.route("/home")
def home():
    return render_template("Home.html")

@app.route("/Q1")
def location():
    return render_template("Location.html")

@app.route("/Q1b")
def chooselocation():
    return render_template("chooselocation.html")

@app.route("/Q2")
def duration():
    return render_template("duration.html")

@app.route("/Q3")
def budget():
    return render_template("budget.html")

@app.route("/Q4")
def accompany():
    return render_template("Accompany.html")


