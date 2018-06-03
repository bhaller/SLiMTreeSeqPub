This example has the code needed to run the timing comparison between SLiM without tree-sequence recording, SLiM with tree-sequence recording and mutation overlay, and the coalescent as provided by msprime.  The coalescent is run for both the full population and an n=N/100 sample.

This is basically an extended version of example 1; as with example 1, N=500, r=1e-8, mu=1e-7, and the model is run for 10N generations or until coalescence.  However, here L is varied from 10^ to 10^10, and 10 replicates of each model are run with different seeds.

To run this example, run run_times.R in R (R 3.5.0 used).

Output files for each run will be created in ./output/, and will be used to short-circuit future runs of the same model (the timing information for the run is saved as the last line of the file).  Empty out the ./output folder of all files if you want to run the tests from scratch, or delete specific files to re-run only specific runs.  The .trees files for these sample runs are not provided, as they are quite large in some cases (the whole thing is 29 GB on my machine).


Sample results are provided in this repository:

- in the ./output/ directory
- in comparison.CSV: a CSV file of mean times with standard errors
- in comparison.pdf: a PDF of the final plot generated
