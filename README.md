# ngrams
Finds top n-grams of specified length from all files in directory, and prints or graphs them.

# Credits
ngrams.py is written fully by me, and the util.py and example input files were provided by the RIT Computer Science department.

# Requirements
For frequency to work properly, files must be named bs[YYMMDD].txt with [YYMMDD] replaced with the date. Interprets all years as 20XX.

# Usage
./ngrams [-h] [-d DIR] [--mostCommon MOSTCOMMON] [--frequency FREQUENCY [FREQUENCY ...]] [-w] [-p] [-n N]
* -h: Prints usage and help message
* -d DIR: Directory to read files from, can be replaced with --dir
* --mostCommon MOSTCOMMON: Finds the X most common N-Grams
* --frequency FREQUENCY: Finds the frequency of the passed N-gram for each date
* -w: Enables write mode, prints results to command line, can be replaced with --write
* -p: Enables plot mode, plots results using matplotlib, can be replaced with --plot
* -n: Size of n-grams to read
