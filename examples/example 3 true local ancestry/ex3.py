import os, subprocess, msprime, pyslim
import matplotlib.pyplot as plt
import numpy as np
from timeit import default_timer as timer   # import issues with timeit.timeit() are too annoying...

# the PyCharm console doesn't seem to set up the working directory where we want it; I use this to fix that problem
# examples_dir = "/Users/bhaller/DocumentsSynced/Research/Messer lab/Publication TreeSeq/SLiMTreeSeqPub/examples/"
# os.chdir(examples_dir + "example 3 true local ancestry")


# Run SLiM with tree-sequence recording: ex3_TS.slim
# Model results will be saved to ./ex3_TS.trees
start = timer()
subprocess.check_output(["../slim", "-m", "-s", "0", "./ex3_TS.slim"])
time_TS = timer() - start
print("Time for SLiM with tree-sequence recording: ", time_TS, "\n")

# Load the .trees file and assess the true local ancestry at each base position
ts = pyslim.load("./ex3_TS.trees").simplify()
start = timer()

breaks = np.zeros(ts.num_trees)
ancestry = np.zeros(ts.num_trees)
for tree in ts.trees(sample_counts=True):
    subpop_sum, subpop_weights = 0, 0
    for root in tree.roots:
        leaves_count = tree.num_samples(root) - 1  # subtract one for the root, which is a sample
        subpop_sum += tree.population(root) * leaves_count
        subpop_weights += leaves_count
    breaks[tree.index] = tree.interval[0]
    ancestry[tree.index] = subpop_sum / subpop_weights

time_analysis = timer() - start
print("Time for msprime tree-height analysis: ", time_analysis, "\n")

# Save the final heights to a CSV
with open("./ex3_TS_ancestry.csv", "w") as csvfile:
    print("break, ancestry", file=csvfile)
    for b, a in zip(breaks, ancestry):
        print(b, a, sep=",", file=csvfile)

# Make a simple plot (the publication plot is made in plot_ancestry.R)
plt.plot(breaks, ancestry)
plt.show()
