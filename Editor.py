# Editor.py
# Editor driver for when an editor logs in to the system.

from __future__ import print_function	# print function
import mysql.connector					# mysql functionality
import sys
import random
import time    
from datetime import date, datetime, timedelta

def registerEditor(con, fname, lname):
	addEditor = ("INSERT INTO EDITOR "
		"(FNAME,LNAME) "
		"VALUES (%s, %s)")
	editorData = (fname, lname)
	# Insert new employee
	cursor = con.cursor()
	print("Registering . . . ")
	cursor.execute(addEditor, editorData)
	con.commit()



	getLastEditorNumberQuery = ("SELECT EDITOR.ID AS ID FROM EDITOR ORDER BY EDITOR.ID ASC;")
	cursor.execute(getLastEditorNumberQuery)
	newNumber = 0
	for (number,) in cursor:
		newNumber = int(number)

	print("You have succesfully registered as editor #" + str(newNumber) + "! You can now log in!")

def startEditorShell(con, id):
	try:
		loop = True
		cursor = con.cursor()
		loginHelloQuery = ("SELECT EDITOR.FNAME as FirstName, EDITOR.LNAME as LastName FROM EDITOR WHERE EDITOR.ID=" + id + ";")

		cursor.execute(loginHelloQuery)

		ifExists = 0
		for (FirstName, LastName) in cursor:
			ifExists += 1
			print("Hello {} {}.".format(FirstName, LastName))
			print()
			print("The following table shows you the number of manuscripts \nunder your guidance and the status they are in:")

		if (ifExists == 0):
			print("The editor id you entered is invalid!")
			loop = False

		if (loop == True):
			statusQuery = ("SELECT MANUSCRIPT.STATUS as Status, COUNT(*) as Count FROM MANUSCRIPT WHERE MANUSCRIPT.EDITOR_ID=" + id +  " GROUP BY MANUSCRIPT.STATUS;")

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


		while loop:
			print()
			text = raw_input('What would you like to do next?	')
			textArray = text.split('|')
			print()
			print(textArray)
			print()

			if (len(textArray) > 4):
				print("Please enter a valid command. See the READ.ME documentation for help.")
				continue

			if (textArray[0] == "status"):
				print("The following table shows you the number of manuscripts \nunder your guidance and the status they are in:")
				cursor.execute(statusQuery)
				# iterate through results
				statusRows = ""
				count = 0
				for row in cursor:
					statusRows += "".join(["{:<20}".format(col) for col in row]) + "\n"
					count += 1
				if (count == 0):
					print("You have no manuscripts")
				else:
					print("".join(["{:<20}".format(col) for col in cursor.column_names]))
					print("----------------------------")
					print(statusRows)

			elif (textArray[0] == "logout"):
				print("You have been logged out. Have a great day!")
				break

			elif (textArray[0] == "assign"):
				if (len(textArray) == 3):
					receivedTime = datetime.now().replace(microsecond=0)

					addReviewerForManuscript = ("INSERT INTO REVIEWER_GROUP "
						"(MANUSCRIPT_NUMBER,REVIEWER_NUMBER,DATE_MAN_SENT_FOR_REVIEW) "
						"VALUES (%s, %s, %s)")
					reviewerGroupData = (textArray[1], textArray[2], receivedTime)
					# Insert new employee
					cursor.execute(addReviewerForManuscript, reviewerGroupData)
					con.commit() 

					updateManuscriptStatusToUnderReview = ("UPDATE MANUSCRIPT SET STATUS='Under Review' WHERE MANUSCRIPT.NUMBER=" + textArray[1]+ ";")
					cursor.execute(updateManuscriptStatusToUnderReview)
					con.commit()

					print("Succesfully added a reviewer for manuscript #" + str(textArray[1]) + "!")


				else:
					print("ERROR: Please enter a valid command. See the READ.ME documentation for help.")
					continue

			elif (textArray[0] == "reject"):
				if (len(textArray) == 2):
					updateManuscriptStatusToRejected = ("UPDATE MANUSCRIPT SET STATUS='Rejected' WHERE MANUSCRIPT.NUMBER=" + textArray[1] + ";")
					cursor.execute(updateManuscriptStatusToRejected)
					con.commit()
				else:
					print("ERROR: Please enter a valid command. See the READ.ME documentation for help.")
					continue
			elif (textArray[0] == "accept"):
				if (len(textArray) == 2):
					print("accept!")
					receivedTime = datetime.now().replace(microsecond=0)
					updateManuscriptStatusToAccepted = ("UPDATE MANUSCRIPT SET STATUS='Accepted' WHERE MANUSCRIPT.NUMBER=" + textArray[1] + ";")
					cursor.execute(updateManuscriptStatusToAccepted)
					con.commit()

					updateAcceptedDate = ("UPDATE MANUSCRIPT SET DATE_ACCEPTED='" + str(receivedTime) + "' WHERE MANUSCRIPT.NUMBER=" + textArray[1] + ";")
					cursor.execute(updateAcceptedDate)
					con.commit()

					print("Succesfully updated manuscript to accepted")

				else:
					print("ERROR: Please enter a valid command. See the READ.ME documentation for help.")
					continue
			elif (textArray[0] == "typeset"):
				if (len(textArray) == 3):
					updateManuscriptStatusToTypeset = ("UPDATE MANUSCRIPT SET STATUS='Typeset' WHERE MANUSCRIPT.NUMBER=" + textArray[1] + ";")
					cursor.execute(updateManuscriptStatusToTypeset)
					con.commit()

					updatePageNumbers = ("UPDATE MANUSCRIPT SET NUMBER_OF_PAGES='" + textArray[2] + "' WHERE MANUSCRIPT.NUMBER=" + textArray[1] + ";")
					cursor.execute(updatePageNumbers)
					con.commit()
				else:
					print("ERROR: Please enter a valid command. See the READ.ME documentation for help.")
					continue
			elif (textArray[0] == "schedule"):
				if (len(textArray) == 4):

					checkManuscriptStatus = ("SELECT MANUSCRIPT.STATUS as Status FROM MANUSCRIPT WHERE MANUSCRIPT.NUMBER=" + textArray[1] + ";")
					cursor = con.cursor()
					cursor.execute(checkManuscriptStatus)

					status = ""
					for (Status,) in cursor:
						status = str(Status)
					print (status , textArray[1])





	except mysql.connector.Error as e:
		print("SQL Error: {0}".format(e.msg))
		print("Sorry, you entered an invalid data format for your last command! For security reasons you have been logged out! Please be sure to follow the READ.ME documentation!")
	except:
		print("Unexpected error: {0}".format(sys.exc_info()[0]))
		print("Sorry, you entered an invalid data format for your last command! For security reasons you have been logged out! Please be sure to follow the READ.ME documentation!")


	
	cursor.close()