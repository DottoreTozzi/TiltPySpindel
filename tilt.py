#!/usr/bin/env python2.7
#
# Version 0.1
# This script detects BT LE beacons of TILT Hydrometers nearby.
# The data is being collected, averaged, converted to an iSpindle like JSON and then forwarded to iSpindle.py.
# See README for details.
#
# This is originally based on work by brewdevil:
# https://www.instructables.com/id/Reading-a-Tilt-Hydrometer-With-a-Raspberry-Pi/
#


from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from decimal import Decimal
import blescan
import sys
import datetime
import time
import bluetooth._bluetooth as bluez
import json


# Configuration done in here for now
DEBUG = 0 # Debug mode
METRIC = 1 # Use metric units (%w/w, Celsius instead of SG and F)
RASPYSPINDLESRV = '127.0.0.1'
RASPYSPINDLEPORT = 9501
INTERVAL = 300
# The default device for bluetooth scan. If you're using a bluetooth dongle you may have to change this.
dev_id = 0
# don't edit below here

# TCP iSpindle.py:
ACK = chr(6)  # ASCII ACK (Acknowledge)
NAK = chr(21)  # ASCII NAK (Not Acknowledged)
BUFF = 256  # Buffer Size

# Assign uuid's of various colour tilt hydrometers. BLE devices like the tilt work primarily using advertisements.
# The first section of any advertisement is the universally unique identifier. Tilt uses a particular identifier based on the colour of the device
red = 'a495bb10c5b14b44b5121370f02d74de'
green = 'a495bb20c5b14b44b5121370f02d74de'
black = 'a495bb30c5b14b44b5121370f02d74de'
purple = 'a495bb40c5b14b44b5121370f02d74de'
orange = 'a495bb50c5b14b44b5121370f02d74de'
blue = 'a495bb60c5b14b44b5121370f02d74de'
yellow = 'a495bb70c5b14b44b5121370f02d74de'
pink = 'a495bb80c5b14b44b5121370f02d74de'


# return average of a list
def Average(lst):
    if len(lst) == 0:
        return 0
    else:
        return round(Decimal(sum(lst) / len(lst)), 3)

# scan BLE advertisements until we see one matching our tilt uuid
def getdata():
    try:
        sock = bluez.hci_open_dev(dev_id)

    except:
        print "error accessing bluetooth device..."
        sys.exit(1)

    blescan.hci_le_set_scan_parameters(sock)
    blescan.hci_enable_le_scan(sock)
    data = []
    gotData = 0

    while (gotData == 0):
        returnedList = blescan.parse_events(sock, 10)
        for beacon in returnedList:  # returnedList is a list datatype of string datatypes seperated by commas (,)
            gotDataCount = gotData
            output = beacon.split(',')  # split the list into individual strings in an array
            if output[1] == red:
                tiltColour = 'Red'
                tiltBeer = 'Test'
                tiltId = 1
                gotData += 1
            if output[1] == green:
                tiltColour = 'Green'
                tiltBeer = 'Test'
                tiltId = 2
                gotData += 1
            if output[1] == black:
                tiltColour = 'Black'
                tiltBeer = 'Test'
                tiltId = 3
                gotData += 1
            if output[1] == purple:
                tiltColour = 'Purple'
                tiltBeer = 'Test'
                tiltId = 4
                gotData += 1
            if output[1] == orange:
                tiltColour = 'Orange'
                tiltBeer = 'Test'
                tiltId = 5
                gotData += 1
            if output[1] == blue:
                tiltColour = 'Blue'
                tiltBeer = 'Test'
                tiltId = 6
                gotData += 1
            if output[1] == yellow:
                tiltColour = 'Yellow'
                tiltBeer = 'Test'
                tiltId = 7
                gotData += 1
            if output[1] == pink:
                tiltColour = 'Pink'
                tiltBeer = 'Test'
                tiltId = 8
                gotData += 1
            if gotData > gotDataCount:
                tempF = float(output[2])  # convert the string for the temperature to a float type
                tempC = (tempF - 32) / 1.8
                intGravSG = int(output[3])
                gravSG = float(intGravSG) / 1000
                gravP = (-1 * 616.868) + (1111.14 * gravSG) - (630.272 * gravSG ** 2) + (135.997 * gravSG ** 3)
                if METRIC == 1:
                    tiltGrav = gravP
                    tiltTemp = tempC
                else:
                    tiltGrav = gravSG
                    tiltTemp = tempF
                # tiltTXPower = int(output[4]) # not needed
                tiltRSSI = int(output[5])
                # check if readings are within reasonable range (avoid spike artefacts)
                if (intGravSG >= 985) and (intGravSG <= 1125):
                  newdata = {
                      'ID': tiltId,
                      'name': 'Tilt ' + tiltColour,
                      #'angle': ((gravSG - 0.99) * 1000) / 1.6, # rough estimate
                      'angle': 25 + (gravP * 1.6),
                      'temperature': tiltTemp,
                      'battery': 4.0,
                      'gravity': tiltGrav,
                      'interval': INTERVAL,
                      'rssi': tiltRSSI,
                      'token': '* ' + tiltBeer
                  }
                  data.append(newdata)

    blescan.hci_disable_le_scan(sock)
    return data

