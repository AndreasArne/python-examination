"""
Script for converting from European to Americano
"""

def mToF(meters):
    """
    function, converts from Meter to Feet
    """
    return float(meters)*3.28084

def kmToMp(kms):
    """
    function, converts from km/h to mp/h
    """
    return float(kms)*0.62137

def cToF(cs):
    """
    function, converts from celcius to farenheit
    """
    return float(cs)*9/5+32

print("Convert values")
meter = input("Enter meters above sea level to convert to feet: ")
km = input("Enter plane speed in km/h to convert to miles/h: ")
celcius = input("Enter temperature outside of plane in celcius to convert to farenheit: ")

print(meter + " meters is the same as " + str(round(mToF(meter), 2)) + " feet")
print(km + " kilometers/h is the same as " + str(round(kmToMp(km), 2)) + " miles/h")
print(celcius + " celcius is the same as " + str(round(cToF(celcius), 2)) + " farenheit")
