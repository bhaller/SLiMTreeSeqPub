#!/usr/bin/env python3
description = '''
Run a coalescent simulation for example 1 and save it to a .trees file
'''

import msprime
ts = msprime.simulate(sample_size=1000, Ne=1000, length=1e8, recombination_rate=1e-8, mutation_rate=1e-7)
ts.dump("ex1_msprime.trees")
