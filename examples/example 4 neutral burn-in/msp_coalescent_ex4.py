#!/usr/bin/env python3
description = '''
Run a coalescent simulation for example 4 and save it to a .trees file
This is the alternative method that we present a time for in the paper
'''

import msprime

# note that sample_size is haploid, so it needs to be double Ne to produce n=Ne is diploid terms
ts = msprime.simulate(sample_size=200000, Ne=100000, length=1e8, recombination_rate=1e-8, mutation_rate=1e-7)
ts.dump("ex4_msprime.trees")
