
# 1 概述

包含一个函数，三个类

> 在一些数值范围判断出会抛出异常，注意处理

> 一个函数
> print_comport 打印串口信息


> 三个类
> SingleRelay   单路继电器
> DoubleRelay   双路继电器
> Pump          蠕动泵
> > pump 中涉及到方向的方法是根据其 direction 属性决定的，因此要让设备按照预想的结果运作（防止按键更改方向），需要先更改 direction 的值（ CLOCK 或 ANTICLOCK ），默认为 CLOCK


# 2 创建

```python
""" 创建时只需指定端口即可 """

srelay=SingleRelay(port="COM1")
drelay=DoubleRelay(port="COM1")
pump=Pump(port="COM1")
```

# 3 详细信息

## print_comport

```python
def print_comport():
    """
    打印串口信息
    """
```
## SingleRelay

```python
class SingleRelay(serial.rs485.RS485):
    """
    单路继电器 \n
    继承 serial.rs485.RS485 

    :param _type_ serial: _description_
    """
        self.wait_time = 0.3

    def set_addr(self, addr: int):
        """
        设置继电器地址

        :param _type_ addr: 新地址
        """

    def switch(self):
        """
        判断串口是否打开
        """
    def relay_start(self):
        """
        启动继电器
        """
    def relay_stop(self):
        """
        关闭继电器
        """
    def relay_flick(self):
        """
        继电器点动
        """
```

## DoubleRelay

```python
class DoubleRelay(serial.rs485.RS485):
    """
    双路继电器 \n
    继承 serial.rs485.RS485 

    :param _type_ serial: _description_
    """
        self.wait_time = 0.3

    def set_addr(self, addr: int):
        """
        设置双路继电器地址
        
        :param _type_ addr: 新地址
        """        
    def switch(self):
        """
        判断串口是否打开
        """
    def relay_1_start(self):
        """
        启动一号继电器
        """
    def relay_1_stop(self):
        """
        关闭一号继电器
        """
    def relay_1_flick(self):
        """
        一号继电器点动
        """
    def relay_2_start(self):
        """
        启动二号继电器
        """
    def relay_2_stop(self):
        """
        关闭二号继电器
        """
    def relay_2_flick(self):
        """
        二号继电器点动
        """
    def all_start(self):
        """
        启动所有继电器
        """
    def all_stop(self):
        """
        关闭所有继电器
        """

```

## Pump

```python
class Pump(serial.rs485.RS485):
    """
    蠕动泵 \n
    继承 serial.rs485.RS485 
    """
        self.wait_time = 0.5
        # 当前速度
        self.speed = ""
        # 当前流量
        self.flow = ""
        # 帧头
        self.FLAG = "E9"
        # 地址，默认为 "01"
        self.addr = "01"
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
        # 启停状态
        self.RUN = "01"
        self.STOP = "00"
        self.state = self.STOP
        # 转动方向 顺时针：CLOCK 逆时针：ANTICLOCK
        self.CLOCK = "01"
        self.ANTICLOCK = "00"
        self.direction = self.CLOCK
        # 泵头编号
        self.head_num = "05"
        # 软管编号 01 - 16
        self.hose_num = "05"
        # 操作码
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
    def get_fcs(self, strr: str) -> str:
        """
        根据规则计算异或校验值，返回异或校验值。

        :param _type_ strr: 需要添加异或校验值计算的指令
        :return str: 返回异或校验值
        """
    def modify(self, command: str) -> str:
        """
        替换规则： E9 -> E8 01 , E8 -> E8 00 .

        :param str command: 需要修饰的指令
        :return str: 修饰后的指令
        """
    def demodify(self, command: bytes) -> bytes:
        """
        回复指令 \n
        替换规则： E8 01 -> E9 , E8 00 -> E8.

        :param str command: 需要恢复的指令
        :return str: 恢复的指令
        """
    def set_speed(self, speed: float):
        """
        设置速度，单位是 RPM, 分辨率 0.1 \n
        范围 10 RPM - 1000 RPM

        :param _type_ speed: 应答 "XL"
        """
    def get_speed(self) -> int:
        """
        获取转速、运行状态、运行方向

        :return int:DL、转速、运行状态、运行方向
        """
    def set_flow(self, flow: int, hose_num: int, direction: str):
        """
        流量的单位为 nL/min，即 1 表示 1 nL/min \n
        1 L = 1e3 mL = 1e6 uL = 1e9 nL

        :param _type_ flow: 流量
        :param _type_ hose_num: 软管编号
        :param _type_ direction: 运行方向
        :return _type_: "WL"、实际流量
        """
    def get_flow(self):
        """
        获取流量、运行状态、运行方向、泵头编号、软管编号

        :return _type_:"RL"、流量、运行状态、运行方向、泵头编号、软管编号
        """
    def folw_calib(self, real_flow: int):
        """
        校准流量 \n
        流量的单位为 nL/min，即 1 表示 1 nL/min \n
        1 L = 1e3 mL = 1e6 uL = 1e9 nL

        :param int real_flow: 实测流量
        :return _type_: 应答 "CL"
        """
    def stop(self):
        """
        停止运行
        
        :param _type_ speed: 应答 "XL"
        """
    def full(self):
        """
        全速运行
        
        ：：：：无应答 ：：：：
        """ 
    def turn(self):
        """
        改变方向，不改变状态
        
        :param _type_ speed: 应答 "XL"
        """       
    def set_addr(self, aim_addr: int, new_addr: int):
        """
        设置地址 \n
        aim_addr可以是泵的地址（1-30），也可以是广播址31。 \n
        用广播址设地址时，只能单台设，无应答。

        :param _type_ aim_addr: 目标地址
        :param _type_ new_addr: 新地址
        :return _type_: 应答 "WID"
        """
    def verify_addr(self, addr: int):
        """
        addr只能是泵的地址（1-30）。用于验证所设地址的正确性。\n
        如果有应答返回 pdu 段，否则返回空字符串。

        :param int addr: 目标地址
        :return _type_: 应答 "RID"
        """
    def get_addr(self) -> int:
        """
        获取当前地址，循环验证，需要等待。。。

        :return int: int 类型地址
        """
```
