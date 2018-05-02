#!/usr/bin/env python3
description = '''
Run a coalescent simulation for example 4 and save it to a .trees file
'''

import msprime
ts = msprime.simulate(sample_size=200000, Ne=200000, length=1e8, recombination_rate=1e-8, mutation_rate=0)
ts.dump("ex1_msprime.trees")
