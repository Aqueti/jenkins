import csv
import json
from pymongo import MongoClient 
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('filename', help='specifies csv filename')
args = parser.parse_args()

client = MongoClient('mongodb://localhost:27017')
cases = client["qa"]["cases"]

with open(args.filename, "r") as f:
    reader = csv.DictReader(f, fieldnames = ( "req_id","case_id","parent","desc" ))
    for row in reader:
        cases.insert({"req_id": row["req_id"], "case_id": row["case_id"], "parent": row["parent"], "desc": row["desc"]})
