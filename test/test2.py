# import serial
import time
import serial.tools.list_ports
import serial.rs485
import serial



def print_comport():
    """
    打印串口信息
    """
    ports_list = list(serial.tools.list_ports.comports())
    if len(ports_list) <= 0:
        print("无串口设备。")
    else:
        print("可用串口设备：")
        for comport in ports_list:
            print(list(comport)[0], list(comport)[1])

# 命令
open_1 = "01 05 00 00 FF 00 8C 3A"
message_close_1 = "01 05 00 00 00 00 CD CA"
open_2 = "01 05 00 01 FF 00 DD FA"
close_2 = "01 05 00 01 00 00 9C 0A"
all_open = "01 0F 00 00 00 08 01 FF BE D5"
all_close = "01 0F 00 00 00 08 01 00 FE 95"

try:
    double_relay = serial.Serial(port="COM2",
                                 baudrate=9600,
                                 bytesize=serial.EIGHTBITS,
                                 parity=serial.PARITY_NONE,
                                 stopbits=serial.STOPBITS_TWO,
                                 timeout=0.5)
    # double_relay.rs485_mode = serial.rs485.RS485Settings()

    # 判断串口是否打开
    if double_relay.isOpen():
        print("串口打开成功。")
        print("绑定串口名称：", double_relay.name)
    else:
        print("打开串口失败。")

    while True:
        time.sleep(0.05)

        num = double_relay.in_waiting
        
        if num > 0:
            data = double_relay.read(num)

            print(data)
            
except Exception as e:
    print(e)