import mysql.connector
from mysql.connector import errorcode

config = dict(user='pi', password='12zxcv', host='127.0.0.1', database='weather', raise_on_warnings=True)

try:
    mysql_connection = mysql.connector(**config)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Authentication failed, check credentials")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    mysql_connection.close()

