This example runs essentially the same simulation (N=500, L=1e8, r=1e-8, mu=1e-7, 10N generations or coalescence) in three different ways:

1. With a plain SLiM simulation
2. With tree-sequence recording in SLiM followed by neutral mutation overlay
3. With the coalescent using msprime

It times the three methods and prints timing output.  Of course 10N generations for the forward simulations is not really the same duration as the coalescent, but it is a commonly recommended practice; see the paper for discussion.

To run this example, run ex1.py in Python (Python 3.4.8 was used) from this directory:

python3 ./ex1.py

Note that the code presented for this example in our paper does not include some extraneous cruft, such as timing code, setting the current working directory, and CSV file output, for simplicity.


Sample results:

// ********** Initial memory usage: 1077248 bytes (1052K, 1.02734MB)
// ********** Peak memory usage: 465334272 bytes (454428K, 443.777MB)
Time for SLiM without tree-sequence recording: 211.8973000519909

// ********** Initial memory usage: 1077248 bytes (1052K, 1.02734MB)
// ********** Peak memory usage: 152887296 bytes (149304K, 145.805MB)
Time for SLiM with tree-sequence recording: 4.091438309988007
Time for msprime mutation overlay: 0.27546353702200577
Total time for SLiM + msprime: 4.366901847010013

Total time for coalescent: 0.3456135760061443
