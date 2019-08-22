from app.forms import *
from flask import Flask, request, render_template, flash, redirect, session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.src import *


@app.route('/login', methods=['get', 'post'])
def login():
    if current_user.is_authenticated:
        return redirect('/index')

    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User(username=login_form.username.data, password=login_form.password.data)
        if not user.exist():
            return redirect('/login')

        remember = request.form.get("remember", "no") == "yes"
        login_user(user, remember=remember)

        session['username'] = request.form['username']

        return redirect('/index')

    return render_template('login.html', form=login_form)



@app.route('/')
@app.route('/index')
@login_required
def index():
    cmd = [
        {"$match": {"case_id": {"$ne": None}}},
        {
             "$graphLookup": {
                 "from": CASES_COL_NAME,
                 "startWith": "$parent",
                 "connectFromField": "parent",
                 "connectToField": "desc",
                 "as": "hierarchy"
             }
        }
    ]

    rs = mongo.db[CASES_COL_NAME].aggregate(cmd)
    # rs2 = mongo.db.results.find({"case_id": {"$ne": 0}, "project": state.dd.proj.value[1], "branch": state.dd.branch.value[1], "build": state.dd.build.value[1]})

    cmd = [
        {"$match": {"timestamp": {"$ne": None}}},
        {"$sort": {"timestamp": -1, "case_id": -1, "project": -1, "branch": -1, "build": -1}},
        {"$group" : {"_id" : {"case_id" : "$case_id", "project" : "$project", "branch" : "$branch", "build" : "$build"}, "data" : {"$first" : "$$ROOT"}}},
        {"$project" : {
            "req_id": "$data.req_id",
            "case_id": "$data.case_id",
            "project" : "$data.project",
            "branch" : "$data.branch",
            "build" : "$data.build",
            "user" : "$data.user",
            "timestamp" : "$data.timestamp",
            "links" : "$data.links",
            "result" : "$data.result"
            }
        }
    ]
    rs2 = mongo.db[RESULTS_COL_NAME].aggregate(cmd)

    case_arr = [row for row in rs]
    res_arr = [row for row in rs2]

    tree = Tree()
    for item in case_arr:
        if "case_id" not in item.keys():
            tree.add([e["desc"] for e in item["hierarchy"]] + [item["desc"]])
        else:
            req_id = int(item["req_id"])
            case_id = int(item["case_id"])

            result = -1
            timestamp = None
            user = None
            links = None
            for r_item in res_arr:
                r_case_id = int(r_item["case_id"])
                if r_case_id == case_id and state.dd.equals(proj=r_item["project"], branch=r_item["branch"], build=r_item["build"]):
                    if "links" in r_item.keys():
                        links = r_item["links"]

                    if "timestamp" in r_item.keys():
                        user = r_item["user"]
                        timestamp = int(r_item["timestamp"])
                        result = int(r_item["result"])

                    break

            tree.add(branch=[e["desc"] for e in item["hierarchy"]] + [item["desc"]], req_id=req_id, case_id=case_id, result=result,
                             links=links, user=user, timestamp=timestamp)

    # flash('proj: {}'.format(state.dd.proj.value))

    return render_template("index.html",
                           cases=tree.get(), form=PBBForm(), state=state.dd.get())


@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')


@login_required
@app.route('/pbb_submit', methods=['get', 'post'])
def pbb_submit():
    state.dd.update([request.form.get("proj", None), request.form.get("branch", None), request.form.get("build", None)])

    return redirect('/index')


@login_required
@app.route('/case_submit', methods=['get', 'post'])
def case_submit():
    doc = {"project": state.dd.proj.value[1], "branch": state.dd.branch.value[1], "build": state.dd.build.value[1]}
    doc.update(request.get_json())
    doc["result"] = int(doc["result"])

    q_doc = dict((k,doc[k]) for k in doc.keys() if k not in ("result", "links"))

    if request.method == "POST":
        #mongo.db.results.update_one(q_doc, {"$set": doc}, upsert=True)
        mongo.db.results.insert_one(doc)

    return redirect('/index')


@login_required
@app.route('/acc_details', methods=['get', 'post'])
def acc_details():
    return render_template("acc_details.html")


@login_required
@app.route('/set/')
def set():
    session['key'] = 'value'
    return 'ok'

@login_required
@app.route('/get/')
def get():
    return session.get('key', 'not set')