from __future__ import print_function	# print function
import mysql.connector					# mysql functionality
import sys								# for errors
from Author import *
from Editor import *
from Reviewer import *

SERVER   = "sunapee.cs.dartmouth.edu"
USERNAME = "rajiv" 
PASSWORD = "AA12345678"
DATABASE = "rajiv_db"
QUERY    = "SELECT * FROM REVIEWER;"

print("This line will be printed.")

if __name__ == "__main__":

	try:
		# initialize db connection
		con = mysql.connector.connect(host=SERVER,user=USERNAME,password=PASSWORD, database=DATABASE)


		print("Connection established.")

		cursor = con.cursor()

		cursor.execute(QUERY)

		print("Query executed: '{0}'\n\nResults:".format(QUERY))

		print("".join(["{:<12}".format(col) for col in cursor.column_names]))
		print("--------------------------------------------")

		for row in cursor:
			print("".join(["{:<12}".format(col) for col in row]))


		loop = True
		while loop:
			text = raw_input('Enter a command: ')
			textArray = text.split(' ')

			if (textArray[0] == "register"):
				if (textArray[1] == "author"):
					print("REGISTERING AUTHOR")
					registerAuthor()
					# registerAuthor() # Called from author file
				if (textArray[1] == "editor"):
					print("REGISTERING EDITOR")
					registerEditor()

				if (textArray[1] == "reviewer"):
					print("REGISTERING REVIEWER")
					registerReviewer()

			elif (textArray[0] == "login"):
				if (textArray[1] == "author"):
					print("LOGIN AUTHOR")
					startAuthorShell()
					# registerAuthor() # Called from author file
				if (textArray[1] == "editor"):
					print("LOGIN EDITOR")
					startEditorShell()
					# registerEditor()
				if (textArray[1] == "reviewer"):
					print("LOGIN REVIEWER")
					startReviewerShell()

			else:
				print ("ERROR: There is an error in your syntax. Please try again.")
				break


	except mysql.connector.Error as e:
		print("SQL Error: {0}".format(e.msg))
	except:
		print("Unexpected error: {0}".format(sys.exc_info()[0]))

	con.close()
	cursor.close()

	print("\nConnection terminated.", end='')

