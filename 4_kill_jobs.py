#!/usr/bin/env python3
"""
Kill jobs with a certain status."""

import os
import sys
import re
import numpy as np
import datetime

if len(sys.argv) != 2:
	print("Usage: " + sys.argv[0] + " status")
	print("Status can be: queueing, running, all.")
	exit()


#REFRESH THE job status files again
print("Updating job statuses..")
os.system("./1_update_jobs.py")
print()

killRunning, killQueueing = False, False
if sys.argv[1] == "queueing" or sys.argv[1] == "all":
	killQueueing = True
 
if sys.argv[1] == "running" or sys.argv[1] == "all":
	killRunning = True

countR, countQ = 0, 0

if killRunning:

	runningJobs = np.genfromtxt(fname="runningJobs.txt", delimiter="	")

	for i in range(len(runningJobs)):

		Ec, n0 = runningJobs[i][0], runningJobs[i][1]
		jobname = "U0.1_Ec{0}_n0{1}_PT\n".format(Ec, n0)

		print(jobname)
		os.system("arckill {0}".format(jobname))

		countR+=1

if killQueueing:

	queueingJobs = np.genfromtxt(fname="queueingJobs.txt", delimiter="	")

	for i in range(len(queueingJobs)):

		Ec, n0 = queueingJobs[i][0], queueingJobs[i][1]
		jobname = "U0.1_Ec{0}_n0{1}_PT\n".format(Ec, n0)

		print(jobname)
		os.system("arckill {0}".format(jobname))


		countQ+=1

print("Attempted to kill {0} jobs; {1} running and {2} queueing.".format(countQ+countR, countR, countQ))
