import usb.core
import struct

class E5KDAQ:
    '''Python implementation of InLog E5KDAQ interface.
    Communication method is abstracted to an inherited class.
    '''
    def __init__(self, device_id: int):
        self.device_id = device_id

    def flush(self):
        raise NotImplemented()

    def send_cmd(self, cmd: bytes):
        raise NotImplemented()


class USBDAQ(E5KDAQ):
    def open(self):
        self.dev = usb.core.find(idVendor=0x04b4, idProduct=0x8613)
        # print(dev)
        assert self.dev
        # dev.set_configuration()
        cfg = self.dev.get_active_configuration()
        intf = cfg.interfaces()[0]
        self.ep0, self.ep1 = intf.endpoints()[0:2]
        self.flush

    def flush(self):
        try:
            while True:
                self.ep1.read(64, timeout=50)
        except usb.core.USBTimeoutError:
            pass

    def send_cmd(self, cmd: bytes):
        cmd += b'\r'
        # MAGIC: 88 33 55 77 .3Uw
        buf = struct.pack('<LH', 0x77553388, len(cmd)) + cmd
        print('>', len(cmd), cmd)
        block_count = (len(buf) + 63) // 64
        self.ep0.write(buf.ljust(block_count * 64, b'\0'))
        buf = bytes(self.ep1.read(64))
        hdr, rsplen = struct.unpack('<LH', buf[:6])
        rsp = buf[6:6+rsplen]
        while len(rsp) < rsplen:
            buf = bytes(self.ep1.read(64))
            rsp += buf[:rsplen - len(rsp)]
        print('<', hex(hdr), rsplen, rsp)


def main():
    daq = USBDAQ(0)
    daq.open()

    daq.send_cmd(b'$00IM')
    daq.send_cmd(b'$00F')
    daq.send_cmd(b'$00MISC')
    daq.send_cmd(b'$00M')
    daq.send_cmd(b'^00MAC')
    daq.send_cmd(b'$00P')
    daq.send_cmd(b'#00')
    daq.send_cmd(b'$003')
    daq.send_cmd(b'$008C0')
    # daq.send_cmd(b'@010000')
    daq.send_cmd(b'$01CRC')
    daq.send_cmd(b'@01') # DIO status

    id = 0x01
    addr = 10064
    # Read coil status
    data = struct.pack('>BBHH', id, 0x01, addr, 1)
    daq.send_cmd(data)

    # Write single coil
    data = struct.pack('>BBHH', id, 0x05, addr, 0x0001)
    daq.send_cmd(data)


if __name__ == '__main__':
    main()
