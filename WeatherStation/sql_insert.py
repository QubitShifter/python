import pymysql.cursors
connection = pymysql.connect(host='localhost',
                             user='pi',
                             password='12zxcv',
                             db='',
                             cursorclass=pymysql.cursors.DictCursor
                             )


try:
    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO 'WEATHER_MEASUREMENT_TEST' ('AIR_QUALITY_PM_25', 'AIR_QUALITY_PM_10') VALUES (%s, %s)"
        cursor.execute(sql, ('12.6', '23.5'))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT 'AIR_QUALITY_PM_25', 'AIR_QUALITY_PM_25' FROM 'weather'"
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)
finally:
    connection.close()
