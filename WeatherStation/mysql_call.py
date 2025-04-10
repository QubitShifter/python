#!/usr/bin/python3
import database
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
import mysql.connector as mariadb

config = {
    'host': 'localhost',
    'user': 'pi',
    'password': '12zxcv',
    'database': 'weather',
    'raise_on_warnings': True
}

db_connection = mariadb.connect(**config)
db_cursor = db_connection.cursor()
sql_select_query = "select count(*) from WEATHER_MEASUREMENT;"
db_cursor.execute(sql_select_query)
mysql_result = db_cursor.fetchall()

print(mysql_result)
db_cursor.close()
db_connection.close()
print("MySQL connection is closed")
