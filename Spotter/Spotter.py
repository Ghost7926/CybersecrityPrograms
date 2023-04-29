#!/bin/python3

import sys
import re
from os.path import exists as file_exists

#array for port finding
APnT = [ '\n{}/'.format(x) for x in range(1,65536)]

#declaring strings
reporttxt = 'Nmap scan report for'
porttxt = 'PORT'

def helpme():
	print(r"""
   _____             __  __           
  / ___/____  ____  / /_/ /____  _____
  \__ \/ __ \/ __ \/ __/ __/ _ \/ ___/
 ___/ / /_/ / /_/ / /_/ /_/  __/ /    
/____/ .___/\____/\__/\__/\___/_/     
    /_/       
    
""")
	print("Version 2")
	print("Created by Ryan 'Ghost' Voit")
	print("This program is built to combine the output files created by the tool Nmap.")
	print("It will take two Nmap output files and put them together combining the results in an easier to read format.")
	print("After combining two, it will print the results along with createing a output file.")
	print("If you find any bugs in this program, please contact the creator and state how to recreate the bug.\n")
	print("Syntax: ")
	print("./Spotter.py <file1> <file2>")
	quit()
	

#help argument
if "-h" in sys.argv or "--help" in sys.argv:
	helpme()


#Improper useage of arguments
if len(sys.argv) != 3:
	print("...impropor arguments...\n")
	print("Type './Spotter --help' for help page ")
	print("Syntax: ")
	print("./Spotter <file1> <file2> ")
	quit()

#set args to names for files in system
arg_file1 = sys.argv[1]
arg_file2 = sys.argv[2]

#declare variable to store file
file1 = ""
file2 = ""

try:
	with open(arg_file1) as f:
		file1 = f.read()
except:
	print("Error: Could not read file1")
	quit()

try:
	with open(arg_file2) as f:
		file2 = f.read()
except:
	print("Error: Could not read file2")
	quit()


# checking to see if the files have content with ports 
if porttxt not in file1:
	print("The first file does not have any Nmap content...")
	exit()

if reporttxt not in file2:
	print("The second file does not have any Nmap content...")
	exit()


fin_file = ""

#function taking the nmap scan result for hostname
def report(file):
	#import variables
	global reporttxt, porttxt, APnT

	#if there is a nmap report, removes everything before it and everything after the host name
	if reporttxt in file:
		remq = file[file.find(reporttxt):]
		file = remq
		host = remq[ 0 : remq.index('\n')]
		host = '\n' + host + '\n'
		file = host
		return(file)
	#else, there is no nmap report, give the file back
	else: 
		return(file)

#function for taking the port table top
def column(file):
	global reporttxt, porttxt, APnT
	remq = file[file.find(reporttxt):]
	remq2 = remq[remq.find(porttxt):]
	file = remq2
	tabs = remq2[ 0 : remq2.index('\n')]
	file = file.replace(tabs, "", 1)
	file = tabs
	return(file)

#function to take the ports
def ports(file):
	global reporttxt, porttxt, APnT
	portsec = file
	result = ""
	
	#removes the possibility that another report return could format incorrectly
	if reporttxt in portsec:
		portsec = file[file.find(porttxt):]
	while 1:
		#goes through every port number and prints its file
		try:
			#finds the next port and deletes everything before
			p1 = 0
			pa = ''
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
				result = result + pb
			else:
				pa = '\n' + pa
				result = result + pa
			portsec = pa.replace(pb, '', 1)
			
			if pb == '':
				return(result)					
		except:
			return(result)

file1_morethan1 = ''
file2_morethan1 = ''

for portc1 in APnT:
		num1 = file1.count(portc1)
		if num1 > 1:
			file1_morethan1 = True
			break

for portc2 in APnT:
		num2 = file2.count(portc2)
		if num2 > 1:
			file2_morethan1 = True
			break


if file1_morethan1 is True:
	file1_2 = file1
else:
	file1_2 = report(file1) + column(file1) + ports(file1)

if file2_morethan1 is True:
	file2_2 = file2
else:
	file2_2 = report(file2) + column(file2) + ports(file2)



