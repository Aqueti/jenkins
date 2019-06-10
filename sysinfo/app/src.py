from flask import flash
from flask_pymongo import PyMongo
from app import app
import json


DB_SERVER_IP = "10.0.0.176:27017"
DB_NAME = "qa"
COL_NAME = "sysinfo"

app.config["MONGO_URI"] = "mongodb://" + DB_SERVER_IP + "/" + DB_NAME
mongo = PyMongo(app)

