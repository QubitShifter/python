import pymysql.cursors
import bme280_sensor
import ds18b20_therm
import wind_direction
import interrupt_client
import time
import math
import statistics
from gpiozero import Button

from weather_station_BYO import ground_temp

pressure = bme280_sensor.read_all()
temp_probe = ds18b20_therm.DS18B20()
air_qual = 17.6
#air_qual = tgs2600.TGS2600(adc_channel = 0)
humidity = bme280_sensor.read_all()
wind_dir = 0
wind_dir = wind_direction.wind_direction(adc_channel = 0, config_file="wind_direction.json")
interrupts = interrupt_client.interrupt_client(port = 49501)
wind = 17
gust = 4
rain = 0
temp = 20

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
        cursor.execute(sql, (ambient_temp, ground_temp, '20.6',
                             pressure, humidity, wind_average, wind_speed, wind_gust, rainfall))

    connection.commit()

    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM `WEATHER_MEASUREMENT`"
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)
finally:
    connection.close()
