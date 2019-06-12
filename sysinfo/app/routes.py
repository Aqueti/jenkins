from app.forms import *
from flask import Flask, request, render_template, flash, redirect
from werkzeug.urls import url_parse
from app.src import *


def get_info():
    cmd = [
        {"$match": {"timestamp": {"$ne": None}}},
        {"$sort": {"ip": -1, "timestamp": -1}},
        {"$group": {"_id": {"ip": "$ip"}, "data": {"$first": "$$ROOT"}}},
        {"$project": {
            "data": "$data"
        }
        }
    ]

    rs = mongo.db[COL_NAME].aggregate(cmd)

    info = []
    for row in rs:
        del row["data"]["_id"]
        info.append(row["data"])

    return info


@app.route('/')
@app.route('/version')
def version():

    # flash('proj: {}'.format(state.dd.proj.value))

    return render_template("version.html", info=get_info())


@app.route('/status')
def status():
    return render_template("status.html", info=get_info())


@app.route('/history')
def history():
    return render_template("history.html", info=get_info())