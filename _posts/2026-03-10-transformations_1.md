---
title: 模型变换
author: 凉香栾
date: 2026-03-10 07:31:19 +0800
categories:
  - 计算机图形学
tags:
  - CG
  - 运动学
  - 线性代数
description: 计算机图形学中的空间变换原理，从 2D 线性变换到 3D 齐次坐标，针对复杂的旋转行为进行详细推导。
toc: true
pin: false
math: true
mermaid: true
comment: true
---


> 变换是计算机图形学中最基本的操作之一。计算机图形学中充满了对现实世界的观察和仿真，并尝试用数学方法描述它们，而变换就是一种通过数学方法描述物理运动的技术。
{: .prompt-info }


## 基础2D线性变换

在二维空间中，常用**线性变换**包括缩放（Scaling）、反射（Reflection）、错切（Shearing）和旋转（Rotation）。

线性变换顾名思义，**直线变换后依然是直线，且原点保持不动**。线性变换用矩阵乘法可以表示为：


$$
T(\mathbf{v}) = A \mathbf{v}
$$


对于向量空间$V$中的任意向量$\mathbf{uv}$和标量$c$，变换$T$满足：

1. 加法性：$T(\mathbf{u}+\mathbf{v})=T(\mathbf{u})+T(\mathbf{v})$
2. 齐次性：$T(c\mathbf{v})=cT(\mathbf{v})$

即**线性变换保持向量加法和标量乘法不变**。

计算机屏幕通常只需要描述二维平面和三维空间的运动。假设原坐标为 $X=\begin{pmatrix}x\\y\end{pmatrix}$，变换矩阵为 $M$，则变换后的坐标 $X'$ 可以表示为$X'=MX$。针对具体操作，可以分别求出公式。

- **缩放 (Scaling)**



$$X' = \begin{pmatrix} s_x & 0 \\ 0 & s_y \end{pmatrix} \begin{pmatrix} x \\ y \end{pmatrix}$$


当 $s_x = s_y$ 时为等比例缩放，物体大小改变但形状不变；若两者不相等，物体就会发生拉伸或压扁。

- **反射 (Reflection)**

可以看作是**负数缩放**的特例。

以 $y$ 轴为对称轴进行反射，既 $y$ 轴进行$-1$倍缩放。


$$M_{ref\_y} = \begin{pmatrix} -1 & 0 \\ 0 & 1 \end{pmatrix}$$


同理，若以 $x$ 轴为对称轴进行反射，矩阵为：


$$M_{ref\_x} = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}$$



- **切变 (Shearing)**

这个操作类似于推倒一叠书的侧面，原本垂直的边会发生倾斜，矩形会变成平行四边形。

以沿 $x$ 轴的水平切变为例：点的高度（$y$ 坐标）保持不变，但点的水平位置（$x$ 坐标）会随着它所在高度的不同而发生偏移。偏移量与 $y$ 成正比，设比例因子为 $sh_x$。
其代数关系为：


$$X' = \begin{pmatrix} 1 & sh_x \\ 0 & 1 \end{pmatrix} \begin{pmatrix} x \\ y \end{pmatrix}$$



- **旋转 (Rotation)**

以 2D 旋转矩阵为例，将点绕原点逆时针旋转 $\theta$ 角，假设点到原点的距离为 $r$，初始与横轴夹角为 $\phi$，则原始坐标可以表示为：


$$x=r\cos\phi$$
$$y=r\sin\phi$$


利用三角函数的和角公式可得：


$$x'=r\cos(\phi+\theta)=r\cos\phi\cos\theta-r\sin\phi\sin\theta=x\cos\theta-y\sin\theta$$
$$y'=r\sin(\phi+\theta)=r\sin\phi\cos\theta+r\cos\phi\sin\theta=x\sin\theta+y\cos\theta$$

整理可得：

