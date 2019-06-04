from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import flash
from flask_pymongo import PyMongo
from app import app
from app import login
import json


DB_SERVER_IP = "127.0.0.1:27017"
DB_NAME = "qa"
REQ_COL_NAME = "req"
RES_COL_NAME = "results"

app.config["MONGO_URI"] = "mongodb://" + DB_SERVER_IP + "/" + DB_NAME
mongo = PyMongo(app)


class Tree:
    tree = {}

    def get(self):
        return self.tree

    def add(self, **kwargs):
        branch = kwargs["branch"]

        if len(branch) == 0:
            return

        c_tree = self.tree
        for node in branch:
            if node not in c_tree.keys():
                c_tree.update({node: {}})
            c_tree = c_tree[node]

        c_tree.update({"req_id": kwargs["req_id"], "result": kwargs["result"], "links": kwargs["links"], "user": kwargs["user"], "timestamp": kwargs["timestamp"]})


class User(UserMixin):
    def __init__(self, **kwargs):
        if "username" in kwargs:
            self.username = kwargs["username"]
        if "password" in kwargs:
            self.password = kwargs["password"]
        if "password_hash" in kwargs:
            self.password_hash = kwargs["password_hash"]

        self.id = 1

        self.active = True

    def query_db(self, query):
        rs = mongo.db.users.find(query)
        for row in rs:
            return row

        return None

    def gen_hash(self, password):
        self.password_hash = generate_password_hash(password)
        return self.password_hash

    def verify_passwd(self, password):
        return check_password_hash(password, self.password)

    def exist(self):
        rs = self.query_db({"username": self.username})

        if rs is not None:
            return self.verify_passwd(rs["password"])


class Struct():
    value = None
    choices = None

class DD():
    proj = None
    branch = None
    build = None

    def __init__(self):
        self.proj = Struct()
        self.branch = Struct()
        self.build = Struct()

        self.proj.choices = self.get_list("proj")

        if self.proj.value is None:
            if len(self.proj.choices) > 0:
                self.proj.value = self.proj.choices[-1]

        self.branch.choices = self.get_list("branch")

        if self.branch.value is None:
            if len(self.branch.choices) > 0:
                self.branch.value = next(choice for choice in self.branch.choices if choice[1] == "beta")

        self.build.choices = self.get_list("build")

        if len(self.build.choices) > 0:
            self.build.value = self.build.choices[-1]

    def equals(self, **kwargs):
        res = True

        if "proj" in kwargs:
            res &= self.proj.value[1] == kwargs["proj"]
        if "branch" in kwargs:
            res &= self.branch.value[1] == kwargs["branch"]
        if "build" in kwargs:
            res &= int(self.build.value[1]) == int(kwargs["build"])

        return res

    def get(self):
        return {"proj": self.proj.value, "branch": self.branch.value, "build": self.build.value}

    def get_list(self, name):
        if name == "proj":
            lst = mongo.db.results.distinct("project")
        elif name == "branch":
            lst = mongo.db.results.distinct("branch", {"project": self.proj.value[1]})
        elif name == "build":
            lst = mongo.db.results.distinct("build", {"branch": self.branch.value[1], "project": self.proj.value[1]})
        else:
            lst = list()

        return list(zip([i for i in range(len(lst))], lst))

    def update(self, state):
        if self.proj.value[0] != int(state[0]):
            val = [choice for choice in self.proj.choices if choice[0] == int(state[0])]
            if len(val) != 0:
                self.proj.value = val[0]
            else:
                self.proj.value = self.proj.choices[-1]

            self.branch.choices = self.get_list("branch")
            self.build.choices = self.get_list("build")

            self.branch.value = self.branch.choices[-1]
            self.build.value = self.build.choices[-1]

        elif self.branch.value[0] != int(state[1]):
            val = [choice for choice in self.branch.choices if choice[0] == int(state[1])]
            if len(val) != 0:
                self.branch.value = val[0]
            else:
                self.branch.value = self.branch.choices[-1]

            self.build.choices = self.get_list("build")

            self.build.value = self.build.choices[-1]

        elif self.build.value[0] != int(state[2]):
            val = [choice for choice in self.build.choices if choice[0] == int(state[2])]
            if len(val) != 0:
                self.build.value = val[0]
            else:
                self.build.value = self.build.choices[-1]

            self.build.choices = self.get_list("build")
        else:
            pass


class State():
    dd = None

    def __init__(self):
        self.dd = DD()


state = State()

@login.user_loader
def load_user(id):
    rs = mongo.db.users.find({"id": id})

    for row in rs:
        return User(id=row["id"], username=row["username"], password=row["password"])
