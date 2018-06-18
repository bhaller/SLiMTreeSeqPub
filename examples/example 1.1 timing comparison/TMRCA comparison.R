# TMRCA comparison.R
#
# Ben Haller, 15 June 2018

# This script compares TMRCAs from the L=1e10 runs of our timing comparison to confirm
# that they are the same - that we are comparing apples to apples.  The TMRCAs come
# from running analyse.py on the .trees files output from SLiM and msprime.
# The SLiM TMRCAs have to be rebased by adding 15771, the number of generations the
# SLiM model was run for, because of the way SLiM's forward-time generations are
# recorded in the .trees file.


slim_unrebased <- c(-13779.847765102559, -13772.957739315696, -13776.92762451925, -13769.7897183143, -13768.3931979361, -13777.619290410585, -13775.3025825424, -13780.941982702583, -13777.442651574835, -13775.88890287146)
slim_rebased <- slim_unrebased + 15771

mean(slim_rebased)
sd(slim_rebased)
sd(slim_rebased) / sqrt(length(slim_rebased))		# SEM


msp_unrebased <- c(1990.2242691890829, 1994.9277414420274, 1984.4689777723356, 1999.6955757452238, 1998.2303477781309, 1997.2168255043512, 1994.3178513597218, 1998.3673739638489, 2009.2614072988758, 1995.0473111192055)

mean(msp_unrebased)
sd(msp_unrebased)
sd(msp_unrebased) / sqrt(length(msp_unrebased))		# SEM


t.test(slim_rebased, msp_unrebased)

# For our runs, the t-test gives a p-value of 0.7791, indicating that the mean TMRCAs
# are not significantly different.  We appear to be comparing apples to apples.
