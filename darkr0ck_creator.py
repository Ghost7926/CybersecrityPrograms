#!/bin/python3

file1 = "/usr/share/wordlists/rockyou.txt"
file2 = "/usr/share/wordlists/seclists/Passwords/darkc0de.txt"

with open(file1, "r", encoding="utf-8", errors="ignore") as f1, open(file2, "r", encoding="latin-1", errors="ignore") as f2:
	list1 = f1.readlines()
	list2 = f2.readlines()

combined = list1 + list2
combined = list(set(combined))

with open("darkr0ck.txt", "w", encoding="utf-8") as f:
    # Write each password to the file
    for password in combined:
        f.write(password)
