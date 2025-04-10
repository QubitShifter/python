import pymysql
conn = pymysql.Connect(host='localhost', user='pi', passwd='12zxcv', db='weather')
cur = conn.cursor()
cur.execute("select count(*) from WEATHER_MEASUREMENT;")
for r in cur:
    print(r)
cur.close()
conn.close()