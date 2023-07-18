# Lab

# experiment.py

## 类

### Radar 类

#### 属性

```python
P_t=1.5e3,
freq=5.6e6,
G=45,
T_e=290,
L=6,
F=3,
B=5e6,
theta_e=1,
theta_a=1,
Theta_E=1,
Theta_A=1,
T_sc=2.5,
SNR=20,
f_r=300,
S_min=1
                 
```

#### 方法

```python
get_PD(self, R: float)
compute_SNR(self, sigma, r)
compute_PAP(self, SNR, sigma, r)
```
### Targe 类

#### 属性

```python
distance=[40],
sigma=0.1
```
#### 方法

## 函数

```python
Maximum_coherent_accumulation_time_limit(lambda_, a_r)
```

# constant.py

一些常数

# tek.py

针对 Tek 示波器文件的类

# tools.py

一些工具函数
