from gpiozero import MCP3008
import time
import math

adc = MCP3008(channel=0)
count = 0
volts = [0.4,1.4,1.2,2.8,2.7,2.9,
         2.2,2.3,2.5,2.6,1.8,2.0,0.7,
         0.8,0.1,0.3,0.2,0.6]

while True:
    wind =round(adc.value*3.3,1)
if not wind in volts:
    print('Unknown value ' + str(wind))
else:
    print('Match ' +str(wind))

def get_average(angles):
    sin_sum = 0.0
    cos_sum = 0.0

for angle in angles:
    r = math.radians(angle)
    sin_sum += math.sin(r)
    cos_sum += math.cos(r)

flen = float(len(angles))
s = sin_sum / flen
c = cos_sum / flen
arc = math.degrees(math.atan(s / c))
average = 0.0

if s > 0 and c > 0:
    average = arc
elif c < 0:
    average = arc + 180
elif s < 0 and c > 0:
    average = arc + 360

def get_value(lenght=5):
    data = []
#print("Measuring wind directionfor %d seconds..." % lenght)
    start_time = time.time()

while time.time() - start_time <= lenght:
    wind =round(adc.value*3.3,1)
if not wind in volts:
    print('unknown value ' + str(wind))
else:
    data.append(volts[wind])

return (get_average(data))
return (0.0 if average == 360 else average)