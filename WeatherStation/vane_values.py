resistances = [33000, 6570, 8200, 891,
               1000, 688, 2200, 1410,
               3900, 3140, 16000, 14120,
               120000, 42120, 64900, 21880]


def voltage_divider(r1, r2, vin):
    volt = (vin * r1) / (r1 + r2)
    return round(volt, 3)


for x in range(len(resistances)):
    print(resistances[x], voltage_divider(10000, resistances[x], 3.3))


resistances = [33000, 33200, 32400, 34000, 9400, 8800, 8850, 8830, 8850, 8870,
               1000, 900, 1050, 2000, 2200, 2250, 2230, 3000, 3700, 3900, 3700, 4600, 6500, 7800, 15900,
               15800, 16000, 16100, 16500, 113400, 113800, 115000,  117200, 121000, 121500, 124000, 124500,
               115500, 115000, 41000, 42800, 43000, 43500, 43000, 66000, 66500, 21000, 215000]


def voltage_divider(r1, r2, vin):
    volt = (vin * r1) / (r1 + r2)
    return round(volt, 3)


for x in range(len(resistances)):
    print(resistances[x], voltage_divider(10000, resistances[x], 3.3))
