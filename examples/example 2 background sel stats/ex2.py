import os, subprocess, msprime, statistics, matplotlib.pyplot
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
start = timer()

height_for_pos = []         # heights all along the chromosome
ts = msprime.load("./ex2_TS.trees")
for tree in ts.trees():
    mean_height = statistics.mean([tree.time(root) for root in tree.roots])
    height_for_pos += [mean_height] * int(tree.interval[1] - tree.interval[0])

time_analysis1 = timer() - start
print("Time for msprime tree-height analysis: " + str(time_analysis1) + "\n")


# Convert heights along the chromosome into heights at distances from a gene
start = timer()

min_height = min(height_for_pos)
height_for_pos = [x - min_height for x in height_for_pos]

L, L0, L1 = int(1e8), int(200e3), int(1e3)   # total length, length between genes, gene length
height_for_left_distance, height_for_right_distance = [], []
gene_starts = list(range(L0, L - (L0 + L1) + 1, L0 + L1))
gene_ends = [x + L1 - 1 for x in gene_starts]

for distance in range(1, L0 // 4 + 1):
    left_heights = [height_for_pos[x - distance] for x in gene_starts]
    height_for_left_distance.append(statistics.mean(left_heights))
    right_heights = [height_for_pos[x + distance] for x in gene_ends]
    height_for_right_distance.append(statistics.mean(right_heights))

height_for_distance = height_for_left_distance[::-1] + height_for_right_distance
distances = list(range(-L0//4, 0)) + list(range(1, L0//4 + 1))

time_analysis2 = timer() - start
print("Time for tree-height post-processing: " + str(time_analysis2) + "\n")


# Make a simple plot (the publication plot is made in plot_heights.R)
matplotlib.pyplot.plot(distances, height_for_distance)
matplotlib.pyplot.show()


# Save the final heights to a CSV
csvfile = open("./ex2_TS_heights.csv", "w")
csvfile.write("distance, height\n")
for d, h in zip(distances, height_for_distance):
    csvfile.write(str(d) + ", " + str(h) + "\n")
csvfile.close()



