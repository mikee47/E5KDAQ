'''
Copyright (c) 2009-2012  Inlog Micro system   All rights reserved.

File Name   : E5KDAQ.H
Purpose     : EDAM 5000 Moudles Definition

Revision    : 1.40  (2009/02/11)

Revision    : 4.70 (2013/09/06)
              (1). Add E5K_EthernetSearchDevice function
              (2). Add E5K_BuildHtmFileSystemX function
              (3). support EDAM5039

Revision    : 5.00 (2014/04/16)
              this DLL require to use iusblib.dll,libusb0.dll, and libusb0.sys
        compiled by VS-2010
'''

from enum import IntEnum

# -- Type definations --------------
# typedef     unsigned short     E5K_STATUS;
# typedef     unsigned short     MODULE_ID;
# typedef     long             LONG;  //SDWORD;
# typedef     short            SHORT; //SWORD;
# typedef     unsigned long    ULONG; //DWORD;
# typedef     char             CHAR;  //SBYTE;
# typedef     unsigned int     UINT;  //UINT;
# typedef     int              INT;   //INT;
# typedef     unsigned char    UCHAR; //SBYTE;
# typedef     unsigned short   USHORT;


#define     LED_HOST                1
#define     LED_MODULE              0

# --Event type ---
class InterruptType(IntEnum):
    DI_INT_TYPE = 0 # DI Event
    AD_INT_TYPE = 1 # AI Event

# --Event status ---
class EventStatus(IntEnum):
    DI_LOW_HIGH_INT_STATE = 0    # DI low to high Event
    DI_HIGH_LOW_INT_STATE = 1    # DI high to low Event
    AD_HIGH_ALARM_INT_STATE =    # AI high alarm Event
    AD_LOW_ALARM_INT_STATE = 1   # AI low alarm Event

# -- Digital input mode decleration --
class DigitalInputMode(IntEnum):
    DI_MODE = 0                  # direct input mode
    COUNTER_MODE = 1             # counter mode
    LOW_HIGH_LATCH_MODE = 2      # low to high LATCH mode
    HIGH_LOW_LATCH_MODE = 3      # hjgh to low LATCH mode
    FREQUENCY_MODE = 4           # frequency mode

# -- TCP/IP decleration --
#define     TCP_MODBUS_PORT         502       //Modbus TCP/IP port (TCP)
#define     UDP_ASC_PORT            1025      //ASC command port/MODBUS RTU (UDP)
#define     UDP_BROADCAST_PORT      5048      //broadcast port     (UDP)
#define     BROADCAST_IP            "255.255.255.255"
#define     UDP_ALARM_PORT          5168      //udp alarm port
#define     UDP_STREAM_PORT         5148      //udp Stream port

# -- RS232/485 Rx Timeout --
#define     COM_DEFAULT_TIMEOUT     300

# -- EDAM5015 AD channel types -----------
#define     IECPT100_TYPE1          0x20    // type 0x20:IEC Pt100  -50C ~ 150C
#define     IECPT100_TYPE2          0x21    // type 0x21:IEC Pt100    0C ~ 100C
#define     IECPT100_TYPE3          0x22    // type 0x22:IEC Pt100    0C ~ 200C
#define     IECPT100_TYPE4          0x23    // type 0x23:IEC Pt100    0C ~ 400C
#define     IECPT100_TYPE5          0x24    // type 0x24:IEC Pt100 -200C ~ 200C
#define     JISPT100_TYPE1          0x25    // type 0x25:JIS Pt100  -50C ~ 150C
#define     JISPT100_TYPE2          0x26    // type 0x26:JIS Pt100    0C ~ 100C
#define     JISPT100_TYPE3          0x27    // type 0x27:JIS Pt100    0C ~ 200C
#define     JISPT100_TYPE4          0x28    // type 0x28:JIS Pt100    0C ~ 400C
#define     JISPT100_TYPE5          0x29    // type 0x29:JIS Pt100  -200C ~ 200C
#define     PT1000_TYPE             0x2a    // type 0x2A:Pt1000     -40C ~ 160C
#define     BALCO500_TYPE1          0x2b    // type 0x2B:BALCO500   -30C ~ 120C
#define     Ni604_TYPE1             0x2c    // type 0x2C:Ni         -80C ~ 100C
#define     Ni604_TYPE2             0x2d    // type 0x2D:Ni           0C ~ 100C

#define     E5015_TYPE_START        IECPT100_TYPE1
#define     E5015_TYPE_END          Ni604_TYPE2

# -- EDAM5017 AD channel types -----------
#define     B10V_TYPE               0x07  // type 0X09 bipolar +/-10V
#define     B5V_TYPE                0x08  // type 0X0A bipolar +/-5V
#define     B2P5V_TYPE              0x09  // type 0X09 bipolar +/-2.5V
#define     B1V_TYPE                0x0a  // type 0X0A bipolar +/-1V
#define     B500MV_TYPE             0x0b  // type 0X0B bipolar +/-500mV
#define     B150MV_TYPE             0x0c  // type 0X0C bipolar +/-150mV
#define     U20MA_TYPE              0x0d  // type 0X0D unipolar 0-20mA (250 ohms)
#define     B4T20MA_TYPE            0x0e  // type 0X0E bipolar 4-20mA (250 ohms)

