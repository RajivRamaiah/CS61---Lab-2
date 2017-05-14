
# Reviewer driver for when a reviewer logs in to the system.

from __future__ import print_function	# print function
import mysql.connector					# mysql functionality
import sys
import random
import time    
import getpass
from datetime import date, datetime, timedelta

def addReviewer(con, firstname, lastname, email, affiliation, Master_Key):
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

	print("You have succesfully registered as Reviewer #" + str(newNumber) + "!")

	password1 = ""
	one = 0
	two = 0
	while (one == 0 and two == 0):
		password1 = getpass.getpass(prompt='Please enter a password to use when you log in: ')
		password2 = getpass.getpass(prompt='Verify password: ')
		if (password1 == password2):
			one = 1
			two = 1
		else:
			print("The passwords you entered do not match. Try again:")
			print()

	credentialQuery = ("INSERT INTO CREDENTIALS VALUES ('REVIEWER', " + str(newNumber)  +", AES_ENCRYPT('" + password1 + "','" + Master_Key + "'));")
	cursor.execute(credentialQuery)
	con.commit()

	print("Succes! Your password has been set. You can now log in!")

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


def registerReviewerWithOne(con, firstname, lastname, email, affiliation, RICode, Master_Key):
	addReviewer(con, firstname, lastname, email, affiliation, Master_Key)
	addRICode(con, RICode)

def registerReviewerWithTwo(con, firstname, lastname, email, affiliation, RICode1, RICode2, Master_Key):
	addReviewer(con, firstname, lastname, email, affiliation, Master_Key)
	addRICode(con, RICode1)
	addRICode(con, RICode2)

def registerReviewerWithThree(con, firstname, lastname, email, affiliation, RICode1, RICode2, RICode3, Master_Key):
	addReviewer(con, firstname, lastname, email, affiliation, Master_Key)
	addRICode(con, RICode1)
	addRICode(con, RICode2)
	addRICode(con, RICode3)



def showStatus(con, id):

	statusQuery = ("SELECT MANUSCRIPT.STATUS as Status, COUNT(*) as Count FROM MANUSCRIPT NATURAL JOIN REVIEWER_GROUP "
"WHERE MANUSCRIPT.NUMBER=REVIEWER_GROUP.MANUSCRIPT_NUMBER AND REVIEWER_GROUP.REVIEWER_NUMBER=" + id + " GROUP BY MANUSCRIPT.STATUS ORDER BY FIELD(MANUSCRIPT.STATUS, 'Received', 'Under Review', 'Rejected', 'Accepted', 'Typeset', 'Scheduled', 'Published');")
	cursor = con.cursor()
	cursor.execute(statusQuery)
	print("Below, you will find the number of manuscripts in each phase \nof review (i.e status) that are under your guidance:")
	print()
	# iterate through results
	statusRows = ""
	count = 0
	for row in cursor:
		array = ["{}".format(col) for col in row]
		statusRows += array[1] + " " + array [0] + ". "
		# statusRows += "".join(["{:<20}".format(col) for col in row]) + "\n"
		count += 1
	if (count == 0):
		print("Status: You have no manuscripts!")
	else:
		# print("".join(["{:<20}".format(col) for col in cursor.column_names]))
		# print("----------------------------")
		print(statusRows)
	print()
	print("Below, you will also find a table showing the manuscript \nnumber corresponding to the status that manuscript is in:")
	print()
	statusQuery = ("SELECT MANUSCRIPT.NUMBER as ManuscriptNumber, MANUSCRIPT.STATUS as Status FROM MANUSCRIPT NATURAL JOIN REVIEWER_GROUP "
"WHERE MANUSCRIPT.NUMBER=REVIEWER_GROUP.MANUSCRIPT_NUMBER AND REVIEWER_GROUP.REVIEWER_NUMBER=" + id + " ORDER BY FIELD(MANUSCRIPT.STATUS, 'Received', 'Under Review', 'Rejected', 'Accepted', 'Typeset', 'Scheduled', 'Published');")
	cursor.execute(statusQuery)

	statusRows = ""
	count = 0
	for row in cursor:
		statusRows += "".join(["{:<20}".format(col) for col in row]) + "\n"
		count += 1
	if (count == 0):
		print("You have no manuscripts!")
	else:
		print("".join(["{:<20}".format(col) for col in cursor.column_names]))
		print("----------------------------")
		print(statusRows)



