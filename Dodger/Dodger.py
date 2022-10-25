#!/bin/python3

#This program is meant to show how someone can dodge an authentication filter on a network
#It will change the hostname of the computer to convince the network that it is a diffrent computer from before
#This program is meant to be run before macchanger because hostname alterations require the computer to be restarted to take effect
#This program is for educational purposes only and should not be used with maliciuos intent


import os
import random
import re
import time


print(r"""

  _____            _                 
 |  __ \          | |                
 | |  | | ___   __| | __ _  ___ _ __ 
 | |  | |/ _ \ / _` |/ _` |/ _ \ '__|
 | |__| | (_) | (_| | (_| |  __/ |   
 |_____/ \___/ \__,_|\__, |\___|_|   
                      __/ |          
                     |___/           

""")
print("Version 1.1")
print("Created by Ryan 'Ghost' Voit")
print("\nThis program will change the name of your computer under the /etc/hosts and the /etc/hostname file.")
print("This program is meant to be run prior to macchanger to effectivly dodge the authentication filter.")
print("After the computer has fully restarted should you run the macchanger command.")
print("This program is meant for educational purposes only!")
print("THIS PROGRAM WILL REQUIRE A RESTART AND WILL DO SO ONCE THE CHANGES HAVE BEEN MADE")


def change_me():

        #opens the /hostname file, copies it, and closes it
        hostname_file = open("/etc/hostname", "r")
        HN = hostname_file.read()
        hostname_file.close

        #prints the string
        print("Old Hostname: ")
        print(str(HN) + "\n")

        #reformating the string and alters it
        HN = HN.replace('\n','')
        rem = r'[0-9]'
        originName = re.sub(rem, '', HN)
        pin = random.randint(1111,9999)
        newHN = (originName + str(pin))
        print("New Hostname: ")
        print(newHN)

        #opens the /hostname file and replaces the content with new string created
        hostname_file = open("/etc/hostname", "w")
        hostname_file.write(newHN)
        hostname_file.close


        #opens the /hosts file, copies it, and closes it
        hosts_file = open("/etc/hosts", "r")
        hosts = hosts_file.read()
        hosts_file.close

        #replaces the old name to new name
        hosts = hosts.replace(HN, newHN)

        #opens the /hosts file and writes in the new string
        hosts_file = open("/etc/hosts", "w")
        hosts_file.write(hosts)
        hosts_file.close

        print('\n')

        #countdown to restart
        def countdown(t):
                print("Restarting in... \n")
                while t > 0:
                        print(t)
                        print('\n')
                        t -= 1
                        time.sleep(1)
                print("Good Bye!")
                time.sleep(1)

        countdown(5)

        #restarts the system for everything to take effect
        os.system("reboot")


#asks user if they would like to continue with program
choice = input("Would you like to proceed? \n")

if choice == "yes":
        pat = 1
elif choice == "YES":
        pat = 1
elif choice == "Yes":
        pat = 1
elif choice == "y":
        pat = 1
elif choice == "Y":
        pat = 1
else:
        pat = 0

if pat == 1:
        print("\n")
        change_me()
else:
        print("Goodbye")
