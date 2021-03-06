#!/usr/bin/env python 
# -*- coding: utf-8 -*-
#
#  dwi_to_dti.py
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  In order to run this script, the following software applications 
#  required:
#  ----------------------------------------------------------------
#  (1) dtiestim
#  (2) dtiprocess

import sys
import os

arguments_names = ["DWIVolume", "config", "SubjectFolder", "Mask"]

NUM_ARGUMENTS = 1
NUM_PARAMETERS = len( arguments_names )	- 1
slash = "/"
arguments = {}

debug=False

# -----------------------------------------------
# UNC has an older version of dtiestim and 
# dtiprocess that has where the naming convention 
# of the command line parameters are slightly 
# different

is_unc = True

# ----------------------------------------------

# ----------------------------------------------
# Function definitions
# ----------------------------------------------

def checkParameters(parameters, valid_ones):
	for k in parameters.keys():
		if not (k in valid_ones):
			print "ERROR:", k, "is not a valid paramater!"
			print "For more information use --help"
			exit(-1)
		if parameters[k][0] == '-':
			print "ERROR:",parameters[k], "is not a valid parameter value for", k
			print "For more information use --help"
			exit(-1)

# ----------------------------------------------
# Display help option (--help) to user
# ----------------------------------------------

if len(sys.argv) > 1 and sys.argv[1] == "--help":
	print "   "
  	print "-------- Convert DWI Volume to DTI Volume -------------------"
  	print "   "
  	print "Sintax to run the script: dwi_to_dti.py -config 'config_file_name.txt'"
  	print "Example: dwi_to_dti.py -config config_dwi_to_dti.txt"
  	print "   "
  	print "------------------------------------------------------------"
  	print "------- These key/value pairs must be defined in the config file -------- "
  	print "   "
	print "The config file requires the following format:"
	print "DWIVolume: DWI image"
	print "SubjectFolder: folder containing subject specific files"
	print "Mask: brain mask"
	exit(0)

# ----------------------------------------------
# Basic command line parsing
# ----------------------------------------------

if debug:
	print "Num of arguments passed:",len(sys.argv) -1

if len(sys.argv)-1 != NUM_ARGUMENTS*2:
	print "ERROR: You must pass only",NUM_ARGUMENTS*2,"arguments!"
	print "For more information use --help"
	exit(-1)

i = 1
while i < len(sys.argv):
	print "!"
	if sys.argv[i].find("-") != -1:
		arguments[sys.argv[i][1:]] = sys.argv[i+1]
		i = i + 1
	i = i + 1

if debug:
	print arguments
	print "working directory:",os.getcwd()

checkParameters(arguments, arguments_names)

# ----------------------------------------------
# Parse configuration file
# ----------------------------------------------

f = open(arguments["config"])

lines = f.readlines()
if len(lines) != NUM_PARAMETERS:
	print "ERROR: the config file should only contain",NUM_PARAMETERS,"parameters"
	print "For more information use --help"
	exit(-1)
	
for i in range(0, NUM_PARAMETERS):
	if lines[i].find(":") == -1:
		print "ERROR: The line",i+1,"of the config file is wrong formatted! Format should be PARAMETER:VALUE"
		print "For more information use --help"
		exit(-1)
	tokens = lines[i].rstrip().split(":")
	
	arguments[tokens[0]] = tokens[1]

#checking paramters
checkParameters(arguments, arguments_names)

if debug:
	print arguments

# ----------------------------------------------
# Define subject folder (and associated files)
# ----------------------------------------------

subject_folder = arguments["SubjectFolder"]

if subject_folder[len(subject_folder)-1] != '/':
  subject_folder=subject_folder + "/"
  
for k in arguments.keys():
  arguments[k] = subject_folder + arguments[k]

# ----------------------------------------------
# Create some variables for dtiestim
# ----------------------------------------------

outputDTIName = arguments["DWIVolume"]
outputDTIB0Name = arguments["DWIVolume"]
outputB0Name = arguments["DWIVolume"]
  
outputDTIName = outputDTIName.split(".")[0] + "_DTI" + ".nii.gz"
outputB0Name = outputB0Name.split(".")[0] + "_b0" + ".nii.gz"
outputDTIB0Name = outputDTIB0Name.split(".")[0] + "_b0dti" + ".nii.gz"

cmd = ""

# ----------------------------------------------
# Execute dtiestim
# ----------------------------------------------

if not is_unc:
	cmd = "dtiestim -M "+arguments["Mask"]+" -m wls --correctionType nearest --inputDWIVolume "+arguments["DWIVolume"]+" --outputDTIVolume "+outputDTIName
else:
	cmd = "dtiestim -M "+arguments["Mask"]+" -m wls --correction nearest --dwi_image "+arguments["DWIVolume"]+" --tensor_output "+outputDTIName

os.system( cmd )

cmd = ""

if not is_unc:
	cmd = "dtiestim --inputDWIVolume " + arguments["DWIVolume"] + " --B0 " + outputB0Name + " --tensor_output " + outputDTIB0Name
else:
	cmd = "dtiestim --dwi_image " + arguments["DWIVolume"] + " --B0 " + outputB0Name + " --tensor_output " + outputDTIB0Name

os.system( cmd )

# ----------------------------------------------
# Create some variables for dtiprocess
# ----------------------------------------------

outputFAName = outputDTIName.replace("DTI", "FA")
outputRDName = outputDTIName.replace("DTI", "RD")
outputADName = outputDTIName.replace("DTI", "AD")

# ----------------------------------------------
# Execute dtiprocess
# ----------------------------------------------

if not is_unc:
	cmd = "dtiprocess --dti_image "+outputDTIName+" --RD_output "+outputRDName+" --fa_output "+outputFAName+" --lambda1_output " + outputADName + " --saveScalarsAsFloat"
else:
	cmd = "dtiprocess --dti_image "+outputDTIName+" --RD_output "+outputRDName+" --fa_output "+outputFAName+" --lambda1_output " + outputADName + " --scalar_float"

os.system( cmd )

# ----------------------------------------------
# Remove unnecessary files
# ----------------------------------------------

os.system( "rm " + outputDTIB0Name )
