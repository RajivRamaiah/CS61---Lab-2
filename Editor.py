# Editor.py
# Editor driver for when an editor logs in to the system.

from __future__ import print_function	# print function
import mysql.connector					# mysql functionality
import sys
import random
import time    
from datetime import date, datetime, timedelta
import getpass


def registerEditor(con, fname, lname, Master_Key):
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

	print("You have successfully registered as Editor #" + str(newNumber) + "!")

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

	credentialQuery = ("INSERT INTO CREDENTIALS VALUES ('EDITOR', " + str(newNumber)  +", AES_ENCRYPT('" + password1 + "','" + Master_Key + "'));")
	cursor.execute(credentialQuery)
	con.commit()

	print("Success! Your password has been set. You can now log in!")


def showStatus(con, id):

	statusQuery = ("SELECT MANUSCRIPT.STATUS as Status, COUNT(*) as Count FROM MANUSCRIPT WHERE MANUSCRIPT.EDITOR_ID=" + id +  " GROUP BY MANUSCRIPT.STATUS ORDER BY FIELD(MANUSCRIPT.STATUS, 'Received', 'Under Review', 'Rejected', 'Accepted', 'Typeset', 'Scheduled', 'Published');")
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
	statusQuery = ("SELECT MANUSCRIPT.NUMBER as ManuscriptNumber, MANUSCRIPT.STATUS as Status FROM MANUSCRIPT WHERE MANUSCRIPT.EDITOR_ID=" + id +  " ORDER BY FIELD(MANUSCRIPT.STATUS, 'Received', 'Under Review', 'Rejected', 'Accepted', 'Typeset', 'Scheduled', 'Published');")
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

		if (ifExists == 0):
			print("The editor id you entered is invalid!")
			loop = False

		if (loop == True):
			showStatus(con,id)

			print()
			print("Commands at your service:")
			print()
			print("'status' -> Lists all manuscripts you are the editor for \n as well as the status they are in.")
			print()
			print("'assign|<manu#>|<reviewer id>' -> assigns a manuscript to a reviewer.")
			print()
			print("'reject|<manu#>' -> Allows you to reject a manuscript from consideration.")
			print()
			print("'accept|<manu#>' -> Allows you to accept a manuscript to be scheduled and published later.")
			print()
			print("'typeset|<manu#>|<pp>' -> Enter the results of your typesetting, and the number of pages the manuscript will occupy.")
			print()
			print("'schedule|<manu#>|<issueyear>|<issueperiod>' -> Allows you to schedule a manuscript for an issue.")
			print()
			print("'publish|<issueyear>|<issueperiod>' -> Allows you to publish an issue for print.")
			print()
			print("To logout, simply enter 'logout'!")
			print()


		while loop:
			print()
			print("------------------------------------------------------------------------------------------")
			text = raw_input('What would you like to do next?	')
			textArray = text.split('|')
			print()
			# print(textArray)
			print()

			if (len(textArray) > 4):
				print("Please enter a valid command. See the READ.ME documentation for help.")
				continue

			if (textArray[0] == "status"):

				showStatus(con,id)

			elif (textArray[0] == "logout"):
				print("You have been logged out. Have a great day!")

				print()
				print("Hello. Welcome to the manuscript management system. From here, you can register as an")
				print("editor/author/reviewer or login if you already have an account as one of those users.")
				print()
				print("To register as an author, enter: 'register|author|<fname>|<lname>|<address>|<email>|<affiliation>'")
				print("To register as an editor, enter: 'register|editor|<fname>|<lname>'")
				print("To register as a reviewer, enter: 'register|reviewer|<fname>|<lname>|<affiliation>|<ricode1>|<ricode2>|<ricode3>'")
				print()
				print("To login, simply enter 'login|<usertype>|<userID>'")
				print("To logout, simply enter 'exit'")
				print()
				
				break

			# assign <manu#> <reviewer id>
			elif (textArray[0] == "assign"):
				if (len(textArray) == 3):

					# check it is the editors manuscript to alter
					checkEditorAssigned = ("SELECT MANUSCRIPT.NUMBER as Num FROM MANUSCRIPT WHERE MANUSCRIPT.EDITOR_ID=" + id + ";")
					cursor.execute(checkEditorAssigned)

					isEditors = 0
					for (Num, ) in cursor:
						if (str(Num) == textArray[1]):
							isEditors = 1
					if(isEditors == 0):
						print("ERROR: Insufficient Permission. \nYou cannot alter a manuscript not assigned to you as an editor.")
						continue

					# Check that reviewer has the same RI Code as manuscript
					getManuscriptRICode = ("SELECT MANUSCRIPT.RI_CODE as Code FROM MANUSCRIPT WHERE MANUSCRIPT.NUMBER=" + textArray[1] + ";")
					cursor.execute(getManuscriptRICode)

					code = 0
					for (Code, ) in cursor:
						code = int(Code)

					getReviewerCodes = ("SELECT CODE_GROUP.RI_CODE AS CODE FROM CODE_GROUP WHERE CODE_GROUP.REVIEWER_NUMBER=" + textArray[2] + ";")
					cursor.execute(getReviewerCodes)

					validAssignment = 0
					for (CODE, ) in cursor:
						if(str(code) == str(CODE)):
							validAssignment = 1

					if (validAssignment == 1):


						# check that reviewer hasn't already been assigned this manuscript
						checkNotAssigned = ("SELECT REVIEWER_GROUP.MANUSCRIPT_NUMBER as ManNum, REVIEWER_GROUP.REVIEWER_NUMBER as RevNum FROM REVIEWER_GROUP WHERE REVIEWER_GROUP.MANUSCRIPT_NUMBER=" + textArray[1] +  " AND REVIEWER_GROUP.REVIEWER_NUMBER=" + textArray[2] + ";")
						cursor.execute(checkNotAssigned)

						alreadyAssigned = 0
						for (ManNum, RevNum, ) in cursor:
							if (str(ManNum) == textArray[1] and str(RevNum) == textArray [2]):
								alreadyAssigned = 1


						if (alreadyAssigned == 0):
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

							print("Successfully added a reviewer for manuscript #" + str(textArray[1]) + "!")
						else:
							print("ERROR: Duplicate Assignment \nThe assignment already exists!")
					else:
						print("ERROR: Subject Mismatch \nYou cannot assign this manuscript to the reviewer. \nThe reviewer you selected is not specialized in the manuscript's subject matter")


				else:
					print("ERROR: Please enter a valid command. See the READ.ME documentation for help.")
					continue

			elif (textArray[0] == "reject"):
				if (len(textArray) == 2):

					# check it is the editors manuscript to alter
					checkEditorAssigned = ("SELECT MANUSCRIPT.NUMBER as Num FROM MANUSCRIPT WHERE MANUSCRIPT.EDITOR_ID=" + id + ";")
					cursor.execute(checkEditorAssigned)

					isEditors = 0
					for (Num, ) in cursor:
						if (str(Num) == textArray[1]):
							isEditors = 1
					if(isEditors == 0):
						print("ERROR: Insufficient Permission. \nYou cannot alter a manuscript not assigned to you as an editor.")
						continue

					updateManuscriptStatusToRejected = ("UPDATE MANUSCRIPT SET STATUS='Rejected' WHERE MANUSCRIPT.NUMBER=" + textArray[1] + ";")
					cursor.execute(updateManuscriptStatusToRejected)
					con.commit()

					print("Successfully rejected the manuscript.")
				else:
					print("ERROR: Please enter a valid command. See the READ.ME documentation for help.")
					continue
			elif (textArray[0] == "accept"):
				if (len(textArray) == 2):

					# check it is the editors manuscript to alter
					checkEditorAssigned = ("SELECT MANUSCRIPT.NUMBER as Num FROM MANUSCRIPT WHERE MANUSCRIPT.EDITOR_ID=" + id + ";")
					cursor.execute(checkEditorAssigned)

					isEditors = 0
					for (Num, ) in cursor:
						if (str(Num) == textArray[1]):
							isEditors = 1
					if(isEditors == 0):
						print("ERROR: Insufficient Permission. \nYou cannot alter a manuscript not assigned to you as an editor.")
						continue

					receivedTime = datetime.now().replace(microsecond=0)
					updateManuscriptStatusToAccepted = ("UPDATE MANUSCRIPT SET STATUS='Accepted' WHERE MANUSCRIPT.NUMBER=" + textArray[1] + ";")
					cursor.execute(updateManuscriptStatusToAccepted)
					con.commit()

					updateAcceptedDate = ("UPDATE MANUSCRIPT SET DATE_ACCEPTED='" + str(receivedTime) + "' WHERE MANUSCRIPT.NUMBER=" + textArray[1] + ";")
					cursor.execute(updateAcceptedDate)
					con.commit()

					print("Successfully updated manuscript to accepted.")

				else:
					print("ERROR: Please enter a valid command. See the READ.ME documentation for help.")
					continue
			elif (textArray[0] == "typeset"):
				if (len(textArray) == 3):

					# check it is the editors manuscript to alter
					checkEditorAssigned = ("SELECT MANUSCRIPT.NUMBER as Num FROM MANUSCRIPT WHERE MANUSCRIPT.EDITOR_ID=" + id + ";")
					cursor.execute(checkEditorAssigned)

					isEditors = 0
					for (Num, ) in cursor:
						if (str(Num) == textArray[1]):
							isEditors = 1
					if(isEditors == 0):
						print("ERROR: Insufficient Permission. \nYou cannot alter a manuscript not assigned to you as an editor.")
						continue

					updateManuscriptStatusToTypeset = ("UPDATE MANUSCRIPT SET STATUS='Typeset' WHERE MANUSCRIPT.NUMBER=" + textArray[1] + ";")
					cursor.execute(updateManuscriptStatusToTypeset)
					con.commit()

					updatePageNumbers = ("UPDATE MANUSCRIPT SET NUMBER_OF_PAGES='" + textArray[2] + "' WHERE MANUSCRIPT.NUMBER=" + textArray[1] + ";")
					cursor.execute(updatePageNumbers)
					con.commit()

					print("Successfully typeset the manuscript.")
				else:
					print("ERROR: Please enter a valid command. See the READ.ME documentation for help.")
					continue
			elif (textArray[0] == "schedule"):
				if (len(textArray) == 4):

					# check it is the editors manuscript to alter
					checkEditorAssigned = ("SELECT MANUSCRIPT.NUMBER as Num FROM MANUSCRIPT WHERE MANUSCRIPT.EDITOR_ID=" + id + ";")
					cursor.execute(checkEditorAssigned)

					isEditors = 0
					for (Num, ) in cursor:
						if (str(Num) == textArray[1]):
							isEditors = 1
					if(isEditors == 0):
						print("ERROR: Insufficient Permission. \nYou cannot alter a manuscript not assigned to you as an editor.")
						continue

					exit = 0

					#check its been typeset
					checkManuscriptStatus = ("SELECT MANUSCRIPT.STATUS as Status FROM MANUSCRIPT WHERE MANUSCRIPT.NUMBER=" + textArray[1] + ";")
					cursor = con.cursor()
					cursor.execute(checkManuscriptStatus)

					status = ""
					for (Status,) in cursor:
						status = str(Status)

					if (status != "Typeset"):
						print("You cannot schedule a manuscript that hasn't been typeset yet! Trying this again could result in your expulsion as an editor. . .")
						continue

					checkIfJournalPublished = ("SELECT JOURNAL_ISSUE.DATE_PUBLISHED as DatePubl FROM JOURNAL_ISSUE WHERE YEAR=" + textArray[2] + " AND PERIOD=" + textArray[3] + ";")
					cursor = con.cursor()
					cursor.execute(checkIfJournalPublished)

					isPublished = 0
					for (DatePubl, ) in cursor:
						if(DatePubl != None):
							isPublished += 1
					if (isPublished == 1):
						print("ERROR: This issue has already been published. You cannot schedule a manuscript for an issue already published!")
						exit = 1
					if (exit == 1):
						continue

					# Check pages aren't greater than 100
					sumPages = 0
					checkManuscriptPages = ("SELECT MANUSCRIPT.NUMBER_OF_PAGES as Pages FROM MANUSCRIPT WHERE MANUSCRIPT.NUMBER=" + textArray[1] + ";")
					cursor = con.cursor()
					cursor.execute(checkManuscriptPages)

					for (Pages,) in cursor:
						sumPages += Pages


					checkJournalPages = ("SELECT MANUSCRIPT.NUMBER_OF_PAGES as Pages FROM MANUSCRIPT WHERE MANUSCRIPT.JOURNAL_ISSUE_YEAR=" + textArray[2] + " AND MANUSCRIPT.JOURNAL_ISSUE_PERIOD=" + textArray[3] +";")
					cursor = con.cursor()
					cursor.execute(checkJournalPages)

					
					for (Pages,) in cursor:
						sumPages += int(Pages)

					if(sumPages > 100):
						print("ERROR: Scheduling this manuscript for the issue you selected would exceed an issue's 100 page limit!")
						exit=1
					if (exit == 1):
						continue

					# Check that issue doesn't exist
					checkJournalExistence = ("SELECT * FROM JOURNAL_ISSUE WHERE YEAR=" + textArray[2] + " AND PERIOD=" + textArray[3] + ";")
					cursor.execute(checkJournalExistence)

					journalExists = 0
					for row in cursor:
						journalExists += 1


					if (journalExists == 0):
						addIssue = ("INSERT INTO JOURNAL_ISSUE "
							"(YEAR,PERIOD,DATE_PUBLISHED) "
							"VALUES (%s, %s, %s)")
						issueData = (textArray[2], textArray[3], None)
						cursor.execute(addIssue, issueData)
						con.commit()

					updateManuscriptStatusToScheduled = ("UPDATE MANUSCRIPT SET STATUS='Scheduled', MANUSCRIPT.JOURNAL_ISSUE_YEAR='" + textArray[2] 
						+ "', MANUSCRIPT.JOURNAL_ISSUE_PERIOD='" + textArray[3] + "' WHERE MANUSCRIPT.NUMBER=" + textArray[1] + ";")
					cursor.execute(updateManuscriptStatusToScheduled)
					con.commit()

					print("Successfully scheduled manuscript!")

				else:
					print("ERROR: Please enter a valid command. See the READ.ME documentation for help.")
					continue


			elif (textArray[0] == "publish"):
				if (len(textArray) == 3):
					receivedTime = datetime.now().replace(microsecond=0)

					# Check that journal has issues before publishing
					checkIfEmpty = ("SELECT MANUSCRIPT.NUMBER as ManNumber FROM MANUSCRIPT WHERE MANUSCRIPT.JOURNAL_ISSUE_YEAR=" 
						+ textArray[1] + " AND MANUSCRIPT.JOURNAL_ISSUE_PERIOD=" + textArray[2] + ";")
					cursor = con.cursor()
					cursor.execute(checkIfEmpty)

					exists = 0;
					for (ManNumber,) in cursor:
						exists += 1

					# it has issues
					if (exists >= 1):
						checkIfJournalPublished = ("SELECT JOURNAL_ISSUE.DATE_PUBLISHED as DatePubl FROM JOURNAL_ISSUE WHERE YEAR=" + textArray[1] + " AND PERIOD=" + textArray[2] + ";")
						cursor = con.cursor()
						cursor.execute(checkIfJournalPublished)

						isPublished = 0
						for (DatePubl, ) in cursor:
							if(DatePubl != None):
								isPublished += 1
						if (isPublished >= 1):
							print("ERROR: This issue has already been published. You cannot schedule a manuscript for an issue already published!")
							continue

						updateIssue = ("UPDATE JOURNAL_ISSUE SET DATE_PUBLISHED='" +  str(receivedTime) + "' WHERE YEAR=" + textArray[1] +  " AND PERIOD= "  + textArray[2] + ";")
						cursor.execute(updateIssue)
						con.commit()


						getManuscriptsToPublish = ("SELECT MANUSCRIPT.NUMBER as Num FROM MANUSCRIPT WHERE MANUSCRIPT.JOURNAL_ISSUE_YEAR=" + textArray[1] + " AND MANUSCRIPT.JOURNAL_ISSUE_PERIOD=" + textArray[2] +";")
						cursor.execute(getManuscriptsToPublish)

						for (Num, ) in cursor:
							updateManuscriptStatusToPublished = ("UPDATE MANUSCRIPT SET STATUS='Published', MANUSCRIPT.JOURNAL_ISSUE_YEAR='" + textArray[1] 
								+ "', MANUSCRIPT.JOURNAL_ISSUE_PERIOD='" + textArray[2] + "' WHERE MANUSCRIPT.NUMBER=" + str(Num) + ";")
							cursor.execute(updateManuscriptStatusToPublished)
							con.commit()

						print("Successfully published the issue!")
					else:
						print("ERROR: The issue you want to publish has no manuscripts assigned to it. This is unaccepable. . . Please schedule manuscripts for this issue before publishing.")
				else:
					print("ERROR: Please enter a valid command. See the READ.ME documentation for help.")
					continue
			else:
				print("ERROR: Incorrect command syntax.")
				continue


	except mysql.connector.Error as e:
		print("SQL Error: {0}".format(e.msg))
		print("ERROR: Incorrect command syntax. \nFor security reasons you have been logged out! \nPlease be sure to follow the READ.ME documentation!")
	except:
		print("Unexpected error: {0}".format(sys.exc_info()[0]))
		print("ERROR: Incorrect command syntax. \nFor security reasons you have been logged out! \nPlease be sure to follow the READ.ME documentation!")

	
	cursor.close()