$$X'=\begin{pmatrix}\cos\theta&-\sin\theta\\\sin\theta&\cos\theta\end{pmatrix}\begin{pmatrix}x\\y\end{pmatrix}$$

- **复合变换 (Composite Transformations)**

有了上述简单变换，就可以轻易得出各种复合变换。例如想要先缩放 $a$ 倍再旋转 $\theta$ 度，可以写成：

$$
X' = R(\theta) S(a) X
$$

矩阵乘法不满足交换律，因此变换顺序不同，得出的结果也可能不同。但矩阵乘法满足结合律，即

$$
X' = M X , M = R(\theta) S(a)
$$

这意味着不论多么复杂的变换本质上都可以通过**一次矩阵乘法**完成，这极大压缩了计算的空间和时间。

## 仿射变换与齐次坐标

### 平移（Translation）

平移操作 $X'=X+\begin{pmatrix}t_x\\t_y\end{pmatrix}$是一个**仿射变换（Affine Transformation）**，无法找到一个 $2\times2$ 矩阵$M$ 使得 $X'=MX$。

然而如果平移不能写成矩阵乘法，我们就无法将连续的多个变换融合成一个单一的矩阵。

为了解决这个问题，**齐次坐标（Homogeneous Coordinates）**。

我们将 2D 空间嵌入到 3D 空间中 $w=1$ 的平面上。原本的坐标 $(x, y)$ 变成了 $(x, y, 1)$。现在可以通过 $3\times3$ 的一次矩阵乘法来实现这个变换：

$$\begin{pmatrix}x'\\y'\\1\end{pmatrix}=\begin{pmatrix}1&0&t_x\\0&1&t_y\\0&0&1\end{pmatrix}\begin{pmatrix}x\\y\\1\end{pmatrix}=\begin{pmatrix}x+t_x\\y+t_y\\1\end{pmatrix}$$

这个动作相当于长方体切变后将上表面向下做投影。通过支付增加一个维度的代价，我们在更高维度的空间中用**线性变换（切变）** 等效了低维空间中的**仿射变换（平移）**。


### 3D变换

将齐次坐标的概念扩展到 3D 空间，我们只需要使用 $4\times4$ 的矩阵和 $(x, y, z, 1)^T$ 的坐标向量。
一个标准的 3D 仿射变换矩阵结构如下：

$$M=\begin{pmatrix}R_{3\times3}&T_{3\times1}\\0_{1\times3}&1\end{pmatrix}$$

左上角的 $3\times3$ 子矩阵负责处理线性变换（旋转、缩放、切变），右上角的 $3\times1$ 列向量负责平移。


## 3D 旋转

在 3D 空间中，平移和缩放都很直观，但**旋转**则有些复杂。

### 欧拉角

首先容易想到的是，尝试把一次 3D 旋转行为转化成若干 2D 旋转行为的组合，这样就能使用之前的公式了。可以得到绕坐标轴旋转的公式：

$$
R_{x}(\gamma) = \begin{pmatrix}
1 & 0 & 0 \\ 0 & \cos(\gamma) & - \sin(\gamma) \\ 0 & \sin(\gamma) & \cos(\gamma)
\end{pmatrix}, 
R_{y}(\beta) = \begin{pmatrix}
\cos(\beta) & 0 & \sin(\beta) \\ 0 & 1 & 0 \\ -\sin(\beta) & 0 & \cos(\beta)
\end{pmatrix}, 
R_{z}(\alpha) = \begin{pmatrix}
\cos(\alpha) & - \sin(\alpha) & 0 \\ \sin(\alpha) & \cos(\alpha) & 0 \\ 0&0&1
\end{pmatrix}
$$

细心的读者可能已经从中发现了规律，并且发现只有$R_{y}(\beta)$的符号不同。这是因为我们使用的右手坐标系具有旋转轮换性，当我们说“**绕某个轴进行正向（逆时针）旋转**”时，其实是站在该轴的正半轴看向原点。因此绕 $y$ 轴旋转：是在 $zOx$ 平面内旋转，方向必须是  $z \to x$ ，导致这里使用的旋转矩阵实际上被**转置**了。

