To use this script:

First install “sewpy”, a python wrapper of SExtractor. You can find instructions at http://sewpy.readthedocs.io/en/latest/installation.html

Create a text file where each line contains the filename of a .fits image you would like to calculate the shift of with respect to a reference image. The first filename in the list will be the reference image which all other images will be compared against.

Copy the “gauss_4.0_7x7.conv” and “default.nnw” files included into the directory where your images are located. You will run the program from this directory. 

To run, use the text file containing your list of images as a command line argument.

Example run:

User$ source activate iraf27
(iraf27) User$ cd (directory where images are located)
(iraf27) User$ ipython
In [1] run ./calc_shifts.py imglist.txt

Depending on the noise in your image you may need to tweak the DETECT_THRESH and DETECT_MINAREA that sewpy uses.  We have current set a pretty conservative threshold to only get the brightest objects.

The script will extract coordinates of sources from each image using sewpy, do quality cuts to yield a few reliable sources, and use these coordinates to calculate shifts of each image against the first image provided, using xyxymatch. 

The script will make two new directories in the directory you run it from, one titled “work” and the other titled “shifts”. ‘work’ contains files used in intermediate steps to calculate shifts such as Sextractor tables for each file (_sexout.txt), tables with quality cuts (_extracted.txt), and iraf output(_match.txt). The ‘shifts’ directory is where the results are stored and will contain one file after running one time. This (shifts.txt) file will contain each .fits file name with its shift in the x and y direction with respect to the first file in the list. These values can be added to the corresponding image so that each source will appear in the same location in every image. 