def startReviewerShell(con, id):
	
	showStatus(con, id)

	try:
		loop = True
		cursor = con.cursor()

		while loop:
			print()
			print("------------------------------------------------------------------------------------------")
			text = raw_input('What would you like to do next?	')
			textArray = text.split('|')
			print()
			# print(textArray)
			print()

			if (textArray[0] == "status"):
				if (len(textArray) == 1):
					showStatus(con, id)


			elif (textArray[0] == "logout"):
				break

			elif (textArray[0] == "resign"):
				if (len(textArray) == 1):
					response = raw_input('Are you sure you want to resign? (yes/no):')
					if (response == "yes"):
						resignReviewer = ("UPDATE REVIEWER SET STATUS='Resigned' WHERE REVIEWER.NUMBER=" + id + ";")
						cursor.execute(resignReviewer)
						con.commit()
						print("You have succesfully resigned and have been logged out. \nThank you for your service. "
							"Please contact the system administrator \nif you want to reactivate your account. ")
						break;

				else:
					print("ERROR: Incorrect command syntax. Please make sure your command is appropriate as documented in the READ.ME. Thanks!")

			# review|reject|manuscriptnum|appropriate|clarity|methodology|contribution
			elif(textArray[0] == "review"):
				if(len(textArray) == 7):

					checkManuscriptHasNoReview = ("SELECT REVIEW.REVIEWER_NUMBER as Reviewer, REVIEW.MANUSCRIPT_NUMBER as Num "
						"FROM REVIEW WHERE REVIEW.MANUSCRIPT_NUMBER=" + textArray[2] + " AND REVIEW.REVIEWER_NUMBER=" + id +";") 
					cursor.execute(checkManuscriptHasNoReview)

					hasBeenReviewedBefore = 0
					for (Reviewer, Num, ) in cursor:
						if(str(id)==str(Reviewer)):
							if(str(textArray[2])==str(Num)):
								hasBeenReviewedBefore = 1
					if(hasBeenReviewedBefore != 0):
						print("ERROR: You have already submitted a review for this manuscript!")
						continue

					checkManuscriptIsUnderReview = ("SELECT STATUS as Status FROM MANUSCRIPT WHERE MANUSCRIPT.NUMBER=" + textArray[2] +";")
					cursor.execute(checkManuscriptIsUnderReview)

					isUnderReview = 0

					for (Status,) in cursor:
						if(Status == "Under Review"):
							isUnderReview = 1

					checkManuscriptIsReviewers = ("SELECT MANUSCRIPT_NUMBER AS Num FROM REVIEWER_GROUP WHERE REVIEWER_NUMBER=" + id + ";")
					cursor.execute(checkManuscriptIsReviewers)

					count = 0;
					for (Num,) in cursor:
						if(textArray[2] == str(Num)):
							count += 1

					# only allow reviews for manuscript that reviewer is assigned to and that is under review
					if (count == 1 and isUnderReview == 1):
						receivedTime = datetime.now().replace(microsecond=0)
						print("manuscript is reviewers")

						addReview = ("INSERT INTO REVIEW "
							"(REVIEWER_NUMBER,MANUSCRIPT_NUMBER,DATE_REVIEW_RECEIVED,APPROPRIATENESS,CLARITY,METHODOLOGY,CONTRIBUTION,RECOMMENDATION) "
							"VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
						reviewData = (id, textArray[2], receivedTime, textArray[3], textArray[4], textArray[5], textArray[6], textArray[1])
						cursor.execute(addReview, reviewData)
						con.commit() 

					else:
						print("ERROR: No Permission! \nYou cannot submit a review for a manuscript that you \nare not currently assigned to review (i.e in Under Review status)")

				else:
					print("ERROR: Incorrect command syntax. \nPlease make sure your command is appropriate as documented in the READ.ME. \nThanks!")

			else:
				print("ERROR: Incorrect command syntax. \nPlease make sure your command is appropriate as documented in the READ.ME. \nThanks!")





	except mysql.connector.Error as e:
		print("SQL Error: {0}".format(e.msg))
		print("ERROR: Incorrect command syntax. \nFor security reasons you have been logged out! \nPlease be sure to follow the READ.ME documentation!")
	except:
		print("Unexpected error: {0}".format(sys.exc_info()[0]))
		print("ERROR: Incorrect command syntax. \nFor security reasons you have been logged out! \nPlease be sure to follow the READ.ME documentation!")








