# Notes on inspecting E5KDAQ64.DLL

Require USB access with GNU/Linux, e.g. RPi.
Using Python should also support other platforms if required.

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


## Module config

e.g. do_module_config_request()

0x00 BYTE id
0x01 BYTE 'F' (0x46)
0x02 BYTE 0x30: READ
          0x31
          0x32
          0x33
          0x40
          0x41
0x03 BYTE unused
0x04 data[]


  0: 01 46 30
  0: 00 e0 4c 36 01 55         MAC
  6: ff ff ff 00               MASK
 10: c0 a8 01 0b               IP 192.168.1.11
 14: c0 a8 01 01               GW 192.168.1.1
 18: 01                        MODULE ID
 19: 35 30 31 39 00 00 00 00   "5019"
 27: 31 36 20 54 2f 43 20 43   "16 T/C Channels and 2 DI/1 DO"
 35: 68 61 6e 6e 65 6c 73 20
 43: 61 6e 64 20 32 20 44 49
 51: 2f 31 20 44 4f 00 00 00
 59: ff ff ff ff               event_sip[0]
 63: ff ff ff ff               event_sip[1]
 67: ff ff ff ff               event_sip[2]
 71: ff ff ff ff               event_sip[3]
 75: 00 00 00 00               event_triggers[0..3]
 79: ff ff ff ff               stream_sip[0]
 83: ff ff ff ff               stream_sip[1]
 87: ff ff ff ff               stream_sip[2]
 91: ff ff ff ff               stream_sip[3]
 95: 00 00 00 00               stream_active[0..3]
 99: 00                        #PAD#
100: 20 4e 00 00               stream_time_interval (20000)
104: 06                        baudrate (9600)
105: 00                        #PAD#
106: 90 05                     wMiscOptions
108: 19 50                     wOptions
110: 30 30 30 30 30 30 30 30
118: 03 00 04 00 00 00 00 00   version[0..15]
126:

Misc Options 0x0590

0000 0101 1001 0000

 0: 0  WRITE D0 status as power-on
 1: 0  WRITE D0 status as safe value
 2: 0  Power-on value (disable)
 3: 0  Safe value (disable)
 4: 1  Burn-out detect (enable)
 5: 0  DI active (low)
 6: 0  DO active (low)
 7: 1  DHCP (enable)
 8: 1  Webserver (enable)
 9: 0  Modbus CRC (disable)
10: 1  CJC (enable)
11: 0  ASCII data format (engineering)
12: 0  MODBUS data format (engineering)
13: 0  Protocol (ASCII)
14: 00 50Hz

