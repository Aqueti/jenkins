from app.forms import *
from flask import Flask, request, render_template, flash, redirect
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
        return redirect('/index')

    return render_template('login.html', form=login_form)


@app.route('/')
@app.route('/index')
@login_required
def index():
    cmd = [
        {"$match": {"req_id": {"$ne": None}}},
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

    rs = mongo.db[REQ_COL_NAME].aggregate(cmd)
    rs2 = mongo.db.results.find({"req_id": {"$ne": 0}, "project": state.dd.proj.value[1], "branch": state.dd.branch.value[1], "build": state.dd.build.value[1]})

    req_arr = [row for row in rs]
    res_arr = [row for row in rs2]

    tree = Tree()
    for item in req_arr:
        if "req_id" not in item.keys():
            tree.add([e["desc"] for e in item["hierarchy"]] + [item["desc"]])
        else:
            req_id = int(item["req_id"])

            result = -1
            links = None
            for r_item in res_arr:
                r_req_id = int(r_item["req_id"])
                if r_req_id == req_id:
                    if "links" in r_item.keys():
                        links = r_item["links"]
                    result = int(r_item["result"])
                    break

            tree.add(branch=[e["desc"] for e in item["hierarchy"]] + [item["desc"]], req_id=req_id, result=result, links=links)

    # flash('proj: {}'.format(state.dd.proj.value))

    return render_template("index.html",
                           requirements=tree.get(), form=PBBForm(), state=state.dd.get())


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.route('/pbb_submit', methods=['get', 'post'])
@login_required
def pbb_submit():
    state.dd.update([request.form.get("proj", None), request.form.get("branch", None), request.form.get("build", None)])

    return redirect('/index')


@app.route('/req_submit', methods=['get', 'post'])
@login_required
def req_submit():
    doc = {"project": state.dd.proj.value[1], "branch": state.dd.branch.value[1], "build": state.dd.build.value[1]}
    doc.update(request.get_json())
    doc["result"] = int(doc["result"])
    q_doc = dict((k,doc[k]) for k in doc.keys() if k not in ("result", "links"))

    if request.method == "POST":
        mongo.db.results.update_one(q_doc, {"$set": doc}, upsert=True)

    return redirect('/index')
