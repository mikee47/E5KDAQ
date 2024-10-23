import usb.core
import struct
import binascii

PACKET_SIZE = 64

class E5KDAQ:
    '''Python implementation of InLog E5KDAQ interface.
    Communication method is abstracted to an inherited class.
    '''
    def __init__(self, device_id: int):
        self.device_id = device_id

    def flush(self):
        raise NotImplemented()

    def send_request(self, request: bytes) -> bytes:
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

    def send_request(self, request: bytes) -> bytes:
        '''Send a request and return response'''
        MAGIC = 0x77553388
        PACKET_SIZE = 64
        # MAGIC: 88 33 55 77 .3Uw
        buf = struct.pack('<LH', MAGIC, len(request)) + request
        packet_count = (len(buf) + PACKET_SIZE - 1) // PACKET_SIZE
        self.ep0.write(buf.ljust(packet_count * PACKET_SIZE, b'\0'))
        # First response packet contains actual length: use that instead of timeout
        buf = bytes(self.ep1.read(PACKET_SIZE))
        hdr, rsplen = struct.unpack('<LH', buf[:6])
        rsp = buf[6:6+rsplen]
        while len(rsp) < rsplen:
            buf = bytes(self.ep1.read(PACKET_SIZE))
            rsp += buf[:rsplen - len(rsp)]
        return rsp


def main():
    daq = USBDAQ(0)
    daq.open()

    def send_asc_request(request: str):
        print('>', len(request), request)
        response = daq.send_request(request.encode() + b'\r')
        print('<', len(response), response)
        return response

    def send_hex_request(request: bytes):
        print('>', len(request), request)
        response = daq.send_request(request)
        print('<', len(response), response)
        return response

    send_asc_request('$00IM')
    send_asc_request('$00F')
    send_asc_request('$00MISC')
    send_asc_request('$00M')
    send_asc_request('^00MAC')
    # send_request(b'$01P0')
    send_asc_request('$00P')
    send_asc_request('#00')
    send_asc_request('$003')
    send_asc_request('$008C0')
    # daq.send_cmd(b'@010000')
    send_asc_request('$01CRC')
    send_asc_request('@01') # DIO status

    id = 0x01
    addr = 10064
    # Read coil status
    data = struct.pack('>BBHH', id, 0x01, addr, 1)
    send_hex_request(data)

    # Write single coil
    data = struct.pack('>BBHH', id, 0x05, addr, 0x0001)
    send_hex_request(data)

    # get module config
    data = struct.pack('>BBBB', id, 0x46, 0x30, 0)
    rsp = send_hex_request(data)

    print(binascii.hexlify(rsp, ' '))


if __name__ == '__main__':
    main()
