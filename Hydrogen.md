小出昭一郎, 量子力学（I）p89 §4「中心力場内の粒子」、p219 §8「電子のスピン」について備忘録。いつものごとく式番号はこの参考書と同じ。細かい点は飛ばすのでこの参考書を見ながら読んでほしい。

水素原子のシュレーディンガー方程式の解とスピンについてはこの後の章でも度々使う。とくに球面調和関数と角運動量演算子の性質や、それと同じ性質を持ったスピン角運動量の性質は超頻出で、特に次の巻の量子力学（II）§10の「原子と角運動量」で原子の電子配置の性質の基礎とになる。つまりこの2つの章は超重要で、今後何度も読み返すことになるのでここにまとめておく。
## 極座標で表したシュレーディンガー方程式

(「極座標系」『フリー百科事典　ウィキペディア日本語版』。2020年11月28日 (土) 14:45　UTC、URL: [https://ja.wikipedia.org])

ポテンシャルが$r$のみの関数(中心力場)で、定常状態の場合のシュレーディンガー方程式は、
$$
\left[
    -\frac{\hbar^2}{2m}\nabla^2+V(r)
\right]\varphi(\pmb{r})
=\varepsilon\varphi(\pmb{r})\tag{1}
$$
となる。ラプラシアン$\nabla^2$は、球面極座標$(r,\theta,\phi)$では
$$
\nabla^2=
\frac{\partial^2}{\partial r^2}
+\frac{2}{r}\frac{\partial}{\partial r}
+\frac{1}{r^2}\Lambda\tag{5}
$$
ただし、$\Lambda$は、
$$
\Lambda=
\frac{1}{\sin\theta}\frac{\partial}{\partial \theta}
\left(
\sin\theta\frac{\partial}{\partial \theta}
\right)
+\frac{1}{\sin^2\theta}\frac{\partial^2}{\partial \phi^2}\tag{6}
$$
である。式(1)の中心力場のシュレーディンガー方程式を解くためには、
$$
\varphi(r.\theta,\phi)=R(r)Y(\theta,\phi)
$$
と変数分離すると良いことが分かっている。そうすると、シュレーディンガー方程式から、
$$
-\frac{\hbar^2}{2m}
\left(
\frac{\partial^2}{\partial r^2}
+\frac{2}{r}\frac{\partial}{\partial r}
-\frac{\lambda}{r^2}
\right)
R+V(r)R=\varepsilon R\tag{11}
$$
$$
\Lambda Y(\theta,\phi)+\lambda Y(\theta,\phi)=0\tag{12}
$$
と二つの微分方程式が得られる。
## 球関数と角運動量
式(12)の固有値は
$$
\lambda=l(l+1)\hspace{20pt}l=0,1,2,\cdots
$$
で各$l$に対応する固有関数はルジャンドル多項式とルジャンドル陪関数を用いて表せる。それらを
$$
Y^m_l(\theta,\phi)\hspace{20pt}m=-l,-l+1,\cdots,-1,0,1,\cdots,l-1,l
$$
と表すと、
$$
\begin{array}{ccl}
l=0:&s:
&Y^0_0=\frac{1}{\sqrt{4\pi}}\\
\\
l=1:&p0:
&Y^0_1=\sqrt{\frac{3}{4\pi}}\cos\theta
\\
&p\pm1:&Y^{\pm1}_1=\mp\sqrt{\frac{3}{8\pi}}
\sin\theta \mathrm{e}^{\pm i\phi}
\\
\\
l=2:&d0:&Y^0_2=\sqrt{\frac{5}{16\pi}}
(3\cos^2\theta-1)
\\
&d\pm1:&Y^{\pm1}_2=\mp\sqrt{\frac{15}{8\pi}}
\sin\theta\cos\theta \mathrm{e}^{\pm i\phi}\\
&d\pm2:&Y^{\pm2}_2=\sqrt{\frac{15}{32\pi}}
\sin^2\theta \mathrm{e}^{\pm 2i\phi}
\end{array}
$$
となる。これら球面調和関数の性質として、角運動量$\pmb{l}$について、$\pmb{l}^2=-\hbar^2\Lambda$より、角運動量の2乗、$\pmb{l}^2$の固有値は$\hbar^2l(l+1)$でその固有関数は$Y^m_l$である。また、角運動量のz成分、$l_z$の固有値は$m\hbar$で固有関数は同じく$Y^m_l$である。

$l_x$、$l_y$で定義される
$$
l_+=l_x+il_y\hspace{30pt}l_-=l_x-il_y
$$
を$Y^m_l$に作用させると、
$$
\begin{aligned}
l_+Y^m_l(\theta,\phi)
=\hbar\sqrt{(l-m)(l+m+1)}
Y^{m+1}_l(\theta,\phi)\\
l_-Y^m_l(\theta,\phi)
=\hbar\sqrt{(l+m)(l-m+1)}
Y^{m-1}_l(\theta,\phi)
\end{aligned}
$$
と$m$が上下する。また、$m=l$や$m=-l$の時、つまり$Y^l_l$、$Y^{-l}_l$に作用させると
$$
\begin{aligned}
l_+Y^l_l=0\\
l_-Y^{-l}_l=0
\end{aligned}
$$


## 中心力がクーロン力の時:水素原子
原子は中心力がクーロン力である。1電子の場合を考えるので、これは水素原子や$\mathrm{He}^+$原子を表す。原子核のクーロン力場にある電子のポテンシャルは
$$
V(r)=-\frac{Ze^2}{4\pi\epsilon_0r}
$$
である。この$V(r)$を用いて式(11)を解く。ボーア半径を
$$
a_0=\frac{4\pi\epsilon}{me^2}
$$
と定義する。この時、ハミルトニアンの固有値、つまりエネルギーは
$$
\varepsilon_n=-\frac{Z^2me^4}{(4\pi\epsilon_0)^22\hbar^2}\frac{1}{n^2}\hspace{20pt}n=1,2,\cdots
$$
と$n$の値によってとびとびにとる。そして式(11)の固有関数は
$$
\begin{aligned}
R_{1s}(r)&=
\left(\frac{Z}{a_0}\right)^{\frac{3}{2}}
2\mathrm{e}^{-Zr/a_0}\\
\\
R_{2s}(r)&=
\left(\frac{Z}{a_0}\right)^{\frac{3}{2}}
\frac{1}{\sqrt{2}}
\left(1-\frac{1}{2}\frac{Zr}{a_0}\right)
\mathrm{e}^{-Zr/2a_0}\\
R_{2p}(r)&=
\left(\frac{Z}{a_0}\right)^{\frac{3}{2}}
\frac{1}{2\sqrt{6}}
\frac{Zr}{a_0}
\mathrm{e}^{-Zr/2a_0}\\
\\
R_{3s}(r)&=
\left(\frac{Z}{a_0}\right)^{\frac{3}{2}}
\frac{2}{3\sqrt{3}}
\left[
    1-\frac{2}{3}\frac{Zr}{a_0}+\frac{2}{27}\left(\frac{Zr}{a_0}\right)^2
    \right]
\mathrm{e}^{-Zr/3a_0}\\
R_{3p}(r)&=
\left(\frac{Z}{a_0}\right)^{\frac{3}{2}}
\frac{8}{27\sqrt{6}}
\frac{Zr}{a_0}
\left(1-\frac{1}{6}\frac{Zr}{a_0}\right)
\mathrm{e}^{-Zr/3a_0}\\
\end{aligned}
$$
となる。最終的にもとの式(1)中心力場のシュレーディンガー方程式のハミルトニアンの固有関数は$Y_l^m(\theta,\phi)R(r)$となる。


## 電子のスピン

電子は主量子数$n$、方位量子数$l$、磁気量子数$m$で指定される状態の他に、スピンと呼ばれる2つの状態を取ることが分かっている。このスピンの状態で電子は2つの磁気モーメント、つまり角運動量を持っているとみなせる。スピンは相対論から導出できるもので、その詳細は立ち入らない。しかし、スピンは疑似的に角運動量とみなせるので、その角運動量$\pmb{s}$を考えることができて、これは角運動量$\pmb{l}$の類推でその固有値、固有関数の振舞いを特定できる。

$\pmb{l}^2$の固有値は$\hbar^2l(l+1)$、

$l_z$の固有値は$m_l\hbar$で$m_l=-l,-l+1,\cdots,l$

これと同様に、

$\pmb{s}^2$の固有値は$\hbar^2s(s+1)$、

$s_z$の固有値は$m_s\hbar$で$m_s=-s,-s+1,\cdots,s$

この時上の式で、一つの角運動量$\pmb{l}$に対し、$m_l$が$2l+1$種類存在するので、
一つの角運動量$\pmb{l}$に対し$2l+1$の状態が取れることになる。一方、スピンにより電子は2つの状態を取るので、一つのスピン角運動量に対し、$m_s$が2種類ある。 
$$
\begin{aligned}
2s+1&=2\\
s&=\frac{1}{2}
\end{aligned}
$$
である。この$s$を使えば
$$
m_s=\pm\frac{1}{2}
$$
と2つの状態ができる。よって$m_s=+\frac{1}{2}$、$m_s=-\frac{1}{2}$に対応する固有関数をそれぞれ、$\alpha$、$\beta$とすると
$$
\begin{array}{cc}
\pmb{s}^2\alpha
=\frac{3}{4}\hbar\alpha
&\pmb{s}^2\beta
=\frac{3}{4}\hbar\beta\\\\
s_z\alpha
=\frac{1}{2}\hbar\alpha
&s_z\beta
=-\frac{1}{2}\hbar\beta
\end{array}
$$
となる。

## 角運動量とスピン角運動量についてまとめ
2つの角運動量について結果を表にまとめると、
角運動量$\pmb{l}$について、

|  演算子  |  固有値  | 作用した結果 |
| ---- | ---- | ---- |
|  $\pmb{l}^2$  |  $l(l+1)\hbar^2$  | $\pmb{l}^2Y^m_l=l(l+1)\hbar^2Y^m_l$ |
|  $l_z$ |  $m_l\hbar$  | $l_zY^m_l=m_l\hbar Y^m_l$ |
|  $l_+$ |  なし  | $l_+Y^m_l=\hbar\sqrt{(l-m)(l+m+1)}Y^{m+1}_l$ |
|  $l_-$ |  なし  | $l_-Y^m_l=\hbar\sqrt{(l+m)(l-m+1)}Y^{m-1}_l$ |


スピン角運動量$\pmb{s}$について、

|  演算子  |  固有値  | 作用した結果 |
| ---- | ---- | ---- |
|  $\pmb{s}^2$  |  $s(s+1)\hbar^2$  | $\pmb{s}^2\alpha=\frac{3}{4}\hbar\alpha\quad\pmb{s}^2\beta=\frac{3}{4}\hbar\beta$ |
|  $s_z$ |  $m_s\hbar$  | $s_z\alpha=\frac{1}{2}\hbar\alpha\quad s_z\beta=-\frac{1}{2}\hbar\beta$ |
|  $s_+$ |  なし  | $s_+\alpha=0\quad s_+\beta=\hbar\alpha$ |
|  $s_-$ |  なし  | $s_-\alpha=\hbar\beta\quad s_-\beta=0$ |