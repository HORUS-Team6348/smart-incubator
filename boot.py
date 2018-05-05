import esp
import picoweb
import machine
import network
from temperature import DS18B20x

ESSID   = "Incubator-1"

incubator_temperature = DS18B20x(12)
peltier_temperature   = DS18B20x(13)

timer = machine.Timer(0)

counter = 0


def nodebug():
    esp.osdebug(None)


def timerIRQ():
    global counter
    counter += 1
    print("IRQ here!")
    print(counter)


def init():
    ap = network.WLAN(network.AP_IF)
    ap.active(True) 

    timer.init(period=380, mode=machine.Timer.PERIODIC, callback=timerIRQ)


init()