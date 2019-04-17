import json
from app import app
from flask import Flask, request, render_template, flash, redirect
from flask_pymongo import PyMongo
from app.forms import *


DB_SERVER_IP = "127.0.0.1:27017"
DB_NAME = "qa"
REQ_COL_NAME = "requirements"
RES_COL_NAME = ""

app.config["MONGO_URI"] = "mongodb://" + DB_SERVER_IP + "/" + DB_NAME
mongo = PyMongo(app)

state = {"proj": 0, "branch": 0, "build": 1}

class Tree:

    tree = {}

    def get(self):
        return self.tree

    def add(self, branch):
        if len(branch) == 0:
            return

        c_tree = self.tree
        for node in branch:
            if node not in c_tree.keys():
                c_tree.update({node: {}})
            c_tree = c_tree[node]

    def to_json(self):
        #self.tree["root"] = self.tree.pop(None)
        return json.dumps(self.tree)

@app.route('/')
def index():
    cmd = [
        #{"$match": {"req_id": {"$ne": None}}},
        {
             "$graphLookup": {
                 "from": REQ_COL_NAME,
                 "startWith": "$parent",
                 "connectFromField": "parent",
                 "connectToField": "desc",
                 "as": "hierarchy"
             }
        }
    ]

    rs = mongo.db.requirements.aggregate(cmd)

    tree = Tree()
    for item in rs:
        tree.add([e["desc"] for e in item["hierarchy"]] + [item["desc"]])

    # rs = mongo.cx["results"].find({"project": state["proj"], "branch": state["branch"], "build": state["build]})
    # flash('proj: {}, branch: {}, build: {}'.format(state["proj"], state["branch"], state["build"]))

    form = PBBForm()
    if form.validate_on_submit():
        return redirect('/')

    return render_template("index.html",
                           requirements=tree.get(), results=None, form=form, state=state)

@app.route('/submit', methods=['get' , 'post'])
def submit():
    state["proj"] = request.form.get("proj", None)
    state["branch"] = request.form.get("branch", None)
    state["build"] = request.form.get("build", None)

    return redirect('/')
