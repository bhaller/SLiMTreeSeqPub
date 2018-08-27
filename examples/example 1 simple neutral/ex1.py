import os, subprocess, msprime, pyslim
from timeit import default_timer as timer   # import issues with timeit.timeit() are too annoying...

# the PyCharm console doesn't seem to set up the working directory where we want it; I use this to fix that problem
# examples_dir = "/Users/bhaller/DocumentsSynced/Research/Messer lab/Publication TreeSeq/SLiMTreeSeqPub/examples/"
# os.chdir(examples_dir + "example 1 simple neutral")


# Run SLiM without tree-sequence recording: ex1_noTS.slim
# Model results will be saved to ./ex1_noTS.slimbinary
start = timer()
subprocess.check_output(["../slim", "-m", "-s", "0", "./ex1_noTS.slim"])
time_noTS = timer() - start
print("Time for SLiM without tree-sequence recording: " + str(time_noTS) + "\n")


# Run SLiM with tree-sequence recording: ex1_TS.slim
# Model results will be saved to ./ex1_TS.trees
# Then overlay neutral mutations onto ./ex1_TS.trees with msprime and output to ./ex1_TS_overlaid.trees
start = timer()
subprocess.check_output(["../slim", "-m", "-s", "0", "./ex1_TS.slim"])
time_TS = timer() - start
print("Time for SLiM with tree-sequence recording: " + str(time_TS))

start = timer()
ts = pyslim.load("./ex1_TS.trees")
mutated = msprime.mutate(ts, rate=1e-7, random_seed=1, keep=True)
mutated.dump("./ex1_TS_overlaid.trees")
time_overlay = timer() - start
print("Time for msprime mutation overlay: " + str(time_overlay))

print("Total time for SLiM + msprime: " + str(time_TS + time_overlay) + "\n")


# Use msprime to do a plain coalescent simulation with equivalent parameters
# Model results will be saved to ./ex1_msprime.trees
start = timer()
ts = msprime.simulate(sample_size=1000, Ne=500, length=1e8, recombination_rate=1e-8, mutation_rate=1e-7)
ts.dump("./ex1_msprime.trees")
time_coalescent = timer() - start
print("Total time for coalescent: " + str(time_coalescent))




