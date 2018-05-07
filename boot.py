import esp
import utime
#import picoweb
import machine
import network
from temperature import DS18B20x
from kalman import KalmanFilter
from spark import Spark

ESSID   = "Incubator-1"

#peltier_fast    = DS18B20x(14, )
peltier_exact   = DS18B20x(2, b'(D\x12-\t\x00\x00+')
#incubator_fast  = DS18B20x(16, 11)
#incubator_exact = DS18B20x(17, 12)

peltier_model = KalmanFilter(28, 400)
incubator_model = KalmanFilter(28, 400)

spark_controller = Spark(2)

fast_timer  = machine.Timer(0)
exact_timer = machine.Timer(1)
kalman_timer = machine.Timer(2)


def disable_debug():
    esp.osdebug(None)


def fast_timer_IRQ(timer):
    pass


def exact_timer_IRQ(timer):
    z = peltier_exact.get_reading() + 0.15
    peltier_model.measure(z, 0.0044444)
    print(peltier_model.model.mean, peltier_model.model.variance)
    peltier_exact.begin_reading()


def kalman_timer_IRQ(timer):
    peltier_model.predict(0, 0.5)
    incubator_model.predict(0, 0.15)


def init():
    print("Initializing WiFi AP...")
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    print("WiFi AP initialized")

    print(peltier_exact.scan())

    print("Setting resolutions...")
    peltier_exact.set_resolution(12)
    """peltier_exact.set_resolution(12)
        incubator_fast.set_resolution(11)
        incubator_exact.set_resolution(12)"""
    print("Resolutions set")

    print("Initializing temperature sensors...")
    peltier_exact.begin_reading()
    """peltier_exact.init_read()
    incubator_fast.init_read()
    incubator_exact.init_read()"""
    print("Temperature sensors initialized")

    print("Waiting for first readings...")
    utime.sleep_ms(750)
    print("Wait over.")

    peltier_exact_z = peltier_exact.begin_reading()

    print("Initializing Kalman models...")
    peltier_model = KalmanFilter(peltier_exact_z, 1)
    incubator_model = KalmanFilter(peltier_exact_z, 1)

    print("Initializing control loop timers...")
    fast_timer.init(period=380, mode=machine.Timer.PERIODIC, callback=fast_timer_IRQ)
    exact_timer.init(period=755, mode=machine.Timer.PERIODIC, callback=exact_timer_IRQ)
    kalman_timer.init(period=500, mode=machine.Timer.PERIODIC, callback=kalman_timer_IRQ)
    print("Control loop timers initialized")

init()


while True:
    pass