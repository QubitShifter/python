pip import pymysql.cursors
import math
from gpiozero import Button
import bme280_sensor
import wind_direction_byo
import wind
import ds18b20_therm
import time
import statistics

from rainfall import BUCKET_SIZE

store_speeds = []
store_directions = []
wind_speed_sensor = Button(5)
wind_count = 0
radius_cm = 9.5
wind_interval = 5
wind_count = 20
ADJUSTMENTS = 1.18
CM_IN_A_KM = 100000.0
SECS_IN_AN_HOUR = 3600
BUCKET_SIZE = 0.2794
interval = 1
gust = 0


def spin():
    global wind_count
    wind_count = wind_count + 1
    print("spin" + str(wind_count))


def calculate_speed(time_sec):
    global wind_count
    global gust
    circumference_cm = (2 * math.pi) * radius_cm
    rotations = wind_count / 2.0
    dist_km = (circumference_cm * rotations) / CM_IN_A_KM
    km_per_sec = dist_km / time_sec
    km_per_hour = km_per_sec * SECS_IN_AN_HOUR
    dist_cm = circumference_cm * rotations
    final_speed = km_per_hour * ADJUSTMENTS
    return final_speed
    # speed = dist_cm / wind_interval
    # return km_per_hour * ADJUSTMENTS


def bucket_tipped():
    global rain_count
    rain_count = rain_count + 1
    return rain_count


def reset_rainfall():
    global rain_count
    rain_count = 0


def reset_wind():
    global wind_count
    wind_count = 0


def reset_gust():
    global gust
    gist = 0


rain_sensor = Button(6)
rain_sensor.when_pressed = bucket_tipped()
wind_speed_sensor = Button(5)
wind_speed_sensor.when_activated = spin
temp_probe = ds18b20_therm.DS18B20()
connection = pymysql.connect(host='localhost',
                             user='pi',
                             password='098ASDH65CNH12zxcv',
                             db='weather',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor
                             )
while True:
    print('Start')
    start_time = time.time()
    while time.time() - start_time <= wind_interval:
        print('Start2')
        wind_start_time = time.time()
        reset_wind()
        while time.time() - wind_start_time <= wind_interval:
            store_directions.append(wind_direction_byo.get_value())

        final_speed = calculate_speed(wind_interval)
        store_speeds.append(final_speed)
    wind_average = wind_direction_byo.get_average(store_directions)
    wind_gust = max(store_speeds)
    wind_speed = wind.statistics.mean(store_speeds)
    rainfall = rain_count * BUCKET_SIZE
    reset_rainfall()
    store_speeds = []
    store_directions = []
    obj = ds18b20_therm.read_temp()
    ground_temp = ds18b20_therm.read_temp()
    humidity, pressure, ambient_temp = bme280_sensor.read_all()
    print(wind_speed, wind_gust, rainfall, wind_average,  ground_temp, humidity, pressure, ambient_temp)
try:
    with connection.cursor() as cursor:
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
        cursor.execute(sql, (ambient_temp, ground_temp, '12.6', '22.8',
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