#define     E5017_TYPE_START        B10V_TYPE
#define     E5017_TYPE_END          B4T20MA_TYPE

# -- EDAM5019/5039 AD channel types -----------
#define     B2P5V_TYPE              0x09  // type 0X09 bipolar +/-2.5V
#define     B1V_TYPE                0x0a  // type 0X0A bipolar +/-1V
#define     B500MV_TYPE             0x0b  // type 0X0B bipolar +/-500mV
#define     B150MV_TYPE             0x0c  // type 0X0C bipolar +/-150mV
#define     U20MA_TYPE              0x0d  // type 0X0D unipolar 0-20mA (250 ohms)
#define     B4T20MA_TYPE            0x0e  // type 0X0E bipolar 4-20mA (250 ohms)
#define     TC_J_TYPE               0x0F  // T/C J type
#define     TC_K_TYPE               0x10  // T/C K type
#define     TC_T_TYPE               0x11  // T/C T type
#define     TC_E_TYPE               0x12  // T/C E type
#define     TC_R_TYPE               0x12  // T/C R type
#define     TC_S_TYPE               0x14  // T/C S type
#define     TC_B_TYPE               0x15  // T/C B type

#define     E5019_TYPE_START        B2P5V_TYPE
#define     E5019_TYPE_END          TC_B_TYPE

#define     E5039_TYPE_START        B2P5V_TYPE
#define     E5039_TYPE_END          TC_B_TYPE

#define     ZERO_TYPE               1
#define     SPAN_TYPE               2

#define     ALARM_EVENT_TYPE        0
#define     STREAM_EVENT_TYPE       1

#define     INT_QUE_DEEP            32  //do not change
#define     INT_QUE_SIZE            1024

