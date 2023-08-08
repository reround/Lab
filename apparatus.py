#!/c/Users/shun/AppData/Local/Programs/Python/Python38/python
# -*- encoding: utf-8 -*-
'''
@File    :   apparatus.py
@Time    :   2023/07/25 17:21
@Author  :   shun
@Description  :   TODO
'''

import time

import serial.tools.list_ports
import serial.rs485

from functools import reduce


def print_comport():
    """
    打印串口信息
    """
    ports_list = list(serial.tools.list_ports.comports())
    if len(ports_list) <= 0:
        print("无串口设备。")
    else:
        # print(list(ports_list))
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

        self.baudrate = 9600
        self.bytesize = serial.EIGHTBITS
        self.parity = serial.PARITY_NONE
        self.stopbits = serial.STOPBITS_TWO

        self.wait_time = 0.3

        self.addr = "01"
        self.set_addr_command = "FE " + self.addr + " FF"
        self.relay_start_command = self.addr + " AA FF"
        self.relay_stop_command = self.addr + " BB FF"
        self.relay_flick_command = self.addr + " CC FF"

    def set_addr(self, addr: int):
        """
        设置继电器地址

        :param _type_ addr: 新地址
        """
        if 1 > addr > 255:
            raise (Exception("地址错误：1 - 255"))

        self.addr = hex(addr)[2:].rjust(2, "0")
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


