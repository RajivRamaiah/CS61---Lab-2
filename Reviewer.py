# Reviewer.py
# Reviewer driver for when a reviewer logs in to the system.

from __future__ import print_function	# print function
import mysql.connector					# mysql functionality
import sys

def addReviewer(con, firstname, lastname):
	#INSERT INTO DATABASE
	add_reviewer = ("INSERT INTO REVIEWER "
		"(FNAME,LNAME,STATUS) "
		"VALUES (%s, %s, %s)")
	data_reviewer = (firstname, lastname, 'Active')
	cursor = con.cursor()
	print("Registering . . . ")
	cursor.execute(add_reviewer, data_reviewer)
	con.commit()

	#Get reviewer ID
	getLastReviewerNumberQuery = ("SELECT REVIEWER.ID AS ID FROM REVIEWER ORDER BY REVIEWER.ID ASC;")
	cursor.execute(getLastReviewerNumberQuery)
	newNumber = 0
	for (number,) in cursor:
		newNumber = int(number)

	print("You have succesfully registered as Reviewer #" + str(newNumber) + "! You can now log in!")

def addRICode(con, RICode):
	cursor = con.cursor()
	#
	getLastReviewerNumberQuery = ("SELECT REVIEWER.ID AS ID FROM REVIEWER ORDER BY REVIEWER.ID ASC;")
	cursor.execute(getLastReviewerNumberQuery)
	newNumber = 0
	for (number,) in cursor:
		newNumber = int(number)

	add_RICode = ("INSERT INTO RICode "
		"(REVIEWER_NUMBER,RI_CODE) "
		"VALUES (%s, %s)")
	data_ri = (newNumber, RICode)
	cursor.execute(add_RICode, data_ri)
	con.commit()


def registerReviewerWithOne(con, firstname, lastname, RICode):
	addReviewer(con, firstname, lastname)
	addRICode(con, RICode)

def registerReviewerWithTwo(con, firstname, lastname, RICode1, RICode2):
	addReviewer(con, firstname, lastname)
	addRICode(con, RICode1)
	addRICode(con, RICode2)

def registerReviewerWithTwo(con, firstname, lastname, RICode1, RICode2, RICode3):
	addReviewer(con, firstname, lastname)
	addRICode(con, RICode1)
	addRICode(con, RICode2)
	addRICode(con, RICode3)




def startReviewerShell():
	print("START AUTHOR SHELL HERE")