line1_1 = file1_2.split('\n')
line1_2 = file2_2.split('\n')

if line1_1[1] != line1_2[1]:
	print(repr(line1_1[1]))
	print(repr(line1_2[1]))
	print("These reports are of two different hosts. I can not combine these.")
	exit()
else:
	fin_file = fin_file + "\n" + line1_1[1] + "\n"

#grab the port tab from input, and remove
remq = file1_2[file1_2.find(porttxt):]
file1_2 = remq

port_1 = remq[ 0 : remq.index('\n')]
file1_2 = file1_2.replace(port_1, "", 1)

#grab the port tab from origin, and remove
remq = file2_2[file2_2.find(porttxt):]
file2_2 = remq
port_2 = remq[ 0 : remq.index('\n')]
file2_2 = file2_2.replace(port_2, "", 1)


#find the bigger port tab and add it to output
if len(port_1) > len(port_2):
	fin_file = fin_file + port_1 + "\n"
else:
	fin_file = fin_file + port_2 + "\n"






'''
sudo:

find the first occurance of APnT in file 1
if no occurance
	hold till other done
find the first occurance of APnT in file 2
if no occurance
	hold till other done
compare
if they same, 
	print both to next occurance of apnt in the file
they different
	print till the next occance of APnT in the file
if they both are done
	print the remaining of the text of both
remove from the text that was printed
repeat from top

'''

file1_3 = file1_2
file2_3 = file2_2

#I = file1
#O = file2



