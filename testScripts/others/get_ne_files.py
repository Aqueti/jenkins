import pymongo
import os


mc = pymongo.MongoClient('mongodb://127.0.0.1:27017')
col = mc['acos_local']['files']

for row in list(col.find({})):
  if not os.path.exists(row['filename']):
#    col.delete_many({"filename": row['filename']})
    print('no file for doc: ', row['filename'])

path = "/media/datasets/0"

for (dirpath, dirnames, filenames) in os.walk(path):
  for filename in filenames:
    f_path = dirpath + "/" + filename
    rs = list(col.find({"filename": f_path}))
    if len(rs) != 1:
      print("no doc for file: ", f_path)
