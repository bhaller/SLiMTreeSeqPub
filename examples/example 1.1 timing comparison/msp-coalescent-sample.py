#!/usr/bin/env python3
description = '''
Run a coalescent simulation for example 1 and save it to a .trees file
'''

import argparse
import msprime

parser = argparse.ArgumentParser(description=description)
parser.add_argument("--length", "-L", type=str, dest="Lstr", 
                    help="chromosome length", default="1e8")
parser.add_argument("--rep", "-r", type=int, dest="rep", 
                    help="replicate", default=0)
args = parser.parse_args()

# note that sample_size is haploid, Ne is diploid
ts = msprime.simulate(sample_size=10, Ne=500, length=float(args.Lstr), recombination_rate=1e-8, mutation_rate=1e-7)
ts.dump("output/msp_L=" + args.Lstr + "_" + str(args.rep) + "_XS.trees")
