import usb.core
import struct
from enum import IntEnum
from dataclasses import dataclass
from collections.abc import Sequence
from array import array as Array
from ipaddress import IPv4Address
import socket

PACKET_SIZE = 64

MacAddress = str

@dataclass
class ModelInfo:
    num_analogue_input_channels: int = 0
    num_analogue_output_channels: int = 0
    num_digital_input_channels: int = 0
    num_digital_output_channels: int = 0


MODELINFO_5015 = ModelInfo(
    num_analogue_input_channels = 12,
)

MODELINFO_5017 = ModelInfo(
    num_analogue_input_channels = 16,
    num_digital_input_channels = 2,
    num_digital_output_channels = 1
)

MODELINFO_5018 = MODELINFO_5017
MODELINFO_5019 = MODELINFO_5017

MODELINFO_5028 = ModelInfo(
    num_digital_input_channels = 24,
    num_digital_output_channels = 8,
)

MODELINFO_5029 = ModelInfo(
    num_digital_input_channels = 16,
    num_digital_output_channels = 16,
)

MODELINFO_5039 = ModelInfo(
    num_analogue_input_channels = 8,
    num_digital_input_channels = 8,
    num_digital_output_channels = 8,
)

MODELINFO_5060 = ModelInfo(
    num_digital_input_channels = 12,
    num_digital_output_channels = 10,
)

MODELINFO: dict[int, ModelInfo] = {
  0x5015: MODELINFO_5015,
  0x5017: MODELINFO_5017,
  0x5018: MODELINFO_5018,
  0x5019: MODELINFO_5019,
  0x5028: MODELINFO_5028,
  0x5029: MODELINFO_5029,
  0x5039: MODELINFO_5039,
  0x5060: MODELINFO_5060,
}

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

    def __init__(self, value: int):
        for i, fld in enumerate(self.__dataclass_fields__.values()):
            mask = 0x0003 if fld.name == 'filter_freq' else 0x0001
            setattr(self, fld.name, fld.type((value >> i) & mask))


@dataclass
class Options:
    pass


class ChannelType(IntEnum):
    BIPOLAR_10V     = 0x07  # bipolar +/-10V
    BIPOLAR_5V      = 0x08  # bipolar +/-5V
    BIPOLAR_2V5     = 0x09  # bipolar +/-2.5V
    BIPOLAR_1V      = 0x0a  # bipolar +/-1V
    BIPOLAR_500MV   = 0x0b  # bipolar +/-500mV
    BIPOLAR_150MV   = 0x0c  # bipolar +/-150mV
    UNIPOLAR_20MA   = 0x0d  # unipolar 0-20mA (250 ohms)
    BIPOLAR_20MA    = 0x0e  # bipolar 4-20mA (250 ohms)
    THERMOCOUPLE_J  = 0x0F  # T/C J type
    THERMOCOUPLE_K  = 0x10  # T/C K type
    THERMOCOUPLE_T  = 0x11  # T/C T type
    THERMOCOUPLE_E  = 0x12  # T/C E type
    THERMOCOUPLE_R  = 0x12  # T/C R type
    THERMOCOUPLE_S  = 0x14  # T/C S type
    THERMOCOUPLE_B  = 0x15  # T/C B type
    IECPT100_TYPE1  = 0x20  # IEC Pt100  -50C ~ 150C
    IECPT100_TYPE2  = 0x21  # IEC Pt100    0C ~ 100C
    IECPT100_TYPE3  = 0x22  # IEC Pt100    0C ~ 200C
    IECPT100_TYPE4  = 0x23  # IEC Pt100    0C ~ 400C
    IECPT100_TYPE5  = 0x24  # IEC Pt100 -200C ~ 200C
    JISPT100_TYPE1  = 0x25  # JIS Pt100  -50C ~ 150C
    JISPT100_TYPE2  = 0x26  # JIS Pt100    0C ~ 100C
    JISPT100_TYPE3  = 0x27  # JIS Pt100    0C ~ 200C
    JISPT100_TYPE4  = 0x28  # JIS Pt100    0C ~ 400C
    JISPT100_TYPE5  = 0x29  # JIS Pt100 -200C ~ 200C
    PT1000          = 0x2a  # Pt1000     -40C ~ 160C
    BALCO500_TYPE1  = 0x2b  # BALCO500   -30C ~ 120C
    Ni604_TYPE1     = 0x2c  # Ni         -80C ~ 100C
    Ni604_TYPE2     = 0x2d  # Ni           0C ~ 100C