令 $\cos$ 为 $c$，$\sin$ 为 $s$，依次相乘可以得到：

 $$R= R_z(\alpha) R_y(\beta) R_x(\gamma) = \begin{pmatrix} c_\alpha c_\beta & c_\alpha s_\beta s_\gamma - s_\alpha c_\gamma & c_\alpha s_\beta c_\gamma + s_\alpha s_\gamma \\ s_\alpha c_\beta & s_\alpha s_\beta s_\gamma + c_\alpha c_\gamma & s_\alpha s_\beta c_\gamma - c_\alpha s_\gamma \\ -s_\beta & c_\beta s_\gamma & c_\beta c_\gamma \end{pmatrix}$$

旋转矩阵 $R$ 可以表示先绕 $x$ 轴旋转 $\gamma$ (Roll，翻滚)；再绕 $y$ 轴旋转 $\beta$ (Pitch，俯仰)；最后绕 $z$ 轴旋转 $\alpha$ (Yaw，偏航) 的旋转行为。矩阵乘法没有交换性，定义顺序是必要的，这里选择的顺序比较常用。

这就是用**欧拉角**和**旋转矩阵**表示3D旋转的方法，称 $\alpha$ 为进动角，$\beta$ 为章动角，$\gamma$ 为自旋角。

### 欧拉旋转定理

我们希望所有的旋转都能用旋转矩阵来表示，即我们希望能证明：

**任意旋转行为都可以找到一组欧拉角，使得按照欧拉角旋转的结果与之等效。**

直接证明它有点困难，我们可以拆分成两步：

1. 考虑物体绕任意向量轴$\mathbf{n}$旋转$\theta$角的行为，可以视为以$\mathbf{n}$为新坐标轴（不妨设为$z$轴）进行$R_{z}(\theta)$的操作。我们只要找到一个可以把原坐标系旋转变换为新坐标系的矩阵$P$，就可以得到这一行为的总旋转矩阵$R = P R_{z}(\theta) P^{-1}$.
2. 证明任意旋转行为都等效于绕任意向量轴$\mathbf{n}$旋转$\theta$角的行为。

我们先证明第二点。

空间旋转行为满足齐次性和可加性，是一种线性变换。所以一定存在一个旋转矩阵 $R$ 能表示任意旋转。如果第二点成立，旋转轴 $\mathbf{n}$ 在旋转后应该不变，即 $R \mathbf{n} = \mathbf{n}$ . 这意味着 $R$ 必然有特征值 $\lambda = 1$，且对应的特征向量就是 $\mathbf{n}$.

对于任意 3D 旋转矩阵 $R$，它是一个正交矩阵（则 $R^T R = I$）且行列式为 $1$ （因为旋转一个物体，物体内部任意两点之间的**距离**不会变，任意两条线段之间的**夹角**也不会变） 。

下求$\det(R-I)$:

$$\begin{aligned} \det(R - I) &= \det(R - R R^T) \\ &= \det(R(I - R^T)) \\ &= \det(R) \det(I - R^T) \\ & = 1 \cdot \det(I-R) \\ & = (-1) ^3 \det(R- I)\end{aligned}$$

可得 $\det (R -I) = 0$，说明 $\lambda = 1$ 确实是旋转矩阵的特征值，证毕。我们证明了**欧拉旋转定理**。


### 轴角（Axis-Angle）

接下来证明第一点。将向量 $\mathbf{v}$ 绕单位轴向量 $\mathbf{n}$ 旋转 $\theta$ 角度，这种表示旋转的方法称为轴角。

