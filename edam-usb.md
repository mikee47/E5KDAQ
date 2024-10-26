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
          0x40: READ
          0x41: READ channel types?
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


`ModuleConfigX` contains additional "%AAGETFIXADDR\r" command.

```
> 13 %01GETFIXADDR
< 34 b'!01C0A8010BC0A80101FFFFFF00000A00\r'
```

 0: !01
 3: C0 A8 01 0B   IP
11: C0 A8 01 01   GW
19: FF FF FF 00   MASK
27: 00 0A         DHCP
31: 00            DHCP_flag (0), WebReadOnlyFlag (0)


READ 0x41: Get channel types

< 37
01 46 41
90 05 c0 a8 01 0b ff ff ff 00 c0 a8 01 01 00 00 00 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10

 0: 90 05                   0x0590 Same as from MISC command
 2: c0 a8 01 0b             IP
 6: ff ff ff 00             Mask
10: c0 a8 01 01             GW
14: 00 00                   digital input types
16: 00                      digital output type
17: 10 10 10 10 10 10 10 10 analogue input types 0-7
25: 10 10 10 10 10 10 10 10 " 8-15
33: 10                      Presumably for CJC

Number of channels depends on device type, requires lookup table.
See decompiled `read_device_data` function.
Information returned from `E5K_GetModuleIOChannels`.


## E5K_ReadAllDataFromModule

Code appears model-specific.

```
struct MODULE_DATA
{
  0     ULONG     Din;
  4     ULONG     Dout;
  8     ULONG     DiLatch;
 12     ULONG     DiCounter[32]; // 32*4 = 128
 140    double    AiNormalValue[16]; // 16*8 = 128
 268    double    AiMaxValue[16];
 396    double    AiMinValue[16];
 524    USHORT    AiHighAlarmstatus;
 526    USHORT    AiLowAlarmstatus;
 528    USHORT    AiBurnOut ;                     //EDAM 5019/5015/5039 only
 530    double    CJCTemperature  ;               //EDAM 5019/5039 only//
 538    double    AoValue[16];
 666
} MODULE_DATA;
```

module_config_request(0x40) returns 280 bytes:

01 46 00           HEADER
  0:    00
  1:    00 00 00 00
  5:    00 00 00 01
  9:    00 00 00 00

 13:    00 00 00 00     ULONG[32] big endian: DiCounter ?
        00 00 00 00
        00 00 00 00
        00 00 00 00
        00 00 00 00
        00 00 00 00
        00 00 00 00
        00 00 00 00
        00 00 00 00
        00 00 00 00
        00 00 00 00
        00 00 00 00
        00 00 00 00
        00 00 00 00
        00 00 00 00
        00 00 00 00

        00 00 00 00
        00 00 00 00
        00 00 00 00
        00 00 00 00
        00 00 00 00
        00 00 00 00
        00 00 00 00
        00 00 00 00
        00 00 00 00
        00 00 00 00
        00 00 00 00
        00 00 00 00
        00 00 00 00
        00 00 00 00
        00 00 00 00
        00 00 00 00
        
141:    7f ff
        00 00
        00 00
        00 00
        00 00
        00 00
        00 00
        00 00
        00 00
        00 00
        00 00
        00 00
        00 00
        7f ff
        00 00
        7f ff
        
173:    7f ff
        00 00
        00 00
        00 00
        00 00
        00 00
        00 00
        00 00
        00 00
        00 00
        00 00
        00 00
        00 00
        7f ff
        00 00
        7f ff

205:    7f ff
        00 00
        00 00
        00 00
        00 00
        00 00
        00 00
        00 00
        00 00
        00 00
        00 00
        00 00
        00 00
        7f ff
        00 00
        7f ff

237:    00 00
        00 00
        a0 01
        00 ee

245:    00 00 00 00
        00 00 00 00
        00 00 00 00
        00 00 00 00
        00 00 00 00
        00 00 00 00
        00 00 00 00
        00 00 00 00

 
MODULE_DATA::Din = (buf[1] * 0x1000000) + (buf[2] * 0x10000) + (buf[3] * 0x100) + buf[4];


## Calibration

E5K_STATUS E5K_ReadAICalibrationCoefficient(MODULE_ID id, ULONG* Coefficient, CHAR Regtype);

    Regtype can be 0x01 or 0x02.

    0x01: "~AACALZ"
    0x02: "~AACALS"


E5K_STATUS E5K_WriteAICalibrationCoefficient(MODULE_ID id, ULONG Coefficient, CHAR Regtype);

    "~AACALZnnnnnnnn"
    "~AACALSnnnnnnnn"

    nnnnnnnn == co-efficient hex string


E5K_STATUS E5K_CalibrateAIZeroSpan(MODULE_ID id, USHORT Calchno, CHAR Adtype);

    "$AACALcctt"

    cc == calchno
    tt == adtype


## E5K_ReadAIChannelConfig

"$AAGcc"

Read AI channel config
> 6 $01G00
< 26 b'!01101000**+0.0000+0.0000\r'

 0 !01
 3 10       0x10 wType
 5 1        0x01 wActive
 6 0        0x00 wInAverage
 7 0        0x00 wHiAlarmMode ('L' -> 2, 'M' -> 1, other -> 0)
 8 0        0x00 wLoAlarmMode
 9 *        wHiAlarmDo: '*' -> 0xff, other -> hex digit value
10 *        wLoAlarmDo
11 +0.0000  fHighLimit. For writing "%c%00004d.%01d"
18 +0.0000  fLowLimit

E5K_SetAIChannelConfig

"$AAGcc..."

Data format same as for reading.


## Multi-channel reads

Use undocumented modbus register ranges with `read input register` command 0x06.
One reason for this could be that the data is unambiguously returned in binary format.

`E5K_ReadMultiChannelColdJunctionOffset` @ 366
`E5K_ReadMultiDICounter` @ 700, each register is 32 bits (i.e. 2 modbus registers)
`E5K_ReadAINormalMultiChannel` @ 1500
`E5K_ReadAIMaximumMultiChannel` @ 1600
`E5K_ReadAIMinimumMultiChannel` @ 1700


## E5K_SetDOMultipleChannels

E5K_STATUS  E5K_SetDOMultipleChannels  (MODULE_ID id,ULONG dwActchn,UCHAR bMode);

Uses undocumented "#AAEmcccccccc"

m = bMode
cccccccc = dwActchn


## E5K_StartMultipleDOPulse

Just repeats `Write Single Do Pulse Counts` and `Start/Stop DO Pulse Counts` for each channel.

