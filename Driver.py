from __future__ import print_function	# print function
import mysql.connector					# mysql functionality
import sys								# for errors
from Author import *
from Editor import *
from Reviewer import *

SERVER   = "sunapee.cs.dartmouth.edu"
USERNAME = "rajiv" 
PASSWORD = "AA12345678"# raw_input("Enter the MASTER_KEY: ")
DATABASE = "rajiv_db"

if __name__ == "__main__":

	try:
		# initialize db connection
		con = mysql.connector.connect(host=SERVER,user=USERNAME,password=PASSWORD, database=DATABASE)

		print("Connection established.")

		loop = True
		while loop:
			print()
			text = raw_input('Enter a command: ')
			textArray = text.split('|')
			print()
			print(textArray)
			print()

			# REGISTER
			if (textArray[0] == "register"):
				if (textArray[1] == "author"):
					print("REGISTERING AUTHOR")
					registerAuthor(con, textArray[2], textArray[3], textArray[4], textArray[5], textArray[6])


				if (textArray[1] == "editor"):
					print("REGISTERING EDITOR")
					registerEditor()

				if (textArray[1] == "reviewer"):
					print("REGISTERING REVIEWER")
					registerReviewer()

			# LOGIN
			elif (textArray[0] == "login"):
				if (textArray[1] == "author"):
					print("Logging you in! Please wait one moment . . .")
					print()
					startAuthorShell(con, textArray[2])

				if (textArray[1] == "editor"):
					print("LOGIN EDITOR")
					startEditorShell()

				if (textArray[1] == "reviewer"):
					print("LOGIN REVIEWER")
					startReviewerShell()

			else:
				print ("ERROR: There is an error in your syntax. Please try again.")



	except mysql.connector.Error as e:
		print("SQL Error: {0}".format(e.msg))
	except:
		print("Unexpected error: {0}".format(sys.exc_info()[0]))

	con.close()

	print("\nConnection terminated.", end='')

