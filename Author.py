# Author.py
# Author driver for when an author logs in to the system.

from __future__ import print_function	# print function
import mysql.connector					# mysql functionality
import sys			
import random
import time    
import getpass
from datetime import date, datetime, timedelta
import getpass

def registerAuthor(con, firstname, lastname, address, email, affiliation, MASTER_KEY):
	add_author = ("INSERT INTO AUTHOR "
		"(FNAME,LNAME,MAILING_ADDRESS,E_MAIL,AFFILIATION) "
		"VALUES (%s, %s, %s, %s, %s)")
	data_author = (firstname, lastname, address, email,  affiliation)
	# Insert new employee
	cursor = con.cursor()
	cursor.execute(add_author, data_author)
	con.commit()

	getLastAuthorNumberQuery = ("SELECT AUTHOR.ID AS ID FROM AUTHOR ORDER BY AUTHOR.ID ASC;")
	cursor.execute(getLastAuthorNumberQuery)
	newNumber = 0
	for (number,) in cursor:
		newNumber = int(number)

	print("You have succesfully registered as author #" + str(newNumber) + "!")
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

	credentialQuery = ("INSERT INTO CREDENTIALS VALUES ('AUTHOR', " + str(newNumber)  +", AES_ENCRYPT('" + password1 + "','" + MASTER_KEY + "'));")
	cursor.execute(credentialQuery)
	con.commit()

	print("Succes! Your password has been set. You can now log in!")

def showStatus(con, id):

	statusQuery = ("SELECT MANUSCRIPT.STATUS as Status, COUNT(*) as Count FROM MANUSCRIPT WHERE MANUSCRIPT.AUTHOR_ID=" + id +  " GROUP BY MANUSCRIPT.STATUS ORDER BY FIELD(MANUSCRIPT.STATUS, 'Received', 'Under Review', 'Rejected', 'Accepted', 'Typeset', 'Scheduled', 'Published');")
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
		count += 1
	if (count == 0):
		print("Status: You have no manuscripts!")
	else:
		print(statusRows)
	print()
	print("Below, you will also find a table showing the manuscript \nnumber corresponding to the status that manuscript is in:")
	print()
	statusQuery = ("SELECT MANUSCRIPT.NUMBER as ManuscriptNumber, MANUSCRIPT.STATUS as Status FROM MANUSCRIPT WHERE MANUSCRIPT.AUTHOR_ID=" + id +  " ORDER BY FIELD(MANUSCRIPT.STATUS, 'Received', 'Under Review', 'Rejected', 'Accepted', 'Typeset', 'Scheduled', 'Published');")
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
		print("-----------------------------------")
		print(statusRows)



