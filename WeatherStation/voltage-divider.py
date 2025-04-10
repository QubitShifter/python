resistances = [33000, 6570, 8200, 891, 1000, 688, 2200, 1410, 3900, 3140, 16000, 14120, 120000, 42120, 64900, 21880]


def voltage_divider(r1, r2, vin):
    volt = (vin * r1) / (r1 + r2)
    return round(volt, 3)


for omh in omhs(len(resistance)):
    print(resistances[omh], voltage_divider(10000, resistances[omh], 3.3))
