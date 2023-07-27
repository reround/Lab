#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test.py
@Time    :   2023/07/20 16:19
@Author  :   shun
@Description  :   用于测试
'''

import time

import serial
from apparatus import DoubleRelay, Pump


pump = Pump(port="COM3",
            baudrate=9600,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_TWO,
            timeout=0.5)
pump.choose_speed(50)
time.sleep(0.1)
pump.close()

if __name__ == '__main__':
    relay = DoubleRelay(port="COM2",
                        baudrate=9600,
                        bytesize=serial.EIGHTBITS,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_TWO,
                        timeout=0.5)
    func = {
        "1": relay.relay_1_start,
        "2": relay.relay_1_stop,
        "3": relay.relay_1_flick,
        "4": relay.relay_2_start,
        "5": relay.relay_2_stop,
        "6": relay.relay_2_flick,
        "7": relay.all_start,
        "8": relay.all_stop,
        "9": exit
    }

    while True:
        print("""
            "1": relay.relay_1_start,
            "2": relay.relay_1_stop,
            "3": relay.relay_1_flick,
            "4": relay.relay_2_start,
            "5": relay.relay_2_stop,
            "6": relay.relay_2_flick,
            "7": relay.all_start,
            "8": relay.all_stop,
            "9": exit
            """)
        opt = input("::>")
        if opt in func.keys():
            func[opt]()
        else:
            print("no opt")
