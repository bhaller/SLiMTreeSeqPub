This example shows how to add a neutral burn-in period to a non-neutral model.  Ideally it will involve running the non-neutral model in SLiM first, and then "recapitating" it in msprime by constructing a coalescent history for all of the initial individuals in the forward simulation and overlaying neutral mutations onto that constructed history.  This is presently waiting on support for recapitation to be added to msprime, which seems likely to happen for the 0.6.1 release.

The procedure below is old, from when we were thinking that the method would involve running a coalescent simulation first, and then loading that coalescent sim into SLiM as an initial state for the non-neutral model.  Recapitation should be better.

Since running tree-sequence recording runs in SLiM is pretty fast, an alternative strategy for this example could be to run the simulation in SLiM from the start with no mutations, wait for coalescence to occur, then turn on the non-neutral dynamics, finish the run, save a .trees file, and then overlay neutral mutations onto that with msprime.  This would also work fine, presumably, but would be slower than recapitation.


PROCEDURE FOR RUNNING EXAMPLE 4:

cd into the "example 4 neutral burn-in" directory

time python /Users/bhaller/DocumentsSynced/Research/Messer\ lab/SLiM\ project/Publication\ TreeSeq/examples/example\ 4\ neutral\ burn-in/msp_coalescent_ex4.py 

which takes 694m48.030s user + 3m7.133s system = 41875.16 seconds (697.9193 minutes, 11.63199 hours)

then...

TBD
