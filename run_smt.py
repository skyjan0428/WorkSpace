import os

def run_smt_file(path, size):
	for i in range(1, size+1):
		print("running ./%s/%d.smt" % (path, i))
		os.system("cvc4 --lang=smt --strings-exp ./%s/%d.smt" % (path, i))



run_smt_file('distutils_get_build_version', 21)