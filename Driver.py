from __future__ import print_function	# print function
import mysql.connector					# mysql functionality
import sys								# for errors
from Author import *
from Editor import *
from Reviewer import *
import Config
import time
import getpass


if __name__ == "__main__":

	try:
		# initialize db connection
		con = mysql.connector.connect(host=Config.SERVER,user=Config.USERNAME,password=Config.PASSWORD, database=Config.DATABASE)

		loop = True
		FinalPassword = getpass.getpass(prompt='Please Enter The Database Master Key: ')
		print()
		print("Hello. Welcome to the manuscript management system. From here, you can register as an")
		print("editor/author/reviewer or login if you already have an account as one of those users.")
		print()
		print("To register as an author, enter: 'register|author|<fname>|<lname>|<address>|<email>|<affiliation>'")
		print("To register as an editor, enter: 'register|editor|<fname>|<lname>'")
		print("To register as a reviewer, enter: 'register|reviewer|<fname>|<lname>|<affiliation>|<ricode1>|<ricode2>|<ricode3>'")
		print()
		print("To login, simply enter 'login|<usertype>|<userID>'")
		print()

		while loop:
			# print()
			# print("Hello. Welcome to the manuscript management system. From here, you can register as an")
			# print("editor/author/reviewer or login if you already have an account as one of those users.")
			# print()
			# print("To register as an author, enter: 'register|author|<fname>|<lname>|<address>|<email>|<affiliation>'")
			# print("To register as an editor, enter: 'register|editor|<fname>|<lname>'")
			# print("To register as a reviewer, enter: 'register|reviewer|<fname>|<lname>|<affiliation>|<ricode1>|<ricode2>|<ricode3>'")
			# print()
			# print("To login, simply enter 'login|<usertype>|<userID>'")
			# print()

			print()
			print("------------------------------------------------------------------------------------------")
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
						registerAuthor(con, textArray[2], textArray[3], textArray[4], textArray[5], textArray[6], FinalPassword)

				# register|editor|fname|lname
				if (textArray[1] == "editor"):
					print("Registering Editor . . .")
					registerEditor(con, textArray[2], textArray[3], FinalPassword)

				# register|reviewer|fname|lname|email|affiliation|one|two|three
				if (textArray[1] == "reviewer"):
					if (len(textArray) == 7):
						print("Registering Reviewer . . .")
						registerReviewerWithOne(con, textArray[2], textArray[3], textArray[4], textArray[5], textArray[6], FinalPassword)
					elif (len(textArray) == 8):
						print("Registering Reviewer . . .")
						registerReviewerWithTwo(con, textArray[2], textArray[3], textArray[4], textArray[5], textArray[6], textArray[7], FinalPassword)
					elif (len(textArray) == 9):
						print("Registering Reviewer . . .")
						registerReviewerWithThree(con, textArray[2], textArray[3], textArray[4], textArray[5], textArray[6], textArray[7], textArray[8], FinalPassword)
					else:
						print("ERROR: Must register reviewer with 1-3 RI Codes")

			# LOGIN
			elif (textArray[0] == "login"):
				if(len(textArray) == 3):
					if (textArray[1] == "author"):
						PASSWORD = "AA12345678" #must reset since it is lost after the first login
						userpass = getpass.getpass(prompt='Please enter your password: ')
						cursor = con.cursor()
						checkPassword = ("SELECT AES_DECRYPT(CREDENTIALS.PASSWORD, '" + FinalPassword + "') AS PASSWORD FROM CREDENTIALS WHERE CREDENTIALS.USER_TYPE='AUTHOR' AND CREDENTIALS.ID=" + textArray[2] + ";")
						cursor.execute(checkPassword)

						decryptedPassword = ""
						for (PASSWORD,) in cursor:
							decryptedPassword = PASSWORD

						cursor.close()
						if(userpass == decryptedPassword):
							print("Loging In . . .")
							time.sleep(0.5)
							print("------------------------------------------------------------------------------------------")

							startAuthorShell(con, textArray[2])
						else:
							print("ERROR: You entered an incorrect password.")

					elif (textArray[1] == "editor"):

						PASSWORD = "AA12345678" #must reset since it is lost after the first login
						userpass = getpass.getpass(prompt='Please enter your password: ')
						cursor = con.cursor()
						checkPassword = ("SELECT AES_DECRYPT(CREDENTIALS.PASSWORD, '" + FinalPassword + "') AS PASSWORD FROM CREDENTIALS WHERE CREDENTIALS.USER_TYPE='EDITOR' AND CREDENTIALS.ID=" + textArray[2] + ";")
						cursor.execute(checkPassword)

						decryptedPassword = ""
						for (PASSWORD,) in cursor:
							decryptedPassword = PASSWORD

						cursor.close()
						if(userpass == decryptedPassword):
							print("Loging In . . .")
							time.sleep(0.5)
							print("------------------------------------------------------------------------------------------")


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

						userpass = getpass.getpass(prompt='Please enter your password: ')
						cursor = con.cursor()
						checkPassword = ("SELECT AES_DECRYPT(CREDENTIALS.PASSWORD, '" + FinalPassword + "') AS PASSWORD FROM CREDENTIALS WHERE CREDENTIALS.USER_TYPE='REVIEWER' AND CREDENTIALS.ID=" + textArray[2] + ";")
						cursor.execute(checkPassword)

						decryptedPassword = ""
						for (PASSWORD,) in cursor:
							decryptedPassword = PASSWORD

						cursor.close()
						if(userpass == decryptedPassword):
							print("Loging In . . .")
							time.sleep(0.5)
							print("------------------------------------------------------------------------------------------")

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

