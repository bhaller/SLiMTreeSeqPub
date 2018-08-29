import os, subprocess, msprime, statistics, pyslim
import matplotlib.pyplot as plt
import numpy as np

from timeit import default_timer as timer   # import issues with timeit.timeit() are too annoying...

# the PyCharm console doesn't seem to set up the working directory where we want it; I use this to fix that problem
# examples_dir = "/Users/bhaller/DocumentsSynced/Research/Messer lab/Publication TreeSeq/SLiMTreeSeqPub/examples/"
# os.chdir(examples_dir + "example 2 background sel stats")


# Run SLiM with tree-sequence recording: ex2_TS.slim
# Model results will be saved to ./ex2_TS.trees
start = timer()
subprocess.check_output(["../slim", "-m", "-s", "0", "./ex2_TS.slim"])
time_TS = timer() - start
print("Time for SLiM with tree-sequence recording: " + str(time_TS) + "\n")

# Load the .trees file and measure the tree height at each base position
ts = pyslim.load("./ex2_TS.trees").simplify()

start = timer()

height_for_pos = np.zeros(int(ts.sequence_length))
for tree in ts.trees():
    mean_height = statistics.mean([tree.time(root) for root in tree.roots])
    left, right = map(int, tree.interval)
    height_for_pos[left: right] = mean_height

time_analysis1 = timer() - start
print("Time for msprime tree-height analysis: ", time_analysis1, "\n")
start = timer()

height_for_pos = height_for_pos - np.min(height_for_pos)
L, L0, L1 = int(1e8), int(200e3), int(1e3)   # total length, length between genes, gene length
gene_starts = np.arange(L0, L - (L0 + L1) + 1, L0 + L1)
gene_ends = gene_starts + L1 - 1
max_distance = L0 // 4
height_for_left_distance = np.zeros(max_distance)
height_for_right_distance = np.zeros(max_distance)
for d in range(max_distance):
    height_for_left_distance[d] = np.mean(height_for_pos[gene_starts - d - 1])
    height_for_right_distance[d] = np.mean(height_for_pos[gene_ends + d + 1])
height_for_distance = np.hstack([
        height_for_left_distance[::-1], height_for_right_distance])
distances = np.hstack([np.arange(-max_distance, 0), np.arange(1, max_distance + 1)])

time_analysis2 = timer() - start
print("Time for tree-height post-processing: ", time_analysis2, "\n")

plt.plot(distances, height_for_distance)
plt.show()

# Save the final heights to a CSV
csvfile = open("./ex2_TS_heights.csv", "w")
csvfile.write("distance, height\n")
for d, h in zip(distances, height_for_distance):
    a = csvfile.write(str(d) + ", " + str(h) + "\n")

csvfile.close()
