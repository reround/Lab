#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   pump.py
@Time    :   2023/07/25 23:33
@Author  :   shun
@Description  :   蠕动泵
'''
import time
import serial.tools.list_ports
import serial.rs485

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
        self.write(bytes.fromhex("01 06 00 04 00 01 09 CB"))
        
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
        ...
    
    def choose_flow(self, flow):
        ...
    

if __name__ == '__main__':
    pass