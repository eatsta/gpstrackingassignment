# main.py

from flask import Blueprint, render_template
from flask_login import login_required, current_user
import psycopg2
from time import sleep
main = Blueprint('main', __name__)

def grabber(device_id,lat,long):
    con = psycopg2.connect(database="", user="", password="", host="localhost", port="5432")
    cur = con.cursor()
    cur.execute("SELECT device_id,latitude,longtitude from iotdata order by key desc limit 1")
    gps = cur.fetchall()
    for row in gps:
        device_id=row[0]
        lat=row[1]
        long=row[2]

    return device_id,lat,long

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)
@main.route('/map')
def map():
    device_id=0
    long=0
    lat=0
    device_id,lat,long=grabber(device_id,lat,long)
    return render_template('map.html', lat=lat, long=long, device_id=device_id,name=current_user.name)
