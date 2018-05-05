class Sensor_init:
    def __init__(self, pin):
        import machine
        import onewire
        self.dat = machine.Pin(pin)
        self.ds  = onewire.DS18B20(onewire.OneWire(self.dat))
        return self.ds