def dbgprint(s):
    if DEBUG: print(str(s))

def main():
    updateSecs = INTERVAL  # time in seconds between sending data
    firstUpdate = 60  # time in seconds until the very first update

    timestamp = time.time()  # Get current time for beginning of loop
    updateTime = timestamp + firstUpdate  # Set the time for the next update

    devices = []

    while True:
        data = getdata()
        if len(devices) < len(data):
            # if new tilt comes into play, immediately reset
            devices = []
            for item in data:
                dev = {
                    'id': item['ID'],
                    'name': item['name'],
                    'angle': [],
                    'temperature': [],
                    'gravity': [],
                    'battery': item['battery'],
                    'interval': item['interval'],
                    'rssi': item['rssi'],
                    'token': item['token']
                }
                devices.append(dev)
        # we now have everything we need in order to gather (and later average) the actual readings
        # i.e. we should have all the tilt hydrometers registered now with lists for the readings.
        # so let' store these now
        for item in data:
            for dev in devices:
                if dev['id'] == item['ID']:
                    dev['angle'].append(item['angle'])
                    dev['temperature'].append(item['temperature'])
                    dev['gravity'].append(item['gravity'])

        # Data is ready!


        if time.time() > updateTime:  # if we've reached the update time then send the data
            updateTime = updateTime + updateSecs # first reset the timer
            # prepare the data to be sent
            for dev in devices:
                #print dev
                #print len(dev['gravity'])
                outdata = {
                    'ID': dev['id'],
                    'name': dev['name'],
                    'angle': Average(dev['angle']),
                    'temperature': Average(dev['temperature']),
                    'gravity': Average(dev['gravity']),
                    'battery': dev['battery'],
                    'interval': dev['interval'],
                    'RSSI': dev['rssi'],
                    'token': dev['token']
                }
                dbgprint(outdata)
                out = json.dumps(outdata)
                # Now send to iSpindle server via generic TCP socket, 1 device each
                s = socket(AF_INET, SOCK_STREAM)
                s.connect((RASPYSPINDLESRV, RASPYSPINDLEPORT))
                s.send(out)
                rcv = s.recv(BUFF)
                if rcv[0] == ACK:
                    dbgprint(' - received ACK - OK!')
                elif rcv[0] == NAK:
                    dbgprint(' - received NAK - Not OK...')
                else:
                    dbgprint(' - received: ' + rcv)

                s.close()
                # and let's not be hectic
                time.sleep(1)
            devices = []


if __name__ == "__main__":  # dont run this as a module
    main()

