#!/usr/bin/env python3
description = '''
Run a coalescent simulation for example 4 and save it to a .trees file
This is the alternative method that we present a time for in the paper
'''

import msprime
ts = msprime.simulate(sample_size=100000, Ne=100000, length=1e8, recombination_rate=1e-8, mutation_rate=1e-7)
ts.dump("ex4_msprime.trees")
