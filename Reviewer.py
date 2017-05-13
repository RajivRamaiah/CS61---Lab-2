
# Reviewer driver for when a reviewer logs in to the system.

from __future__ import print_function	# print function
import mysql.connector					# mysql functionality
import sys
import random
import time    
from datetime import date, datetime, timedelta

def addReviewer(con, firstname, lastname, email, affiliation):
	#INSERT INTO DATABASE
	add_reviewer = ("INSERT INTO REVIEWER "
		"(FNAME,LNAME,EMAIL,AFFILIATION,STATUS) "
		"VALUES (%s, %s, %s, %s, %s)")
	data_reviewer = (firstname, lastname, email, affiliation, 'Active')
	cursor = con.cursor()
	cursor.execute(add_reviewer, data_reviewer)
	con.commit()

	#Get reviewer ID
	getLastReviewerNumberQuery = ("SELECT REVIEWER.NUMBER AS ID FROM REVIEWER ORDER BY REVIEWER.NUMBER ASC;")
	cursor.execute(getLastReviewerNumberQuery)
	newNumber = 0
	for (number,) in cursor:
		newNumber = int(number)

	print("You have succesfully registered as Reviewer #" + str(newNumber) + "! You can now log in!")

def addRICode(con, RICode):
	cursor = con.cursor()
	#
	getLastReviewerNumberQuery = ("SELECT REVIEWER.NUMBER AS ID FROM REVIEWER ORDER BY REVIEWER.NUMBER ASC;")
	cursor.execute(getLastReviewerNumberQuery)
	newNumber = 0
	for (number,) in cursor:
		newNumber = int(number)

	add_RICode = ("INSERT INTO CODE_GROUP VALUES (%s, %s)")
	data_ri = (newNumber, RICode)
	cursor.execute(add_RICode, data_ri)
	con.commit()


def registerReviewerWithOne(con, firstname, lastname, email, affiliation, RICode):
	addReviewer(con, firstname, lastname, email, affiliation)
	addRICode(con, RICode)

def registerReviewerWithTwo(con, firstname, lastname, email, affiliation, RICode1, RICode2):
	addReviewer(con, firstname, lastname, email, affiliation)
	addRICode(con, RICode1)
	addRICode(con, RICode2)

def registerReviewerWithThree(con, firstname, lastname, email, affiliation, RICode1, RICode2, RICode3):
	addReviewer(con, firstname, lastname, email, affiliation)
	addRICode(con, RICode1)
	addRICode(con, RICode2)
	addRICode(con, RICode3)



def showStatus(con, id):

	# Reviewer_Manuscripts = []

	# findManuscriptsQuery = ("SELECT MANUSCRIPT_NUMBER AS MANUSCRIPT FROM REVIEWER_GROUP WHERE REVIEWER_NUMBER="+id+" ORDER BY MANUSCRIPT_NUMBER ASC;")
	# cursor = con.cursor()
	# cursor.execute(findManuscriptsQuery)

	# for (MANUSCRIPT,) in cursor:
	# 	newNumber = int(number)

	
	
	statusQuery = ("SELECT MANUSCRIPT.STATUS as Status, COUNT(*) as Count FROM MANUSCRIPT JOIN REVIEWER_GROUP WHERE REVIEWER_NUMBER=" + id +  " GROUP BY MANUSCRIPT.STATUS;")
	cursor2 = con.cursor()
	cursor2.execute(statusQuery)
	

	# iterate through results
	statusRows = ""
	count = 0
	for row in cursor2:
		statusRows += "".join(["{:<20}".format(col) for col in row]) + "\n"
		count += 1
	if (count == 0):
		print("You have no manuscripts!")
	else:
		print("".join(["{:<20}".format(col) for col in cursor2.column_names]))
		print("----------------------------")
		print(statusRows)



def startReviewerShell(con, id):
	
	print("START AUTHOR SHELL HERE")
	showStatus(con, id)

	try:
		loop = True
		cursor = con.cursor()

		while loop:
			print()





