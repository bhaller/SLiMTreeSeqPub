import os, subprocess, msprime, pyslim
import numpy as np
import matplotlib.pyplot as plt

from timeit import default_timer as timer   # import issues with timeit.timeit() are too annoying...

# the PyCharm console doesn't seem to set up the working directory where we want it; I use this to fix that problem
# examples_dir = "/Users/bhaller/DocumentsSynced/Research/Messer lab/Publication TreeSeq/SLiMTreeSeqPub/examples/"
# os.chdir(examples_dir + "example 4 neutral burn-in")


# Run SLiM with tree-sequence recording: ex4_TS.slim
# Model results will be saved to ./ex4_TS_decap.trees
start = timer()
subprocess.check_output(["../slim", "-m", "-s", "2", "ex4_TS.slim"])
time_TS = timer() - start
print("Time for SLiM with tree-sequence recording: ", time_TS, "\n")


# Load the .trees file
ts = pyslim.load("ex4_TS_decap.trees")    # no simplify!


# Calculate tree heights, giving uncoalesced sites the maximum time
def tree_heights(ts):
    heights = np.zeros(ts.num_trees + 1)
    for tree in ts.trees():
        if tree.num_roots > 1:  # not fully coalesced
            heights[tree.index] = ts.slim_generation
        else:
            root_children = tree.children(tree.root)
            real_root = tree.root if len(root_children) > 1 else root_children[0]
            heights[tree.index] = tree.time(real_root)
    heights[-1] = heights[-2]  # repeat the last entry for plotting with step
    return heights


# Plot tree heights before recapitation (the publication plot is made in plot_heights.R)
breakpoints = list(ts.breakpoints())
heights = tree_heights(ts)
plt.step(breakpoints, heights, where='post')
plt.show()


# Save the heights to a CSV
csvfile = open("ex4_TS_decap_heights.csv", "w")
csvfile.write("start,heights\n")
for x in zip(breakpoints, heights):
    a = csvfile.write(",".join(map(str,x)) + "\n")

csvfile.close()


# Recapitate!
start = timer()

recap = ts.recapitate(recombination_rate=3e-10, Ne=1e5, random_seed=1)

time_analysis1 = timer() - start
print("Time for msprime recapitation: " + str(time_analysis1) + "\n")

recap.dump("ex4_TS_recap.trees")


# Plot the tree heights after recapitation
breakpoints = list(recap.breakpoints())
heights = tree_heights(recap)
plt.step(breakpoints, heights, where='post')
plt.show()


# Save the heights to a CSV
csvfile = open("ex4_TS_recap_heights.csv", "w")
csvfile.write("start,heights\n")
for x in zip(breakpoints, heights):
    a = csvfile.write(",".join(map(str,x)) + "\n")

csvfile.close()


# Overlay neutral mutations
start = timer()

mutated = msprime.mutate(recap, rate=1e-7, random_seed=1, keep=True)
mutated.dump("ex4_TS_recap_overlaid.trees")

time_overlay = timer() - start
print("Time for msprime mutation overlay: " + str(time_overlay))
