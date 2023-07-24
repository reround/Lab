import time
import serial.tools.list_ports
import serial.rs485


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


# TODO 指令（待验证）

message_open_1 = "01 05 00 00 FF 00 8C 3A"
message_close_1 = "01 05 00 00 00 00 CD CA"
message_open_2 = "01 05 00 01 FF 00 DD FA"
message_close_2 = "01 05 00 01 00 00 9C 0A"
message_all_open = "01 0F 00 00 00 08 01 FF BE D5"
message_all_close = "01 0F 00 00 00 08 01 00 FE 95"


class double_relay(serial.rs485.RS485):
    """
    双路继电器 \n
    继承 serial.rs485.RS485 

    :param _type_ serial: _description_
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def switch(self):
        """
        判断串口是否打开
        """
        if self.isOpen():
            print("串口打开成功。")
            print("绑定串口名称：", double_relay.name)
        else:
            print("打开串口失败。")

    def open_1(self):
        """
        打开一号继电器
        """
        self.write(bytes.fromhex(message_open_1))

    def close_1(self):
        """
        关闭一号继电器
        """
        self.write(bytes.fromhex(message_close_1))

    def open_2(self):
        """
        打开二号继电器
        """
        self.write(bytes.fromhex(message_open_2))

    def close_2(self):
        """
        关闭二号继电器
        """
        self.write(bytes.fromhex(message_close_2))

    def bytes2str(self, data):
        data = str(data)
        print(data)
        print(data[2:-1])


if __name__ == "__main__":

    try:
        double_relay = double_relay(port="COM1",
                                    baudrate=9600,
                                    bytesize=serial.EIGHTBITS,
                                    parity=serial.PARITY_NONE,
                                    stopbits=serial.STOPBITS_TWO,
                                    timeout=0.5)
    except Exception as e:
        print(e)
    else:
        double_relay.switch()
        double_relay.open_1()
        double_relay.bytes2str(b"\xFF")
    finally:
        double_relay.close()
