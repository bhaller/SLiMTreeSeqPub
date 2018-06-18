This example shows how to add a neutral burn-in period to a non-neutral model.  Ideally it will involve running the non-neutral model in SLiM first, and then "recapitating" it in msprime by constructing a coalescent history for all of the initial individuals in the forward simulation and overlaying neutral mutations onto that constructed history.  This is presently waiting on support for recapitation to be added to msprime, which seems likely to happen for the 0.6.1 release.

Probably the best alternative to recapitation would be to use msprime to generate neutral mutations for a coalesced population, providing the initial burn-in state, and then load that into SLiM and simulate from there.  The msp_coalescent_ex4.py script runs the coalescent for that, to see how long it would take.  It took:

     9308.32 real      9267.23 user        32.65 sys

which is 9299.88 seconds or 2.58 hours.