我们可以在垂直于 $\mathbf{n}$ 的平面上任意找两个互相垂直的单位向量 $\mathbf{u}$ 和 $\mathbf{v}$。这样 $\mathbf{u}, \mathbf{v}, \mathbf{n}$ 就构成了一组新的标准正交基。 将它们按列排布构成一个变换矩阵（是正交的） $P = [\mathbf{u}, \mathbf{v}, \mathbf{n}]$。

计算$R = P R_z(\theta) P^T$：

$$
\begin{align}
R &= [\mathbf{u}, \mathbf{v}, \mathbf{n}] \begin{pmatrix} \cos\theta & -\sin\theta & 0 \\ \sin\theta & \cos\theta & 0 \\ 0 & 0 & 1 \end{pmatrix} \begin{pmatrix} \mathbf{u}^T \\ \mathbf{v}^T \\ \mathbf{n}^T \end{pmatrix} \\
 &= \cos\theta(\mathbf{u}\mathbf{u}^T + \mathbf{v}\mathbf{v}^T) + \sin\theta(\mathbf{v}\mathbf{u}^T - \mathbf{u}\mathbf{v}^T) + \mathbf{n}\mathbf{n}^T
\end{align}
 $$

因为 $\mathbf{u}, \mathbf{v}, \mathbf{n}$ 是空间的一组标准正交基，所以 $\mathbf{u}\mathbf{u}^T + \mathbf{v}\mathbf{v}^T + \mathbf{n}\mathbf{n}^T = I$（单位矩阵）。因此可以替换掉第一项：$\mathbf{u}\mathbf{u}^T + \mathbf{v}\mathbf{v}^T = I - \mathbf{n}\mathbf{n}^T$。

根据三重向量积的性质，矩阵 $(\mathbf{v}\mathbf{u}^T - \mathbf{u}\mathbf{v}^T)$ 作用于任何向量，其效果等价于用 $\mathbf{n}$ 去叉乘该向量。我们可以将其替换为 $\mathbf{n}$ 的反对称矩阵（叉乘矩阵），记作 $N$ 或 $[\mathbf{n}]_\times$。

代入整理可得：

$$R = \cos\theta I + (1 - \cos\theta)\mathbf{n}\mathbf{n}^T + \sin\theta N$$

这就是罗德里格斯旋转公式。


### 万向节死锁 (Gimbal Lock)

我们现在有了轴角这个利器，旋转行为看起来简单了很多。但我还是会好奇，如果指定一个轴角旋转（因为我们已经把所有旋转都变成轴角旋转了），怎样找到对应这个旋转的欧拉角呢？

假设我们已经通过罗德里格斯旋转公式（或其他什么方式都行）得到了一个确定的 $3\times3$ 旋转矩阵 $R$，它的每一个元素都是已知的常数：


$$R = \begin{pmatrix} r_{11} & r_{12} & r_{13} \\ r_{21} & r_{22} & r_{23} \\ r_{31} & r_{32} & r_{33} \end{pmatrix}$$

之前已经求过欧拉角表示的旋转矩阵，只需要用对应元素相等的方法求解方程组$R_z(\alpha) R_y(\beta) R_x(\gamma) = R$ 即可。


1. **求解 $\beta$ (Pitch, 绕 Y 轴)**

观察展开后的矩阵，左下角的值 $r_{31}$ 最简单：

$$r_{31} = -\sin\beta$$


$$\beta = \arcsin(-r_{31})$$


_(通常我们限制 $\beta \in [-\frac{\pi}{2}, \frac{\pi}{2}]$ 以保证多解情况下的唯一性。)_

2. **求解 $\gamma$ (Roll, 绕 X 轴)**

观察最下面一行的另外两个元素：

$$r_{32} = \cos\beta \sin\gamma$$


$$r_{33} = \cos\beta \cos\gamma$$


$$\frac{r_{32}}{r_{33}} = \frac{\cos\beta \sin\gamma}{\cos\beta \cos\gamma} = \tan\gamma$$

所以 $\gamma = \arctan\left(\frac{r_{32}}{r_{33}}\right)$。


