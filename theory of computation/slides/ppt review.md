* DFA、DFA、RE间的相互转化

  
  
* 泵引理证明非正则、非上下文无关

  
  
* Recognizable language

  | Automata                                  | Recognizable language            |
  | ----------------------------------------- | -------------------------------- |
  | Deterministic finite automata (DFA)       | regular languages                |
  | Nondeterministic finite automata (NFA)    | regular languages                |
  | Regular languages Pushdown automata (PDA) | context-free languages           |
  | Linear bounded automata (LBA)             | context-sensitive language       |
  | Turing machines (TM)                      | recursively enumerable languages |

* Call a language **Turing Recognizable**, if some TM recognizes it.

  *other name: = Turing Acceptable, Recursively Enumerable*

  *Decidable = Solvable*

  如果一个语言 $S$ 是图灵可识别的，那么存在一台图灵机 $M$ ，当 $M$ 的输入 $\omega\in S$ 时，$M$ 一定会停机并进入 $accept$ 状态；否则，$M$ 可能停机并进入拒绝状态，或者永不停机。

  如果一个语言 $S$ 是图灵可判定的，$M$ 总能停机。

* *某些语言是图灵不可识别的*

  * 对任意字母表 $\Sigma$ ，所有串的集合 $\Sigma^*$ 是可数的

    如：$\Sigma=\{0,1\}$，则 $\Sigma^*=\{\epsilon,0,1,00,01,10,11,000,001,...\}$

  * 设 $\mathcal{L}$ 是字母表 $\Sigma$ 上所有语言的集合，一个语言 $L \in \mathcal{L}$ 是 $\Sigma^*$ 的一个子集。

    如：$L = \{0,00,01,000,001,...\}$

  * $\mathcal{X}_L$ 是 $L$ 的特征序列，两者一一对应。若 $L$ 中的元素出现在 $\Sigma^*$ 中则为 $1$，否则为 $0$

    如： $\mathcal{X}_L = 0\quad 1\quad 0\quad 1\quad 1\quad 0\quad 0\quad 1\quad 1\quad ...$

  * $\mathcal{X}_L \in \mathcal{B}$ ，而 $\mathcal{B}$ 是不可数的（01无穷序列的集合）

  以上可以得出：**所有语言的集合是不可数的**。

  补图灵可识别（co-Turing-recognizable）：一个语言 $L$ 的补（complement）是 $\bar{L}=\Sigma^* - L$ 。若一个语言是图灵可识别，且补图灵可识别，则这个语言是可判定的。

  **图灵机是可数的**

  - TM encoding（==例题== slides page 536 ~ 544）

  eg.  $\overline{A_{TM}}$ 是图灵不可识别的

* Standard TM simulates Stay-Option TM: 

  * the stay option

  ```mermaid
  graph LR;  
  　　A((Q1)) -- a->b,S --> B((Q2))
  ```

  * simulation: x is any possible symbol

  ```mermaid
  graph LR;  
  　　A((Q1)) -- a->b,L --> C((Qt)) -- x->x,R --> B((Q2))
  ```

* Nondeterministic TM key points:

  - configurations form a tree, each children nodes are yielded by their parent configuration
  - so, every configuration can be encode an address uniquely
  - use breadth first search (there may exist infinite path)
  
* A 问题归约到 B 问题，等价于用 B 问题的解构造一个 A 问题的解

  - 若 A 归约到 B，且 A 是不可判定的，则 B 是不可判定的

  - 若 A 归约到 B，且 B 是可判定的，则 A 是可判定的

* Post 对应问题（==例题== slides page 611 ~ 619）

* 递归

  $A = P_{<B>}$ ，打印 $<B>$ ，然后停机

  $B=$ “ 对输入 $<M>$ 

            1. 计算 $q(<M>)$，即 $<A>$  *（这里 M 就是 B）*
               2. 将其结果与 $<B>$ 组成一个完整的TM描述
               3. 打印这个描述，停机 “

  

  对于 $q$：$q(\omega)$ 打印 $P_{\omega}$ 的描述 $<P_{\omega}>$，其中 $P_{\omega}$ 是无视输入，只在带上写下 $\omega$ 的TM

  $Q=$ “ 对于输入 $\omega$ 

  1. 构造TM $P_{\omega}$

     $P_{\omega}=$ “ 对任意输入 $x$

     1. 抹除 $x$
     2. 在带上写下 $\omega$
     3. 停机 “

  2. 输出 $<P_{\omega}>$ “

  

  递归定理：一个 TM 可以获得它自己的描述，并用它来做运算

* $w^{R}$ 表示 $w$ 逆序

* 分析算法时间复杂度（考过）

  $A = \{0^k1^k|k\ge 0\}$ （==例题== slides page 692 ~ 695）

* P、NP、NPC典型例题和证明