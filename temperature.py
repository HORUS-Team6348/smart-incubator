import machine
import onewire

_CONVERT = const(0x44)
_RD_SCRATCH = const(0xbe)
_WR_SCRATCH = const(0x4e)

class DS18B20x:
    def __init__(self, pin, resolution=12, rom="plch"):
        self.pin = machine.Pin(pin)
        self.ow  = onewire.OneWire(self.pin)
        self.rom = rom

        if resolution == 12:
            return
        elif resolution in [9, 10, 11]:
            self.set_resolution(resolution)
        else:
            raise Exception('Invalid resolution - must be 9, 10, 11 or 12 bits')

    def scan(self):
        return [rom for rom in self.ow.scan() if rom[0] == 0x10 or rom[0] == 0x28]

    def set_resolution(self, resolution):
        self.ow.reset(True)
        self.ow.select_rom(self.rom)
        self.ow.writebyte(_WR_SCRATCH)
        self.ow.write(0x00)
        self.ow.write(0x00)
        if resolution == 9:
            self.ow.write(0x1f)
        if resolution == 10:
            self.ow.write(0x3f)
        if resolution == 11:
            self.ow.write(0x5f)

    def begin_reading(self):
        self.ow.reset(True)
        self.ow.writebyte(self.ow.SKIP_ROM)
        self.ow.writebyte(_CONVERT)

    def read_scratch(self):
        self.ow.reset(True)
        self.ow.select_rom(self.rom)
        self.ow.writebyte(_RD_SCRATCH)
        self.ow.readinto(self.buf)
        if self.ow.crc8(self.buf):
            raise Exception('CRC error')
        return self.buf

    def write_scratch(self, buf):
        self.ow.reset(True)
        self.ow.select_rom(self.rom)
        self.ow.writebyte(_WR_SCRATCH)
        self.ow.write(buf)

    def get_reading(self):
        #TODO: Adapt for lower resolution readings
        buf = self.read_scratch(self.rom)
        if self.rom[0] == 0x10:
            if buf[1]:
                t = buf[0] >> 1 | 0x80
                t = -((~t + 1) & 0xff)
            else:
                t = buf[0] >> 1
            return t - 0.25 + (buf[7] - buf[6]) / buf[7]
        else:
            t = buf[1] << 8 | buf[0]
            if t & 0x8000:  # sign bit set
                t = -((t ^ 0xffff) + 1)
            return t / 16

