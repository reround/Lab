#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   apparatus.py
@Time    :   2023/07/25 17:21
@Author  :   shun
@Description  :   定义两个继电器
'''

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


class SingleRelay(serial.rs485.RS485):
    """
    单路继电器 \n
    继承 serial.rs485.RS485 

    :param _type_ serial: _description_
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.wait_time = 0.1

        self.addr = "01"
        self.set_addr_command = "FE " + self.addr + " FF"
        self.relay_start_command = self.addr + " AA FF"
        self.relay_stop_command = self.addr + " BB FF"
        self.relay_flick_command = self.addr + " CC FF"

    def set_addr(self, addr):
        """
        设置继电器地址
        
        """
        self.addr = addr
        self.set_addr_command = "FE " + self.addr + " FF"
        self.relay_start_command = self.addr + " AA FF"
        self.relay_stop_command = self.addr + " BB FF"
        self.relay_flick_command = self.addr + " CC FF"

        self.write(bytes.fromhex(self.set_addr_command))
        time.sleep(self.wait_time)

    def switch(self):
        """
        判断串口是否打开
        """
        if self.isOpen():
            print("串口打开成功。")
            print("绑定串口名称：", self.name)
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


class DoubleRelay(serial.rs485.RS485):
    """
    双路继电器 \n
    继承 serial.rs485.RS485 

    :param _type_ serial: _description_
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.wait_time = 0.1

        self.addr = "01"
        self.set_addr_command = "FE " + self.addr + " FF"
        self.relay_1_start_command = self.addr + " AA FF"
        self.relay_1_stop_command = self.addr + " BB FF"
        self.relay_1_flick_command = self.addr + " CC FF"
        self.relay_2_start_command = self.addr + " DD FF"
        self.relay_2_stop_command = self.addr + " EE FF"
        self.relay_2_flick_command = self.addr + " FF FF"

    def set_addr(self, addr):
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

        self.write(bytes.fromhex(self.set_addr_command))
        time.sleep(self.wait_time)

    def switch(self):
        """
        判断串口是否打开
        """
        if self.isOpen():
            print("串口打开成功。")
            print("绑定串口名称：", self.name)
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
        time.sleep(self.wait_time)
        self.relay_2_start()

    def all_stop(self):
        """
        关闭所有继电器
        """
        self.relay_1_stop()
        time.sleep(self.wait_time)
        self.relay_2_stop()

    def read_addr(self):
        """
        读取继电器地址

        :return _type_: 双路继电器地址
        """
        return self.addr


class Pump(serial.rs485.RS485):
    """
    蠕动泵 \n
    继承 serial.rs485.RS485 

    :param _type_ serial: _description_
    
    1. 转速设定：01 06 00 01 13 88 D5 5C   设定转速为:50RPM.
    2. 启动：01 06 00 04 00 01 09 CB
    3. 停止：01 06 00 04 00 00 C8 0B
    4. 全速：01 06 00 04 00 02 49 CA
    5. 流量设定：01 10 00 02 00 02 04 02 25 51 00 5F 95   设定流量为：36ml/min

    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.wait_time = 0.1

        self.addr = "01"
        self.speed = "00"
        self.flow = "00"

        self.speed_command = ""
        self.flow_command = ""

    def start(self):
        """
        启动蠕动泵
        """
        self.write(bytes.fromhex("01 06 00 04 10 00 C5 CB"))

    def stop(self):
        """
        关闭蠕动泵
        """
        self.write(bytes.fromhex("01 06 00 04 00 00 C8 0B"))

    def full_speed(self):
        """
        全速运行
        """
        self.write(bytes.fromhex("01 06 00 04 00 02 49 CA"))

    def choose_speed(self, speed):
        """
        选择速度，单位是 RPM, 分辨率 0.01 \n
        范围 0.01 RPM - 100 RPM

        :param _type_ speed: _description_
        """
        speed = str(hex(speed * 100))[2:].rjust(4, "0")
        speed = "01 06 00 01 " + speed + "D5 5C"
        self.write(bytes.fromhex(speed))

    def choose_flow(self, flow):
        """
        选择流量，单位是 ml/min

        :param _type_ flow: _description_
        """
        flow = str(hex(flow * 1000000))[2:].rjust(8, "0")
        flow = "01 10 00 02 00 02 04 " + flow + " 5F 95"
        self.write(bytes.fromhex(flow))


if __name__ == "__main__":

    ...
    # print_comport()
