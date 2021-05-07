import os
import subprocess
import json
import os
import datetime as dt


def ex(cmd):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    return result.stdout.decode('utf-8') #+ return result.stderr.decode('utf-8')


FPS = 15
def check_ts(ts):
    t0 = ts[0]
    for t in ts:
        if t-t0:
            fps = 1e6 / (t-t0)
            if abs(FPS - fps)/max(FPS, fps) > 0.05:
                print("found lost frames:", FPS-fps)

        t0 = t

parser_path = '/media/data/ContainerParser'
storage_path = '/media/data/0'


for folder in os.listdir(storage_path):
    ts = int(os.stat(storage_path + '/' + folder).st_mtime)
    print("\nLAST MODIFIED:", dt.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S.%f'), end='\n\n')

    for file in os.listdir(storage_path + '/' + folder):
      ts = []
      if file.endswith('.hc'):
          file_path = storage_path + '/' + folder + '/' + file
          res = ex(parser_path + ' -l ' + file_path)
          for row in res.split('\n'):
              if len(row) > 0:
                  cont_info = json.loads(row)
                  ts.append(int(cont_info['timestamp']))

          check_ts(ts)
          print(file_path + ': checked')
