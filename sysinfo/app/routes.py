from app.forms import *
from flask import Flask, request, render_template, flash, redirect
from werkzeug.urls import url_parse
from app.src import *


@app.route('/')
@app.route('/version')
def version():
    cmd = [
        {"$match": {"timestamp": {"$ne": None}}},
        {"$sort": {"ip": -1, "timestamp": -1}},
        {"$group" : {"_id" : {"ip" : "$ip"}, "data" : {"$first" : "$$ROOT"}}},
        {"$project" : {
            "data": "$data"
            }
        }
    ]

    rs = mongo.db[COL_NAME].aggregate(cmd)

    info = []
    for row in rs:
        del row["data"]["_id"]
        info.append(row["data"])

    # flash('proj: {}'.format(state.dd.proj.value))

    return render_template("version.html", info=info)


@app.route('/status')
def status():
    info = "{}"

    return render_template("status.html", info=info)


@app.route('/history')
def history():
    info = "{}"

    return render_template("history.html", info=info)