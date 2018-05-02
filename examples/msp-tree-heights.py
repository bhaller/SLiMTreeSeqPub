#!/usr/bin/env python3
description = '''
Read an existing tree sequence file and dump out the heights of its trees
'''

import sys, os
import gzip
import glob
import re
import argparse
import numpy as np

import msprime

parser = argparse.ArgumentParser(description=description)
parser.add_argument("--tree_file", "-t", type=str, dest="tree_file", 
					help="name of file to load tree sequences from")
parser.add_argument("--basedir", "-o", type=str, dest="basedir", 
					help="name of directory to save output files to")
parser.add_argument("--logfile", "-g", type=str, dest="logfile", 
					help="name of log file")

args = parser.parse_args()
argdict = vars(args)

if args.basedir is None or args.tree_file is None:
	print(description)
	raise ValueError("Must specify at least basedir and tree_file (run with -h for help).")

if args.logfile is None:
	args.logfile = os.path.join(args.basedir, "tree_heights.txt")


logfile = open(args.logfile, "w")

def write_heights():
	treefile = args.tree_file
	logfile.write("start, end, height\n")
	ts = msprime.load(treefile)
	for tree in ts.trees():
		interval = tree.interval
		mean_height = np.mean([tree.time(root) for root in tree.roots])	# all same height, in fact, I think?
		logfile.write(str(interval[0]) + ", " + str(interval[1]))
		logfile.write(", " + str(mean_height) + "\n")
	return True

write_heights()

logfile.close()

























