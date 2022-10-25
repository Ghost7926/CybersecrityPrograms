#!/bin/python3

#
#	THIS PROJECT IS INCOMPLETE
#

import sys 
from os.path import exists as file_exists

help_strings = ['-h', '--help']

def helpme():
	print("Hello and welcome to Spotter!")
	print("this is built to work with the default nmap output format")
	quit()

#gets the arg length
args = len(sys.argv)

#checking if theres a name argument
if args == 1:
	print("You did not give a name for the output file!!")
	print("Type './Spotter --help' for help page \n")
	print("Syntax: ")
	print("nmap x.x.x.x | ./Spotter <outfile> ")
	quit()
#is there too many arguments
elif args >= 3:
	print("You gave too many arguments!!")
	print("Type './Spotter --help' for help page \n")
	print("Syntax: ")
	print("nmap x.x.x.x | ./Spotter <outfile> ")
	quit()

#if there is an argument, begin the process
else:
	#using the argument as output file name
	argument = str(sys.argv[1])
	
	#is it a help page string
	if argument in help_strings:
		helpme()
		
	#checking if file starts with "-"
	if argument.startswith('-'):
		print("We do no recognise that switch!!")
		print("Type './Spotter --help' for help page \n")
		print("Syntax: ")
		print("nmap x.x.x.x | ./Spotter <outfile> ")
		quit()
	#EXIT IF
	

	#takes piped output and sets it to COP, gives a comment incase user executes without input and has argument
	COP = str(sys.stdin.read())  # TYPE -h or --help FOR HELP PAGE
	
	if len(COP) == 0:
		print("You did not give an input!!")
		print("Type './Spotter --help' for help page \n")
		print("Syntax: ")
		print("nmap x.x.x.x | ./Spotter <outfile> ")
		quit()
	#EXIT IF


	#creates var to put data of old file into
	origin = ""
	

	print(COP)
	
	# does the file already exist, if so, take the content and set it to origin
	if file_exists(argument):

		in_file = open(argument, 'r')
		origin = in_file.read()
		in_file.close
	#EXIT IF

	#formatting
	fin = origin + COP


	#setting foratted output to file
	out_file = open (argument, 'w')
	out_file.write(fin)
	out_file.close
