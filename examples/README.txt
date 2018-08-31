This directory contains subdirectories for the examples shown in this publication.  To run the examples, you should:

1. Obtain a binary of SLiM, either by installing it or building it from sources (see the SLiM manual)

2. Place a link to the SLiM binary (named "slim") in this directory; this local copy will be used by all examples; on linux or OSX you can do this by running, in this directory:
```
ln -s $(which slim) .
```

3. cd into a particular example directory

4. Follow the instructions in the README.txt file in that subdirectory

You will also need Python installed (version 3.4.8 or later is recommended), and you will need various Python packages installed such as pyslim, msprime, numpy, and matplotlib.  To produce the publication plots, you will need R installed (probably any version from 3.0 onward will be fine).