> 在实际代码实现中，直接使用 $\arctan$ 会导致丢失象限信息（因为 $\frac{-y}{-x}$ 和 $\frac{y}{x}$ 的结果一样），并且当 $r_{33}=0$ 时会导致除零异常。因此，在任何编程语言（如 C++, Java, Python）中，求这两个角都使用 `atan2(y, x)` 函数。


3. **求解 $\alpha$ (Yaw, 绕 Z 轴)**

同理，观察第一列的另外两个元素：

$$r_{21} = \sin\alpha \cos\beta$$


$$r_{11} = \cos\alpha \cos\beta$$

同样$\alpha = \arctan\left( \frac{r_{21} }{r_{11}} \right)$

细心的读者可能注意到了，我们在求 $\gamma$ 和 $\alpha$ 的时候，前提是 $\cos\beta$ 可以被约掉。**但如果 $\cos\beta = 0$ 呢？**

假设 $\beta = 90^\circ$，此时 $\sin\beta = 1, \cos\beta = 0$：

整理可得：

$$R_{\beta=90^\circ} = \begin{pmatrix} 0 & \sin(\gamma - \alpha) & \cos(\gamma - \alpha) \\ 0 & \cos(\gamma - \alpha) & \sin(\gamma - \alpha) \\ -1 & 0 & 0 \end{pmatrix}$$

可见在这个矩阵中，$\alpha$ 和 $\gamma$ 不再独立，它们只能以 $(\gamma - \alpha)$ 的整体形式出现。这意味着单独改变 $\alpha$ 和 $\gamma$ 产生的视觉效果和代数结果是等价的，物体丢失了一个旋转的自由度。这个现象被称为万向节死锁。

为了避免这个问题并在空间中进行平滑插值，我们通常使用**轴角**或**四元数**。

### 四元数 (Quaternion) 

> 对于目前的笔者来说，这部分属于扩展知识，笔者也没有深入研究，只在此做简单介绍。

四元数衍生于轴角法，本质上是把轴+角的信息包装进一个四维的复数空间中。一个用于表示旋转的单位四元数 $q$ 可以写成一个标量和一个 3D 向量的组合：

$$q = \left( \cos\left(\frac{\theta}{2}\right), \mathbf{n}\sin\left(\frac{\theta}{2}\right) \right)$$

现代图形学基本都会使用四元数处理旋转，核心原因有三个：

- 可以避免万向节死锁。
- 插值平滑。在计算机中模拟物体从姿态 A 平滑过渡到姿态 B 时，直接对欧拉角的三个数值或矩阵进行线性插值，会导致物体发生奇怪的扭曲或非匀速转动。而四元数支持“球面线性插值”（Spherical Linear Interpolation），能够算出两点间的最短弧线，从而实现更平滑的旋转动画。
- 计算开销小。一个 $3\times3$ 的旋转矩阵需要存 9 个浮点数，而四元数只需要 4 个 $(w, x, y, z)$。


## 模型变换总结

如果有人看完本文上述内容却对为什么要进行模型变换仍不知所以，可以思考这样一个情景：

在一个游戏场景空间内，我想放置一个做好的模型。这个模型在做的时候并不知道它将要被放在哪里，所以只好取自身某个点（例如中心）为原点，并记录其它顶点的坐标。

那此时我希望把模型中心放在世界坐标$(100,100,100)$的位置，并对模型进行缩放和旋转的设置。如果这时候对每个顶点都执行一边对模型中心的操作，性能开销显然会变得很大——越复杂的模型越是如此。

所以模型变换的意义就在于，我们可以先设定好模型要做的缩放、旋转和平移操作，利用模型变换的方法将所有操作表示为一个矩阵$M_{model}$ ，而引入的模型默认放在世界坐标的原点，这样只需要一次矩阵乘法的操作就能实现我们想要的结果，这将会非常经济。

