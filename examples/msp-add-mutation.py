#!/usr/bin/env python3
description = '''
Add mutations to an existing tree sequence file and write it out as a treeseq file.
'''

import sys, os
import gzip
import glob
import re
import random
import argparse
import multiprocessing

import msprime

parser = argparse.ArgumentParser(description=description)
parser.add_argument("--tree_file", "-t", type=str, nargs="*", dest="tree_file", 
                    help="name of file to load tree sequences from [default: .trees files in basedir.")
parser.add_argument("--mut_rate", "-u", type=float, nargs="*", dest="mut_rate", 
                    help="mutation rate", default=[1e-8])

parser.add_argument("--basedir", "-o", type=str, dest="basedir", 
                    help="name of directory to save output files to.")
parser.add_argument("--outfile", "-v", type=str, nargs="*", dest="outfile", 
                    help="name of trees output files [default: as trees but with .out.trees]")
parser.add_argument("--logfile", "-g", type=str, dest="logfile", 
                    help="name of log file")
parser.add_argument("--seed", "-d", dest="seed", type=int, 
                    help="random seed", default=random.randrange(1,1000))

parser.add_argument("--njobs", "-j", dest="njobs", type=int, 
        help="number of parallel jobs", default=1)

args = parser.parse_args()
argdict = vars(args)

if args.basedir is None or args.mut_rate is None:
    print(description)
    raise ValueError("Must specify at least basedir and mut_rate (run with -h for help).")

if args.tree_file is None or len(args.tree_file) == 0:
    args.tree_file = glob.glob(os.path.join(args.basedir, "*.trees"))

args.nchroms = len(args.tree_file)

if args.outfile is None or len(args.outfile) == 0:
    args.outfile = [os.path.join(args.basedir, re.sub("[.]trees$", "", os.path.basename(x))) + ".out.trees" for x in args.tree_file]

if args.logfile is None:
    args.logfile = os.path.join(args.basedir, "add_muts.log")

vector_args = ['mut_rate']
for a in vector_args:
    x = argdict[a]
    if (len(x) == 1):
        argdict[a] = x * args.nchroms
    else: 
        if (len(x) != args.nchroms):
            raise ValueError(", ".join(vector_args) + "must all be of length 1 or of length nchroms.")


assert len(args.outfile) == len(args.tree_file)

logfile = open(args.logfile, "w")
seeds = [random.randrange(1,1000) for _ in range(len(args.tree_file))]

def write_treeseq(chrom):
    treefile = args.tree_file[chrom]
    mut_rate = args.mut_rate[chrom]
    seed = seeds[chrom]
    logfile.write("Simulating mutations on" + treefile + "\n")
    ts = msprime.load(treefile)
    rng = msprime.RandomGenerator(seed)
    nodes = msprime.NodeTable()
    edges = msprime.EdgeTable()
    sites = msprime.SiteTable()
    mutations = msprime.MutationTable()
    migrations = msprime.MigrationTable()
    ts.dump_tables(nodes=nodes, edges=edges, migrations=migrations)
    mutgen = msprime.MutationGenerator(rng, mut_rate)
    mutgen.generate(nodes, edges, sites, mutations)
    logfile.write("Saving to" + args.outfile[chrom] + "\n")
    mutated_ts = msprime.load_tables(nodes=nodes, edges=edges, 
                                     sites=sites, mutations=mutations)
    mutated_ts.dump(args.outfile[chrom])

    return True

logfile.write("Beginning simulating mutations on " + str(len(args.tree_file)) + " chromosomes.\n")

p = multiprocessing.Pool(args.njobs)
p.map(write_treeseq, range(len(args.outfile)))

logfile.write("Done!\n")
logfile.close()
