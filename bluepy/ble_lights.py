#!/usr/python
from bluepy import btle
from bluepy.btle import Scanner, DefaultDelegate
from struct import *

ble_light1 = "20:c3:8f:8d:c2:c0"
ble_light2 = "20:c3:8f:8d:8c:9e"

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print "Discovered device", dev.addr
        elif isNewData:
            print "Received new data from", dev.addr

def scanForLights():
    result = 0; # 0=no lights, 1= light 1, 2= light 2, 3= both lights
    scanner = Scanner().withDelegate(ScanDelegate())
    devices = scanner.scan(3.0)
    for dev in devices:
        if dev.addr == ble_light1:
            print("Found Light 1")
            result = result | 0x01

        if dev.addr == ble_light2:
            print("Found Light 2")
            result = result | 0x02
    #     print "Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi)
    #     for (adtype, desc, value) in dev.getScanData():
    #         print "  %s = %s" % (desc, value)
    return result
    
def checkLights():
    p1 = btle.Peripheral(ble_light1)
    p2 = btle.Peripheral(ble_light2)
    
    v = pack("I", 0x00000000)
    
    svc = p1.getServiceByUUID("0000ffb0-0000-1000-8000-00805f9b34fb")
    h = svc.getCharacteristics()[4]
    p1.writeCharacteristic(h.valHandle, v, withResponse=True)
    p1.disconnect()
    
    svc = p2.getServiceByUUID("0000ffb0-0000-1000-8000-00805f9b34fb")
    h = svc.getCharacteristics()[4]
    p2.writeCharacteristic(h.valHandle, v, withResponse=True)
    p2.disconnect()

def writeLight(id, v):
    if id == 1:
        p = btle.Peripheral(ble_light1)
    elif id == 2:
        p = btle.Peripheral(ble_light2)
    
    svc = p.getServiceByUUID("0000ffb0-0000-1000-8000-00805f9b34fb")
    h = svc.getCharacteristics()[4]
    p.writeCharacteristic(h.valHandle, v, withResponse=True)
    p.disconnect()

def main():
    v = pack("I", 0x00000000)
    result = scanForLights()
    
    if result == 0:
        print("No light found")
    elif result == 1:
        writeLight(1, v)
    elif result == 2:
        writeLight(2, v)
    elif result == 3:
        writeLight(1, v)
        writeLight(2, v)

if __name__ == "__main__":
    main()