import os, subprocess, statistics, msprime, pyslim, matplotlib.pyplot
from timeit import default_timer as timer   # import issues with timeit.timeit() are too annoying...
import matplotlib.pyplot as plt
import numpy as np

# the PyCharm console doesn't seem to set up the working directory where we want it; I use this to fix that problem
# examples_dir = "/Users/bhaller/DocumentsSynced/Research/Messer lab/Publication TreeSeq/SLiMTreeSeqPub/examples/"
# os.chdir(examples_dir + "example 4 neutral burn-in")


# Run SLiM with tree-sequence recording: ex4_TS.slim
# Model results will be saved to ./ex4_TS_decap.trees
start = timer()
subprocess.check_output(["../slim", "-m", "-s", "22", "./ex4_TS.slim"])
time_TS = timer() - start
print("Time for SLiM with tree-sequence recording: ", time_TS, "\n")

ts = pyslim.load("./ex4_TS_decap.trees")    # no simplify!


def tree_heights(ts):
    ns = ts.num_samples
    heights = np.zeros(ts.num_trees + 1)
    for tree in ts.trees():
        real_roots = [
            tree.children(root)[0] if len(tree.children(root)) == 1 else root
            for root in tree.roots]
        heights[tree.index] = statistics.mean(tree.time(root) for root in real_roots)
    # repeat the last entry for plotting with step
    heights[ts.num_trees] = heights[ts.num_trees - 1]
    return heights

# Plot tree heights before recapitation (the publication plot is made in plot_heights.R)
breakpoints = list(ts.breakpoints())
heights = tree_heights(ts)
plt.step(breakpoints, heights, where='post')
plt.show()

csvfile = open("./ex4_TS_decap_heights.csv", "w")
csvfile.write("start,heights\n")
for x in zip(breakpoints, heights):
    a = csvfile.write(",".join(map(str,x)) + "\n")

csvfile.close()


# recapitate!
start = timer()

recap = ts.recapitate(recombination_rate=2e-9, Ne=100000)
recap.dump("ex4_TS_recap.trees")

time_analysis1 = timer() - start
print("Time for msprime recapitation: " + str(time_analysis1) + "\n")


# plot the tree heights after recapitation
breakpoints = list(recap.breakpoints())
heights = tree_heights(recap)
plt.step(breakpoints, heights, where='post')
plt.show()

csvfile = open("./ex4_TS_recap_heights.csv", "w")
csvfile.write("start,heights\n")
for x in zip(breakpoints, heights):
    a = csvfile.write(",".join(map(str,x)) + "\n")

csvfile.close()


# overlay neutral mutations
start = timer()

mutated = msprime.mutate(recap, rate=1e-7, random_seed=1, keep=True)
mutated.dump("./ex4_TS_recap_overlaid.trees")

time_overlay = timer() - start
print("Time for msprime mutation overlay: " + str(time_overlay))


# alternative method: run an msprime simulation for the coalescent burn-in
# note that sample_size is haploid, so it needs to be double Ne to produce n=Ne is diploid terms
start = timer()

ts = msprime.simulate(sample_size=200000, Ne=100000, length=1e8, recombination_rate=2e-9, mutation_rate=1e-7)
ts.dump("ex4_msprime.trees")

time_coalescent = timer() - start
print("Time for msprime coalescent: " + str(time_coalescent))

