import machine
import onewire

class Sensor:

    def __init__(self, pin, resolution):
        self.dat = machine.Pin(pin)
        self.ds  = onewire.DS18B20(onewire.OneWire(self.dat))

        self.ds.reset()
        self.ds.select(addr)
        self.ds.write(0x4E)
        self.ds.write(0x00)
        self.ds.write(0x00)
        if resolution == "9":
            self.ds.write(0x1f)
        if resolution == "10":
            self.ds.write(0x3f)
        if resolution == "11":
            self.ds.write(0x5f)


    def init_read(self, ds):
        ds.convert_temp()

    def read (self, ds, rom):
        ds.read_temp(rom)












