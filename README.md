# ngrams
Finds top n-grams of specified length from files, and prints or graphs them.

# Credits
ngrams.py is written fully by me, and the util.py and example input files were provided by the RIT Computer Science department.

# Requirements
For frequency to work properly, files must be named bs[YYMMDD].txt with [YYMMDD] replaced with the date. Interprets all years as 20XX.

# Usage
ngrams.py [-h] [-d DIR] [--mostCommon MOSTCOMMON] [--frequency FREQUENCY [FREQUENCY ...]] [-w] [-p] [-n N]
* -h: Prints usage and help message
* -d DIR: Directory to read files from
* --mostCommon MOSTCOMMON: Finds the X most common N-Grams
* --frequency FREQUENCY: Finds the frequency of the passed N-gram for each date
* -w: Enables write mode, prints results to command line
* -p: Enables plot mode, plots results using matplotlib
* -n: Size of n-grams to read
-d can be replaced with --dir, -w can be replaced with --write, and -p can be replaced with --plot
