import usb.core
import struct

class E5KDAQ:
    '''Python implementation of InLog E5KDAQ interface.
    Communication method is abstracted to an inherited class.
    '''
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
        buf = struct.pack('<LH', 0x77553388, len(cmd)) + cmd
        print('>', len(cmd), cmd)
        self.ep0.write(buf.ljust(64, b'\0'))
        buf = bytes(self.ep1.read(64))
        hdr, rsplen = struct.unpack('<LH', buf[:6])
        rsp = buf[6:6+rsplen]
        while len(rsp) < rsplen:
            buf = bytes(self.ep1.read(64))
            rsp += buf[:rsplen - len(rsp)]
        print('<', hex(hdr), rsplen, rsp)


def main():
    daq = USBDAQ()
    daq.open()

    # cmd = b'\x88\x33\x55\x77\x05\x00\x00\x00$00F\r'.ljust(64, b'\0')
    daq.send_cmd(b'$00IM\r')
    daq.send_cmd(b'$00F\r')
    daq.send_cmd(b'$00MISC\r')
    daq.send_cmd(b'$00M\r')
    daq.send_cmd(b'^00MAC\r')
    daq.send_cmd(b'$00P\r')
    daq.send_cmd(b'#00\r')
    daq.send_cmd(b'$003\r')
    daq.send_cmd(b'$008C0\r')


if __name__ == '__main__':
    main()
