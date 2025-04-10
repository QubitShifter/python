import pymysql.cursors
connection = pymysql.connect(host='localhost',
                             user='pi',
                             password='12zxcv',
                             db='weather',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor
                             )



try:
    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `WEATHER_MEASUREMENT` (`AMBIENT_TEMPERATURE`, " \
              "                                    `GROUND_TEMPERATURE`, " \
              "                                     `AIR_QUALITY_PM_25`, " \
              "                                     `AIR_QUALITY_PM_10`, " \
              "                                     `AIR_QUALITY`, " \
              "                                     `AIR_PRESSURE`, " \
              "                                     `HUMIDITY`, " \
              "                                     `WIND_DIRECTION`, " \
              "                                     `WIND_SPEED`, " \
              "                                     `WIND_GUST_SPEED`, " \
              "                                     `RAINFALL`  ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, ('37.5', '37.9', '11.11', '33.33', '55.55', '223.7', '88.0', '246.2', '45.6', '24', '33.2'))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

    with connection.cursor() as cursor:
        # Read a single record
        sql = "select * from WEATHER_MEASUREMENT"
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)
finally:
    connection.close()
