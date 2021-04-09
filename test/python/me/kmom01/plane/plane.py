"""
Script for converting from European to Americano
"""

def mToF(meters):
    """
    function, converts from Meter to Feet
    """
    return round(float(meters)*3.28084, 2)

def kmToMp(kms):
    """
    function, converts from km/h to mp/h
    """
    return round(float(kms)*0.62137, 2)

def cToF(cs):
    """
    function, converts from celcius to farenheit
    """
    return round(float(cs)*9/5+32, 2)

print("Convert values")
meter = input("Enter meters above sea level to convert to feet: ")
km = input("Enter plane speed in km/h to convert to miles/h: ")
celcius = input("Enter temperature outside of plane in celcius to convert to farenheit: ")

print(meter + " meters is the same as " + str(mToF(meter)) + " feet")
print(km + " kilometers/h is the same as " + str(kmToMp(km)) + " miles/h")
print(celcius + " celcius is the same as " + str(cToF(celcius)) + " farenheit")
