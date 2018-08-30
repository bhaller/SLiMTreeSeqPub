import os, subprocess, statistics, msprime, pyslim
import matplotlib.pyplot as plt

from timeit import default_timer as timer   # import issues with timeit.timeit() are too annoying...

# the PyCharm console doesn't seem to set up the working directory where we want it; I use this to fix that problem
# examples_dir = "/Users/bhaller/DocumentsSynced/Research/Messer lab/Publication TreeSeq/SLiMTreeSeqPub/examples/"
# os.chdir(examples_dir + "example 4 neutral burn-in")


# Run SLiM with tree-sequence recording: ex4_TS.slim
# Model results will be saved to ./ex4_TS_decap.trees
start = timer()
subprocess.check_output(["../slim", "-m", "-s", "22", "./ex4_TS.slim"])
time_TS = timer() - start
print("Time for SLiM with tree-sequence recording: ", time_TS, "\n")


# Load the .trees file
ts = pyslim.load("./ex4_TS_decap.trees")    # no simplify!


# Plot tree heights before recapitation (the publication plot is made in plot_heights.R)
def tree_heights(ts):
     ns = ts.num_samples
     for tree in ts.trees(sample_counts=True):
        times = [(tree.time(root) if ((tree.num_samples(root) < ns) or (len(tree.children(root)) > 1)) else tree.time(tree.children(root)[0]))
                 for root in tree.roots]
        yield sum(times)/len(times)
     yield sum(times)/len(times)   # repeat the last entry for plotting with step

breakpoints = list(ts.breakpoints())
heights = list(tree_heights(ts))
plt.step(breakpoints, heights, where='post')
plt.show()


# Save the heights to a CSV
csvfile = open("./ex4_TS_decap_heights.csv", "w")
csvfile.write("start,heights\n")
for x in zip(breakpoints, heights):
    a = csvfile.write(",".join(map(str,x)) + "\n")

csvfile.close()


# Recapitate!
start = timer()

recap = ts.recapitate(recombination_rate=2e-9, Ne=100000)

time_analysis1 = timer() - start
print("Time for msprime recapitation: " + str(time_analysis1) + "\n")

recap.dump("ex4_TS_recap.trees")


# Plot the tree heights after recapitation
breakpoints = list(recap.breakpoints())
heights = list(tree_heights(recap))
plt.step(breakpoints, heights, where='post')
plt.show()


# Save the heights to a CSV
csvfile = open("./ex4_TS_recap_heights.csv", "w")
csvfile.write("start,heights\n")
for x in zip(breakpoints, heights):
    a = csvfile.write(",".join(map(str,x)) + "\n")

csvfile.close()


# Overlay neutral mutations
start = timer()

mutated = msprime.mutate(recap, rate=1e-7, random_seed=1, keep=True)
mutated.dump("./ex4_TS_recap_overlaid.trees")

time_overlay = timer() - start
print("Time for msprime mutation overlay: " + str(time_overlay))


# Alternative method: run an msprime simulation for the coalescent burn-in
# note that sample_size is haploid, so it needs to be double Ne to produce n=Ne is diploid terms
start = timer()

ts = msprime.simulate(sample_size=200000, Ne=100000, length=1e8, recombination_rate=2e-9, mutation_rate=1e-7)
ts.dump("ex4_msprime.trees")

time_coalescent = timer() - start
print("Time for msprime coalescent: " + str(time_coalescent))

