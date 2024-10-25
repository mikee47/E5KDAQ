import usb.core
import struct
from binascii import hexlify
from dataclasses import dataclass

PACKET_SIZE = 64

IpAddress = bytes
MacAddress = bytes

def int_to_temp(value: int, scale: float = 1370.0):
    '''Obtain temperature values'''
    if isinstance(value, list):
        return [int_to_temp(x) for x in value]
    return round(value * scale / 32767, 1)


@dataclass
class ModuleConfig:
    mac: MacAddress
    mask: IpAddress
    ip: IpAddress
    gw: IpAddress
    id: int
    module_name: str
    module_desc: str
    event_sip: list[IpAddress]
    event_trigger: list[bool]
    stream_sip: list[IpAddress]
    stream_active: list[bool]
    stream_time_interval: int
    baudrate: int
    misc_options: int
    options: int
    version: str

    FORMAT = '<6s4s4s4s1B8s32s4s4s4s4s4?4s4s4s4s4?xLBxHH16s'

    def __init__(self, data: bytes):
        values = struct.unpack(self.FORMAT, data)
        self.mac = values[0]
        self.mask = values[1]
        self.ip = values[2]
        self.gw = values[3]
        self.id = values[4]
        self.module_name = values[5].decode().rstrip('\0')
        self.module_desc = values[6].decode().rstrip('\0')
        self.event_sip = values[7:11]
        self.event_trigger = values[11:15]
        self.stream_sip = values[15:19]
        self.stream_active = values[19:23]
        self.stream_time_interval = values[23]
        self.baudrate = values[24]
        self.misc_options = values[25]
        self.options = values[26]
        self.version = values[27]


@dataclass
class ModuleData:
    d_in: int
    d_out: int
    di_latch: int
    di_counter: list[int]
    ai_normal_value: list[float]
    ai_max_value: list[float]
    ai_min_value: list[float]
    ai_high_alarm_status: int
    ai_low_alarm_status: int
    ai_burnout: int
    cjc_temperature: float
    ao_value: list[float]

    def __init__(self, data: bytes):
        # values = struct.unpack(self.FORMAT, data)

        values = struct.unpack('>x3L32L16h16h16h4H16h', data)
        self.d_in = values[0]
        self.d_out = values[1]
        self.di_latch = values[2]
        self.di_counter = values[3:35]
        self.ai_normal_value = [int_to_temp(x) for x in values[35:51]]
        self.ai_max_value = [int_to_temp(x) for x in values[51:67]]
        self.ai_min_value = [int_to_temp(x) for x in values[67:83]]
        self.ai_high_alarm_status = values[83]
        self.ai_low_alarm_status = values[84]
        self.ai_burnout = values[85]
        self.cjc_temperature = values[86] / 10
        # TODO: AO values require different scale
        self.ao_value = [int_to_temp(x) for x in values[87:102]]


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

    def send_asc_request(request: str, comment: str):
        print(comment)
        print('>', len(request), request)
        response = daq.send_request(request.encode() + b'\r')
        print('<', len(response), response)
        return response

    def send_hex_request(request: bytes, comment: str):
        print(comment)
        print('>', len(request), request)
        response = daq.send_request(request)
        print('<', len(response), response)
        return response

    send_asc_request('$00IM', 'Undocumented')
    send_asc_request('$00F', 'Read firmware version')
    send_asc_request('$00MISC', 'Undocumented')
    send_asc_request('$00M', 'Read module name')
    send_asc_request('^00MAC', 'Read MAC Address')
    # send_request(b'$01P0')
    send_asc_request('$00P', 'Read communication protocol')
    send_asc_request('#00', 'Read all analogue inputs')
    send_asc_request('$003', 'Read CJC temperature')
    send_asc_request('$008C0', 'Read single A/D channel range')

    # daq.send_cmd(b'@010000')
    send_asc_request('$01CRC', 'Read CRC status')
    send_asc_request('@01', 'Read DIO status')

    send_asc_request('$01SW', 'Read web server status')
    send_asc_request('$01DHCP', 'Read DHCP status')
    send_asc_request('$01IP', 'Read IP address')
    send_asc_request('$01GATE', 'Read gateway address')
    send_asc_request('$01MASK', 'Read network mask')


    if False:
        ip = [192, 168, 1, 11]
        gw = [192, 168, 1, 1]
        mask = [255, 255, 255, 0]
        def hex_str(x: list[int]):
            return hexlify(bytes(x)).decode().upper()
        send_asc_request('$01IP' + hex_str(ip), 'Set IP')
        send_asc_request('$01GATE' + hex_str(gw), 'Set GW')
        send_asc_request('$01MASK' + hex_str(mask), 'Set Mask')

    id = 0x01
    addr = 10064
    # Read coil status
    data = struct.pack('>BBHH', id, 0x01, addr, 1)
    send_hex_request(data, 'Read coil status')

    # Write single coil
    data = struct.pack('>BBHH', id, 0x05, addr, 0x0001)
    send_hex_request(data, 'Write single coil')

    # get module config
    data = struct.pack('>BBBB', id, 0x46, 0x30, 0)
    rsp = send_hex_request(data, 'Get module config')
    config = ModuleConfig(rsp[3:])
    print(config)
    print(f'{config.misc_options=:x}, {config.options=:x}')

    # ModuleConfigX
    rsp = send_asc_request('%01GETFIXADDR', 'ModuleConfigX')

    # E5K_ReadAllDataFromModule
    data = struct.pack('>BBBB', id, 0x46, 0x40, 0)
    rsp = send_hex_request(data, 'E5K_ReadAllDataFromModule')
    module_data = ModuleData(rsp[3:])
    print(module_data)

    # get channel types
    data = struct.pack('>BBBB', id, 0x46, 0x41, 0)
    rsp = send_hex_request(data, 'Get channel types')
    print(hexlify(rsp, ' '))

    # Read channels burnout status
    send_asc_request('$01B', 'Read channels burnout status')

    # E5K_ReadAIChannelConfig
    send_asc_request('$01G00', 'Read AI channel config')

    if False:
        # E5K_ReadAICalibrationCoefficient
        send_asc_request('~01CALZ', 'E5K_ReadAICalibrationCoefficient')
        # < 12 b'!01001C0122\r'
        # => 0x001C0122

        send_asc_request('~01CALS', 'E5K_ReadAICalibrationCoefficient')
        # < 12 b'!010054878E\r'
        # => 0x0054878E

        # E5K_CalibrateAIZeroSpan        (MODULE_ID  id,USHORT Calchno,CHAR Adtype)
        send_asc_request('$01CAL01', 'E5K_CalibrateAIZeroSpan')



if __name__ == '__main__':
    main()
