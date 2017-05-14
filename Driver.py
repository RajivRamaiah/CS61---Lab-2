from __future__ import print_function	# print function
import mysql.connector					# mysql functionality
import sys								# for errors
from Author import *
from Editor import *
from Reviewer import *
import time
import getpass

SERVER   = "sunapee.cs.dartmouth.edu"
USERNAME = "rajiv" 
PASSWORD = getpass.getpass(prompt='Please Enter The Database Master Key: ')
DATABASE = "rajiv_db"

if __name__ == "__main__":

	try:
		# initialize db connection
		con = mysql.connector.connect(host=SERVER,user=USERNAME,password=PASSWORD, database=DATABASE)

		loop = True
		while loop:
			print()
			text = raw_input('Enter a command: ')
			textArray = text.split('|')
			print()
			# print(textArray)
			print()

			# REGISTER
			if (textArray[0] == "register"):
				if(len(textArray) == 7):
					if (textArray[1] == "author"):
						print("Registering Author . . .")
						registerAuthor(con, textArray[2], textArray[3], textArray[4], textArray[5], textArray[6], PASSWORD)

				# register|editor|fname|lname
				if (textArray[1] == "editor"):
					print("Registering Editor . . .")
					registerEditor(con, textArray[2], textArray[3], PASSWORD)

				# register|reviewer|fname|lname|email|affiliation|one|two|three
				if (textArray[1] == "reviewer"):
					if (len(textArray) == 7):
						print("Registering Reviewer . . .")
						registerReviewerWithOne(con, textArray[2], textArray[3], textArray[4], textArray[5], textArray[6], PASSWORD)
					elif (len(textArray) == 8):
						print("Registering Reviewer . . .")
						registerReviewerWithTwo(con, textArray[2], textArray[3], textArray[4], textArray[5], textArray[6], textArray[7], PASSWORD)
					elif (len(textArray) == 9):
						print("Registering Reviewer . . .")
						registerReviewerWithThree(con, textArray[2], textArray[3], textArray[4], textArray[5], textArray[6], textArray[7], textArray[8], PASSWORD)
					else:
						print("ERROR: Must register reviewer with 1-3 RI Codes")

			# LOGIN
			elif (textArray[0] == "login"):
				if(len(textArray) == 3):
					if (textArray[1] == "author"):
						PASSWORD = "AA12345678" #must reset since it is lost after the first login
						userpass = getpass.getpass(prompt='Please enter your password: ')
						cursor = con.cursor()
						checkPassword = ("SELECT AES_DECRYPT(CREDENTIALS.PASSWORD, '" + PASSWORD + "') AS PASSWORD FROM CREDENTIALS WHERE CREDENTIALS.USER_TYPE='AUTHOR' AND CREDENTIALS.ID=" + textArray[2] + ";")
						cursor.execute(checkPassword)

						decryptedPassword = ""
						for (PASSWORD,) in cursor:
							decryptedPassword = PASSWORD

						cursor.close()
						if(userpass == decryptedPassword):
							print("Loging In . . .")
							time.sleep(1)
							print()

							startAuthorShell(con, textArray[2])
						else:
							print("ERROR: You entered an incorrect password.")

					elif (textArray[1] == "editor"):

						PASSWORD = "AA12345678" #must reset since it is lost after the first login
						userpass = getpass.getpass(prompt='Please enter your password: ')
						cursor = con.cursor()
						checkPassword = ("SELECT AES_DECRYPT(CREDENTIALS.PASSWORD, '" + PASSWORD + "') AS PASSWORD FROM CREDENTIALS WHERE CREDENTIALS.USER_TYPE='EDITOR' AND CREDENTIALS.ID=" + textArray[2] + ";")
						cursor.execute(checkPassword)

						decryptedPassword = ""
						for (PASSWORD,) in cursor:
							decryptedPassword = PASSWORD

						cursor.close()
						if(userpass == decryptedPassword):
							print("Loging In . . .")
							time.sleep(1)
							print()


							startEditorShell(con, textArray[2])

						else:
							print("ERROR: You entered an incorrect password.")

		

					elif (textArray[1] == "reviewer"):
						cursor = con.cursor()
						checkIfResigned = ("SELECT REVIEWER.STATUS AS Status FROM REVIEWER WHERE REVIEWER.NUMBER=" + textArray[2] + ";")
						cursor.execute(checkIfResigned)

						resigned = 0
						for (Status,) in cursor:
							if(Status == "Resigned"):
								resigned = 1

						if (resigned==1):
							print("ERROR: Resigned Reviewer. \nYou cannot login since you have resigned. \nPlease contact the system administrator to reactivate your acount.")
							continue

						PASSWORD = "AA12345678" #must reset since it is lost after the first login
						userpass = getpass.getpass(prompt='Please enter your password: ')
						cursor = con.cursor()
						checkPassword = ("SELECT AES_DECRYPT(CREDENTIALS.PASSWORD, '" + PASSWORD + "') AS PASSWORD FROM CREDENTIALS WHERE CREDENTIALS.USER_TYPE='REVIEWER' AND CREDENTIALS.ID=" + textArray[2] + ";")
						cursor.execute(checkPassword)

						decryptedPassword = ""
						for (PASSWORD,) in cursor:
							decryptedPassword = PASSWORD

						cursor.close()
						if(userpass == decryptedPassword):
							print("Loging In . . .")
							time.sleep(2)
							print()

							startReviewerShell(con, textArray[2])
						else:
							print("ERROR: You entered an incorrect password.")

					else:
						print ("ERROR: There is an error in your syntax. Please try again.")

				else:
					print ("ERROR: There is an error in your syntax. Please try again.")
			elif (textArray[0] == "exit"):
				break

			else:
				print ("ERROR: There is an error in your syntax. Please try again.")


		con.close()

	except mysql.connector.Error as e:
		if(e.msg == "Access denied for user 'rajiv'@'10.31.196.1' (using password: YES)"):
			print("ERROR: You entered an incorrect Master Key.")
		else:
			print("SQL Error: {0}".format(e.msg))
			print("ERROR: Incorrect command syntax. \nFor security reasons you have been logged out! \nPlease be sure to follow the READ.ME documentation!")
	except:
		print("Unexpected error: {0}".format(sys.exc_info()[0]))
		print("ERROR: Incorrect command syntax. \nFor security reasons you have been logged out! \nPlease be sure to follow the READ.ME documentation!")

