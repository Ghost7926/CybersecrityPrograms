#!/bin/python3

import sys 
from os.path import exists as file_exists

#array for port finding
APnT = [ '\n{}/'.format(x) for x in range(1,65536)]

#declaring strings
reporttxt = 'Nmap scan report for'
porttxt = 'PORT'

help_strings = ['-h', '--help']

def helpme():
	print(r"""
   _____             __  __           
  / ___/____  ____  / /_/ /____  _____
  \__ \/ __ \/ __ \/ __/ __/ _ \/ ___/
 ___/ / /_/ / /_/ / /_/ /_/  __/ /    
/____/ .___/\____/\__/\__/\___/_/     
    /_/       
    
""")
	print("Version 1.0")
	print("Created by Ryan 'Ghost' Voit")
	print("This program is built to work in tandum with the tool nmap.")
	print("It will keep your scan results organized in one continuously updated file.")
	print("If you find any bugs in this program, please contact the creator and state how I can recreate the bug.\n")
	print("Syntax:")
	print("nmap x.x.x.x | ./Spotter.py output")
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
	

	#takes piped output and sets it to input_file, gives a comment incase user executes without input and has argument
	input_file = str(sys.stdin.read())  # TYPE -h or --help FOR HELP PAGE
	
	if len(input_file) == 0:
		print("You did not give an input!!")
		print("Type './Spotter --help' for help page \n")
		print("Syntax: ")
		print("nmap x.x.x.x | ./Spotter <outfile> ")
		quit()
	#EXIT IF


	#creates var to put data of old file into
	origin = ""
	

	print(input_file)
	
	# does the file already exist, if so, take the content and set it to origin
	if file_exists(argument):

		in_file = open(argument, 'r')
		origin = in_file.read()
		in_file.close
	#EXIT IF

	#formatting
	#fin = origin + input_file
	
	f_input = ""
	editfile = input_file
		#function for printing the report lines
	def report():
		#import variables
		global reporttxt, porttxt, f_input, APnT, editfile
		
		#is there a port table in the remaining text
		is_port = editfile.find(porttxt)
		
		#is a port table in the remaining document
		if is_port != -1:
		 	#when a report comes before the port table and theres a port table in the doc
			while editfile.find(reporttxt) < editfile.find(porttxt) and is_port > -1:
				#if the nmap report string is in the remaining file, cut it out and put it into the f_input
				if reporttxt in editfile:
					remq = editfile[editfile.find(reporttxt):]
					editfile = remq
					host = remq[ 0 : remq.index('\n')]
					editfile = editfile.replace(host, '')
					host = '\n' + host + '\n'
					f_input = f_input + host
				else:
					return
		else:
			#no port table, then reformat it diffrently
			if reporttxt in editfile:
					remq = editfile[editfile.find(reporttxt):]
					editfile = remq
					host = remq[ 0 : remq.index('\n')]
					editfile = editfile.replace(host, '')
					host = '\n' + host
					f_input = f_input + host
					f_input = f_input + editfile
			else:
				return
	#function for printing the port table tab
	def column():
		global reporttxt, porttxt, f_input, APnT, editfile
		remq = editfile[editfile.find(porttxt):]
		editfile = remq
		tabs = remq[ 0 : remq.index('\n')]
		editfile = editfile.replace(tabs, "", 1)
		f_input = f_input + tabs
	
	#function to take the ports and add them into the f_input
	def ports():
		global reporttxt, porttxt, f_input, APnT, editfile
		portsec = editfile
		
		#removes the possibility that another report return could format incorrectly
		if reporttxt in portsec:
			portsec = editfile[ 0 : editfile.index(reporttxt)]
			editfile = editfile.replace(portsec, '')
	
	
		while 1:
			#goes through every port number and prints its f_input
			try:
				#finds the next port and deletes everything before
				p1 = 0
				pa = ""
				while p1 < len(APnT) and len(pa) < 2:
					pa = portsec[portsec.find(APnT[p1]):]
					p1 += 1
					
				start_new_line = pa.startswith("\n")
			
				if start_new_line == True:
					pa = pa.replace('\n', '', 1)
				
				#finds the following port and deletes it
				p2 = 0	
				pb = ""
				while p2 < len(APnT) and len(pb) < 2:
					try:
						pb = pa[ 0 : pa.index(APnT[p2])]

					except:
						p2 += 1
		
				#prints what was found, if nothing, print what remains 
				if pb != '':
					pb = '\n' + pb
					f_input = f_input + pb
				else:
					pa = '\n' + pa
					f_input = f_input + pa
				portsec = pa.replace(pb, '', 1)
				
				if pb == '':
					return					
			except:
				return
	#run the format section
	def format():
		while reporttxt in editfile:
			report()
			column()
			ports()
	fin = ''
	def combine():
		global reporttxt, porttxt, f_input, APnT, editfile, origin, fin
		outfile = ''		
		edit_I = f_input
		edit_O = origin
		#gets the nmap report line from the input
		remq = edit_I[edit_I.find(reporttxt):]
		host_I = remq[ 0 : remq.index('\n')]
		
		#checks if the input ip is in the originfile, if not, just add the input to the origin file
		if host_I in origin:
			beforeIP = edit_O[ 0 : edit_O.index(host_I)]
			outfile = outfile + beforeIP + host_I
		else:
			outfile = originfile + "\n\n" + infile
			quit()
		
		#remove the scan report txt
		remq = edit_O[edit_O.find(reporttxt):]
		edit_O = remq
		host_O = remq[ 0 : remq.index('\n')]
		edit_O = edit_O.replace(host_O, "", 1)
			
		
		#grab the port tab from input, and remove
		remq = edit_I[edit_I.find(porttxt):]
		edit_I = remq
		port_I = remq[ 0 : remq.index('\n')]
		edit_I = edit_I.replace(port_I, "", 1)
		
		
		#grab the port tab from origin, and remove
		remq = edit_O[edit_O.find(porttxt):]
		edit_O = remq
		port_O = remq[ 0 : remq.index('\n')]
		edit_O = edit_O.replace(port_O, "", 1)
		
		
		#find the bigger port tab and add it to output
		if len(port_O) > len(port_I):
			outfile = outfile + '\n' + port_O
		else:
			outfile = outfile + '\n' + port_I
		
		

		#	   PORT PRINTING		
		while 1:
			try:
				Ii = 0
				pI = ""
				while Ii < len(APnT) and len(pI) < 2:
					pI = edit_I[edit_I.find(APnT[Ii]):]
					Ii += 1
				Ii -= 1
				
				start_new_line = pI.startswith("\n")
				if start_new_line == True:
					pI = pI.replace('\n', '', 1)
		
		
				port_line_I = pI[ 0 : pI.index('\n')]
					
			
				#get the same port line from the previous 
				if APnT[Ii] in edit_O:
					#print all the ports that we skipped
					portbefore = edit_O[ 0 : edit_O.index(APnT[Ii])]
					outfile = outfile + portbefore
					
					#remove the previus ports that are not needed	
					remq = edit_O[edit_O.find(APnT[Ii]):]
					edit_O = remq
					
					#removes the new line so it can find what were looking for
					start_new_line = edit_O.startswith("\n")
					if start_new_line == True:
						edit_O = edit_O.replace('\n', '', 1)
						
					port_line_O = edit_O[ 0 : edit_O.index('\n')]
			
					if len(port_line_O) > len(port_line_I):
						outfile = outfile + port_line_O + "\n"
					else:
						outfile = outfile + '\n' + port_line_I
			
					#remove the port lines
					edit_O = edit_O.replace(port_line_O, "", 1)
					edit_I = edit_I.replace(port_line_I, "", 1)
	
					edit_O = "\n|" + edit_O
			
					#remove to the next port
					port_content_O = ""
					Oi = 0	
					while Oi < len(APnT) and len(port_content_O) < 2:
						try:
							port_content_O = edit_O[ 0 : edit_O.index(APnT[Oi])]
						except:
							Oi += 1			
					if port_content_O != '':
						outfile = outfile + port_content_O
					else:
						outfile = outfile + edit_O
					outfile = outfile + "\n-------------------------------------------------------\n"
					
					#input ports
					
					edit_I = "\n|" + edit_I
					
					port_content_I = ""
					Iic = 0	
					while Iic < len(APnT) and len(port_content_I) < 2:
						try:
							port_content_I = edit_I[ 0 : edit_I.index(APnT[Iic])]
						except:
							Iic += 1
		
					if port_content_I != '':
						outfile = outfile + port_content_I
					else:
						outfile = outfile + edit_I
					outfile = outfile + "\n-------------------------------------------------------\n"
			
					edit_O = edit_O.replace(port_content_O, "", 1)
					edit_I = edit_I.replace(port_content_I, "", 1)

				#if this is a new port, add it between the already known ports
				else:
					edit_I = "\n|" + edit_I
					
					port_content_I = ""
					Iic = 0	
					while Iic < len(APnT) and len(port_content_I) < 2:
						try:
							port_content_I = edit_I[ 0 : edit_I.index(APnT[Iic])]
						except:
							Iic += 1
		
					if port_content_I != '':
						outfile = outfile + port_content_I
					else:
						outfile = outfile + edit_I
					outfile = outfile + "\n-------------------------------------------------------\n"
					edit_I = edit_I.replace(port_content_I, "", 1)
			except:
				break
				
		#reformat repeats to clean up ending output
		outfile = outfile.replace("\n\n", "\n")
		outfile = outfile.replace("|\n", "")
		outfile = outfile.replace("-------------------------------------------------------\n-------------------------------------------------------", "-------------------------------------------------------\n")
		fin = outfile
	
	
	
	
	
	#main... pretty much
	if origin == '':
		format()
		out_file = open (argument, 'w')
		out_file.write(f_input)
		out_file.close
			
	else:
		format()
		combine()

		out_file = open (argument, 'w')
		out_file.write(fin)
		out_file.close
