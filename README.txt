This repository is for work on a paper about tree-sequence recording in SLiM

./outline has outline drafts
./paper has paper drafts
./examples has the examples we're using

Each example folder has a file named _PROCEDURE.txt that spells out how to execute the example yourself

The .gitignore file for this repo prevents .trees, .slimout, .csv, and .log files from being committed, so you can run the examples directly in their directories to generate all those files, without git getting confused.  You'll need your own custom build of SLiM to run the examples, which should be made with the treesequence branch of https://github.com/jgallowa07/SLiM/tree/treeSequence since this stuff has not yet made it into the MesserLab nonWF branch.

Enjoy!