class DoubleRelay(serial.rs485.RS485):
    """
    双路继电器 \n
    继承 serial.rs485.RS485 

    :param _type_ serial: _description_
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.baudrate = 9600
        self.bytesize = serial.EIGHTBITS
        self.parity = serial.PARITY_NONE
        self.stopbits = serial.STOPBITS_TWO

        self.wait_time = 0.3

        self.addr = "01"
        self.set_addr_command = "FE " + self.addr + " FF"
        self.relay_1_start_command = self.addr + " AA FF"
        self.relay_1_stop_command = self.addr + " BB FF"
        self.relay_1_flick_command = self.addr + " CC FF"
        self.relay_2_start_command = self.addr + " DD FF"
        self.relay_2_stop_command = self.addr + " EE FF"
        self.relay_2_flick_command = self.addr + " FF FF"

    def set_addr(self, addr: int):
        """
        设置双路继电器地址
        
        :param _type_ addr: 新地址
        """
        if 1 > addr > 255:
            raise (Exception("地址错误：1 - 255"))

        self.addr = hex(addr)[2:].rjust(2, "0")
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


class Pump(serial.rs485.RS485):
    """
    蠕动泵 \n
    继承 serial.rs485.RS485 
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.baudrate = 1200
        self.bytesize = serial.EIGHTBITS
        self.stopbits = serial.STOPBITS_ONE
        self.parity = serial.PARITY_EVEN

        self.wait_time = 0.5

        # 速度
        self.speed = ""
        # 流量
        self.flow = ""

        # 帧头
        self.FLAG = "E9"
        # 地址，默认为 "01"
        self.addr: str = "01"
        # pdu的长度
        self.len = "00"
        # pdu格式 应用层编码数据内容
        self.pdu = ""
        # 校验 ：addr、 len 、pdu的异或
        self.fcs = ""
        # 指令字符串
        self.command = ""
        # 应答字符串
        self.response = ""

        # 启停状态 启动："1"，停止："0"。
        # 全速状态 全速运行："1"，正常运行："0"。
        # self.state = 全速状态 + 启停状态
        self.RUN = "01"
        self.STOP = "00"
        self.state = self.STOP
        # 转动方向 direction
        # 顺时针：CLOCK "01"
        # 逆时针：ANTICLOCK "00"
        self.CLOCK = "01"
        self.ANTICLOCK = "00"
        self.direction = self.CLOCK
        # 泵头编号
        self.head_num = "05"
        # 软管编号 01 - 16
        self.hose_num = "05"

        # 操作码
        # C 、D 、I 、L 、R 、W 、X
        # 43、44、49、4C、52、57、58
        self.opt = {
            "XL": "584C",
            "DL": "444C",
            "WL": "574C",
            "RL": "524C",
            "CL": "434C",
            "WID": "574944",
            "RID": "524944"
        }

    def switch(self):
        """
        判断串口是否打开
        """
        if self.isOpen():
            print("串口打开成功。")
            print("绑定串口名称：", self.name)
        else:
            print("打开串口失败。")

    def get_fcs(self, strr: str) -> str:
        """
        根据规则计算异或校验值，返回异或校验值。

        :param _type_ strr: 需要添加异或校验值计算的指令
        :return str: 返回异或校验值
        """

        def xor(x, y):
            return x ^ y

        strr = bytes.fromhex(strr)
        strr = hex(reduce(xor, strr[1:]))
        return strr[2:].rjust(2, "0")

    def modify(self, command: str) -> str:
        """
        替换规则： E9 -> E8 01 , E8 -> E8 00 .

        :param str command: 需要修饰的指令
        :return str: 修饰后的指令
        """
        command = command.replace(" ", "").upper()
        index = 2
        while index < len(command):

            if command[index:index + 2] == "E9":
                command = command[:index] + "E801" + command[index + 2:]
                index += 2
            elif command[index:index + 2] == "E8":
                command = command[:index] + "E800" + command[index + 2:]
                index += 2
            index += 2
        return command

    def demodify(self, command: bytes) -> bytes:
        """
        恢复指令 \n
        替换规则： E8 01 -> E9 , E8 00 -> E8.

        :param str command: 需要恢复的指令
        :return str: 恢复的指令
        """
        temp = bytearray()

        index = 1
        while index < len(command):
            if command[index] != 232:
                temp.append(command[index])
            else:
                if command[index + 1] == 0:
                    temp.append(232)
                else:
                    temp.append(233)
                index += 1
            index += 1
        temp.insert(0, 233)
        return bytes(temp)

    def set_speed(self, speed: float) -> str:
        """
        设置速度，单位是 RPM, 分辨率 0.1 \n
        范围 10 RPM - 1000 RPM

        :param _type_ speed: 应答 "XL"
        """
        if speed < 10 or speed > 1000:
            raise (Exception("速度范围错误：10 - 1000"))

        # 转为字符串
        speed = str(speed)
        speed = speed.split(".")
        if len(speed) > 1:
            len_ = len(speed[1])
            if len_ > 1:
                raise (Exception("分辨率为 0.1"))
            else:
                speed = speed[0] + speed[1]
        else:
            speed = speed[0] + "0"

        speed = hex(int(speed))[2:].rjust(4, "0")
        if self.state == self.STOP:
            self.state = self.RUN
        self.len = "06"
        self.pdu = self.opt["XL"] + speed + self.state + self.direction
        self.command = self.FLAG + self.addr + self.len + self.pdu
        self.fcs = self.get_fcs(self.command)
        self.command = self.modify(self.command + self.fcs)
        print("->", self.command)
        self.write(bytes.fromhex(self.command))

        time.sleep(self.wait_time)

        if self.in_waiting != 0:
            self.response = str(
                self.demodify(self.read(self.in_waiting))[3:5])[2:4]
            print("<-", self.response)
            return self.response
        return ""

    #* 在停止时：运行状态 00 、运行方向 00
    #* 在运行时：有待分析
    def get_speed(self) -> int:
        """
        获取转速(float)、运行状态(str)、运行方向(str)

        :return int:DL、转速、运行状态、运行方向
        """
        self.len = "02"
        self.pdu = self.opt["DL"]
        self.command = self.FLAG + self.addr + self.len + self.pdu
        self.fcs = self.get_fcs(self.command)
        self.command = self.modify(self.command + self.fcs)
        print("->", self.command)
        self.write(bytes.fromhex(self.command))

        time.sleep(self.wait_time)

        if self.in_waiting != 0:
            data = self.demodify(self.read(self.in_waiting))
            print(data)
            self.response = str(data[3:5])[2:4]
            self.speed = int.from_bytes((data[5:7]), byteorder='big') / 10
            self.state = hex(int.from_bytes(data[7:8],
                                            byteorder='big'))[2:].rjust(
                                                2, "0")
            self.direction = hex(int.from_bytes(data[8:9],
                                                byteorder='big'))[2:].rjust(
                                                    2, "0")
            print("<-", self.response, self.speed, self.state, self.direction)
            return self.response, self.speed, self.state, self.direction
        return ""

    def set_flow(self, flow: int, hose_num: int, direction: str):
        """
        流量的单位为 nL/min，即 1 表示 1 nL/min \n
        1 L = 1e3 mL = 1e6 uL = 1e9 nL

        :param _type_ flow: 流量
        :param _type_ hose_num: 软管编号
        :param _type_ direction: 运行方向
        :return _type_: "WL"、实际流量
        """
        if hose_num < 1 or hose_num > 16:
            raise (Exception("软管编号错误：1 - 16 ."))

        #! 如果软管只有一个编号，那么可以直接使用软管编号属性
        hose_num = hex(hose_num)[2:].rjust(2, "0")
        flow = hex(flow)[2:].rjust(8, "0")

        self.state = self.RUN
        self.direction = direction
        self.len = "0A"
        self.hose_num = hose_num
        self.pdu = self.opt[
            "WL"] + flow + self.state + self.direction + self.head_num + self.hose_num
        self.command = self.FLAG + self.addr + self.len + self.pdu
        self.fcs = self.get_fcs(self.command)
        self.command = self.modify(self.command + self.fcs)
        print("->", self.command)
        self.write(bytes.fromhex(self.command))

        time.sleep(self.wait_time)

        if self.in_waiting != 0:
            data = self.demodify(self.read(self.in_waiting))
            self.response = str(data[3:5])[2:4]
            real_flow = int.from_bytes((data[5:7]), byteorder='big')

            print("<-", self.response, real_flow)
            return self.response, real_flow
        return ""

    def get_flow(self):
        """
        获取流量(int, nL/min)、运行状态(str)、运行方向(str)、泵头编号(str)、软管编号(str)

        :return _type_:"RL"、流量、运行状态、运行方向、泵头编号、软管编号
        """
        self.len = "02"
        self.pdu = self.opt["RL"]
        self.command = self.FLAG + self.addr + self.len + self.pdu
        self.fcs = self.get_fcs(self.command)
        self.command = self.modify(self.command + self.fcs)
        print("->", self.command)
        self.write(bytes.fromhex(self.command))

        time.sleep(self.wait_time)

        if self.in_waiting != 0:
            data = self.demodify(self.read(self.in_waiting))
            self.response = str(data[3:5])[2:4]
            self.flow = int.from_bytes((data[5:9]), byteorder='big')
            self.state = hex(int.from_bytes(data[9:10],
                                            byteorder='big'))[2:].rjust(
                                                2, "0")
            self.direction = hex(int.from_bytes(data[10:11],
                                                byteorder='big'))[2:].rjust(
                                                    2, "0")
            self.head_num = hex(int.from_bytes(data[11:12],
                                               byteorder='big'))[2:].rjust(
                                                   2, "0")
            self.hose_num = hex(int.from_bytes(data[12:13],
                                               byteorder='big'))[2:].rjust(
                                                   2, "0")

            print("<-", self.response, self.flow, self.state, self.direction,
                  self.head_num, self.hose_num)
            return self.response, self.flow, self.state, self.direction, self.head_num, self.hose_num
        return ""

    def folw_calib(self, real_flow: int):
        """
        校准流量 \n
        流量的单位为 nL/min，即 1 表示 1 nL/min \n
        1 L = 1e3 mL = 1e6 uL = 1e9 nL

        :param int real_flow: 实测流量
        :return _type_: 应答 "CL"
        """
        real_flow = hex(real_flow)[2:].rjust(8, "0")
        self.len = "06"
        self.pdu = self.opt["CL"] + real_flow
        self.command = self.FLAG + self.addr + self.len + self.pdu
        self.fcs = self.get_fcs(self.command)
        self.command = self.modify(self.command + self.fcs)
        print("->", self.command)
        self.write(bytes.fromhex(self.command))

        time.sleep(self.wait_time)

        if self.in_waiting != 0:
            self.response = str(
                self.demodify(self.read(self.in_waiting))[3:5])[2:4]
            print("<-", self.response)
            return self.response
        return ""

    def stop(self):
        """
        停止运行
        
        :param _type_ speed: 应答 "XL"
        """
        speed = hex(0)[2:].rjust(4, "0")
        self.state = self.STOP
        self.len = "06"
        self.pdu = self.opt["XL"] + speed + self.state + self.direction
        self.command = self.FLAG + self.addr + self.len + self.pdu
        self.fcs = self.get_fcs(self.command)
        self.command = self.modify(self.command + self.fcs)
        print("->", self.command)
        self.write(bytes.fromhex(self.command))

        time.sleep(self.wait_time)

        if self.in_waiting != 0:
            self.response = str(
                self.demodify(self.read(self.in_waiting))[3:5])[2:4]
            print("<-", self.response)
            return self.response
        return ""

    def full(self):
        """
        全速运行
        
        ：：：：无应答 ：：：：
        """
        return self.set_speed(1000)

    def turn(self):
        """
        改变方向，不改变状态
        
        :param _type_ speed: 应答 "XL"
        """
        _, self.speed, self.state, self.direction = self.get_speed()
        # 改变方向
        if self.direction == self.CLOCK:
            self.direction = self.ANTICLOCK
        else:
            self.direction = self.CLOCK

        # 只改变方向，不改变状态
        if self.state != self.STOP:
            self.stop()
            return self.set_speed(self.speed * 10)
        else:
            return self.stop()

    def set_addr(self, aim_addr: int, new_addr: int):
        """
        设置地址 \n
        aim_addr可以是泵的地址（1-30），也可以是广播址31。 \n
        用广播址设地址时，只能单台设，无应答。

        :param _type_ aim_addr: 目标地址
        :param _type_ new_addr: 新地址
        :return _type_: 应答 "WID"
        """

        if aim_addr < 1 or aim_addr > 31:
            raise (Exception("目标地址范围错误：1-31"))
        if new_addr < 1 or new_addr > 30:
            raise (Exception("新地址范围错误：1-30"))
        new_addr_temp = new_addr  # 临时保存
        aim_addr = hex(aim_addr)[2:].rjust(2, "0")
        new_addr = hex(new_addr)[2:].rjust(2, "0")
        self.len = "04"
        self.pdu = self.opt["WID"] + new_addr
        self.command = self.FLAG + aim_addr + self.len + self.pdu
        self.fcs = self.get_fcs(self.command)
        self.command = self.modify(self.command + self.fcs)
        print("->", self.command)
        self.write(bytes.fromhex(self.command))

        time.sleep(self.wait_time)

        if self.in_waiting != 0:
            self.response = str(
                self.demodify(self.read(self.in_waiting))[3:6])[2:5]
            print("<-", self.response)
            # 重新设置地址（在接收到回执后）
            self.addr = hex(new_addr_temp)[2:].rjust(2, "0")
            return self.response
        return ""

    def verify_addr(self, addr: int):
        """
        addr只能是泵的地址（1-30）。用于验证所设地址的正确性。\n
        如果有应答返回 pdu 段，否则返回空字符串。

        :param int addr: 目标地址
        :return _type_: 应答 "RID"
        """
        if addr < 1 or addr > 30:
            raise (Exception("地址范围错误：1-30"))

        addr = hex(addr)[2:].rjust(2, "0")
        self.len = "03"
        self.pdu = self.opt["RID"]
        self.command = self.FLAG + addr + self.len + self.pdu
        self.fcs = self.get_fcs(self.command)
        self.command = self.modify(self.command + self.fcs)
        self.write(bytes.fromhex(self.command))
        print("->", self.command)

        time.sleep(self.wait_time)

        if self.in_waiting != 0:
            self.response = str(
                self.demodify(self.read(self.in_waiting))[3:6])[2:5]
            print("<-", self.response)
            return self.response
        return ""

    def get_addr(self) -> int:
        """
        获取当前地址，循环验证，需要等待。。。

        :return int: int 类型地址
        """
        for i in range(1, 31):
            if pump.verify_addr(i):
                return i

    # TODO 还未实现
    def get_direction(self) -> str:
        """
        获取实际运行方向

        :return str: 实际运行方向
        """
        _, _, _, self.direction, _, _ = self.get_flow()
        return self.direction


if __name__ == "__main__":
    print_comport()
    pump = Pump(port="COM4")

    pump.switch()
    pump.addr = "02"

    # pump.direction = pump.CLOCK
    # pump.direction = pump.ANTICLOCK
    # pump.set_speed(11.2)
    # print(pump.get_speed())
    print("ssssssssssss", pump.get_speed())
    print("ffffffffff", pump.get_flow())
    print("real_dir", pump.get_direction)

    time.sleep(1)
    pump.turn()

    # pump.set_speed(11.2)
    print("ssssssssssss", pump.get_speed())
    print("ffffffffff", pump.get_flow())
    print("real_dir", pump.get_direction)

    # # pump.full()
    time.sleep(1)
    pump.stop()

    pump.close()
