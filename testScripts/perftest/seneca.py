import os
import time
try:
    import AQT
except ImportError:
    print('no AQT lib found')
    exit(1)

def exec(cmd):
    return os.popen(cmd).readlines()[0].strip()

if exec('whoami') != 'root':
    print('app requires root privs')
    exit(1)

print("\n1. Generic Storage Benchmarking")

NUM_OF_ATTEMPTS = 2
dev_id = '/dev/sda1'

print("\ntest#1.1 - Write Performance to Data Drive")

res = {k: [] for k in ("total_time", "mbs")}

cmd = "dd if=" + dev_id + " of=test_file bs=64M count=16 2>&1 | awk '/copied/ {print $8,$10}' && sync"
for i in range(0, NUM_OF_ATTEMPTS):
    output = exec(cmd).split(" ")
    res["total_time"].append(float(output[0]))
    res["mbs"].append(float(output[1]))

print("write perf:")
print("avg total time: " + str(sum(res["total_time"]) / NUM_OF_ATTEMPTS))
print("avg mb/s: " + str(sum(res["mbs"]) / NUM_OF_ATTEMPTS))

print("\ntest#1.2 - Read Performance to Data Drive")

res = {k: [] for k in ("total_time", "mbs")}

cmd = "/sbin/sysctl -w vm.drop_caches=3"
exec(cmd)
cmd = "dd of=" + dev_id + " if=test_file bs=64M count=16 2>&1 | awk '/copied/ {print $8,$10}' && sync"

for i in range(0, NUM_OF_ATTEMPTS):
    output = exec(cmd).split(" ")
    res["total_time"].append(float(output[0]))
    res["mbs"].append(float(output[1]))

print("write perf:")
print("avg total time: " + str(sum(res["total_time"]) / NUM_OF_ATTEMPTS))
print("avg mb/s: " + str(sum(res["mbs"]) / NUM_OF_ATTEMPTS))

os.system("rm test_file")
