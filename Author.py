# Author.py
# Author driver for when an author logs in to the system.

from __future__ import print_function	# print function
import mysql.connector					# mysql functionality
import sys			
import random
import time    
from datetime import date, datetime, timedelta


def addAuthor():
	print("ADD AUTHOR HERE")

def registerAuthor(con, firstname, lastname, address, email, affiliation):
	add_author = ("INSERT INTO AUTHOR "
		"(FNAME,LNAME,MAILING_ADDRESS,E_MAIL,AFFILIATION) "
		"VALUES (%s, %s, %s, %s, %s)")
	data_author = (firstname, lastname, address, email,  affiliation)
	# Insert new employee
	cursor = con.cursor()
	print("Registering . . . ")
	cursor.execute(add_author, data_author)
	con.commit()
	print("You have succesfully registered! You can now log in!")

def showStatus(con):
	statusQuery = ("SELECT MANUSCRIPT.STATUS as Status, COUNT(*) as Count FROM MANUSCRIPT WHERE MANUSCRIPT.AUTHOR_ID=" + id +  " GROUP BY MANUSCRIPT.STATUS;")
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

def startAuthorShell(con, id):

	try:
		cursor = con.cursor()
		loginHelloQuery = ("SELECT AUTHOR.FNAME as FirstName, AUTHOR.LNAME as LastName, AUTHOR.MAILING_ADDRESS as Address FROM AUTHOR WHERE AUTHOR.ID=" + id + ";")

		cursor.execute(loginHelloQuery)

		for (FirstName, LastName, Address) in cursor:
			print("Hello {} {}. Here is your address: {}".format(FirstName, LastName, Address))
			print()

		# Just shows the tables with manuscript and status
		# statusQuery = ("SELECT MANUSCRIPT.NUMBER as ManuscriptNumber, MANUSCRIPT.TITLE as ManuscriptTitle, MANUSCRIPT.STATUS " + 
		# 	"as ManuscriptStatus FROM MANUSCRIPT WHERE MANUSCRIPT.AUTHOR_ID=" + id + ";")

		statusQuery = ("SELECT MANUSCRIPT.STATUS as Status, COUNT(*) as Count FROM MANUSCRIPT WHERE MANUSCRIPT.AUTHOR_ID=" + id +  " GROUP BY MANUSCRIPT.STATUS;")

		cursor.execute(statusQuery)


		# iterate through results
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


		loop = True
		while loop:
			print()
			text = raw_input('What would you like to do next? ')
			textArray = text.split('|')
			print()
			print(textArray)
			print()

			if (textArray[0] == "status"):
				cursor.execute(statusQuery)
				# iterate through results
				statusRows = ""
				count = 0
				for row in cursor:
					statusRows += "".join(["{:<20}".format(col) for col in row]) + "\n"
					count += 1
				if (count == 0):
					print("You have no manuscripts you pleb")
				else:
					print("".join(["{:<20}".format(col) for col in cursor.column_names]))
					print("----------------------------")
					print(statusRows)

			elif (textArray[0] == "logout"):
				print("You have been logged out. Have a great day!")
				break

			elif (textArray[0] == "retract"):
				if (len(textArray) == 2):
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
					print("reached if statement 7")

					updateAuthorAffiliation = ("UPDATE AUTHOR SET AFFILIATION= '" + textArray[2] + "' WHERE AUTHOR.ID=" + id + ";")
					cursor.execute(updateAuthorAffiliation)
					con.commit()

					manuscriptData = (textArray[1], "Received", textArray[6], receivedTime, textArray[3], id, editorToAssign, value, value, value, value, value, value, )

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
					print("reached if statement 6")

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
					print("reached if statement 5")

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
		print("SQL Error: {0}".format(e.msg))
	except:
		print("Unexpected error: {0}".format(sys.exc_info()[0]))

	
	cursor.close()


