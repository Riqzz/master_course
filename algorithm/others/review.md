#### 10 摊还分析

**聚合分析**：一个 $n$ 个操作的序列最坏情况下花费的总时间是 $T(n)$ ，那么每个操作的摊还代价为 $T(n)/n$

例1：一个初值为 $0$ 的 $k$ 位计数器执行 $n$ 个插入操作的翻转总数为：
$$
\sum\limits_{i=0}^{k-1}\lfloor \frac{n}{2^i} \rfloor < n \sum\limits_{i=0}^{\infty} \frac{1}{2^i} = 2n
$$
其中，$i$ 表示从低位开始的位数，每 $n$ 个插入最坏情况为 $O(n)$，单次插入平均（摊还）代价为 $O(n)/n=O(1)$

例2：对一个动态表执行 $n$ 次插入操作，第 i 次的代价为：
$$
c_i=
\begin{cases}
i& i-1等于2的幂\\
1& 其他
\end{cases}
$$
因此，n 次总代价为：
$$
\sum\limits^n_{i=1}c_i \le \sum\limits^{\lfloor lgn \rfloor}_{j=0}2^j < n+2n=3n
$$
![image-20201104001121803](C:\Users\lenovo\AppData\Roaming\Typora\typora-user-images\image-20201104001121803.png)

**核算法**：

对不同的操作赋予不同的费用，赋予某些操作的费用可能多于或少于其实际代价，将赋予一个操作的费用称为他的摊还代价。当一个操作的摊还代价超过其实际代价时，将多出的差额存储，称为信用；当摊还代价小于实际代价时，用信用支付差额。

将第 $i$ 次操作的摊还代价记为 $\hat{c}_i$ ，其实际代价记为 $c_i$，要求：
$$
\sum\limits^n_{i=1}\hat{c}_i \ge \sum\limits^n_{i=1}c_i
$$
例1：

例2：

![image-20201104001231292](C:\Users\lenovo\AppData\Roaming\Typora\typora-user-images\image-20201104001231292.png)

**势能法**：

$\Phi$ 

例2：



#### 13 线性规划

**标准型**
$$
\begin{align}
max \quad &\sum\limits_{j=1}^nc_j x_j &\\
s.t. \quad &\sum\limits_{j=1}^n a_{ij} x_j \le b_i, \quad &i=1,2,...,m\\
& \qquad\quad  x_j \ge 0, \quad &j=1,2,...,m
\end{align}
$$

1. 目标函数是 $min f(x)$ ，转换为 $max (-f(x))$ 
2. 变量 $x_j$ 无非负约束，用 $x_j'-x_j''$ 替换 $x_j$，并增加非负约束 $x_j'\ge0,x_j''\ge0$
3. 等式约束 $\alpha_ix=b_i$，转换为 $\alpha_ix \ge b_i,\alpha_ix\le b_i$
4. 大于等于号，两边加负号变成小于等于

**松弛型**

对 $\sum\limits_{j=1}^n a_{ij} x_j \le b_i$，加入新的约束 $s$ （做题时一般用新的 $x_i$）：
$$
\begin{align}
s &= b_i - \sum\limits_{j=1}^n a_{ij} x_j \\
s &\ge 0
\end{align}
$$


**单纯形法**

​	根据目标函数变量的系数（正的、最大的）决定操作哪个哪个

​	在约束条件中，令其他变量都为零，找到这个变量的最紧的值，以确定旋转用哪个约束条件

​	找到这个约束条件后，将这个参数换到左边，用原来的非基本变量表示

​	再将这个约束条件带入目标函数，这样在目标函数中会出现一个正常量

重复，直到目标函数变量的系数全为负



#### 14 快速傅里叶变换

Python 代码

```python
from math import sin, cos, pi

class Complex:

    def __init__(self, r, i):
        self.r = r
        self.i = i
    
    def __add__(self, rhs):
        r = self.r + rhs.r
        i = self.i + rhs.i
        return Complex(r, i)

    def __sub__(self, rhs):
        r = self.r - rhs.r
        i = self.i - rhs.i
        return Complex(r, i)

    def __mul__(self, rhs):
        r = (self.r * rhs.r) - (self.i * rhs.i)
        i = self.r * rhs.i + self.i * rhs.r
        return Complex(r, i)


def fft(arr):
    n = len(arr)
    if n == 1:
        return arr
    
    wn = Complex(cos(2*pi/n), sin(2*pi/n))
    w = Complex(1, 0)

    a0 = list()
    a1 = list()
    for i in range(0, n, 2):
        a0.append(arr[i])
        a1.append(arr[i+1])

    y0 = fft(a0)
    y1 = fft(a1)

    ya = list()
    yb = list()
    for k in range(0, n>>1):
        ya.append(y0[k] + w*y1[k])
        yb.append(y0[k] - w*y1[k])
        w = w * wn
    
    for i in yb:
        ya.append(i)
    
    return ya


x = [Complex(i, 0) for i in range(4)]
y = fft(x)
```



