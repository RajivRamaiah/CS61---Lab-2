# Editor.py
# Editor driver for when an editor logs in to the system.

from __future__ import print_function	# print function
import mysql.connector					# mysql functionality
import sys			

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
		cursor = con.cursor()
		loginHelloQuery = ("SELECT EDITOR.FNAME as FirstName, EDITOR.LNAME as LastName FROM EDITOR WHERE EDITOR.ID=" + id + ";")

		cursor.execute(loginHelloQuery)

		for (FirstName, LastName) in cursor:
			print("Hello {} {}.".format(FirstName, LastName))
			print()
			print("The following table shows you the number of manuscripts \nunder your review and the status they are in:")

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


		loop = True
		while loop:
			print()
			text = raw_input('What would you like to do next?	')
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
					print("You have no manuscripts")
				else:
					print("".join(["{:<20}".format(col) for col in cursor.column_names]))
					print("----------------------------")
					print(statusRows)

			elif (textArray[0] == "logout"):
				print("You have been logged out. Have a great day!")
				break

			elif (textArray[0] == "assign"):
				

	except mysql.connector.Error as e:
		print("SQL Error: {0}".format(e.msg))
	except:
		print("Unexpected error: {0}".format(sys.exc_info()[0]))

	
	cursor.close()