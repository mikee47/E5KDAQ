import e5kdaq
from e5kdaq import ModbusFunction, ModuleConfig, ModuleData
import struct

def hex_to_str(data: bytes) -> str:
    return data.hex(' ')


def main():
    daq = e5kdaq.USBDAQ()
    daq.open()
    # daq = e5kdaq.NetworkDAQ()
    # daq.open('192.168.1.11')

    for name, prop in type(daq).__dict__.items():
        if isinstance(prop, e5kdaq.ReaderProperty):
            print(f'{name} = {getattr(daq, name)}')

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

    def read_input_registers(addr: int, count: int, comment: str) -> list:
        print(comment)
        data = daq.read_input_registers(addr, count)
        print('<', data)
        return data

    print(f'id {daq.id:x}, model {daq.model:x}, name "{daq.name}", desc "{daq.desc}"')
    print(daq.info)

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

    send_asc_request('$016', 'Read channel enable/disable status')

    # daq.set_ip_address('192.168.1.11', '192.168.1.1', '255.255.255.255')

    # def send_modbus_request(id: int, command: int, addr: int, args: bytes):

    print('Read DO: ', daq.read_coils(64, 1)[0])

    print('Enable/disable channels')
    daq.write_coils(256, [0, 1, 0, 0,   0, 0, 1, 0,   0, 0, 0, 1,   0, 0, 0, 0])

    data = daq.read_coils(256, 16)
    print('Analogue channel status', data)

    print('Set DO')
    daq.write_coils(64, [1])

    data = read_input_registers(293, 17, 'Read CJC and channels')
    print('@', [x/10 for x in data])

    print('Read analogue input types')
    types = daq.read_analogue_input_types()
    print([x.name for x in types])

    print('Read analogue inputs')
    data = daq.read_analogue_inputs()
    print(data)

    read_input_registers(30080, 2, 'Read digital inputs types')
    read_input_registers(0, 2, 'Read base register range')

    # Read ModuleConfig
    config = daq.read_module_config()
    print(config)
    print(f'OPTIONS: {config.options:x}')

    # Read ModuleConfigX
    rsp = send_asc_request('%01GETFIXADDR', 'ModuleConfigX')

    # E5K_ReadDIChannelConfig
    rsp = send_asc_request('%01C00', 'ReadDIChannelConfig')

    print('E5K_ReadAllDataFromModule', daq.read_module_data())

    print('E5K_ReadModuleIOChannels', daq.read_module_iochannels())

    print('Get module IO Channels')
    data = daq.send_config_request(0x41)
    print(hex_to_str(data))

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
