#!/usr/bin/env python3
"""
It turns out that if one does many submissions in a row, some cases are skipped. This script checks which ones were skipped (from the loop.log file) and resubmits them.
"""

import os
import sys
import re
import numpy as np


try:
	if sys.argv[1]=="-f":
		print("Got argument -f, overwriting any previously saved jobs.")
except IndexError:
	pass

print("Updating jobs..")
os.system("./1_update_jobs.py")
print()

#Get the finished jobs and save them to folders according to job names (-J flag), and inside the folder results/ (-D results option). Overwrite previous jobs if given the -f flag.
print("Downloading..")


#THIS DOWNLOADS ALL FINISHED JOBS - NOT APPROPRIATE IF YOU HAVE OTHER BATCHES OF JOBS
if 0:

	try:
		if sys.argv[1]=="-f":
			os.system("arcget -a -s Finished -J -D results -f -t 100")

	except IndexError:
		os.system("arcget -a -s Finished -J -D results")

else:

	finished = np.genfromtxt(fname="finishedJobs.txt", delimiter="	")

	for i in range(len(finished)):
		
		jobname = "U0.1_Ec{0}_n0{1}_PT".format(finished[i][0], finished[i][1])

		print(jobname)

		try:
			if sys.argv[1]=="-f":
				os.system("arcget {0} -J -D results -f -t 100".format(jobname))

		except IndexError:
			os.system("arcget {0} -J -D results".format(jobname))



print()
print("Updating the jobs statuses again..")
os.system("./1_update_jobs.py")

print("DONE")
