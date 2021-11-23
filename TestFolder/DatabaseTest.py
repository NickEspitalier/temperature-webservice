# this file is only used to check the database connection and if the data are returned
import mysql.connector
from mysql.connector import errorcode

try:
    database = mysql.connector.connect(user='root', password='password',
                                       host='127.0.0.1',
                                       database='finalprojectiot')

    my_cursor = database.cursor()

    my_cursor.execute("SELECT * FROM reports")

    results = my_cursor.fetchall()

    for x in results:
        print("Date: {}  Temperature: {}    Humidity: {}".format(x[1], x[2], x[3]))

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    database.close()
