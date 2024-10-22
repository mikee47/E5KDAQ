import usb.core
import struct

def main():
    dev = usb.core.find(idVendor=0x04b4, idProduct=0x8613)
    # print(dev)
    if not dev:
        return

    # dev.set_configuration()
    cfg = dev.get_active_configuration()
    intf = cfg.interfaces()[0]
    ep0 = intf.endpoints()[0]
    ep1 = intf.endpoints()[1]

    try:
        ep1.read(64, timeout=50)
    except usb.core.USBTimeoutError:
        pass

    def send_cmd(cmd: bytes):
        buf = struct.pack('<LH', 0x77553388, len(cmd)) + cmd
        print('>', buf)
        ep0.write(buf.ljust(64, b'\0'))
        buf = bytes(ep1.read(64))
        hdr, rsplen = struct.unpack('<LH', buf[:6])
        rsp = buf[6:6+rsplen]
        while len(rsp) < rsplen:
            buf = bytes(ep1.read(64))
            rsp += buf[:rsplen - len(rsp)]
        print('<', hex(hdr), rsplen, rsp)

    # cmd = b'\x88\x33\x55\x77\x05\x00\x00\x00$00F\r'.ljust(64, b'\0')
    send_cmd(b'$00IM\r')
    send_cmd(b'$00F\r')
    send_cmd(b'$00MISC\r')
    send_cmd(b'$00M\r')
    send_cmd(b'^00MAC\r')
    send_cmd(b'$00P\r')
    send_cmd(b'#00\r')


if __name__ == '__main__':
    main()
