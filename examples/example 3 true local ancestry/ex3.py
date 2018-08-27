import os, subprocess, msprime, pyslim, matplotlib.pyplot
from timeit import default_timer as timer   # import issues with timeit.timeit() are too annoying...

# the PyCharm console doesn't seem to set up the working directory where we want it; I use this to fix that problem
# examples_dir = "/Users/bhaller/DocumentsSynced/Research/Messer lab/Publication TreeSeq/SLiMTreeSeqPub/examples/"
# os.chdir(examples_dir + "example 3 true local ancestry")


# Run SLiM with tree-sequence recording: ex3_TS.slim
# Model results will be saved to ./ex3_TS.trees
start = timer()
subprocess.check_output(["../slim", "-m", "-s", "0", "./ex3_TS.slim"])
time_TS = timer() - start
print("Time for SLiM with tree-sequence recording: " + str(time_TS) + "\n")

# Load the .trees file and assess the true local ancestry at each base position
start = timer()

starts, ends, subpops = [], [], []         # chromosome intervals with an ancestry proportion
ts = pyslim.load("./ex3_TS.trees").simplify()
for tree in ts.trees(sample_counts=True):
    subpop_sum, subpop_weights = 0, 0
    for root in tree.roots:
        leaves_count = tree.num_samples(root) - 1  # subtract one for the root, which is a sample
        subpop_sum += tree.population(root) * leaves_count
        subpop_weights += leaves_count
    starts.append(tree.interval[0])
    ends.append(tree.interval[1])
    subpops.append(subpop_sum / float(subpop_weights))

time_analysis = timer() - start
print("Time for msprime tree-height analysis: " + str(time_analysis) + "\n")


# Make a simple plot (the publication plot is made in plot_ancestry.R)
x = [x for pair in zip(starts, ends) for x in pair]     # interleave starts and ends
y = [x for x in subpops for _ in (0, 1)]                # duplicate subpops
matplotlib.pyplot.plot(x, y)
matplotlib.pyplot.show()


# Save the final heights to a CSV
csvfile = open("./ex3_TS_ancestry.csv", "w")
csvfile.write("start, end, subpop\n")
for s, e, p in zip(starts, ends, subpops):
    csvfile.write(str(s) + ", " + str(e) + ", " + str(p) + "\n")

csvfile.close()
