import os
import sys
import argparse
import hashlib
from functools import partial


def md5sum(filename):
	with open(filename, mode='rb') as f:
		d = hashlib.md5()
		for buf in iter(partial(f.read, 128), b''):
			d.update(buf)
	return d.hexdigest()

path = os.path.dirname(os.path.abspath(__file__))

if len(sys.argv) <= 2:
	print("at least two folders are to be provided")
	exit(1)
else:
	fld_arr = sys.argv[1:]
	for fld in fld_arr:
		if not os.path.exists(os.path.join(path, fld)):
			print("folder doesn't exist: %s" % os.path.join(path, fld))
			exit(1)

for root, dirs, files in os.walk(os.path.join(path, fld_arr[0])):
	for file in files:
		for fld in fld_arr[1:]:
			orig = os.path.join(root, file)
			dest = orig.replace(os.path.join(path, fld_arr[0]), os.path.join(path, fld))

			if not os.path.exists(dest):
				print("file not found: %s" % dest)
				continue

			if md5sum(orig) != md5sum(dest):
				print("md5 mismatches: %s" % dest)
