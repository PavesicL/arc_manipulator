#!/usr/bin/env python3
"""
Reads the arcstat output and parses the jobs. Saves the data to .txt files by categories.
"""

import os
import sys
import re
from arc_functions import readNameFile

#get a regex general form of the name
regexName, _ = readNameFile("nameFile", regex=True)

#READ THE FILE WITH ALL REQUESTED JOBS TO A LIST
f = open("jobsToSend.txt", "r")
jobsToSend = [line.rstrip('\n') for line in f]	#strip the newline characters


#SAVE THE INFORMATION ABOUT THE JOBS FROM THE QUEUE TO statJobs.txt
print("Getting job info..")
os.system("arcstat -a  > statJobs.txt")

#GET A JOB LIST FROM THE CLUSTER WITH CURRENT JOB STATUS
#allJobs is a list; allJobs[i]=[jobname, status]. allJobsToCompare is a list of just job names, and is as such directly comparable element by element to jobsToSend.
allJobs, allJobsToCompare = [], []
with open("statJobs.txt", "r") as jobsF:

	here=0
	for line in jobsF:

		if here==0:		
			a = re.search("("+regexName+")", line)
			if a:
				here=1
				name = a.group(1)

				allJobs.append([name])
				allJobsToCompare.append(name)

		if here==1:
			a = re.search("State: (.*)", line)
			if a:
				state = a.group(1)
				here = 0
				allJobs[-1].append(state)

#CHECK results/ FOLDER FOR ALL SAVED JOBS, APPEND THESE TO allJobs TOO
allSavedJobs = sorted(os.listdir("results/"))
for folder in allSavedJobs:

	a = re.search("("+regexName+")", folder)
	if a:
		name = a.group(1)

		allJobs.append([name, "Saved"])
		allJobsToCompare.append(name)


#CHECK IF THERE ARE JOBS THAT WERE SENT BUT WERE NEITHER OBTAINED BY arcstat NOR FOUND IN THE results/ FOLDER
for i in range(len(jobsToSend)):
	if not jobsToSend[i] in allJobsToCompare:
		allJobs.append([jobsToSend[i]] + ["Vanished"])


#all jobs states available here: http://manpages.ubuntu.com/manpages/bionic/man1/arcstat.1.html
finishedJobs, runningJobs, queueingJobs, failedJobs, savedJobs, vanishedJobs = [], [], [], [], [], []
for i in range(len(allJobs)):

	if allJobs[i][-1] == "Finished":
		finishedJobs.append(allJobs[i][0])

	elif allJobs[i][-1] == "Saved":
		savedJobs.append(allJobs[i][0])

	elif allJobs[i][-1] == "Running":
		runningJobs.append(allJobs[i][0])

	elif allJobs[i][-1] == "Preparing" or allJobs[i][-1] == "Submitting" or allJobs[i][-1] == "Queuing": 
		queueingJobs.append(allJobs[i][0])

	elif allJobs[i][-1] == "Failed" or allJobs[i][-1] == "Killed":#or allJobs[i][-1] == "Deleted":
		failedJobs.append(allJobs[i][0])
	
	elif allJobs[i][-1] == "Vanished":
		vanishedJobs.append(allJobs[i][0])
		

#FOR EACH JOB STATE, SAVE THE CORRESPONDING LIST TO A FILE		
allTypes = ["finished", "saved", "running", "queing", "failed", "vanished"]
listed = [finishedJobs, savedJobs, runningJobs, queueingJobs, failedJobs, vanishedJobs]

for i in range(len(allTypes)):
	file = allTypes[i] + "Jobs.txt"
	with open(file, "w") as ff:
		ff.writelines([i+"\n" for i in listed[i] ])

print("Updated lists.")
print("There is: {0} running, {1} queueing, {2} finished, {3} failed, {4} vanished and {5} saved jobs; for a total of {6} jobs."
	.format(len(runningJobs), len(queueingJobs), len(finishedJobs), len(failedJobs), len(vanishedJobs), len(savedJobs), 
		len(vanishedJobs)+len(savedJobs)+len(runningJobs)+len(queueingJobs)+len(finishedJobs)+len(failedJobs)))