// -- Error Code table -----------
class ErrorCode(IntEnum):
    STATUS_NO_ERROR                     = 0x00 # No Error
    STATUS_NOT_SUPPORT_MODULE           = 0x01 # Device Not supported
    STATUS_DEVICE_NOT_FOUND             = 0x02 # Device is not existed
    STATUS_DRIVER_NOT_OPEN              = 0x03 # Device not activated
    STATUS_DRIVER_OPEN_FAIL             = 0x04 # Device driver open fail
    STATUS_DEVICE_TIMEOUT               = 0x05 # Device time out
    STATUS_DEVICE_REPSONSE_ERROR        = 0x06 # Device Response Error
    STATUS_INVALID_DRIVER_VERSION       = 0x07 # Invalid Driver version
    STATUS_INVALID_DEVICE_ID            = 0x08 # Invalid ID Number
    STATUS_DEVICE_ID_OVERLAP            = 0x09 # Device ID overlaped
    STATUS_INVALID_INTERFACE_TYPE       = 0x10 # Invalid Interace Type
    STATUS_INVALID_PASSWORD             = 0x11 # Invalid Pass Word or password not be verified
    STATUS_INVALID_ASCII_COMMAND        = 0x12 # Invalid ASCII Command
    STATUS_EVENT_ALREADY_ENABLED        = 0x13 # Event Already enabled
    STATUS_NO_EVENT_DATA                = 0x14 # No Event Data
    STATUS_OPTION_OUT_OF_RANGE          = 0x15 # Arguments Out Of Range
    STATUS_INVALID_PORT_NUMBER          = 0x16 # Invalid Port Number
    STATUS_INVALID_DO_DATA              = 0x17 # Invalid DO Data
    STATUS_INVALID_DIO_CHANNEL          = 0x18 # Invalid Digital Channel Number
    STATUS_INVALID_TIMER_VALUE          = 0x19 # Invalid Timer Value
    STATUS_INVALID_TIMER_MODE           = 0x20 # Invalid Timer Mode
    STATUS_INVALID_COUNTER_NO           = 0x21 # Invalid Counter Number
    STATUS_INVALID_COUNTER_VALUE        = 0x22 # Invalid Counter Value
    STATUS_INVALID_COUNTER_MODE         = 0x23 # Invalid Counter Mode
    STATUS_INVALID_AD_FILTER            = 0x24 # Invalid A/D Filter Type
    STATUS_INVALID_AD_MODE              = 0x25 # Invalid A/D Mode
    STATUS_INVALID_AD_CHANNEL           = 0x26 # Invalid A/D channel number
    STATUS_INVALID_AD_GAIN              = 0x27 # Invalid A/D Gain
    STATUS_INVALID_AD_RANGE             = 0x28 # Invalid A/D Range
    STATUS_INVALID_AD_COUNT             = 0x29 # Invalid A/D count Value
    STATUS_INVALID_AD_SCAN_RATE         = 0x30 # Invalid A/D Scan Rate
    STATUS_FIFO_HALF_NOTREADY           = 0x31 # A/D FIFO Half Not Ready
    STATUS_INVALID_DA_CHANNEL           = 0x32 # Invalid D/A channel number
    STATUS_INVALID_DA_VALUE             = 0x33 # Invalid D/A Value
    STATUS_INVALID_DEBOUNCE_MODE        = 0x34 # Invalid Debounce Mode
    STATUS_INVALID_DEBOUNCE_TIME        = 0x35 # Invalid Debounce Time
    STATUS_INVALID_MODBUS_FUNCTION      = 0x36 # Invalid MODBUS Function
    STATUS_INVALID_MODBUS_START_ADDRESS = 0x37 # Invalid MODBUS Start Address
    STATUS_MODBUS_OUT_OF_RANGE          = 0x38 # MODBUS Address Out Of Range or command length error
    STATUS_MODBUS_DISCRETE_QTY_OVER32   = 0x39 # MODBUS Range over 32 Channel
    STATUS_WINSCK_NOT_OPEN              = 0x40 # WINSCK Not Opened
    STATUS_WINSCK_STARTUP_FAILURE       = 0x41 # Windows winsock2 start up error
    STATUS_INVALID_IP                   = 0x42 # Invalid IP address or IP already open
    STATUS_TCP_SOCKET_FAILURE           = 0x43 # Can Not Create TCP Socket
    STATUS_UDP_SOCKET_FAILURE           = 0x44 # Can Not Create UDP Socket
    STATUS_SET_IP_TIMEOUT_FAILURE       = 0x45 # Can Not Set TCP/IP Timeout
    STATUS_SEND_TO_IP_FAILURE           = 0x46 # Can Not Send Package To Destination
    STATUS_RECEIVE_FROM_IP_FAILURE      = 0x47 # No Package Received Until Timeout
    STATUS_READ_STREAM_DATA_FAILURE     = 0x48 # Unable To Read Stream Data
    STATUS_IP_NOT_CONNECTED             = 0x49 # No Connection To Remote IP Address
    STATUS_ALARM_INFO_EMPTY             = 0x50 # Alarm Event Buffer Empty
    STATUS_STREAM_INFO_EMPTY            = 0x51 # Stream Event Buffer Empty
    STATUS_MEMALLOC_ERROR               = 0x52 # Unable To Allocate Memory
    STATUS_PING_TIMEOUT                 = 0x53 # Can Not Ping Remote IP Address
    STATUS_ASCII_CHECKSUM_ERROR         = 0x54 # ASCII Check Sum error
    STATUS_MODBUS_CRC_ERROR             = 0x55 # MODBUS crcCRC error
    STATUS_NOT_INSUBNET                 = 0x56 # IP not in the subnet
    STATUS_COMM_ALREADY_OPEN            = 0x57 # COMM port already open
    STATUS_NO_ENOUGH_BUFFERSIZE         = 0x58 # no enough buffer size to receive data
    STATUS_INVALID_PARAMETERS           = 0x59 # invalid parameters
    STATUS_DATA_OVER_1024_BYTE          = 0x60 # USB data over 1024 bytes
    STATUS_INVALID_HOST_IP              = 0x61 # Invalid host IP
    STATUS_INVALID_STREAM_IP            = 0x62 # Invalid stream IP
    STATUS_INVALID_ALARM_IP             = 0x63 # Invalid alarm IP
    STATUS_OPEN_PLF_FAIL                = 0x64 # Can not open web page list file
    STATUS_OPEN_HTM_FAIL                = 0x65 # Can not open web page file
    STATUS_OPEN_OUT_FAIL                = 0x66 # Can output Web page obj code file
    STATUS_END                          = 0x67 # Error Code Out of Range

