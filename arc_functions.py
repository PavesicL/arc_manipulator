#!/usr/bin/env python3

"""
Functions used within the arc_manipulator scripts.
"""

import os
import sys
import re

def readNameFile(file, regex=False):
	"""
	Reads the nameFile and returns a jobname and a list of parameters and their types.
	If regex = true, instead of a python formatted string, return the name as a regex expression string.  
	INPUT:
	file - relative path to the file with the information about jobname and parameters.
	regex - wheter to return the name as a regex expression string
	OUTPUT:
	name/regexname - a jobname, a python formatted string or a regex type string
	paramsList - a list of all parameters and their types, paramsList[i] = [param, paramtype]
	"""

	paramsCheck = False
	paramsList = []

	with open(file, "r") as f:

		for line in f:

			a = re.search("name\s*=\s*(.*)", line)	
		
			b = re.search("params\s*{", line) 
			c = re.search("}\s*endparams", line) 
			
			d = re.search("\s*(\w*)\s*(\w*)", line)
			
			if line[0] == "#":	#this line is a comment
				pass
			if a:	#this line has the name, save it
				name = a.group(1)
			if b:	#we are in the part of the file with the params info
				paramsCheck=True
				continue
			if c:	#we are past the part of the file with the params info
				paramsCheck=False

			if paramsCheck and d:	#parse parameters
				param, paramtype = d.group(1), d.group(2)
				paramsList.append([param, paramtype])

	if regex:
		regexname = re.sub("{[0-9]+}", "(-*[0-9]+\.*[0-9]*)", name)	#replace all instances of {number} in the name with ([0-9]+.*[0-9]*), which matches floats and ints
		return regexname, paramsList
	
	else:
		return name, paramsList

def nameToParamsVals(jobname, nameFile="nameFile"):
	"""
	Given a job name, return a list of parameters and a list of their values.
	INPUT:
	jobname - the name of the job
	nameFile - relative path to the file with the information about jobname and parameters.
	OUTPUT:
	params - a list of parameters
	vals - a list of their values, in the same order
	"""

	regexname, paramsList = readNameFile(nameFile, regex=True)
	
	params, vals = [], []
	
	a = re.search(regexname, jobname)	#match the regexname with the jobname
	for i in range(len(paramsList)):

		param = paramsList[i][0]
		val = float(a.group(i+1))

		params.append(param)
		vals.append(val)		

	return params, vals