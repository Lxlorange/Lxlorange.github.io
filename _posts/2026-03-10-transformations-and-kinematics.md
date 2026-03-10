---
title: 物体变换与运动
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

通过支付增加一个维度的代价，我们在更高维度的空间中用**线性变换（切变）** 完美等效了低维空间中的**仿射变换（平移）**。

## 3D变换

将齐次坐标的概念扩展到 3D 空间，我们只需要使用 $4\times4$ 的矩阵和 $(x, y, z, 1)^T$ 的坐标向量。
一个标准的 3D 仿射变换矩阵结构如下：

$$M=\begin{pmatrix}R_{3\times3}&T_{3\times1}\\0_{1\times3}&1\end{pmatrix}$$

左上角的 $3\times3$ 子矩阵负责处理线性变换（旋转、缩放、错切），右上角的 $3\times1$ 列向量负责平移。我们同理可以得出


## 3D 旋转

在 3D 空间中，平移和缩放都很直观，但**旋转**异常复杂。常见的表示方法有欧拉角、旋转矩阵、轴角（Axis-Angle）和四元数。

### 欧拉角的万向节死锁 (Gimbal Lock)

欧拉角将旋转分解为绕 X、Y、Z 三个互相垂直轴的独立旋转（例如 Roll-Pitch-Yaw）。它直观且易于理解，但存在致命的数学缺陷：**万向节死锁**。
当其中一个旋转轴（通常是中间那个轴）旋转到 $90^{\circ}$ 时，另外两个旋转轴会重合，导致系统丢失一个自由度。为了避免这个问题并在空间中进行平滑插值，我们通常使用**轴角**或**四元数**。

### 罗德里格斯旋转公式 (Rodrigues' Rotation Formula)

> 如果给定一个旋转轴向量 $\mathbf{n}$（单位向量）和一个旋转角度 $\theta$，我们如何直接写出对应的 $3\times3$ 旋转矩阵？

这就是著名的**罗德里格斯旋转公式**解决的问题。它不依赖于欧拉角的拆分，直接在 3D 空间中进行向量分解。

假设我们要将向量 $\mathbf{v}$ 绕单位轴向量 $\mathbf{n}$ 旋转 $\theta$ 角度，得到新向量 $\mathbf{v'}$，所需的旋转矩阵$R$为：

$$R=I+(\sin\theta)N+(1-\cos\theta)N^2$$

{% capture proof_content_rodrigues %}
**推导过程：**

1. **正交分解**：首先将向量 $\mathbf{v}$ 分解为平行于旋转轴的分量 $\mathbf{v}_{||}$ 和垂直于旋转轴的分量 $\mathbf{v}_{\bot}$。
   $$\mathbf{v}_{||}=(\mathbf{v}\cdot\mathbf{n})\mathbf{n}$$
   $$\mathbf{v}_{\bot}=\mathbf{v}-\mathbf{v}_{||}=\mathbf{v}-(\mathbf{v}\cdot\mathbf{n})\mathbf{n}$$

2. **旋转平行分量**：平行于旋转轴的分量在旋转过程中保持不变。
   $$\mathbf{v}'_{||}=\mathbf{v}_{||}$$

3. **旋转垂直分量**：垂直分量 $\mathbf{v}_{\bot}$ 在垂直于 $\mathbf{n}$ 的平面内发生旋转。为了计算旋转，我们构造一个与 $\mathbf{v}_{\bot}$ 正交且长度相等的辅助向量 $\mathbf{w}$。利用叉乘可以很容易得到：
   $$\mathbf{w}=\mathbf{n}\times\mathbf{v}_{\bot}=\mathbf{n}\times(\mathbf{v}-\mathbf{v}_{||})=\mathbf{n}\times\mathbf{v}$$
   
   现在，$\mathbf{v}_{\bot}$ 和 $\mathbf{w}$ 构成了一组正交基。在这个平面内旋转 $\theta$ 角，相当于在这组基上进行 2D 旋转：
   $$\mathbf{v}'_{\bot}=\mathbf{v}_{\bot}\cos\theta+\mathbf{w}\sin\theta$$

4. **合成最终向量**：将旋转后的平行分量和垂直分量相加。
   $$\mathbf{v}'=\mathbf{v}'_{||}+\mathbf{v}'_{\bot}$$
   $$\mathbf{v}'=(\mathbf{v}\cdot\mathbf{n})\mathbf{n}+(\mathbf{v}-(\mathbf{v}\cdot\mathbf{n})\mathbf{n})\cos\theta+(\mathbf{n}\times\mathbf{v})\sin\theta$$
   $$\mathbf{v}'=\mathbf{v}\cos\theta+(1-\cos\theta)(\mathbf{n}\cdot\mathbf{v})\mathbf{n}+(\mathbf{n}\times\mathbf{v})\sin\theta$$

这就是罗德里格斯旋转公式的向量形式。如果将其写成矩阵形式 $R\mathbf{v}$，利用叉乘矩阵（叉积的矩阵表示 $N$），即可以得到矩阵形式。
{% endcapture %} {% include components/collapsible.html title="罗德里格斯旋转公式推导证明" content=proof_content_rodrigues %}

