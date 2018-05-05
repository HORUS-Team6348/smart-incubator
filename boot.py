import esp
import network
from temperature import DS18B20x

ESSID   = "Incubator-1"
IP      = "192.168.0.1"
SUBNET  = "255.255.255.0"
GATEWAY = "192.168.0.1"
DNS     = "8.8.8.8"


incubator_temperature = DS18B20x(12)
peltier_temperature   = DS18B20x(13)


def nodebug():
    esp.osdebug(None)


def init():
    ap = network.WLAN(network.STA_IF)
    ap.active(True)
    ap.config(essid=ESSID)

    incubator_temperature.init()
    peltier_temperature.init()


init()