'''

typedef struct ALARM_EVENT_INFO
{
    USHORT    szID;                 //the ID address which cause the alarm Event
    UCHAR     szIP[4];              //Target IP
    USHORT    wIntType;             //0= DI Event,1= AD Event
    USHORT    wChno;                //Event channel number
    USHORT    wStatus;              //=0 for low to high Event for DI or high alarm for AI channel
                                    //=1 for high to low Event for DI or low alarm for AI channel
    double    fAddata;              //AD data if AD alarm occured
} ALARM_EVENT_INFO;

typedef struct STREAM_EVENT_INFO
{
    USHORT    wszID;                //the ID address which cause the alarm change
    UCHAR     szIP[4];
    ULONG     dwDi;
    ULONG     dwDiLatch;
    ULONG     dwDiCount[32];
    ULONG     dwDo;
    double    fAiNorValue[17];      //normal AD values(channel #0~15 and average channel)
    double    fAiMaxValue[16];
    double    fAiMinValue[16];
    USHORT    wAiHighAlarmstatus;
    USHORT    wAiLowAlarmstatus;
    USHORT    wAiBurnOut ;          //EDAM5019/5015/5039 only
    double    fCJCTemperature;      //EDAM 5019/5039 only unit of 0.1C//
    double    fAoValue[16];
} STREAM_EVENT_INFO;

typedef void (WINAPI *ALARM_EVENT_HANDLER)(USHORT Id) ;


typedef struct E5K_DEVICE_ID_INFO
{
    USHORT     dev_id;
    USHORT     dev_name;
    UCHAR      dev_ip[20];
    CHAR       open_name[20];

} E5K_DEVICE_ID_INFO ;

typedef struct MODULE_CONFIG {

    CHAR       bmac[6];                     //mac address  where SYBTE =char
    CHAR       bmask[4];                    //mask address
    UCHAR      bip[4];                      //IP address
    UCHAR      bgate[4];                    //gateway
    UCHAR      bmodule_id;                  //module id number
    UCHAR      bmodule_name[8];             //user's define module name =8 CHARs
    UCHAR      bmodule_desc[32];            //module descriptions =32
    UCHAR      sevent_sip[4][4];            //event trigger IP addresses
    UCHAR      bevent_trigger[4];           //enable/disable event trigger
    UCHAR      sstream_sip[4][4];           //acvtive-send stream IP addresses
    UCHAR      bstream_active[4];           //enable/disable acvtive-send stream ,0=disbale/1=enable
    ULONG      dwstream_time_interval;      //time interval for acvtive-send
    UCHAR      bbaudrate;                   //3=1200,4=2400,5=4800,6=9600,7=19200,8=38400,9=57600,10=115200
    USHORT     wMiscOptions;                //(bit 0)save current DO status as power on value and wirte to eeprom//
                                            //(bit 1)save current DO status as safe value and wirte to eeprom//
                                            //(bit 2)enable/disable power on value function//
                                            //(bit 3)enable/disable safe value function//
                                            //(bit 4)enable/disable burn out detection //
                                            //(bit 5)DI active state 0=low active,1=high active
                                            //(bit 6)DO active state 0=low active,1=high active
                                            //(bit 7)DHCP 0=disnable,1=enable
                                            //(bit 8)WebServer 0=disnable,1=enable
                                            //(bit 9)Modbus CRC 0=disable,1=enable
                                            //(bit10)disbale/enable CJC, 0=disable/1 =enable(for EDAM5019/5039 only)
                                            //(bit11)ASCII data format 0=enginerring, 1=2's
                                            //(bit12)MODBUS data format 0=enginerring,1=2's
                                            //(bit13)Ptotocol 0=ASCI protocol,1=MODBUS protocol
                                            //(bit14~bir15) 00=50Hz,01=60Hz,10=60Hz,11=120Hz
   USHORT     wOptions;
   CHAR       sversion[38];
} MODULE_CONFIG  ;

typedef struct MODULE_CONFIGX {

    UCHAR     bmac[6];                      //mac address  where SYBTE =char
    UCHAR     bmask[4];                     //mask address
    UCHAR     bip[4];                       //IP address
    UCHAR     bgate[4];                     //gateway
    UCHAR     bmodule_id;                   //module id number
    UCHAR     bmodule_name[8];              //user's define module name =8 SBYTEs
    UCHAR     bmodule_desc[32];             //module descriptions =32
    UCHAR     sevent_sip[4][4];             //event trigger IP addresses
    UCHAR     bevent_trigger[4];            //enable/disable event trigger
    UCHAR     sstream_sip[4][4];            //acvtive-send stream IP addresses
    UCHAR     bstream_active[4];            //enable/disable acvtive-send stream ,0=disbale/1=enable
    ULONG     dwstream_time_interval;       //time interval for acvtive-send
    UCHAR     bbaudrate;                    //3=1200,4=2400,5=4800,6=9600,7=19200,8=38400,9=57600,10=115200
    USHORT    wMiscOptions;                 //(bit 0)save current DO status as power on value and wirte to eeprom//
                                            //(bit 1)save current DO status as safe value and wirte to eeprom//
                                            //(bit 2)enable/disable power on value function//
                                            //(bit 3)enable/disable safe value function//
                                            //(bit 4)enable/disable burn out detection //
                                            //(bit 5)DI active state 0=low active,1=high active
                                            //(bit 6)DO active state 0=low active,1=high active
                                            //(bit 7)DHCP 0=disnable,1=enable
                                            //(bit 8)WebServer 0=disnable,1=enable
                                            //(bit 9)Modbus CRC 0=disable,1=enable
                                            //(bit10)disbale/enable CJC, 0=disable/1 =enable(for EDAM5019/5039 only)
                                            //(bit11)ASCII data format 0=enginerring, 1=2's
                                            //(bit12)MODBUS data format 0=enginerring,1=2's
                                            //(bit13)Ptotocol 0=ASCI protocol,1=MODBUS protocol
                                            //(bit14~bir15) 00=50Hz,01=60Hz,10=60Hz,11=120Hz
   USHORT     Options;
   UCHAR      sversion[38];
   # ----------------------------------------
   UCHAR      bFixIP[4];
   UCHAR      bFixGate[4] ;
   UCHAR      bFixMask[4];
   USHORT     wDHCP_timeout;
   USHORT     wDHCP_flag  ;
   USHORT     wWebReadOnly_flag     ;       //Web page read only flag, 0=read/write, 1=read only
   # ------------------------------------------
   UCHAR      ReserveByte[32] ;
} MODULE_CONFIGX  ;


typedef struct MODULE_DATA
{
    ULONG     Din;
    ULONG     Dout;
    ULONG     DiLatch;
    ULONG     DiCounter[32];
    double    AiNormalValue[16];
    double    AiMaxValue[16];
    double    AiMinValue[16];
    USHORT    AiHighAlarmstatus;
    USHORT    AiLowAlarmstatus;
    USHORT    AiBurnOut ;                     //EDAM 5019/5015/5039 only
    double    CJCTemperature  ;               //EDAM 5019/5039 only//
    double    AoValue[16];

} MODULE_DATA;

typedef struct MODULE_IOCHANNELS
{
    UCHAR     cdevname[10];                   //User's define Module name =8 SBYTEs
    UCHAR     cIPaddress[16];
    USHORT    wAIChns;
    USHORT    wAOChns;
    USHORT    wDIChns;
    USHORT    wDOChns;

}MODULE_IOCHANNELS;

# --configuration of DI channel --
typedef struct AI_CHANNEL_CONFIG
{
    USHORT    wType;
    USHORT    wActive;
    USHORT    wInAverage;
    USHORT    wHiAlarmMode;
    USHORT    wLoAlarmMode;
    USHORT    wHiAlarmDo;
    USHORT    wLoAlarmDo;
    double    fHighLimit;
    double    fLowLimit;
} AI_CHANNEL_CONFIG;

typedef struct DI_CHANNEL_CONFIG
{
    USHORT    wType;                          //DI mode
    USHORT    wIntstatus;                     //latch Event
    USHORT    wdi_debounce_timeinterval;      //debounce time interval

} DI_CHANNEL_CONFIG;

'''

 INT E5K_GetRunTimeOS(void );

 # --Open/Close Device functions ---
 SHORT       E5K_OpenModuleUSB          (MODULE_ID Devid);
 SHORT       E5K_OpenModuleIP           (CHAR Ip[],ULONG ConnectTimeout,ULONG TxTimeout,ULONG RxTimeout);
 SHORT       E5K_OpenModuleCOM          (MODULE_ID Devid,USHORT COMport,ULONG RxTotalTimeOut,ULONG RxTimeoutInterval,ULONG Baudrate,CHAR ChksumCRC);
 E5K_STATUS  E5K_CloseModules           (void);
 E5K_STATUS  E5K_CloseModuleID          (MODULE_ID id);

 E5K_STATUS  E5K_EthernetSearchDevice(E5K_DEVICE_ID_INFO *pd,CHAR destIP[]);
 USHORT      E5K_GetHostIPConfig        (CHAR HostIP[],CHAR HostMask[],CHAR HostDesc[]) ;
 E5K_STATUS  E5K_SetHostNICAddress      (CHAR *NicIP);
 E5K_STATUS  E5K_GetLocalIP             (CHAR *ip0,CHAR *ip1,CHAR *ip2,CHAR *ip3);
 USHORT      E5K_GetLocalIPEx           (CHAR ip[]);
 USHORT      E5K_SearchModules          (E5K_DEVICE_ID_INFO *pd,USHORT interface_type );
 E5K_STATUS  E5K_IsHostIPExisted        (CHAR *bHostIP);
 E5K_STATUS  E5K_SetCurrentInterface    (MODULE_ID id,USHORT interface_type);
 E5K_STATUS  E5K_ReadCurrentInterface   (MODULE_ID id,USHORT *interface_type);
 E5K_STATUS  E5K_ReadModuleConfig       (MODULE_ID id,MODULE_CONFIG *mp);
 E5K_STATUS  E5K_ReadModuleConfigX      (MODULE_ID id,MODULE_CONFIGX *mp);
 E5K_STATUS  E5K_SetModuleConfig        (MODULE_ID id,MODULE_CONFIG  *mp);
 E5K_STATUS  E5K_SetModuleConfigX       (MODULE_ID id,MODULE_CONFIGX *mp);
 E5K_STATUS  E5K_VerifyPassWord         (MODULE_ID id ,CHAR PassWord[], USHORT length);
 E5K_STATUS  E5K_ChangePassWord         (MODULE_ID id,CHAR oldPassWord[], USHORT oldlength,CHAR newPassWord[], USHORT newlength);
 E5K_STATUS  E5K_GetLastErrorCode       (void);
 E5K_STATUS  E5K_GetErrorDescription    (USHORT werr,CHAR ErrStr[]);

 INT         E5K_StartAlarmEventIP      (CHAR *IPADDRESS) ;
 E5K_STATUS  E5K_StopAlarmEventIP       (CHAR *IPADDRESS);
 INT         E5K_StartAlarmEventUSB     (MODULE_ID id) ;
 E5K_STATUS  E5K_StopAlarmEventUSB      (MODULE_ID id);
 E5K_STATUS  E5K_ReadAlarmEventData     (ALARM_EVENT_INFO AlarmIntInfo[]);
 E5K_STATUS  E5K_ReadAlarmEventDataUSBEx(ALARM_EVENT_INFO EventIntInfo[],USHORT id);
 E5K_STATUS  E5K_ReadAlarmEventDataIPEx (ALARM_EVENT_INFO EventIntInfo[],CHAR TargetIP[]);

 LONG        E5K_StartStreamEvent       (CHAR *IPADDRESS) ;
 E5K_STATUS  E5K_StopStreamEvent        (CHAR *IPADDRESS);
 E5K_STATUS  E5K_ReadStreamEventData    (STREAM_EVENT_INFO StreamIntInfo[]);
 E5K_STATUS  E5K_ReadStreamEventDataEx  (STREAM_EVENT_INFO StreamIntInfo[],CHAR TargetIP[]);

 E5K_STATUS  E5K_GetSYSVersion          (USHORT *Major,USHORT *Minor);
 E5K_STATUS  E5K_GetDLLVersion          (USHORT *Major,USHORT *Minor);
 E5K_STATUS  E5K_ReadAllDataFromModule  (MODULE_ID id ,MODULE_DATA *mp);
 E5K_STATUS  E5K_GetModuleIOChannels    (MODULE_ID id,MODULE_IOCHANNELS *mp);

 # --ASCII command functions--
 E5K_STATUS  E5K_SendASCRequestAndWaitResponse( MODULE_ID id, CHAR asccmd[], CHAR response[],USHORT rxbuffersize);
 E5K_STATUS  E5K_RecvASCII              (MODULE_ID id ,CHAR Rxbuffer[],USHORT BufferSize);
 E5K_STATUS  E5K_SendASCII              (MODULE_ID id ,UCHAR asccmd[]);

 # --MODBUS functions--
 E5K_STATUS  E5K_WriteModBusDiscrete    (MODULE_ID id,USHORT startaddr,USHORT counts, CHAR Discrete[]);
 E5K_STATUS  E5K_WriteModBusRegister    (MODULE_ID id,USHORT startaddr,USHORT counts, SHORT regs[]);
 E5K_STATUS  E5K_ReadModBusRegister     (MODULE_ID id,USHORT startaddr,USHORT counts, SHORT regs[]);
 E5K_STATUS  E5K_ReadModBusDiscrete     (MODULE_ID id,USHORT startaddr,USHORT counts, CHAR Discrete[]);
 E5K_STATUS  E5K_SendHEXRequestAndWaitResponse( MODULE_ID id , CHAR cTxData[],USHORT wTxlen, CHAR cRxdata[],USHORT *wRxlen,USHORT buffersize);
 E5K_STATUS  E5K_CalculateCRC16         (UCHAR bData[], USHORT wLen, USHORT *wCRC);
 E5K_STATUS  E5K_SendHEX                (MODULE_ID id , CHAR cTxData[],USHORT wTxlen);
 E5K_STATUS  E5K_RecvHEX                (MODULE_ID id ,CHAR Rxbuffer[],USHORT *wRxlen,USHORT BufferSize);

 # --DI functions--
 E5K_STATUS  E5K_SetDIChannelConfig     (MODULE_ID id ,USHORT chn,DI_CHANNEL_CONFIG *Mode);
 E5K_STATUS  E5K_ReadDIChannelConfig    (MODULE_ID id ,USHORT chn,DI_CHANNEL_CONFIG *Mode);
 E5K_STATUS  E5K_ReadDIStatus           (MODULE_ID id ,ULONG *Didata);
 E5K_STATUS  E5K_ReadDILatch            (MODULE_ID id ,ULONG *Dilatch);
 E5K_STATUS  E5K_ClearAllDILatch        (MODULE_ID id);
 E5K_STATUS  E5K_ClearSingleDICounter   (MODULE_ID id ,USHORT chan);
 E5K_STATUS  E5K_ReadMultiDICounter     (MODULE_ID id,USHORT startchn,USHORT counts, ULONG counterval[]);
 E5K_STATUS  E5K_ReadDIDebounceMode     (MODULE_ID id,USHORT *Mode);
 E5K_STATUS  E5K_SetDIDebounceMode      (MODULE_ID id,USHORT Mode);

 # --DO functions--
 E5K_STATUS  E5K_WriteDO                (MODULE_ID id,ULONG dodata);
 E5K_STATUS  E5K_ReadDOStatus           (MODULE_ID id,ULONG *doval);
 E5K_STATUS  E5K_SetDOSingleChannel     (MODULE_ID id,USHORT chano,UCHAR status);
 E5K_STATUS  E5K_SetDOPulseWidth        (MODULE_ID id,USHORT Dochn,USHORT highInterval, USHORT LowInterval);
 E5K_STATUS  E5K_StartDOPulse           (MODULE_ID id,USHORT Dochn,USHORT Pulses);
 E5K_STATUS  E5K_StartMultipleDOPulse   (USHORT id,ULONG Dochnbit,USHORT Pulses[]);
 E5K_STATUS  E5K_ReadDOPulseWidth       (MODULE_ID id,USHORT Dochn,USHORT *highInterval, USHORT *LowInterval);
 E5K_STATUS  E5K_StopDOPulse            (MODULE_ID id,USHORT Dochn);
 E5K_STATUS  E5K_ReadDOPulseCount       (MODULE_ID id,USHORT Dochn,USHORT *counts);
 E5K_STATUS  E5K_SetDOPowerOnValue      (MODULE_ID id,ULONG PowerOnValue);
 E5K_STATUS  E5K_ReadDOPowerOnValue     (MODULE_ID id,ULONG *PowerOnValue);
 E5K_STATUS  E5K_SetDOMultipleChannels  (MODULE_ID id,ULONG dwActchn,UCHAR bMode);

 # --DI/O functions
 E5K_STATUS  E5K_ReadDIOActiveLevel     (MODULE_ID id,CHAR  *DIActiveval,CHAR  *DOActiveval);
 E5K_STATUS  E5K_SetDIOActiveLevel      (MODULE_ID id,CHAR  DIActiveval,CHAR DOActiveval);

 # --A/D functions--
 E5K_STATUS  E5K_ReadAIChannelType      (MODULE_ID id,USHORT AIChannel,USHORT *AIType);
 E5K_STATUS  E5K_SetAIChannelType       (MODULE_ID id,USHORT AIChannel,USHORT AItype);
 E5K_STATUS  E5K_SetSingleChannelColdJunctionOffset (MODULE_ID id ,USHORT chno,double Cjtemp);
 E5K_STATUS  E5K_ReadSingleChannelColdJunctionOffset(MODULE_ID id,USHORT chno,double *CJoffset);
 E5K_STATUS  E5K_ReadMultiChannelColdJunctionOffset (MODULE_ID id ,USHORT startch,USHORT chcounts,double *Cjtemp);
 E5K_STATUS  E5K_SetMultiChannelColdJunctionOffset  (MODULE_ID id ,USHORT startch,USHORT counts,double *Cjtemp);
 E5K_STATUS  E5K_ReadColdJunctionTemperature(MODULE_ID id,double *CJtemp);
 E5K_STATUS  E5K_ReadColdJunctionStatus     (MODULE_ID id ,CHAR *Cjs);
 E5K_STATUS  E5K_SetColdJunction            (MODULE_ID  id,CHAR opt);
 E5K_STATUS  E5K_ReadAIChannelConfig        (MODULE_ID id ,USHORT chno,AI_CHANNEL_CONFIG *mType);
 E5K_STATUS  E5K_SetAIChannelConfig         (MODULE_ID id ,USHORT ch,AI_CHANNEL_CONFIG *MC);
 E5K_STATUS  E5K_ReadAINormalMultiChannel   (MODULE_ID id ,USHORT startch,USHORT counts,double *AItemp);
 E5K_STATUS  E5K_ReadAIBurnOutStatus        (MODULE_ID id ,USHORT *status);
 E5K_STATUS  E5K_ReadAIAlarmStatus          (MODULE_ID  id,USHORT *HiAlarm,USHORT *LoAlarm);
 E5K_STATUS  E5K_SetAIBurnOut               (MODULE_ID id ,CHAR setting);
 E5K_STATUS  E5K_ReadAIBurnOut              (MODULE_ID id ,CHAR *setting);
 E5K_STATUS  E5K_SetAIModuleFilter          (MODULE_ID id ,USHORT Hz);
 E5K_STATUS  E5K_ReadAIModuleFilter         (MODULE_ID id ,USHORT *Hz);
 E5K_STATUS  E5K_SetAIChannelEnable         (MODULE_ID id ,USHORT AIstatus);
 E5K_STATUS  E5K_ReadAIChannelEnable        (MODULE_ID id ,USHORT *AIstatus);
 E5K_STATUS  E5K_ReadAIMaximumMultiChannel  (MODULE_ID id ,USHORT start,USHORT count,double *AItemp);
 E5K_STATUS  E5K_ReadAIMinimumMultiChannel  (MODULE_ID id ,USHORT start,USHORT count,double *AItemp);
 E5K_STATUS  E5K_ResetAIMaximum             (MODULE_ID  id,USHORT Resetopt);
 E5K_STATUS  E5K_ResetAIMinimum             (MODULE_ID id ,USHORT Restopt);
 E5K_STATUS  E5K_ResetAIHighAlarm           (MODULE_ID id ,USHORT clearoption);
 E5K_STATUS  E5K_ResetAILowAlarm            (MODULE_ID  id,USHORT clearoption);
 E5K_STATUS  E5K_CalibrateAIZeroSpan        (MODULE_ID  id,USHORT Calchno,CHAR Adtype);
 E5K_STATUS  E5K_ReadAIChannelAverage       (MODULE_ID  id,USHORT *AIaverage);
 E5K_STATUS  E5K_SetAIChannelAverage        (MODULE_ID  id,USHORT Option);

 # --LED functions--
 E5K_STATUS  E5K_SetLEDControl              (MODULE_ID id,CHAR ControlOption);
 E5K_STATUS  E5K_WriteDataToLED             (MODULE_ID id,ULONG LedData);
 E5K_STATUS  E5K_FlashLED                   (MODULE_ID id,ULONG LedData,USHORT FlashCounts);

