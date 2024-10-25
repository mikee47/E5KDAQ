import usb.core
import struct
from enum import IntEnum
from dataclasses import dataclass
from collections.abc import Sequence

PACKET_SIZE = 64

IpAddress = bytes
MacAddress = bytes

class ModbusFunction(IntEnum):
	ReadCoils = 0x01                                                                                                
	ReadDiscreteInputs = 0x02                                                                                       
	ReadHoldingRegisters = 0x03                                                                                     
	ReadInputRegisters = 0x04                                                                                       
	WriteSingleCoil = 0x05                                                                                          
	WriteSingleRegister = 0x06                                                                                      
	ReadExceptionStatus = 0x07                                                                                      
	GetComEventCounter = 0x0b                                                                                       
	GetComEventLog = 0x0c                                                                                           
	WriteMultipleCoils = 0x0f                                                                                       
	WriteMultipleRegisters = 0x10                                                                                   
	ReportServerId = 0x11                                                                                           
	MaskWriteRegister = 0x16                                                                                        
	ReadWriteMultipleRegisters = 0x17


class State(IntEnum):
    active_low = 0
    active_high = 1


class DataFormat(IntEnum):
    engineering = 0
    binary = 1 # 2's complement


class Protocol(IntEnum):
    ascii = 0
    modbus = 1


class FilterFreq(IntEnum):
    freq_50hz = 0
    freq_60hz = 1
    freq_60hz2 = 2
    freq_120hz = 3

@dataclass
class MiscOptions:
    save_DO_power_on_value: bool    # Save current DO status as power on value and write to eeprom
    save_DO_safe_value: bool        # Save current DO status as safe value and write to eeprom
    enable_power_on_value: bool     # Enable/disable power on value function//
    enable_safe_value: bool         # Enable/disable safe value function//
    enable_burn_out_detect: bool    # Enable/disable burn out detection //
    di_active: State                # DI active state 0=low active, 1=high active
    do_active: State                # DO active state 0=low active, 1=high active
    enable_dhcp: bool               # DHCP 0=disable, 1=enable
    enable_webserver: bool          # WebServer 0=disable, 1=enable
    enable_modbus_crc: bool         # Modbus CRC 0=disable, 1=enable
    enable_cjc: bool                # Enable/disable CJC, 0=disable, 1=enable (for EDAM5019/5039 only)
    ascii_data_format: DataFormat   # ASCII data format 0=enginerring, 1=2's
    modbus_data_format: DataFormat  # MODBUS data format 0=enginerring, 1=2's
    protocol: Protocol              # Protocol 0=ASCII, 1=MODBUS
    filter_freq: FilterFreq         # 00=50Hz, 01=60Hz, 10=60Hz, 11=120Hz

    FIELDS = {
        'save_DO_power_on_value': 0,
        'save_DO_safe_value': 1,
        'enable_power_on_value': 2,
        'enable_safe_value': 3,
        'enable_burn_out_detect': 4,
        'di_active': 5,
        'do_active': 6,
        'enable_dhcp': 7,
        'enable_webserver': 0x100,
        'enable_modbus_crc': 0x200,
        'enable_cjc': 0x400,
        'ascii_data_format': 0x800,
        'modbus_data_format': 0x1000,
        'protocol': 0x2000,
    }

    def __init__(self, value: int):
        for i, fld in enumerate(self.__dataclass_fields__.values()):
            if fld.name == 'filter_freq':
                self.filter_freq = FilterFreq(value >> 14)
            else:
                setattr(self, fld.name, fld.type((value >> i) & 0x0001))


@dataclass
class Options:
    pass

def hex_to_str(data: bytes) -> str:
    return data.hex(' ')


def int_to_temp(value: int, scale: float = 1370.0):
    '''Obtain temperature values'''
    if isinstance(value, Sequence):
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
    misc_options: MiscOptions
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
        self.misc_options = MiscOptions(values[25])
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

    FORMAT = '>x3L32L16h16h16h4H16h'

    def __init__(self, data: bytes):
        values = struct.unpack(self.FORMAT, data)
        self.d_in = values[0]
        self.d_out = values[1]
        self.di_latch = values[2]
        self.di_counter = values[3:35]
        # TODO: Values depend on configured channel type
        self.ai_normal_value = int_to_temp(values[35:51])
        self.ai_max_value = int_to_temp(values[51:67])
        self.ai_min_value = int_to_temp(values[67:83])
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
        print(f'> {len(request):3d}: {request}')
        response = daq.send_request(request.encode() + b'\r')
        print(f'< {len(response):3d}: {response}')
        return response

    def send_hex_request(request: bytes, comment: str):
        print(comment)
        print(f'> {len(request):3d}: {hex_to_str(request)}')
        response = daq.send_request(request)
        print(f'< {len(response):3d}: {hex_to_str(response)}')
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
            return bytes(x).hex().upper()
        send_asc_request('$01IP' + hex_str(ip), 'Set IP')
        send_asc_request('$01GATE' + hex_str(gw), 'Set GW')
        send_asc_request('$01MASK' + hex_str(mask), 'Set Mask')

    # def send_modbus_request(id: int, command: int, addr: int, args: bytes):


    id = 0x01
    # Read coil status
    data = struct.pack('>BBHH', id, ModbusFunction.ReadCoils, 10064, 1)
    send_hex_request(data, 'Read coil status')

    # Write single coil
    data = struct.pack('>BBHH', id, ModbusFunction.WriteSingleCoil, 10064, 0x0001)
    send_hex_request(data, 'Write single coil')

    # Read input registers
    data = struct.pack('>BBHH', id, ModbusFunction.ReadInputRegisters, 30293, 17)
    rsp = send_hex_request(data, 'Read input registers')
    data = struct.unpack('>3x17h', rsp)
    print(data)
    print('@', [x/10 for x in data])

    # get module config
    data = struct.pack('>BBBB', id, 0x46, 0x30, 0)
    rsp = send_hex_request(data, 'Get module config')
    config = ModuleConfig(rsp[3:])
    print(config)

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
    print(hex_to_str(rsp))

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
