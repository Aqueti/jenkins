import os
import subprocess
import json


def ex(cmd):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    return result.stdout.decode('utf-8') #+ return result.stderr.decode('utf-8')

def check_ts(ts):
    t0 = ts[0]
    for t in ts:
        if t0 > t:
            print('ERROR: ' + str(t0) + ' ' + str(t))
        
        t0 = t
    

parser_path = '/home/mosaic/Downloads/ContainerParser'
storage_path = '/media/datasets/0'

for folder in os.listdir(storage_path):
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