# --- Advanced TCP/IP functions for multiple NIC cards --------------------------------
 SHORT       E5K_OpenModuleIPEx      (CHAR Ip[],ULONG ConnectTimeout,ULONG TxTimeout,ULONG RxTimeout,CHAR HostIP[]);
 USHORT      E5K_IsIPInLocalSubnetEx (CHAR *bRemoteIP,CHAR HostIp[]);
 SOCKET      E5K_TCPConnectEx        (CHAR szIP[], u_short port,INT iConnectionTimeout,INT iSendTimeout,INT iReceiveTimeout,CHAR HostIP[]);
 SOCKET      E5K_UDPConnectEx        (CHAR szIP[],u_short s_port,u_short d_port,INT iConnectionTimeout,INT iSendTimeout,INT iReceiveTimeout,BOOL *Insubnet,CHAR HostIP[]);
 LONG        E5K_StartStreamEventEx  (CHAR *TargetIP,CHAR *HostIP) ;
 LONG        E5K_StartAlarmEventIPEx (CHAR *TargetIP,CHAR *HostIP) ;

# ---- TCP --------------------------------------------------------------------------
 USHORT      E5K_IsValidIPAddress   (CHAR *bRemoteIP);
 USHORT      E5K_IsIPInLocalSubnet   (CHAR *bRemoteIP);
 USHORT      E5K_TCPSendData         (SOCKET sock,CHAR *pData,u_short wDataLen);
 USHORT      E5K_TCPRecvData         (SOCKET sock,CHAR *pData,u_short wBufferLen);
 USHORT      E5K_TCPPing             (CHAR zIP[],INT timeout);
 USHORT      E5K_TCPAllDisconnect    (void);
 USHORT      E5K_TCPDisconnect       (SOCKET sock);
 SOCKET      E5K_TCPConnect          (CHAR szIP[], u_short port,INT iConnectionTimeout,INT iSendTimeout,INT iReceiveTimeout);

