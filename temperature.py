import machine
import onewire

_CONVERT = const(0x44)
_RD_SCRATCH = const(0xbe)
_WR_SCRATCH = const(0x4e)

class DS18B20x:
    def __init__(self, pin, resolution):
       self.pin = machine.Pin(pin)
       self.ow  = onewire.OneWire(self.pin)

        if resolution == 12:
            return

        self.ds.reset()
        self.ds.select()
        self.ds.write(0x4E)
        self.ds.write(0x00)
        self.ds.write(0x00)
        if resolution == 9:
            self.ds.write(0x1f)
        if resolution == 10:
            self.ds.write(0x3f)
        if resolution == 11:
            self.ds.write(0x5f)

       def scan(self):
           return [rom for rom in self.ow.scan() if rom[0] == 0x10 or rom[0] == 0x28]

       def convert_temp(self):
           self.ow.reset(True)
           self.ow.writebyte(self.ow.SKIP_ROM)
           self.ow.writebyte(_CONVERT)

       def read_scratch(self, rom):
           self.ow.reset(True)
           self.ow.select_rom(rom)
           self.ow.writebyte(_RD_SCRATCH)
           self.ow.readinto(self.buf)
           if self.ow.crc8(self.buf):
               raise Exception('CRC error')
           return self.buf

       def write_scratch(self, rom, buf):
           self.ow.reset(True)
           self.ow.select_rom(rom)
           self.ow.writebyte(_WR_SCRATCH)
           self.ow.write(buf)

       def read_temp(self, rom):
           buf = self.read_scratch(rom)
           if rom[0] == 0x10:
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

    def init_read(self, ds):
        ds.convert_temp()

    def read (self, ds, rom):
        ds.read_temp(rom)
