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


class DoubleRelay(serial.rs485.RS485):
    """
    双路继电器 \n
    继承 serial.rs485.RS485 

    :param _type_ serial: _description_
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # 设置地址
        self.set_addr()

    def set_addr(self, addr="01"):
        """
        设置双路继电器地址
        
        """
        self.addr = addr
        self.set_addr_command = "FE " + self.addr + " FF"
        self.relay_1_start_command = self.addr + " AA FF"
        self.relay_1_stop_command = self.addr + " BB FF"
        self.relay_1_flick_command = self.addr + " CC FF"
        self.relay_2_start_command = self.addr + " DD FF"
        self.relay_2_stop_command = self.addr + " EE FF"
        self.relay_2_flick_command = self.addr + " FF FF"

    def switch(self):
        """
        判断串口是否打开
        """
        if self.isOpen():
            print("串口打开成功。")
            print("绑定串口名称：", double_relay.name)
        else:
            print("打开串口失败。")

    def relay_1_start(self):
        """
        启动一号继电器
        """
        self.write(bytes.fromhex(self.relay_1_start_command))

    def relay_1_stop(self):
        """
        关闭一号继电器
        """
        self.write(bytes.fromhex(self.relay_1_stop_command))

    def relay_1_flick(self):
        """
        一号继电器点动
        """
        self.write(bytes.fromhex(self.relay_1_flick_command))

    def relay_2_start(self):
        """
        启动二号继电器
        """
        self.write(bytes.fromhex(self.relay_2_start_command))

    def relay_2_stop(self):
        """
        关闭二号继电器
        """
        self.write(bytes.fromhex(self.relay_2_stop_command))

    def relay_2_flick(self):
        """
        二号继电器点动
        """
        self.write(bytes.fromhex(self.relay_2_flick_command))

    def all_start(self):
        """
        启动所有继电器
        """
        self.relay_1_start()
        self.relay_2_start()

    def all_stop(self):
        """
        关闭所有继电器
        """
        self.relay_1_stop()
        self.relay_2_stop()
        
    def all_flick(self):
        """
        所有继电器点动
        """
        self.relay_1_flick()
        self.relay_2_flick()

    def read_addr(self):
        """
        读取继电器地址

        :return _type_: 双路继电器地址
        """
        return self.addr


class SingleRelay(serial.rs485.RS485):
    """
    单路继电器 \n
    继承 serial.rs485.RS485 

    :param _type_ serial: _description_
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # 设置地址
        self.set_addr()

    def set_addr(self, addr="01"):
        """
        设置继电器地址
        
        """
        self.addr = addr
        self.set_addr_command = "FE " + self.addr + " FF"
        self.relay_start_command = self.addr + " AA FF"
        self.relay_stop_command = self.addr + " BB FF"
        self.relay_flick_command = self.addr + " CC FF"

    def switch(self):
        """
        判断串口是否打开
        """
        if self.isOpen():
            print("串口打开成功。")
            print("绑定串口名称：", double_relay.name)
        else:
            print("打开串口失败。")

    def relay_start(self):
        """
        启动继电器
        """
        self.write(bytes.fromhex(self.relay_start_command))

    def relay_stop(self):
        """
        关闭继电器
        """
        self.write(bytes.fromhex(self.relay_stop_command))

    def relay_flick(self):
        """
        继电器点动
        """
        self.write(bytes.fromhex(self.relay_flick_command))

    def read_addr(self):
        """
        读取继电器地址

        :return _type_: 继电器地址
        """
        return self.addr


if __name__ == "__main__":

    try:
        double_relay = DoubleRelay(port="COM2",
                                   baudrate=9600,
                                   bytesize=serial.EIGHTBITS,
                                   parity=serial.PARITY_NONE,
                                   stopbits=serial.STOPBITS_TWO,
                                   timeout=0.5)
    except Exception as e:
        print(e)
    else:
        double_relay.switch()
        double_relay.set_addr(addr="02")
        double_relay.relay_1_stop()
        pass
    finally:
        time.sleep(0.1)
        double_relay.close()

    # print_comport()