def ip_to_str(data: bytes) -> str:
    return '.'.join(str(x) for x in data)


def mac_to_str(data: bytes) -> str:
    return data.hex(':')


def int_to_temp(value: int, scale: float = 1370.0):
    '''Obtain temperature values'''
    if isinstance(value, Sequence):
        return [int_to_temp(x) for x in value]
    return round(value * scale / 32767, 1)


@dataclass
class DeviceInfo:
    id: int
    model: int
    name: str
    desc: str


@dataclass
class ModuleConfig:
    mac: MacAddress
    netmask: IPv4Address
    ipaddr: IPv4Address
    gateway: IPv4Address
    id: int
    module_name: str
    module_desc: str
    event_sip: list[IPv4Address]
    event_trigger: list[bool]
    stream_sip: list[IPv4Address]
    stream_active: list[bool]
    stream_time_interval: int
    baudrate: int
    misc_options: MiscOptions
    options: int
    version: str

    FORMAT = '<6s4s4s4s1B8s32s4s4s4s4s4?4s4s4s4s4?xLBxHH16s'

    def __init__(self, data: bytes):
        values = struct.unpack(self.FORMAT, data)
        self.mac = mac_to_str(values[0])
        self.netmask = ip_to_str(values[1])
        self.ipaddr = ip_to_str(values[2])
        self.gateway = ip_to_str(values[3])
        self.id = values[4]
        self.module_name = values[5].decode().rstrip('\0')
        self.module_desc = values[6].decode().rstrip('\0')
        self.event_sip = [ip_to_str(x) for x in values[7:11]]
        self.event_trigger = values[11:15]
        self.stream_sip = [ip_to_str(x) for x in values[15:19]]
        self.stream_active = values[19:23]
        self.stream_time_interval = values[23]
        self.baudrate = values[24]
        self.misc_options = MiscOptions(values[25])
        self.options = values[26]
        self.version = values[27]


@dataclass
class ModuleIoChannels:
    misc: int # Same as from MISC command, not sure what that is
    ipaddr: IPv4Address
    netmask: IPv4Address
    gateway: IPv4Address
    digital_input_types: list
    digital_output_types: list
    analogue_input_types: list[ChannelType]
    average_type: ChannelType

    def __init__(self, model: int, data: bytes):
        info = MODELINFO[model]

        FORMAT = '<H4s4s4s' \
            + f'{info.num_digital_input_channels}s' \
            + f'{info.num_digital_output_channels}s' \
            + f'{info.num_analogue_input_channels}s'
        if info.num_analogue_input_channels:
            FORMAT += 'B'

        values = struct.unpack(FORMAT, data)
        self.misc = values[0]
        self.ipaddr = IPv4Address(values[1])
        self.netmask = IPv4Address(values[2])
        self.gateway = IPv4Address(values[3])
        self.digital_input_types = [int(x) for x in values[4]]
        self.digital_output_types = [int(x) for x in values[5]]
        self.analogue_input_types = [ChannelType(x) for x in values[6]]
        self.average_type = ChannelType(values[7]) if info.num_analogue_input_channels else None


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


class ReaderProperty():
    def __init__(self, req: str, rsp_hdrlen: int = 3):
        self.req = req
        self.rsp_hdrlen = rsp_hdrlen

    # def getter(self, fget):
    #     return ReaderProperty(fget, None, None, None)

    # def setter(self, fset: Callable[[Any, Any], None]) -> property: ...
    # def deleter(self, fdel: Callable[[Any], None]) -> property: ...

    def __get__(self, obj, objtype=None):
        return obj.read_prop(self.req, self.rsp_hdrlen)

    # def __set__(self, obj: Any, value: Any) -> None: ...
    # def __delete__(self, obj: Any) -> None: ...
    # def fget(self) -> Any: ...
    # def fset(self, value: Any) -> None: ...
    # def fdel(self) -> None: ...


