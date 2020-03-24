#!/usr/bin/env python3
"""
Sends all jobs with status Failed or Vanished to the cluster.
"""

import os
import sys
import re
from arc_functions import nameToParamsVals


def editInputFile(params, vals):
	"""
	Rewrites the input file inputFile.txt so that the three parameters are set and everything else is the same. 
	This function is specific for the DMRG inputFiles!
	"""

	#DMRG SPECIFIC!!!
	Delta=0.026
	for i in range(len(params)):
		if params[i] == "Ec":
			vals[i] *= Delta


	with open("SAMPLEinputFile.txt", "r") as originalF:
		with open("inputFile.txt", "w+") as newF:
			for line in originalF:
				written=0	#if the line was already written to the new file

				for i in range(len(params)):	#iterate over all params - check if one of them matches the line, then overwrite it
					param = params[i]
					val = vals[i]

					if re.search("\s+"+param+"\s*=", line):
						newF.write("	"+param+" = {0}\n".format(val))
						written=True

				if not written:
					newF.write(line)
	return None				

#REFRESH THE job status files again
#print("Updating job statuses..")
#os.system("./1_update_jobs.py")
#print()


#READ FAILED AND VANISHED JOBS TO LIST
f = open("failedJobs.txt", "r")
failedJobs = [line.rstrip('\n') for line in f]	#strip the newline characters

f = open("vanishedJobs.txt", "r")
vanishedJobs = [line.rstrip('\n') for line in f]	#strip the newline characters


print("Cleaning failed jobs..")
for i in failedJobs:
	print(i)
	os.system("arcclean {0}".format(i))


count=0	#total count of sent jobs

#Resend failed jobs:
print("Resending failed..")
for jobname in failedJobs:

	params, vals = nameToParamsVals(jobname, nameFile="nameFile")

	editInputFile(params, vals)

	#set the name of the job
	with open("SAMPLEsendjob.xrsl", "r") as oldF:
		with open("sendjob.xrsl", "w+") as newF:

			for line in oldF:
				if re.search("jobname=", line):
					newF.write('(jobname="{0}")\n'.format(jobname))
				else:
					newF.write(line)	

	count += 1
	os.system("echo {0} {1}".format(count, jobname))
	os.system("arcsub -c maister.hpc-rivr.um.si sendjob.xrsl")

print()

print("Resending vanished..")
for jobname in vanishedJobs:

	params, vals = nameToParamsVals(jobname, nameFile="nameFile")
	
	editInputFile(params, vals)

	#set the name of the job
	with open("SAMPLEsendjob.xrsl", "r") as oldF:
		with open("sendjob.xrsl", "w+") as newF:

			for line in oldF:
				if re.search("jobname=", line):
					newF.write('(jobname="{0}")\n'.format(jobname))
				else:
					newF.write(line)	

	count += 1
	os.system("echo {0} {1}".format(count, jobname))
	os.system("arcsub -c maister.hpc-rivr.um.si sendjob.xrsl")


if count>0:
	print("Attempted to send {0} jobs.".format(count))
else:
	print("No jobs to send.")