while 1:
	try:

		#find the first instence of the array in the files
		Ii = 0
		pI = ""
		while Ii < len(APnT) and len(pI) < 2:
			pI = file1_3[file1_3.find(APnT[Ii]):]
			Ii += 1
		Ii -= 1

		Oi = 0
		pO = ""
		while Oi < len(APnT) and len(pO) < 2:
			pO = file2_3[file2_3.find(APnT[Oi]):]
			Oi += 1
		Oi -= 1
		
		#if the file1 port is earlier than file2 port
		if Ii < Oi or Oi == 65534:
		
			#remove \n if needed
			start_new_line = pI.startswith("\n")
			if start_new_line == True:
				pI = pI.replace('\n', '', 1)

			#remove everything after next \n
			port_line_I = pI[ 0 : pI.index('\n')]

			fin_file = fin_file + port_line_I + "\n"

			#remove the line from the file
			file1_3 = file1_3.replace(port_line_I, "", 1)

			#remove \n if needed
			start_new_line = file1_3.startswith("\n")
			if start_new_line == True:
				file1_3 = file1_3.replace('\n', '', 1)

			#add this cause formatting 
			file1_3 = "\n|" + file1_3

			# find the next instence of the array APnT and remove it and eveythig after
			port_content_I = ""
			Iic = 0	
			while Iic < len(APnT) and len(port_content_I) < 2:
				try:
					port_content_I = file1_3[ 0 : file1_3.index(APnT[Iic])]
				except:
					Iic += 1

			# remove the new line if needed
			start_new_line = port_content_I.startswith("\n|")
			if port_content_I == True:
				port_content_I = port_content_I.replace('\n', '', 1)

			#printing content of the ports
			if port_content_I != '':
				fin_file = fin_file + port_content_I + "\n"
			else:
				fin_file = fin_file + file1_3 + "\n--------------------------------------\n"


			file1_3 = file1_3.replace(port_content_O, "", 1)

		if Ii > Oi or Ii == 65534:

			#remove \n if needed
			start_new_line = pO.startswith("\n")
			if start_new_line == True:
				pO = pO.replace('\n', '', 1)

			#remove everything after next \n
			port_line_O = pO[ 0 : pO.index('\n')]

			fin_file = fin_file + port_line_O + "\n"

			#remove the line from the file
			file2_3 = file2_3.replace(port_line_O, "", 1)

			#remove \n if needed
			start_new_line = file2_3.startswith("\n")
			if start_new_line == True:
				file2_3 = file2_3.replace('\n', '', 1)

			#add this cause formatting 
			file2_3 = "\n|" + file2_3

			# find the next instence of the array APnT and remove it and eveythig after
			port_content_O = ""
			Oic = 0	
			while Oic < len(APnT) and len(port_content_O) < 2:
				try:
					port_content_O = file2_3[ 0 : file2_3.index(APnT[Oic])]
				except:
					Oic += 1

			# remove the new line if needed
			start_new_line = port_content_O.startswith("\n|")
			if port_content_O == True:
				port_content_O = port_content_O.replace('\n', '', 1)

			#printing content of the ports
			if port_content_O != '':
				fin_file = fin_file + port_content_O + "\n"
			else:
				fin_file = fin_file + file2_3 + "\n--------------------------------------\n"


			file2_3 = file2_3.replace(port_content_O, "", 1)

		if Ii == Oi:
			
			#remove \n if needed
			start_new_line = pI.startswith("\n")
			if start_new_line == True:
				pI = pI.replace('\n', '', 1)

			#remove everything after next \n
			port_line_I = pI[ 0 : pI.index('\n')]

			fin_file = fin_file + port_line_I + "\n"
			#remove the line from the file
			file1_3 = file1_3.replace(port_line_I, "", 1)
			#print(file1_3)

			#remove \n if needed
			start_new_line = file1_3.startswith("\n")
			if start_new_line == True:
				file1_3 = file1_3.replace('\n', '', 1)

			#add this cause formatting 
			file1_3 = "\n|" + file1_3

			# find the next instence of the array APnT and remove it and eveythig after
			port_content_I = ""
			Iic = 0	
			while Iic < len(APnT) and len(port_content_I) < 2:
				try:
					port_content_I = file1_3[ 0 : file1_3.index(APnT[Iic])]
				except:
					Iic += 1

			# remove the new line if needed
			start_new_line = port_content_I.startswith("\n|")
			if port_content_I == True:
				port_content_I = port_content_I.replace('\n', '', 1)

			#printing content of the ports
			if port_content_I != '':
				fin_file = fin_file + port_content_I + "\n"
			else:
				fin_file = fin_file + file1_3 + "\n--------------------------------------\n"


			file1_3 = file1_3.replace(port_content_I, "", 1)

			#remove \n if needed
			start_new_line = pO.startswith("\n")
			if start_new_line == True:
				pO = pO.replace('\n', '', 1)

			#remove everything after next \n
			port_line_O = pO[ 0 : pO.index('\n')]

			fin_file = fin_file + port_line_O + "\n"

			#remove the line from the file
			file2_3 = file2_3.replace(port_line_O, "", 1)

			#remove \n if needed
			start_new_line = file2_3.startswith("\n")
			if start_new_line == True:
				file2_3 = file2_3.replace('\n', '', 1)

			#add this cause formatting 
			file2_3 = "\n|" + file2_3

			# find the next instence of the array APnT and remove it and eveythig after
			port_content_O = ""
			Oic = 0	
			while Oic < len(APnT) and len(port_content_O) < 2:
				try:
					port_content_O = file2_3[ 0 : file2_3.index(APnT[Oic])]
				except:
					Oic += 1

			# remove the new line if needed
			start_new_line = port_content_O.startswith("\n|")
			if port_content_O == True:
				port_content_O = port_content_O.replace('\n', '', 1)

			#printing content of the ports
			if port_content_O != '':
				fin_file = fin_file + port_content_O + "\n"
			else:
				fin_file = fin_file + file2_3 + "\n--------------------------------------\n"


			file2_3 = file2_3.replace(port_content_O, "", 1)

	except:
			break


fin_file = fin_file.replace("\n\n", "\n")
fin_file = fin_file.replace("\n \n", "\n")
fin_file = fin_file.replace("|\n", "")
fin_file = fin_file.replace("||", "|")
fin_file = fin_file.replace("--------------------------------------\n--------------------------------------", "--------------------------------------\n")

print(fin_file)


counter = 1
while 1:
	if counter == 1:
		filename = "output.txt"
	else:
		filename = "output" + str(counter) + ".txt"
	try:
		with open(filename, "x") as f:
			f.write(fin_file)
		break
	except FileExistsError:
		counter += 1
