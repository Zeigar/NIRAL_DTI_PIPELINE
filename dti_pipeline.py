#!/usr/bin/env python 
# -*- coding: utf-8 -*-
#
#  niral_dti_system.py
#  
#  Copyright 2015 Andy <Andy@ANDY-PC>
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
# 


NUM_ARGUMENTS = 1
NUM_PARAMETERS = 6
FLAG_PARAMETERS = 6
slash = "/"
import sys
import os
arguments = {}
flag_arguments = {}




# this function is going to try to find a file that contains 'DWI' on its name
def findDWI(files):
  for f in files:
    if (f.find("DWI") != -1 and f.find("stripped") == -1 and f.find("RD") == -1 and f.find("FA") == -1 and f.find("DTI") == -1 and f.find("RA") == -1 and f.find("MD") == -1 ):
      return f
    
  return None

# this function is going to try to find a file that contains 'brainmask' on its name 
def findBrainMask(files):
  for f in files:
    if (f.find("brainmask") != -1):
      return f
    
  return None

# this function is going to try to find a file that contains 'RD' on its name 
def findRD(files):
  for f in files:
    if (f.find("RD") != -1):
      return f
    
  return None

# this function is going to try to find a file that contains 'FA' on its name 
def findFA(files):
  for f in files:
    if (f.find("FA") != -1):
      return f
    
  return None

# This function creates a configuration file by giving the name of the file, and its parameters
# paramaters -> a dictionary containing all the keys (parameters names) and values (locations) 
def createConfigFile(filename, parameters):
  f = open(filename, "wt")
  
  for k in parameters.keys():
    f.write(k+":"+parameters[k]+"\n")
  f.close()


# Checking if he user entered the correct parameters in order to run the script
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

# Displaying the help option to the user
if len(sys.argv) > 1 and sys.argv[1] == "--help":
	print ""
	print "------This is the main script of the pipeline------"
	print "Syntax to run this script: python niral_dti_system.py -config config_global_system.txt "
	print ""
	print "The config file requires the following format:"
	print "ATLAS:location of the ATLAS file"
	print "T1:location of the T1 file"
	print "T2:location of the T2 file"
	print "SubjectFolder:SubjectFolder_Directory"
	print "SubjectList:SubjectList file location"
	print ""
	exit(0)

		
print "Num of arguments passed:",len(sys.argv) -1


# Error message in case of using wrong numbers of parameters
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
print arguments
print "working directory:",os.getcwd()

#reading config file and parsing its new parameters
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


# This is the dictionary. These names, except for 'config', must be in the config file
arguments_names = ["T1", "config", "T2", "ATLAS", "SubjectFolder", "SubjectList","flags"]

## the next *** lines below are related to the flag file that says what scripts will run 
flag_names = ["dwi_to_dti","inv_warp_image","fdt_bedpost","extract_brain_region","create_fdt_masks","fdt_probtrackx2"]

flag_file = open(arguments["flags"])

f_lines = flag_file.readlines()
if len(f_lines) != FLAG_PARAMETERS:
  print "ERROR: the flag file must contain only ",FLAG_PARAMETERS," parameters"
  print "Type --help for more information"
  exit(-1)

for g in range(0, FLAG_PARAMETERS):
	if f_lines[g].find(":") == -1:
		print "ERROR: The line",g+1,"of the config file is wrong formatted! Format should be PARAMETER:VALUE"
		print "ACCEPTABLE VALUES: YES or NO"
		print "For more information use --help"
		exit(-1)
	tokens_2 = f_lines[g].rstrip().split(":")
	
	if tokens_2[1] != "yes" and tokens_2[1] != "no":
	  exit(-1)
	  print "Flag could not find the correct values."
		
	flag_arguments[tokens_2[0]] = tokens_2[1]
	
checkParameters(flag_arguments,flag_names)	

###



checkParameters(arguments, arguments_names)

subject_folder = arguments["SubjectFolder"]

# checking if the slash exists
if subject_folder[len(subject_folder)-1] != '/':
  subject_folder=subject_folder + "/"

f = open(arguments["SubjectList"])


