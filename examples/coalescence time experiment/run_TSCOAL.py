# Test how long it takes to achieve coalescence in a neutral model
# The model uses N=500, so 10N == 5000.  How does that compare?

import os, subprocess, re, statistics
from timeit import default_timer as timer   # import issues with timeit.timeit() are too annoying...

examples_dir = "/Users/bhaller/DocumentsSynced/Research/Messer lab/Publication TreeSeq/SLiMTreeSeqPub/examples/"
os.chdir(examples_dir + "coalescence time experiment")

def run_TSCOAL(Lstr, seed):
    bytes = subprocess.check_output(["../slim", "-s", str(seed), "-d", "Lstr='" + Lstr + "'", "./TSCOAL.slim"])
    output = bytes.decode("utf-8")
    lines = output.splitlines()
    for line in lines:
        if re.search("(.*): coalescence achieved.", line):
            return int(line.split(':')[0])
    return None

# do runs for 1..1e9 in bulk
for L in ["1", "10", "1e2", "1e3", "1e4", "1e5", "1e6", "1e7", "1e8", "1e9"]:
    start = timer()
    ret = [run_TSCOAL(L, x) for x in range(0,500)]
    print(L + ": mean == " + "{0:.2f}".format(statistics.mean(ret)), end='')
    print(", sd = " + "{0:.2f}".format(statistics.stdev(ret)), end='')
    print(", sem = " + "{0:.2f}".format(statistics.stdev(ret) / (len(ret) ** 0.5)), end='')
    print(", data == " + str(ret))
    print("elapsed time: " + "{0:.2f}".format(timer() - start) + "\n")

# do 1e10 runs one by one, since they take so long
# most of these were done on the CBSU cluster, in the end; too slow
for rep in range(0,500):
    start = timer()
    ret = run_TSCOAL("1e10", rep)
    print("1e10 rep " + str(rep) + ": " + str(int(ret)) + " (elapsed time: " + "{0:.2f}".format(timer() - start) + ")")












