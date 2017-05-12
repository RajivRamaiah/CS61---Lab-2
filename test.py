"""
  dbexample.java
  Ira Ray Jenkins

  This simple example demonstrates connecting to a MySQL database and 
  executing a sample query.
"""
from __future__ import print_function        # make print a function
import mysql.connector                       # mysql functionality
import sys                                   # for misc errors

SERVER   = "sunapee.cs.dartmouth.edu"        # db server to connect to
USERNAME = "rajiv"                            # user to connect as
PASSWORD = "AA12345678"                            # user's password
DATABASE = "rajiv_db"                              # db to user
QUERY    = "SELECT * FROM REVIEWER;"       # query statement

print("This line will be printed.")
if __name__ == "__main__":

  try:
    # initialize db connection
    con = mysql.connector.connect(host=SERVER,user=USERNAME,password=PASSWORD, database=DATABASE)

    print("Connection established.")

    # initialize a cursor
    cursor = con.cursor()

    # query db
    cursor.execute(QUERY)

    print("Query executed: '{0}'\n\nResults:".format(QUERY))

    # print table header
    print("".join(["{:<12}".format(col) for col in cursor.column_names]))
    print("--------------------------------------------")


    # iterate through results
    for row in cursor:
      print("".join(["{:<12}".format(col) for col in row]))

  except mysql.connector.Error as e:        # catch SQL errors
    print("SQL Error: {0}".format(e.msg))
  except:                                   # anything else
    print("Unexpected error: {0}".format(sys.exc_info()[0]))
   
  # cleanup
  con.close()
  cursor.close()

  print("\nConnection terminated.", end='')

