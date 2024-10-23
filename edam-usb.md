dev = usb.core.find(idVendor=0x04b4, idProduct=0x8613)
dev.set_configuration()
cfg = dev.get_active_configuration()
intf = cfg.interfaces()[0]
ep0 = intf.endpoints[0]
ep1 = intf.endpoints[1]

cmd=b'\x88\x33\x55\x77\x05\x00\x00\x00$00F\r'.ljust(64, b'\0')
ep0.write(cmd)
rsp = esp1.read(64)



## WriteModbusRegister

0x00 BYTE id          Slave ID
0x01 BYTE 0x10        Function code
0x02 WORD address     MSB first
0x04 WORD count       MSB first
0x06 data[]

Modbus commands require mapped addresses as per manual.
For example, DO is 10064.
