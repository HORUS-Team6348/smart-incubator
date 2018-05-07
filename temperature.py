import machine
import onewire

_CONVERT = const(0x44)
_RD_SCRATCH = const(0xbe)
_WR_SCRATCH = const(0x4e)

class DS18B20x:
    def __init__(self, pin, rom):
        self.pin = machine.Pin(pin)
        self.ow  = onewire.OneWire(self.pin)
        self.rom = rom
        self.buf = bytearray(9)

        self.set_resolution(12)

    def scan(self):
        return [rom for rom in self.ow.scan() if rom[0] == 0x28]

    def set_resolution(self, resolution):
        self.resolution = resolution
        self.ow.reset(True)
        self.ow.select_rom(self.rom)
        self.ow.writebyte(_WR_SCRATCH)
        self.ow.writebyte(0x00)
        self.ow.writebyte(0x00)
        if resolution == 9:
            self.ow.writebyte(0x1f)
        if resolution == 10:
            self.ow.writebyte(0x3f)
        if resolution == 11:
            self.ow.writebyte(0x5f)
        if resolution == 12:
            self.ow.writebyte(0x7f)

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
        buf = self.read_scratch()
        t = buf[1] << 8 | buf[0]

        if t & 0x8000:  # sign bit set
            t = -((t ^ 0xffff) + 1)

        if self.resolution == 11:
            t = t >> 1
            t = t << 1
        elif self.resolution == 10:
            t = t >> 2
            t = t << 2
        elif self.resolution == 9:
            t = t >> 3
            t = t << 3

        return t / 16