class E5KDAQ:
    '''Python implementation of InLog E5KDAQ interface.
    Communication method is abstracted to an inherited class.
    '''
    version = ReaderProperty('$F')
    ipaddr = ReaderProperty('$IP')
    gateway = ReaderProperty('$GATE')
    netmask = ReaderProperty('$MASK')
    macaddr = ReaderProperty('^MAC')
    module_name = ReaderProperty('$M')
    analogue_inputs_normal = ReaderProperty('#', 1)
    analogue_inputs_max = ReaderProperty('#MH', 1)
    analogue_inputs_min = ReaderProperty('#ML', 1)

    def send_request(self, request: bytes) -> bytes:
        raise NotImplemented()

    def read_prop(self, req: str, rsp_hdrlen: int):
        req = req[0] + f'{self.id:02X}' + req[1:] + '\r'
        rsp = self.send_request(req.encode())
        return rsp[rsp_hdrlen:].decode()

    def read_device_info(self) -> DeviceInfo:
        data = self.send_request(b'$00IM\r')
        self.id = int(data[1:3], 16)
        self.model = int(data[3:7], 16)
        self.name = data[7:15].decode()
        self.desc = data[15:-1].decode()

    @property
    def info(self) -> ModelInfo:
        return MODELINFO[self.model]

    def send_config_request(self, code: int):
        '''Send internal configuration request

        This is undocumented and looks like a modbus request with function 0x46.
        Command codes are:

            0x30: Read module config
            0x31: Write module config
            0x32: Write module config? No authentication required. See `so_set_module_config_ll`.
            0x33: Set password
            0x40: Read module data
            0x41: Read channel types
        '''
        req = struct.pack('>BBBB', self.id, 0x46, code, 0)
        rsp = self.send_request(req)
        return rsp[3:]

    def read_module_config(self) -> ModuleConfig:
        data = self.send_config_request(0x30)
        return ModuleConfig(data)

    def read_module_data(self) -> ModuleData:
        '''Implementation of E5K_ReadAllDataFromModule API call'''
        data = self.send_config_request(0x40)
        return ModuleData(data)

    def read_module_iochannels(self) -> ModuleIoChannels:
        data = self.send_config_request(0x41)
        return ModuleIoChannels(self.model, data)

    def read_input_registers(self, addr: int, count: int, regtype: type = int) -> list[int]:
        '''Read a set of MODBUS input registers

        addr -- starting address
        count -- number of registers to read
        regtype -- optional type for returning register values
        '''
        req = struct.pack('>BBHH', self.id, ModbusFunction.ReadInputRegisters, addr, count)
        rsp = self.send_request(req)
        # TODO: Handle errors
        return [regtype(x) for x in struct.unpack(f'>3x{count}h', rsp)]

    def read_analogue_input_types(self) -> list[ChannelType]:
        n = self.info.num_analogue_input_channels
        if n == 0:
            return []
        return self.read_input_registers(348, n, ChannelType)

    def read_analogue_inputs(self) -> Array[float]:
        req = f'#{self.id:02x}\r'.encode()
        rsp = self.send_request(req)
        return Array('d', [float(rsp[o:o+7]) for o in range(1, len(rsp)-2, 7)])

    def read_coils(self, addr: int, count: int) -> Array['b']:
        req = struct.pack('>BBHH', self.id, ModbusFunction.ReadCoils, addr, count)
        rsp = self.send_request(req)
        print(rsp.hex(' '))
        bits = int.from_bytes(rsp[3:], byteorder='little', signed=False)
        return Array('B', [((bits >> i) & 1) for i in range(count)])

    def write_coils(self, addr: int, data: list):
        bits = 0
        bit_count = len(data)
        for x in reversed(data):
            bits = (bits << 1) | (1 if x else 0)
        byte_count = (bit_count + 7) // 8
        values = bits.to_bytes(byte_count, byteorder='little', signed=False)
        req = struct.pack('>BBHHB', self.id, ModbusFunction.WriteMultipleCoils, addr, len(data), byte_count) + values
        self.send_request(req)

    def set_ip_address(self, ipaddr: any, gateway: any, netmask: any):
        def setaddr(tag: str, addr: any):
            addr = IPv4Address(addr).packed.hex().upper()
            req = f'${self.id:02X}{tag}{addr}\r'.encode()
            self.send_request(req)
        setaddr('IP', ipaddr)
        setaddr('GATE', gateway)
        setaddr('MASK', netmask)


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
        self.read_device_info()

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


class NetworkDAQ(E5KDAQ):
    def open(self, ipaddr: any):
        self.socket_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_udp.settimeout(2)
        self.socket_udp.connect((ipaddr, 1025))
        self.read_device_info()

    def send_request(self, request: bytes) -> bytes:
        '''Send a request and return response'''
        self.socket_udp.send(request)
        rsp = self.socket_udp.recv(PACKET_SIZE * 33)
        return rsp
