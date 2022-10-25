#!/bin/python3

import sys

#import the file being edited and put it into beginfile
in_file2 = open('nmapAvv3389.txt', 'r')
beginfile = in_file2.read()
in_file2.close

#array for port finding
APnT = [ '\n{}/'.format(x) for x in range(1,65536)]

#declaring strings
reporttxt = 'Nmap scan report for'
porttxt = 'PORT'
output = ""

#set the begin file to a file that will be edited throuout the program
editfile = beginfile

#function for printing the report lines
def report():
	#import variables
	global reporttxt, porttxt, editfile, is_port, output, APnT, num_n, num
	
	#is there a port table in the remaining text
	is_port = editfile.find(porttxt)
	
	#is a port table in the remaining document
	if is_port != -1:
	 	#when a report comes before the port table and theres a port table in the doc
		while editfile.find(reporttxt) < editfile.find(porttxt) and is_port > -1:
			#if the nmap report string is in the remaining file, cut it out and put it into the output
			if reporttxt in editfile:
				remq = editfile[editfile.find(reporttxt):]
				editfile = remq
				host = remq[ 0 : remq.index('\n')]
				editfile = editfile.replace(host, '')
				host = '\n' + host + '\n'
				output = output + host
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
				output = output + host
				output = output + editfile
		else:
			return
		
#function for printing the port table tab
def column():
	global reporttxt, porttxt, editfile, is_port, output, APnT, APn, num_n, num
	remq = editfile[editfile.find(porttxt):]
	editfile = remq
	tabs = remq[ 0 : remq.index("\n")]
	editfile = editfile.replace(tabs, "", 1)
	output = output + tabs


#function to take the ports and add them into the output
def ports():
	global reporttxt, porttxt, editfile, is_port, output, APnT, APn, num_n, num
	portsec = editfile
	
	#removes the possibility that another report return could format incorrectly
	if reporttxt in portsec:
		portsec = editfile[ 0 : editfile.index(reporttxt)]
		editfile = editfile.replace(portsec, '')


	while 1:
		#goes through every port number and prints its output
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
			
			#finds the following port and deletes it, if no port, print what remains 
			p2 = 0	
			pb = ""
			while p2 < len(APnT) and len(pb) < 2:
				try:
					pb = pa[ 0 : pa.index(APnT[p2])]
				except:
					p2 += 1
			
			#prints what was found
			if pb != '':
				pb = '\n' + pb
				output = output + pb
			else:
				pa = '\n' + pa
				output = output + pa
			portsec = pa.replace(pb, '', 1)
			
			if pb == '':
				return
			
			
		except:
			return



#main
while reporttxt in editfile:
	report()
	column()
	ports()

print(output)
