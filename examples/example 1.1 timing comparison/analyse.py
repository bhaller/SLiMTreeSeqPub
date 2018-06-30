# analyse.py
#
# originally by Jerome Kelleher; adapted and TMRCA code added by Ben Haller

# Invoke this as "python analyse.py <file>" to get some summary statistics on a .trees file

import msprime
import sys
import numpy as np


ts = msprime.load(sys.argv[1])


print("num_samples = ", ts.num_samples)
print("num_nodes = ", ts.num_nodes)
print("num_individuals = ", ts.num_individuals)
print("num_populations = ", ts.num_populations)
print("num_edges = ", ts.num_edges)
print("num_trees = ", ts.num_trees)
print("num_sites = ", ts.num_sites)
print("num_mutations = ", ts.num_mutations)


# count average roots per site
num_roots = np.zeros(ts.num_trees)
for tree in ts.trees():
    num_roots[tree.index] = tree.num_roots

print("mean(num_roots) = ", np.mean(num_roots))


# count TMRCA weighted by interval lengths, with TMRCA at each site weighted by tree samples per root
tmrca_acc, tmrca_weight = 0, 0
min_height = float("inf")

for tree in ts.trees():
    height_acc, height_weight = 0, 0
    for root in tree.roots:
        leaves_count = tree.num_samples(root) - 1  # subtract one for the root, which is a sample
        height = tree.time(root)
        height_acc += height * leaves_count
        height_weight += leaves_count
        min_height = min(min_height, height)
    mean_height = height_acc / height_weight
    interval = tree.interval[1] - tree.interval[0]
    tmrca_acc += mean_height * interval
    tmrca_weight += interval

print("min_height = ", min_height)
print("mean(TMRCA) = ", tmrca_acc / tmrca_weight)


# SLiM .trees files record time as forwards time, which makes the raw TMRCA wrong (negative, in fact).
# The best way to correct this is to add the number of generations that the model ran to the raw TMRCA.
# However, if the generation count is not available, a very rough correction is to subtract the
# minimum tree height.  This is inaccurate and should not be used if accurate absolute TMRCA values
# are needed.

#print("rebased mean(TMRCA) = ", tmrca_acc / tmrca_weight - min_height)
