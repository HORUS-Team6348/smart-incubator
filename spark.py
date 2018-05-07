import machine


class Spark:
    def __init__(self, pin):
        self.pin = machine.Pin(pin)
        self.pwm = machine.PWM(self.pin, freq=50)
        self.set(0)

    @staticmethod
    def map(val):
        """Maps -1 to 1 -> 51 to 103"""
        return int(26 * val + 77)

    def set(self, val):
        self.pwm.duty(self.map(val))