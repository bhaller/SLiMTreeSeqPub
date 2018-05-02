#!/usr/bin/env python3
description = '''
Read an existing tree sequence file and dump out the mean ancestry at each position
'''

import sys, os
import gzip
import glob
import re
import argparse
import numpy as np

import warnings
with warnings.catch_warnings():
	warnings.filterwarnings("ignore",category=FutureWarning)	# ignore h5py warning
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
	args.logfile = os.path.join(args.basedir, "tree_ancestry.txt")


logfile = open(args.logfile, "w")

def write_subpops():
	treefile = args.tree_file
	logfile.write("start, end, subpop\n")
	ts = msprime.load(treefile)
	for tree in ts.trees(sample_counts=True):
		interval = tree.interval
		subpop_sum = 0
		subpop_weights = 0
		for root in tree.roots:
			subpop = tree.population(root)
			leaves_count = tree.num_samples(root) - 1  # subtract one for the root, which is a sample
			subpop_sum += subpop * leaves_count
			subpop_weights += leaves_count
		mean_subpop = subpop_sum / float(subpop_weights)
		logfile.write(str(interval[0]) + ", " + str(interval[1]))
		logfile.write(", " + str(mean_subpop) + "\n")
	return True

write_subpops()

logfile.close()


