# ---- UDP ----------------------------------------------------------------------------
 USHORT      E5K_UDPSendData         (SOCKET sock,CHAR *pData,u_short wDataLen);
 USHORT      E5K_UDPRecvData         (SOCKET sock,CHAR *pData,u_short wBufferLen);
 USHORT      E5K_UDPSendASCStr       (SOCKET  sock,CHAR *pstrData);
 USHORT      E5K_UDPRecvASCStr       (SOCKET  sock,CHAR *pstrData,u_short wStrbufferlen);
 USHORT      E5K_UDPDisconnect       (SOCKET  sock);
 USHORT      E5K_UDPAllDisconnect    (void);
 SOCKET      E5K_UDPConnect         (CHAR szIP[],u_short s_port,u_short d_port,INT iConnectionTimeout,INT iSendTimeout,INT iReceiveTimeout,BOOL *Insubnet);
# ---- COMM Port ----------------------------------------------------------------------
 INT         COMM_Write              (INT ComPortNumber,UCHAR *pBuf,INT Buflen);
 INT         COMM_Read               (INT ComPortNumber,UCHAR *pBuf,INT Buflen);
 INT         COMM_ReadASCII          (INT ComPortNumber,UCHAR *pBuf,INT Buflen);
 INT         COMM_Close              (INT ComPortNumber);
 INT         COMM_Open               (INT ComPortNumber,LONG baudrate, LONG rxTotalTime,LONG rxTimeOutInterval);
 INT         COMM_ClearRX            (INT ComPortNumber);
 E5K_STATUS  WINAPI E5K_SetRXTimeOutOption  (ULONG RxTotalTimeout,ULONG RxChrTimeOutInterval);
 INT         COMM_SetRxTotalTimeOut  (INT ComPortNumber, LONG RxTotalTimeOut) ;//,long RxCharElapseTime);
 LONG        COMM_ReadRxTotalTimeOut (INT comp);
 INT         COMM_SetRxCharElapseTime(INT comp, LONG RxCharElapseTime);
 LONG        COMM_ReadRxCharElapseTime(INT comp);
 ULONG       COMM_FileOpen           (CHAR *Filename);
 void        COMM_FileClose          (void);
 ULONG       COMM_FileRead           (CHAR *pbuf,ULONG Fileoffset,ULONG bufLen);

# ---- PGM ----------------------------------------------------------------------
 ULONG       E5K_USBPgmOpen          (CHAR *DevInfo);  //0 to 63
 INT         E5K_USBPgmClose         (ULONG hfile);
 USHORT      E5K_USBPgmWrite         (ULONG hFile,CHAR *buffer,USHORT size);
 USHORT      E5K_USBPgmRead          (ULONG hFile,CHAR *buffer,USHORT BufferSize, ULONG timeout);

# -- Reserved for calibration, Do not use following functions in your application
E5K_STATUS   E5K_WriteAICalibrationCoefficient (MODULE_ID  id,ULONG Coefficient,CHAR Regtype);
E5K_STATUS   E5K_ReadAICalibrationCoefficient  (MODULE_ID  id,ULONG *Coefficient,CHAR Regtype);
INT          E5K_BuildHtmFileSystemX           (CHAR *CfgFileName,CHAR *OutFileName,CHAR  *Errmsg);
void         E5K_DebugPrint (char *s);

#ifdef __cplusplus
  }
#endif

#endif

