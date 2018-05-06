import esp
import utime
import picoweb
import machine
import network
from temperature import DS18B20x

ESSID   = "Incubator-1"

peltier_fast    = DS18B20x(12, 11)
peltier_exact   = DS18B20x(13, 12)
incubator_fast  = DS18B20x(14, 11)
incubator_exact = DS18B20x(15, 12)

fast_timer  = machine.Timer(0)
exact_timer = machine.Timer(1)


def nodebug():
    esp.osdebug(None)

def fast_timer_IRQ(timer):
    pass

def exact_timer_IRQ(timer):
    pass


def init():
    print("Initializing WiFi AP...")
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    print("WiFi AP initialized")

    print("Initializing temperature sensors...")
    """peltier_fast.init_read()
    peltier_exact.init_read()
    incubator_fast.init_read()
    incubator_exact.init_read()"""
    print("Temperature sensors initialized")

    print("Waiting for first readings...")
    utime.sleep_ms(750)
    print("Wait over.")

    print("Initializing control loop timers...")
    fast_timer.init(period=380, mode=machine.Timer.PERIODIC, callback=fast_timer_IRQ)
    exact_timer.init(period=755, mode=machine.Timer.PERIODIC, callback=exact_timer_IRQ)
    print("Control loop timers initialized")

init()


while True:
    pass