def startAuthorShell(con, id):

	try:
		cursor = con.cursor()
		loginHelloQuery = ("SELECT AUTHOR.FNAME as FirstName, AUTHOR.LNAME as LastName, AUTHOR.MAILING_ADDRESS as Address FROM AUTHOR WHERE AUTHOR.ID=" + id + ";")

		cursor.execute(loginHelloQuery)

		for (FirstName, LastName, Address) in cursor:
			print("Hello {} {}. Here is your address: {}".format(FirstName, LastName, Address))
			print()

		showStatus(con, id)

		print()
		print("Commands at your service:")
		print()
		print("'status' -> Lists all manuscripts you are the primary author for \n as well as the status they are in.")
		print()
		print("'retract|<ManuscriptNumber' \n   -> Removes one of your manuscripts.")
		print()
		print("'submit|<title>|<Affiliation>|<RICode>|<author2>|<author3>|<author4>|<filename>' \n   -> Allows you to submit a manuscript")

		loop = True
		while loop:
			print()
			print("------------------------------------------------------------------------------------------")
			text = raw_input('What would you like to do next? ')
			textArray = text.split('|')
			print()
			# print(textArray)
			print()

			if (textArray[0] == "status"):
				showStatus(con, id) 

			elif (textArray[0] == "logout"):
				print("You have been logged out. Have a great day!")
				break

			elif (textArray[0] == "retract"):
				if (len(textArray) == 2):

					checkPermissionQuery = ("SELECT MANUSCRIPT.AUTHOR_ID as AuthorID FROM MANUSCRIPT WHERE MANUSCRIPT.NUMBER=" + textArray[1] + ";")
					cursor = con.cursor()
					cursor.execute(checkPermissionQuery)

					realAuthorID = 0
					for (AuthorID,) in cursor:
						realAuthorID = int(AuthorID)
					print (realAuthorID , id)

					if (int(realAuthorID) != int(id)):
						print("You cannot retract a manuscript that you aren't the primary author for!")
					elif (int(realAuthorID) == int(id)):
						answer = raw_input('Are you sure you want to retract manuscript ' + textArray[1] + '? (yes/no)')
						if (answer == "yes"):

							# delete in proper order
							# DELETE FROM CODE_GROUP;
							# DELETE FROM REVIEWER_GROUP;
							# DELETE FROM SECONDARY_AUTHOR;
							# DELETE FROM MANUSCRIPT;
							# DELETE FROM EDITOR;
							# DELETE FROM RI_CODE;
							# DELETE FROM AUTHOR;
							# DELETE FROM MANUSCRIPT;
							# DELETE FROM JOURNAL_ISSUE;
							# DELETE FROM REVIEW;
							# DELETE FROM REVIEWER;
							deleteQuery1 = ("DELETE FROM REVIEWER_GROUP WHERE MANUSCRIPT_NUMBER=" + textArray[1] + ";")
							deleteQuery2 = ("DELETE FROM SECONDARY_AUTHOR WHERE MANUSCRIPT_NUMBER=" + textArray[1] + ";")
							deleteQuery3 = ("DELETE FROM MANUSCRIPT WHERE NUMBER=" + textArray[1] + ";")
							deleteQuery4 = ("DELETE FROM REVIEW WHERE MANUSCRIPT_NUMBER=" + textArray[1] + ";")
							cursor.execute(deleteQuery1)
							cursor.execute(deleteQuery2)
							cursor.execute(deleteQuery3)
							cursor.execute(deleteQuery4)
							con.commit()

			elif (textArray[0] == "submit"):
				try:
					#find number of editors in system
					numberOfEditors = 0
					cursor = con.cursor()
					editorCountQuery = ("SELECT COUNT(*) as Count FROM EDITOR;")
					cursor.execute(editorCountQuery)
					for (count,) in cursor:
						numberOfEditors=int(count)
					editorToAssign = random.randint(1,numberOfEditors)

					# submit <title> <Affiliation> <RICode> <author2> <author3> <author4> <filename>
					receivedTime = datetime.now().replace(microsecond=0)

					value = None
					addManuscript = ("INSERT INTO MANUSCRIPT "
						"(TITLE, STATUS, CONTENT, DATE_RECEIVED, RI_CODE, AUTHOR_ID, EDITOR_ID, PAGE_NUMBER_IN_ISSUE, ORDER_IN_ISSUE, " + 
						"DATE_ACCEPTED, NUMBER_OF_PAGES, JOURNAL_ISSUE_YEAR, JOURNAL_ISSUE_PERIOD) "
						"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

					addSecondaryAuthor = ("INSERT INTO SECONDARY_AUTHOR "
						"(FNAME,LNAME,MANUSCRIPT_NUMBER,ORDER_IN_MANUSCRIPT) "
						" VALUES (%s, %s, %s, %s)")

					if (len(textArray) == 8):
						print("reached if statement 8")

						updateAuthorAffiliation = ("UPDATE AUTHOR SET AFFILIATION= '" + textArray[2] + "' WHERE AUTHOR.ID=" + id + ";")
						cursor.execute(updateAuthorAffiliation)
						con.commit()

						manuscriptData = (textArray[1], "Received", textArray[7], receivedTime, textArray[3], id, editorToAssign, value, value, value, value, value, value, )
						print("Submitting manuscript . . . ")
						cursor.execute(addManuscript, manuscriptData)
						con.commit()


						getLastManuscriptNumberQuery = ("SELECT MANUSCRIPT.NUMBER AS Number FROM MANUSCRIPT ORDER BY MANUSCRIPT.NUMBER ASC;")
						cursor.execute(getLastManuscriptNumberQuery)
						newNumber = 0
						for (number,) in cursor:
							newNumber = int(number)


						name = textArray[4].split(' ')
						secondaryAuthorData = (name[0], name[1], newNumber, 1)
						cursor.execute(addSecondaryAuthor, secondaryAuthorData)
						con.commit()

						name = textArray[5].split(' ')
						secondaryAuthorData2 = (name[0], name[1], newNumber, 2)
						cursor.execute(addSecondaryAuthor, secondaryAuthorData2)
						con.commit()

						name = textArray[6].split(' ')
						secondaryAuthorData3 = (name[0], name[1], newNumber, 3)
						cursor.execute(addSecondaryAuthor, secondaryAuthorData3)
						con.commit()

						print("You have succesfully submitted manuscript #" + str(newNumber) + "!!!")

					elif (len(textArray) == 7):

						updateAuthorAffiliation = ("UPDATE AUTHOR SET AFFILIATION= '" + textArray[2] + "' WHERE AUTHOR.ID=" + id + ";")
						cursor.execute(updateAuthorAffiliation)
						con.commit()

						manuscriptData = (textArray[1], "Received", textArray[6], receivedTime, textArray[3], id, editorToAssign, value, value, value, value, value, value)

						print("Submitting manuscript . . . ")
						cursor.execute(addManuscript, manuscriptData)
						con.commit()

						getLastManuscriptNumberQuery = ("SELECT MANUSCRIPT.NUMBER AS Number FROM MANUSCRIPT ORDER BY MANUSCRIPT.NUMBER ASC;")
						cursor.execute(getLastManuscriptNumberQuery)
						newNumber = 0
						for (number,) in cursor:
							newNumber = int(number)

						name = textArray[4].split(' ')
						secondaryAuthorData = (name[0], name[1], newNumber, 1)
						cursor.execute(addSecondaryAuthor, secondaryAuthorData)
						con.commit()

						name = textArray[5].split(' ')
						secondaryAuthorData2 = (name[0], name[1], newNumber, 2)
						cursor.execute(addSecondaryAuthor, secondaryAuthorData2)
						con.commit()

						print("You have succesfully submitted manuscript #" + str(newNumber) + "!!!")

					elif (len(textArray) == 6):

						updateAuthorAffiliation = ("UPDATE AUTHOR SET AFFILIATION= '" + textArray[2] + "' WHERE AUTHOR.ID=" + id + ";")
						cursor.execute(updateAuthorAffiliation)
						con.commit()

						manuscriptData = (textArray[1], "Received", textArray[5], receivedTime, textArray[3], id, editorToAssign, value, value, value, value, value, value, )

						print("Submitting manuscript . . . ")
						cursor.execute(addManuscript, manuscriptData)
						con.commit()

						getLastManuscriptNumberQuery = ("SELECT MANUSCRIPT.NUMBER AS Number FROM MANUSCRIPT ORDER BY MANUSCRIPT.NUMBER ASC;")
						cursor.execute(getLastManuscriptNumberQuery)
						newNumber = 0
						for (number,) in cursor:
							newNumber = int(number)

						name = textArray[4].split(' ')
						secondaryAuthorData = (name[0], name[1], newNumber, 1)
						cursor.execute(addSecondaryAuthor, secondaryAuthorData)
						con.commit()

						print("You have succesfully submitted manuscript #" + str(newNumber) + "!!!")

					elif (len(textArray) == 5):

						updateAuthorAffiliation = ("UPDATE AUTHOR SET AFFILIATION= '" + textArray[2] + "' WHERE AUTHOR.ID=" + id + ";")
						cursor.execute(updateAuthorAffiliation)
						con.commit()

						manuscriptData = (textArray[1], "Received", textArray[4], receivedTime, textArray[3], id, editorToAssign, value, value, value, value, value, value, )

						# Insert new employee
						print("Submitting manuscript . . . ")
						cursor.execute(addManuscript, manuscriptData)
						con.commit()

						getLastManuscriptNumberQuery = ("SELECT MANUSCRIPT.NUMBER AS Number FROM MANUSCRIPT ORDER BY MANUSCRIPT.NUMBER ASC;")
						cursor.execute(getLastManuscriptNumberQuery)
						newNumber = 0
						for (number,) in cursor:
							newNumber = int(number)

						print("You have succesfully submitted manuscript #" + str(newNumber) + "!!!")


					else:
						print("ERROR: Incorrect command syntax. Please make sure your command is appropriate as documented in the READ.ME. Thanks!")
				except mysql.connector.Error as e:
					print("ERROR: No reviewer with subject matter expertise is enrolled to review this manuscript!")

			else:
					print("ERROR: Incorrect command syntax. Please make sure your command is appropriate as documented in the READ.ME. Thanks!")


	except mysql.connector.Error as e:
		print("SQL Error: {0}".format(e.msg))
		print("ERROR: Incorrect command syntax. \nFor security reasons you have been logged out! \nPlease be sure to follow the READ.ME documentation!")
	except:
		print("Unexpected error: {0}".format(sys.exc_info()[0]))
		print("ERROR: Incorrect command syntax. \nFor security reasons you have been logged out! \nPlease be sure to follow the READ.ME documentation!")

	
	cursor.close()


