This example runs essentially the same simulation (N=500, L=1e8, r=1e-8, mu=1e-7, 10N generations or coalescence) in three different ways:

1. With a plain SLiM simulation
2. With tree-sequence recording in SLiM followed by neutral mutation overlay
3. With the coalescent using msprime

It times the three methods and prints timing output.  Of course 10N generations for the forward simulations is not really the same duration as the coalescent, but it is a commonly recommended practice; see the paper for discussion.

To run this example, run ex1.py in Python (Python 3.4.8 was used).

Note that the code presented for this example in our paper does not include the timing code or the current working directory cruft, for simplicity.


Sample results:

// ********** Initial memory usage: 1060864 bytes (1036K, 1.01172MB)
// ********** Peak memory usage: 501035008 bytes (489292K, 477.824MB)
Time for SLiM without tree-sequence recording: 216.86819804800325

// ********** Initial memory usage: 1060864 bytes (1036K, 1.01172MB)
// ********** Peak memory usage: 141217792 bytes (137908K, 134.676MB)
Time for SLiM with tree-sequence recording: 3.8857379039982334
Time for msprime mutation overlay: 0.18694955899263732
Total time for SLiM + msprime: 4.072687462990871

Total time for coalescent: 0.302550803986378