# This loop runs according to the number of Subjects the user wants to process
for subject in f.readlines():
  print "Running the following subject: ", subject.rstrip()
  
  current_subject_folder = subject_folder + subject.rstrip()
  
  if current_subject_folder[len(current_subject_folder)-1] != '/':
    current_subject_folder=current_subject_folder + "/"
  current_subject_files  = os.listdir( current_subject_folder ) 
  
  output_config_folder = current_subject_folder+"config"
  os.system("mkdir "+output_config_folder)
  
  if flag_arguments["dwi_to_dti"] == "yes":
    # Calling the script that transforms the DWI in the DTI space
    createConfigFile(current_subject_folder+"config/config_dwi_to_dti.txt", {"Mask":findBrainMask(current_subject_files), 
      "DWIVolume":findDWI(current_subject_files), "SubjectFolder":current_subject_folder})
    print "Running DWI to DTI script:"
  
    if os.system("python dwi_to_dti.py -config "+current_subject_folder+"config/config_dwi_to_dti.txt") != 0:
      print "the dwi_to_dti.py script has failed!"
      exit(-1)
  elif flag_arguments["dwi_to_dti"] == "no":
     print "The dwi_to_dti script will not run. It was canceled in the flag file!!"
  
  current_subject_files  = os.listdir( current_subject_folder ) 
  
  OUT_ANTS_PREFIX = findFA( current_subject_files )
  OUT_ANTS_PREFIX = OUT_ANTS_PREFIX[ :OUT_ANTS_PREFIX.rfind("Trio")+4 ] + "_ANTS_FA_"
  
  if flag_arguments["inv_warp_image"] == "yes":
    # Applying the registration to the Subject 
    createConfigFile(current_subject_folder+"config/config_inv_warp_image.txt", {"REF":findFA(current_subject_files),
      "MOV":arguments["ATLAS"],"OUT_ANTS_PREFIX":OUT_ANTS_PREFIX,"SubjectFolder":current_subject_folder})
    print "Running Warp Image script:"
    if os.system("python inv_warp_image.py -config "+current_subject_folder+"config/config_inv_warp_image.txt") != 0:
      print "the inv_warp_image.py script has failed!"
      exit(-1)
  elif flag_arguments["inv_warp_image"] == "no":
      print "the inv_warp_image script will not run. It was canceled in the flag file!!"
  
  
  if flag_arguments["fdt_bedpost"] == "yes":
    # Running the bedpost script
    createConfigFile(current_subject_folder+"config/config_bedpost.txt", {"INPUT_VOL":findDWI(current_subject_files), 
      "INPUT_MASK":findBrainMask(current_subject_files), "SubjectFolder":current_subject_folder})
    print "Running Bedpost script:"
    if os.system("python fdt_bedpost.py -config "+current_subject_folder+"config/config_bedpost.txt") != 0:
      print "the fdt_bedpost.py script has failed!"
      exit(-1)
  elif flag_arguments["fdt_bedpost"] == "no":
    print "The fdt_bedpost script will not run. It was canceled in the flag file!"
  
  warped_atlas = arguments["ATLAS"][:arguments["ATLAS"].find(".")] + "_deform.nii.gz"
  warped_atlas = warped_atlas[warped_atlas.rfind("/"):]
  
  # loop that runs 90 times to extract all the brain regions
  for i in range(1,2):   
    
    if flag_arguments["extract_brain_region"] == "yes":
      # extracting a brain region
      print "Extracting region " + str(i)
      createConfigFile(current_subject_folder+"config/config_extract_regions.txt", {"INPUT_IMAGE":warped_atlas, 
        "EXTRACT_LABEL":str(i), "SubjectFolder":current_subject_folder})
      if os.system("python extract_brain_region.py -config "+current_subject_folder+"config/config_extract_regions.txt") != 0:
	print "the extract_brain_region.py script has failed!"
	exit(-1)
    
    
    if flag_arguments["create_fdt_masks"] == "yes":
      # creating the masks necessary to run the probtrack
      print "Running FDT Masks script on region " + str(i)
      createConfigFile(current_subject_folder+"config/config_create_fdt_masks.txt", {"SubjectFolder":current_subject_folder, 
        "FAVolume":findFA(current_subject_files), "RDVolume":findRD(current_subject_files), 
        "BrainMask":findBrainMask(current_subject_files), "region_label":str(i) })
      if os.system("python create_fdt_masks.py -config "+current_subject_folder+"config/config_create_fdt_masks.txt") != 0:
	print "the create_fdt_masks.py script has failed!"
	exit(-1)
    
	
    if flag_arguments["fdt_probtrackx2"] == "yes":
      # calling the probtrack script 
      print "Running Probtrack script on region " + str(i)
      createConfigFile(current_subject_folder+"config/config_probtrack.txt", {"OUTPUTFOLDER":str(i), 
        "SEEDFILE":"regions/"+"brain"+str(i)+".nii.gz", "WAYPOINTS":"masks/waypoint.nii.gz", 
        "TERMINATIONMASK":"masks/termination.nii.gz", "EXCLUSIONMASK":"masks/exclusion.nii.gz", 
        "SubjectFolder":current_subject_folder, "ATLAS":"registration" + warped_atlas })
      if os.system("python fdt_probtrackx2.py -config "+current_subject_folder+"config/config_probtrack.txt") != 0:
	print "the fdt_probtrackx2.py script has failed!"
	exit(-1)
    