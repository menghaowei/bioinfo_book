--- 
title: "生物信息学实战手册"
author: "孟浩巍、大壮、官云小姐姐、刘博、连明、徐煜、契卡（按章节顺序排序）"
date: "2020-12-20"
output:
  html_document:
    df_print: paged
  pdf_document: default
bibliography:
- book.bib
- packages.bib
description: 生物信息学实战手册,从入门到独立承担课题
documentclass: ctexbook
geometry:
- b5paper
- tmargin=2.5cm
- bmargin=2.5cm
- lmargin=3.5cm
- rmargin=2.5cm
link-citations: yes
lof: yes
lot: yes
colorlinks: yes
site: bookdown::bookdown_site
biblio-style: apalike
---




# 前言 {-}

生物信息学的本质是使用信息学的手段解决生物学问题。自20世纪60年代发端以来，生物信息学对整个生物领域的发展产生了巨大的影响。2003年在多国科学家的通力合作下，科学家们完成了人类参考基因组的测序，随后越来越多模式生物的参考基因组也完成拼装，生物信息学或者说整个生物学的研究进入了一个新纪元。

2006年Illumina公司开发了第二代测序技术（Next Generation Sequencing，NGS），随着NGS技术的推广，一系列之前看似天方夜谭的测序技术得到应用：

- 如可以对人的每一个基因进行表达水平测定的RNA-Seq技术；
- 对基因组每一个突变进行鉴定的全基因组测序（Whole Genome Sequencing，WGS）；
- 对表观遗传学甲基化水平进行刻画的BS-Seq；
- 对基因组三维结构进行详细刻画的Hi-C技术，ChIA-PET技术等等。

也是因为这些技术的推广与应用，目前生物信息学一个很大的挑战就是理解和分析这些海量的数据。

在分析数据的过程中，使用R语言或者Python语言对原始的生物信息数据进行清洗，加工，分析，展示已经成为主流。不但使用便捷，而且两种编程语言都是开源语言没有版权和商业的限制，更重要的是使用人数众多，常见的问题都能过通过Google搜索到解决方案。

但是在生物信息学蓬勃发展的今天，国内鲜有一本能够将编程技术与实际生物信息学分析结合起来的参考书目，这给众多想要入门生物信息学的同学，老师及需要数据分析的临床医生带来了非常大的挑战。入门门槛较高，学习曲线比较陡峭是妨碍大家学习生信的主要问题，因此本书尝试用贴近真实数据分析的视角，为大家讲解我们认为最重要的生信相关知识点，并给出完整的测试数据及代码，方便大家进行学习。

我们不期能够大而全地介绍每一个生物信息学细节，而希望为大家提供一份较为通俗易懂的入门实战手册，在阅读和实践的过程中逐渐感受到生物信息学数据的处理方式，领会数据处理的原理。同时，针对生物信息学中涉及到的R语言，统计学及相关生物背景知识我也会给出相应的学习建议，方便大家更加深入地学习。



## 致谢 {-}

非常感谢我们编写团队的共同努力，没有各位的付出是不可能有这本书的存在。

在成书过程中：

- 孟浩巍主要负责第1、2、7、8章内容；
- 大壮主要负责第3章的内容；
- 官云小姐姐主要负责第4章的内容；
- 刘博主要负责了第5章的内容；
- 徐煜负责了第8章tSNE部分的内容；
- 契卡主要负责了第9章的内容；

另外，也要非常感谢生物信息学交流群里的朋友和每一位关心、支持我们的朋友，谢谢你们！

\BeginKnitrBlock{flushright}
生物信息学实战手册编写团队
\EndKnitrBlock{flushright}

<!--chapter:end:index.Rmd-->

---
output:
  word_document: default
  pdf_document: default
  html_document: default
---
# 作者简介 {#author .unnumbered}

按章节顺序排序

## 孟浩巍

## 大壮

## 魏官云

## 刘博

## 连明

## 徐煜

## 契卡

<!--chapter:end:0000-author.Rmd-->

---
output:
  word_document: default
  pdf_document: default
  html_document: default
---

# 前言 {#intro .unnumbered}

生物信息学的本质是使用信息学的手段解决生物学问题。自20世纪60年代发端以来，生物信息学对整个生物领域的发展产生了巨大的影响。2003年在多国科学家的通力合作下，科学家们完成了人类参考基因组的测序，随后越来越多模式生物的参考基因组也完成拼装，生物信息学或者说整个生物学的研究进入了一个新纪元。

2006年Illumina公司开发了第二代测序技术（Next Generation Sequencing，NGS），随着NGS技术的推广，一系列之前看似天方夜谭的测序技术得到应用：

- 如可以对人的每一个基因进行表达水平测定的RNA-Seq技术；
- 对基因组每一个突变进行鉴定的全基因组测序（Whole Genome Sequencing，WGS）；
- 对表观遗传学甲基化水平进行刻画的BS-Seq；
- 对基因组三维结构进行详细刻画的Hi-C技术，ChIA-PET技术等等；
- 对没有参考基因组的生物进行基因组的测序与组装
- ……

也是因为这些技术的推广与应用，目前生物信息学一个很大的挑战就是理解和分析这些海量的数据。

在分析数据的过程中，使用R语言或者Python语言对原始的生物信息数据进行清洗，加工，分析，展示已经成为主流。不但使用便捷，而且两种编程语言都是开源语言没有版权和商业的限制，更重要的是使用人数众多，常见的问题都能过通过Google搜索到解决方案。

但是在生物信息学蓬勃发展的今天，国内鲜有一本能够将编程技术与实际生物信息学分析结合起来的参考书目，这给众多想要入门生物信息学的同学，老师及需要数据分析的临床医生带来了非常大的挑战。入门门槛较高，学习曲线比较陡峭是妨碍大家学习生信的主要问题，因此本书尝试用贴近真实数据分析的视角，为大家讲解我们认为最重要的生信相关知识点，并给出完整的测试数据及代码，方便大家进行学习。

我们不期能够大而全地介绍每一个生物信息学细节，而希望为大家提供一份较为通俗易懂的入门手册，在阅读和实践的过程中逐渐感受到生物信息学数据的处理方式，领会数据处理的原理。同时，针对生物信息学中涉及到的R语言，统计学及相关生物背景知识我也会给出相应的学习建议，方便大家更加深入地学习。

总之，学习的路上，有万千条的路径，我们的目的是为你提供一条参考的可能。尽信书不如无书，领会精神，体会数据处理的方法论，远比会敲几行代码更重要，也对以后的发展更有帮助。

种一棵树，最好的时间是十年前，其次，便是现在！

希望在前进的路上，我们能够共勉！

<!--chapter:end:0010-introduction.Rmd-->

# 高通量测序技术基础{#basic_knowledge}

## Illumina 测序技术原理
目前我们接触到的很多生物信息学的技术，都是基于NGS技术的，比如RNA-Seq，ChIP-Seq，FAIRE-Seq，ChIA-PET，Hi-C等等。所谓的NGS就是Next Generation Sequencing，翻译为“下一代测序技术”，或者是“第二代测序技术”。之所以这么叫，是因为相比较于第一代测序技术其测序通量有了很大的提升。

其实，二代测序比较常见的有罗氏454测序，Illumina等。但目前最为常用的NGS技术就是illumina测序技术，它能够保证在几十个小时内产生几百G甚至上T的测序数据，完全能够满足高通量测序的通量要求。并且其测序准确程度也是完全能够保证。我在这里很决断的说，在目前高通量测序的科研领域，Illumina测序绝对是主导地位的，几乎没有其他的公司可以撼动它。因此，我们这篇文章就Illumina测序的原理做一个比较详细的介绍，希望对大家入门生物信息学有所帮助。

### 一些常用基本概念的介绍

- **flowcell** 是指Illumina测序时，测序反应发生的位置，1个flowcell含有8条lane
- **lane** 每一个flowcell上都有8条泳道，用于测序反应，可以添加试剂，洗脱等等
- **tile** 每一次测序荧光扫描的最小单位
- **reads** 指测序的结果，1条序列一般称为1条reads
- **bp** base pair 碱基对，用于衡量序列长度
- **双端测序** 只一条序列可能比较长如500bp，我们可以两端每端各测150bp
- **junction** 上面说的双端测序，中间会留有200bp测不到的东西，我们叫junction
- **adapter** 就是测序中需要的一段特定的序列，有类似于引物的功能
- **primer** PCR中的引物

![这就是一台illumina最新的XTen测序仪](./image_intro/pic_01_sequencer.jpg)

![这就是flowcell，图中透明的部分就是lane，每一个lane中整齐排列了无数个tile，只可惜我们肉眼看不到](./image_intro/pic_02_flowcell.jpg)

### 建库

由于Illumina测序策略本身的问题，导致其测序长度不可能太长，目前最好的X Ten也就是双端各150bp，所以不可能直接拿整个基因组去测序，所以在测序的时候需要先打断成一定长度的片段，这个根据需要用不同的策略，一般测人的基因组，我们是将其打断成300 ~ 500bp的长度。这个是根据跑胶控制的。

打断以后会出现末端不平整的情况，用酶补平，所以现在的序列是平末端。

完成补平以后，在3'端使用酶加上一个特异的碱基A

加上A之后就可以利用互补配对的原则，加上adapter，这个adpater可以分成两个部分，一个部分是测序的时候需要用的引物序列，另一部分是建库扩增时候需要用的引物序列

![DNA文库制备的典型流程](./image_intro/pic_03_make_lib.jpg)

### 桥式PCR
将上述的DNA样品调整到合适的浓度加入到flowcell中，再加入特异的化学试剂，就可以使得序列的一端与flowcell上面已经存在的短序列通过化学键十分强健地相连，如下图。图中不同的颜色表示的是两种不同的adpater，分别对应序列之前加入的两种adpater

连接以后就正式开始桥式PCR。首先进行第一轮扩增，将序列补成双链。加入NaOH强碱性溶液破坏DNA的双链，并洗脱。由于最开始的序列是使用化学键连接的，所以不会被洗。

加入缓冲溶液，这时候序列自由端的部分就会和旁边的adpater进行匹配。

进行一轮PCR，在PCR的过程中，序列是弯成桥状，所以叫桥式PCR，一轮桥式PCR可以使得序列扩增1倍。

如此循环下去，就会得到一个具有完全相同序列的簇，一般叫cluster。

![cluster模式图](./image_intro/pic_04_cluster.jpg)

桥式PCR的整体流程大体如下：

![桥式PCR](./image_intro/pic_05_PCR.jpg)

形成这种1个cluster，1个cluster的形态，在整个flowcell中看上去，示意图如下。其中的每1个cluster就算是1群完全相同的序列。

### 测序

测序的过程反而简单了不少。就是来一个primer，然后加入特殊处理过的A，T，C，G四种碱基。特殊的地方有两点，一个是脱氧核糖3号位加入了叠氮基团而不是常规的羟基，保证每次只能够在序列上添加1个碱基；另一方面是，碱基部分加入了荧光基团，可以激发出不同的颜色。

特殊处理的脱氧核糖核酸，引用自：http://www.oezratty.net/，图中的核糖的羟基应该换成-N2的叠氮基团。

![base带有荧光基团](./image_intro/pic_06_base.jpg)

在测序过程中，每1轮测序，保证只有1个碱基加入的当前测序链。这时候测序仪会发出激发光，并扫描荧光。因为一个cluster中所有的序列是一样的，所以理论上，这时候cluster中发出的荧光应该颜色一致。一个测序扫描图片如下：

![测序过程中不同碱基会激发出不同波长的荧光](./image_intro/pic_07_color.jpg)

随后加入试剂，将脱氧核糖3号位的—N2改变成—OH，然后切掉部分荧光基团，使其在下一轮反应中，不再发出荧光。如此往复，就可以测出序列的内容。

![边合成边测序示意图](./image_intro/pic_08_seq_color.jpg)

限制Illumina测序会有长度的原因，主要是下面2点：

1. 测序时，经过长时间的PCR，会有不同步的情况。通俗一点讲，比如一开始1个cluster中是100个完全一样的DNA链，但是经过1轮增加碱基，其中99个都加入了1个碱基，显示了红色，另外1个没有加入碱基，不显示颜色。这时候整体为红色，我们可以顺利得到结果。随后，在第2轮再加入碱基进行合成的时候，就变成了，之前没有加入的加入了1个碱基显示红色，剩下的99个显示绿色，这个时候就会出现杂信号。当测序长度不断延长，这个杂信号会越来越多，最后很有可能出现，50个红，50个绿色，这时候我们判断不出来到底是什么碱基被合成。

2. 测序过程中，使用的碱基是特殊处理的，有一个非常大的荧光基团修饰。在使用DNA ploymerase的时候，酶的状态也会受到底物的影响，其活性也越来越差。所有基于荧光淬灭原理的测序仪都有类似的问题，比如目前用过自主知识产权的华大智造测序仪，也是有类似的问题。


## PacBio
随便写一点内容！

## Nanopore
随便写一点内容！

## 华大智造测序仪
随便写一点内容！





<!--chapter:end:0020-introduction_of_NGS.Rmd-->

---
title: "040-mapping_and_bam_operation"
output:
  html_document: default
  pdf_document: default
  word_document: default
---
# 测序数据的比对及文件操作 {#mapping_and_BAM}

## 常用比对方法概述

### 从双序列比对说起
双序列比对是一切比对问题的基础。所谓的序列比对就是找到两条序列最佳的匹配方式。

**比对**其实应该对应的单词是alignment，但往往特指低通量的序列之间的比较。比如10条序列，进行多序列比对就是我们常说的 multiple alignment问题；如果是2条序列的比对，我们经常称其为pairwise alignment.

**回贴**通常对应的单词应该是mapping，一般指高通量的数据去寻找基因组的位置。比如我们进行测序以后，有10M对read pair，要去寻找他们在基因组上的位置，这个时候就是一个典型的mapping问题。

alignment与mapping其实是密切相关的概念，所有的mapping软件其实都是从低通量的办法逐步改进而得到的。

其实双序列比对（pairwise alignment）的相关算法，主要是Needleman-Wunsch算法（全局比对）和Smith-Waterman算法（局部比对）。


### 使用BLAST对单条序列进行搜索
当我们在鉴定一些未知名物种的时候，常规的分子生物学操作通常是：提取物种DNA，而后使用通用引物进行pcr扩增，送去公司进行sanger测序，序列结果返回后，通过NCBI进行检索，从而获取分子层面的物种鉴定。

在检索的过程中，我们选择的通常是一整个数据库进行比对，面对上亿的序列信息，如何在极短的时间内完成整个检索并反馈给用户，采用1对1的比对显然是不现实的，故而NCBI采用了一种启发式的序列检索工具Basic Local Alignment Search Tools，简称BLAST。

BLAST的基本原理就是先对数据库所有序列建立index，在输入序列后，对序列分割成若干段，而后通过快速检索与打分，最后反馈给用户。

## 高通量测序数据的比对算法简介
说回到我们手上的高通量数据，类比blast查询，fq文件就是我们要检索的序列，reference genome就是我们手上存在的数据库，我们要做的事情就是把fq里面的序列全部在reference genome上找一下位置。与blast不同的是这回我们面对的是成千上万条序列的检索，而对应的数据库则小了很多，而且检索序列相对于传统的sanger测序序列其实短了很多，根据这些特性不同，软件设计者们设计了各式各样的软件，但按照所使用的核心算法不同，大致可以拆分成两大阵营：hash-table algorithm以及 BWT algorithm

![高通量序列比对原理 Mohammed Alser et al.2020.Technology dictates algorithms: Recent developments in read alignment](image_mapping/1.png)

### 基于哈希表（hash-table）数据结构的比对算法
哈希表是通过把关键码值（key value） 映射到表中的具体位置来进行访问，从而加快数据的查询速度。其核心思想就是采用种子序列定位及延伸算法（seed-and-extend algorithm）。

根据索引构建对象的不同，可以将软件分为两类：基于参考基因组索引的延伸比对软件与基于短序列数据集索引的延伸比对软件。

基于参考基因组索引构建哈希表数据结构的软件代表有PASS跟GASSST，其工作原理就是通过查询短序列在参考基因组的可能检索位点来定位序列可能存在的位置；基于短序列数据集构建索引的则刚好与之相反，此种索引构建方法为大部分哈希表比对软件所采用，代表软件诸如SOAP,SeqMap等等。

而根据哈希表所采用的比对策略不同，又可以分为连续种子序列（contiguous seed）策略与间隔种子（spaced seed）策略。
在了解这两种不同的比对策略之前，让我们先来实际看看哈希表是大概怎么构建的。

#### 哈希表的构建
了解哈希表之前，我们需要补充一个概念k-mer：所谓k-mer，就是将一段序列拆分成包含k个碱基的迭代子序列，即从一条母序列中迭代的选取长度为K个碱基的序列，若母序列的长度为L，k-mer长度为K，那么就可以得到L-K+1个k-mer。

DNA序列是由A,T,C,G四种碱基排序而成，我们可以按四进制给序列进行计数，而后转换为十进制作为哈希表的关键码值生成函数H（x）。

![](image_mapping/2.png)

举个例子，如果某个子序列为ATGCT，其中我们设定A->0, T->1, C->2, G->3,则H（x） = 1 x 4^0 + 2 x 4^1 + 3 x 4^2 + 4 x 4^3 + 0 x 4^4 = 121,这样我们就得到了5-mer序列在哈希表中的关键码值。将上面的方法进一步推广，即可得到在x长度为n的序列，H(X) = I(n) x 4^n + I(n-1) x 4^(n-1) + ... + I(1) X 4^0。
  
在得到一个哈希表之后，我们就相当于知道了所有seed序列的位置，在检索输入序列后，即可快速进行比对反馈，而后进行延伸就得到了序列所在位置。

![k-mer为5](image_mapping/3.png)

#### 连续种子序列策略
  连续种子序列策略是将短序列拆分成k-mer长的子序列，而后查看由基因组k-mer的子序列所构建的哈希表数据结构进行匹配，从而完成整个回溯过程。
  
  这种算法的缺点是显而易见的，即不允许mismatch的存在，如果序列中出现了至少一个位点的突变，则该位点就会被过滤掉。为了弥补这种缺陷，软件设计者们采用了鸽洞原理（pigeonhole principle）对算法进行了修正：首先，将短序列分割成等会参观的多段迭代子序列，进行定位时，如果完成match上，则证明序列定位成功，如果存在mismatch，只要不超过设定的某个mismatch数目，则将该序列设定为候选序列，在所有候选序列汇总后选出最少的mismatch作为回溯序列。而后又陆续推出了一系列的修正算法，如q-gram过滤算法，但由于本书重点不在算法解释，仅作简单介绍，有兴趣的读者可以自行查阅相关文献。
  
![鸽洞原理](image_mapping/4.png)

#### 间隔种子序列策略
  所谓的间隔种子序列策略，就是种子序列中间允许存在若干个不确定的碱基，即在比对过程种允许mismatch的存在。举个例子，间隔种子序列AGxCGTAA，既可以跟AGGCGTAA匹配，也可以跟AGCCGTAA匹配。这样做的优势就是明显增加了比对算法的灵敏度，但反过来，比对所消耗的时间复杂度明显增加。

###  BWT算法介绍
无论采用的是连续种子策略还是间隔种子策略，两者都存在共同的问题，即面对高重复序列的真核生物基因组时，比对效果会比较差，究其原因就是因为k-mer分割所导致的。为了解决这个问题，软件设计者们另辟蹊径，引入了后缀树作为比对算法，但由于后缀树会保留所有字符串的后缀，故而带来内存消耗，时间复杂度以及空间复杂度激增，从而导致了这一类的软件始终不适合大面积的推广。与后缀树对应的是前缀树，因为可以减少很多重复字符串的比较，查询效率会非常高，虽然内存消耗会非常大，但成功的解决了空间复杂度的问题。在现在内存价格持续走低的时代，大内存从来就不是阻碍条件。而我们所提及的BWT算法，本质就是一种前缀树的实现。

所谓BWT (Burrows–Wheeler_transform)数据转换算法，原本是用于文本存储的一种压缩算法，其大致原理是将原来的文本转换为一个相似的文本，转换后使得相同的字符位置连续或者相邻，再通过其他手段对文本进行压缩。
构建BWT的步骤大致如下：

(1)给定一个子序列，譬如：ACAACG，给其后面加入一个后缀$,而后迭代排序。

![](image_mapping/5.png)

(2)按照ASCII码进行大小排序，得到转置矩阵。

![](image_mapping/6.png)

(3)取每个串的最后一个字符串，连成一个序列，即得到BWT='GC$AAC'。

构建完一个BWT之后，在回溯过程其实就是一个解码过程，具体解码步骤如下：

(1)L列的第一个元素为原始序列的最后一个元素（因为$在该位置后面）。
(2)F列中的每一个元素，都是其同一行中的L列的下一个元素。也就是L列是F列的前一个元素。

![此时我们确定了开头就是G](image_mapping/7.png)

![由此确定了第二个字符是C，即目前的序列是GC](image_mapping/9.png)

![确定了是后缀的第二个C，然后这个C的前缀指对后缀的第三个A，我们就知道了目前的序列是GCA](image_mapping/10.png)

![后面依次类推，得到GCAA,而后就是GCAAC,GCAACA](image_mapping/11.png)

## 常用的高通量比对软件
现在最为流行的二代测序比对软件基本都是基于BWT算法的，例如最早的bowtie与bwa，后面针对转录组又开发了bowtie2，再到后面的tophat2，到现在的hisat2。
由于后面的tophat2与hisat2都是基于bowtie2进行改进的，故而这里仅对bwa，bowtie以及bowtie2进行讲解，从粗略的理解深入对这三者进行比较，方便读者在日后的科研工作中进行选择。

首先说一下bwa，其优势在于提供了更多的比对模式选择，可以根据基因组大小进行比对模式选择，也可以根据序列长短进行比对模式选择，同时mem模式对长序列提供了更好的支持，可以处理三代测序数据，更常见于重测序数据的处理。

bowtie与bowtie2，其实bowtie2更像是对bowtie的一个补充。比起bowtie，bowtie2支持了gap，同时也允许了参考基因组出现不确定碱基N，同时支持了局部比对，在中长序列（50-1000bp）的处理上更具速度与准确性。但在面对small RNA等短序列的时候不允许gap与不确定碱基的bowtie更具优势，究其原因就是比对上更为严格，仅支持全局最优的序列作为比对成功序列。

至于bwa与bowtie2在处理转录组数据时，谁更具备优势，其实很难界定，更多是看个人的工具使用倾向，同时在处理长序列的能力方面，作为bowtie2的最新升级版hisat2也在19年下半年的更新中得到了显著性提升，在许多泛基因组的研究中被越来越多的使用。

### 以Bowtie2为例进行实操讲解
下面本书就以bowtie2的安装与使用为例，讲解在使用过程中应该注意的事项。

#### bowtie2的安装
由于bowtie2有将安装包放进conda的channel--bioconda里面，故而最为方便的安装方式是直接使用conda进行安装

首先，如果我们在不知道具体哪个channel的情况下，可以在浏览器中输入“conda cloud”进行检索（以必应为例）

![](image_mapping/12.png)
点进去即可搜索bowtie2

![](image_mapping/13.png)
搜索结果如下

![](image_mapping/14.png)
点进入即可看到安装命令行

![](image_mapping/15.png)

```
conda install -c bioconda bowtie2
#在软件检索完成之后，按照提示输入y即可按照完成

```

![](image_mapping/16.png)

按照完成后即可在命令行中敲出bowtie2，连按tab键补齐三下即可看到所有bowtie2开头的命令

![](image_mapping/17.png)

这种按照方法较为简单，推荐刚入门的新手使用，而对于已经熟悉了的读者，则可以自行下载，并配置全局调用，此处简单介绍，各位以后想自己安装了就可以自行尝试

首先在搜索引擎上搜索bowtie2

![](image_mapping/18.png)

进入官网，即可看到每个版本修复的问题，而在右下角提供的github链接则为我们要下载的源码地址

![](image_mapping/19.png)

点击绿色的clone按键，在window的用户可以下载为zip而后解压传输到服务器上，如果服务器网络较好，也可以通过clone的方式下载到服务器上

![](image_mapping/20.png)

```
git clone https://github.com/BenLangmead/bowtie2.git

```

![](image_mapping/21.png)

```
#由于bowtie2是无需编译的，下载完成后，即可立即使用

#进入下载后的文件夹，不知道文件夹全名是什么可以ls一下，即可看到当前目录的所有文件跟文件夹，选择进入
cd bowtie2 

#看到bowtie2文件夹内的所有文件
ls 

#选择当前文件夹内的程序使用./+文件名，-h即打开说明书，回车一下即可看到bowtie2的使用说明
./bowtie2 -h 

#获取当前的全路径，并复制
pwd 

#打开环境配置的文件，按i进入编辑模式,去到最后一行输入下一列内容
vim ~/.bashrc 

#从home到bowtie2这一段为刚刚pwd复制的全路径
export PATH="$PATH:/home/Alfred/biosoft/bowtie2/bowtie2-2.3.5.1-linux-x86_64/" 

#ESC键退出编辑模式，并按:wq，退出并保存
source ~/.bashrc #更新当前环境

```

由于购买此书基本为新手，故而不推荐大家一开始就进行自行下载，更新环境，能用conda解决就用conda解决，等熟悉了Linux的操作逻辑再自行翻阅尝试即可。

#### bowtie2的使用
作为一名生信从业的科研人员，我们面对不熟悉的软件，第一件事并不是火急火燎的去乱问别人，而是应该秉承着先检索前人使用经验与阅读说明书的原则去熟悉一个新软件，在GitHub的下载页面下面即有bowtie2的使用简要说明

![](image_mapping/22.png)
下面由我跟大家用实际例子做个介绍

首先，我们需要从书上提供的地址下载参考基因组，下载完成之后即为一个fa文件
![](image_mapping/23.png)

我们使用bowtie2做的第一件事就是对这个参考基因组构建一个索引，这一步的目的就是上文提到构建索引表，供后续比对检索回帖

```
bowtie2-build chrX.fa chrX.fa
# bowtie2-build命令为构建索引的命令
# 第一个chrX.fa代表输入的参考序列
# 第二个chrX.fa代表输出的索引文件前缀
# 产生六个.bt2新文件

```

![](image_mapping/24.png)

接着就是拿我们在上一个步骤处理干净的clean data进行回帖操作，这一步可以理解为将所有短序列在参考基因组上找回他们对应的位置，下面我们对bowtie2的参数进行一个大概的认知。

```
#必选参数
# -x <int> 选择索引前缀，即刚刚由bowtie2-build所生成的chrX.fa。
# -1 <int> 双端测序对应的R1.fa，可以为多个文件，并用逗号分开；需要与-2中的R2.fa文件一一对应。
# -2 <int> 双端测序对应的R2.fa.
# -U <int> 单端测序对应的fa，可以为多个文件，并用逗号分开。
# -S <int> 指定所生成的SAM格式的文件前缀。
#常用可选参数
# -p/--threads <num> 设置线程数.默认为1
# --reorder 配合-p使用，使比对结果在顺序与fq的reads顺序一致
# --seed <int> 设置随机种子
# --no-unal 不记录没比对上的reads
# --un-gz <path> 将unpaired reads输出到指定的<path>,并以gzip形式压缩
# --al-gz <path> 将至少能比对1次以上的unpaired reads写入<path>，并以gzip形式压缩
# -5/--trim5 <int> 剪掉5'端<int>个碱基再比对
# -3/--trim3 <int> 剪掉3'端<int>个碱基再比对
#比对参数
#-N <int> 比对时允许的mismatch数目，除非是跨物种比对，一般不更改
#-L <int> 设置比对时reads种子的长度
#-i <int> 设置两个相邻种子间的间隔碱基数
#--n-ceil <func> 设置reads中允许含有的N碱基数目
#--gbar <int> 设置头尾<int>个碱基内不允许的gap数
#--end-to-end 全局比对，为默认模式
#--local 局部比对，多用于找motif，read两端的一些碱基不进行比对罚分
#罚分参数
#--ma <int> 设置匹配得分，仅在--local时生效，比对上一个碱基得<int>分，默认为2，而全局比对时为0
#--mp MX,MN 设置错配罚分，MX即最高罚分，MN为最低分，默认为MX=6，MN=2，如果设置--ignore-qual则每次错配为MX
#--np <int> 当匹配到N时的罚分，默认为1
#--rdg <int1>,<int2> 设置read上打开gap罚分<int1>，延长gap罚分<int2>,默认为5，3
#--rfg <int1>,<int2> 设置reference上打开gap罚分<int1>，延长gap罚分<int2>,默认为5，3
#--score-min <func> 设置有效比对的最小分值，在全局比对时默认为L,-0.6,-0.6，在局部比对时默认为G,20,8
#双端比对参数
#-I/--minins <int> 设置允许插入片段最小长度，默认为0
#-X/--maxins <int> 设置允许插入片段最大长度，默认为500

```

看到这么多参数可能会觉得头晕目眩，其实在我们正常使用中，仅仅是选择必须参数与多线程即可，在比对完成后查看结果再进行调整。

```
bowtie2 -p 10 -x chrX.fa -1 ERR188245_chrX_1.fastq.gz -2 ERR188245_chrX_2.fastq.gz -S ERR188245.sam &

```

#### 对比结果检查
在比对完成之后，bowtie2会输出一段log文件，记录着比对情况，但那只是初略的比对情况，简单的检查可以用，但如果是涉及每个染色体的比对情况，则推荐用qualimap2进行检查。该软件的安装，使用conda即可

```
conda install -c bioconda qualimap
```

而后进行质检也非常简单，选择bamqc即可：

```
qualimap bamqc -bam ERR188245.sam -outdir bamqc_result -outformat PDF:HTML
```

如果想看注释的区域也可以加上gff文件的参数：

```
qualimap bamqc -bam ERR188245.sam -gff chrX.gff -outdir bamqc_result -outformat PDF:HTML

```

## SAM文件与BAM文件操作基础

### SAM文件与BAM文件的介绍 
经过bowtie2比对之后，会生成一个后缀是sam的结果文件，这个文件里面就记录了我们的比对的结果，下面我们使用less指令查看这个文件，看看有什么玄妙的地方

```
less ERR188245.sam

```

![](image_mapping/25.png)

我们可以看到第一行是@HD开头，VN表示版本号，SO表示是否经过排序如果是排过序的是显示coordinate，没有排序则是unsorted
而第二行是@SQ，后面跟的是染色体号以及染色体长度，单位是bp
第三行则是@PG，表示使用的程序跟命令行。
上面这些@开头的部分统称为头文件，记录着一些基本信息
下面一系列格式类似的则是我们的比对结果，每一列记录着不同的信息。
第一列即ERR开头的这些表示的是read的编号，即fq文件的第一行
第二列是一列数字，这列数字叫做flag，即位标识，表示的是比对上的情况，是下面这些情况的数值之和

```
0：比对到参考序列的正链上
1：是paired-end或mate pair中的一条
2：双末端比对的一条
4：没有比对到参考序列上
8：是paired-end或mate pair中的一条，且无法比对到参考序列上
16：比对到参考序列的负链上
32：双末端reads的另一条（mate）比对到参考序列的负链上
64：这条read是mate 1
128：这条read是mate 2
#后续根据比对情况进行过滤就是用到这些数字

```

第三列是表示比对上的参考基因组的某条染色体，如果什么都没比对上则是'*'

第四列是比对上的染色体的具体位置起始位置，从1计数，如果比对不上则是以0计数

第五列是比对质量，MAPQ，即比对结果的可信度，从0到60，数值越高越好，一般认为大于等于20都是可信的。

第六列是比对情况表达式，CIGAR，主要由soft  clipping 、match/mismatch、insertion、deletion、 padding、skipped bases、hard clipping、match、mismatch对应字母S、M、I、D、P、N、H、=、X跟数字组成，38s432N38M，表示前三个碱基被剪切掉了，然后432个碱基被绕过，38个碱基可能是match或者是mismatch的

第七列表示下一片段比对上的参考序列的标号，同一片段用=，没有另外片段则为'*'

第八列表示下一片段比对上的位置，如果不可用则用0

第九列表示Template的长度，最左边得为正，最右边的为负，中间的不用定义正负，不可用则为0

第十列则为比对上的reads对应的序列信息

第十一列则是比对上的序列的质量信息，计分方法同FASTQ文件

看到这里你可能觉得头晕晕的，但其实可以不用记得这么仔细，你只需要知道sam文件就是记录了比对上了哪些reads，比对上的reads在什么位置，这些reads比对的质量怎么样即可了，到真的需要过滤的时候再查看一下具体内容就行了。

### BAM文件的生成
由于我们的sam文件是文本类的文件，这就导致比对所产生的结果文件动辄大几G，对我们硬盘的造成了很大存储压力，如果压缩则能够减小很多体积，而直接转成二进制文件则更为节约体积，故而就诞生了一种二进制格式bam来对比对结果进行存储，除了是二进制以外其存储的内容与sam文件无异。怎么区分这两个呢，我觉得用英文区分就很简单可以区分开，s是string的意思，字符，文本的意思，b是binary的意思，二进制的意思，一下子就知道两者的区别了。

那么转成二进制文件之后，要怎么打开呢？很明显使用less这种打开文本文件的是不适合的了。这个时候就要提到bwa之父李恒大神为sam与bam开发的一个处理利器samtools。首先是国际惯例，安装

```
conda install -c bioconda samtools

```

安装完毕之后就可以在命令行上使用了，首先是将sam文件转换为bam文件：

```
# 将sam文件转换为bam文件
samtools view -b -S ERR188245.sam > ERR188245.bam

# 同样的，我们可以把bam文件转为sam文件
samtools view -h ERR188245.bam > ERR188245.sam
```

那么问题来了，转为bam文件之后，怎么用samtools查看？我们可以将bam转为sam，然后再利用管道符用less查看：

```
# 查看完整的bam文件
samtools view -h ERR188245_chrX.bam | less -S

#如果只想查看头文件
samtools view -H ERR188245_chrX.bam

#如果想跳过头文件
samtools view ERR188245_chrX.bam  | less -S

```

### BAM文件的排序
如果我们是做全基因组测序，那么在进行下游分析之前，需要对bam文件进行一个排序，这个功能可以用samtools，也可以用Picard或者gatk做到。

使用samtools对bam文件进行排序：

```
samtools sort -@ 20 -m 8G -O bam -o ERR188245_chrX.sorted.bam ERR188245_chrX.bam
# @：指定线程数
# m：每个线程分配的最大内存
# O：输出文件格式
# o：输出文件的名字
# 输入文件放在最后
```

如果是picard的话，可以参考下面的命令：
```
java -jar picard.jar SortSam I=ERR188245_chrX.bam  O=ERR188245_chrX.sorted.bam  SORT_ORDER=coordinate

```

如果使用GATK工具，对bam文件进行排序，可以参考：

```
#如果是gatk的话, 先建立index与dict
samtools faidx chrX.fa
gatk CreateSequenceDictionary -R chrX.fa -O chrX.dict

#再使用gatk进行排序
gatk SortSam -I ERR188245_chrX.bam -O ERR188245_chrX.sorted.bam -R chrX.fa -SO coordinate --CREATE_INDEX

```

### BAM文件的index的建立
经过排序之后的bam文件，就可以建立索引，如果不排序则会报错。建立bam文件的索引文件，是为了更方便地

```
samtools index ERR188245_chrX.sorted.bam

```

运行完上面的命令，即可在文件夹中获得一个index文件，一般情况下默认的文件名为bam文件名后面增加`.bai`后缀。比如这里就会生成`ERR188245_chrX.sorted.bam.bai`文件。我们在对排序完的bam文件进行一些特殊的操作时，一般都需要index文件和bam文件在同一文件夹中，否则可能会出现报错的现象。

### 对比对结果进行过滤
果然想通过mapping质量或者比对情况进行过滤，那samtools一定是处理代码最为简洁的。

```
samtools view -h -b -q 20 -F 4 -F 256 ERR188245_chrX.sorted.bam > ERR188245_chrX.q1F4F256.sorted.bam

#-f 提取提取出没有mapping上的reads
#-F 过滤过滤掉没有mapping上的reads，也就是说提取出mapping上的reads
#-u 输出格式为未压缩的bam格式
#-q 过滤掉MAPQ值低某个阈值
#-h 设定输出的SAM文件带有header
#-b 输出格式设定为BAM
#-S 输入格式为SAM
```

### 对比对结果进行统计

如果相对bam文件进行一些基础的统计分析，比如测序片段的数目，整体的突变情况，基因组测序结果的覆盖度等等，都可以用下面的命令生成报告。

```
samtools flagstat ERR188245_chrX.sorted.bam

```

结果文件统计bam文件中reads的比对情况，如多少reads比对上等信息，其中的结果比较丰富，但是需要再使用R或者Python编程进行生成图表。所以，当不追求速度的情况下还是建议用qualimap2软件。


### 去除bam文件中的PCR扩增冗余

这一步，我们经常叫`remove duplication`。所谓的duplication一般是指构建测序文库的过程中，会有PCR扩增的步骤，这个步骤往往会对片段进行多次扩增。如果有来源于同一个原始片段的测序结果比对到了基因组上，有可能会对我们的下游分析造成一些影响。所以，某些情况下需要对bam文件进行冗余的去除，这里的冗余一般习惯上称为`duplication`。

去除duplication的方法一般有两种，1个是使用samtools rmdup命令，另一个是使用GATK/Picard工具中的MarkDuplicates。

```
samtools rmdup ERR188245_chrX.sorted.bam ERR188245_chrX.sorted.rmdup.bam

```
由于samtools的算法是针对单端测序的，故而在对双端测序的bam文件处理效果奇差无比，在处理双端测序的文件时，通常我们更推荐使用gatk或者Picard。

首先对duplicate进行标记

```
gatk MarkDuplicates -I ERR188245_chrX.sorted.bam -O ERR188245_chrX.sorted.mkdup.bam -M ERR188245_chrX.metrics --CREATE_INDEX

```

接着就是移除duplicate，但一般也只是标记不移除。

```
gatk MarkDuplicates REMOVE_DUPLICATES=true -I ERR188245_chrX.sorted.mkdup.bam -O ERR188245_chrX.sorted.rmdup.bam -M ERR188245_chrX.metrics

```

或者使用Picard一步进行上述GATK的两步过程：

```
java -jar picard.jar MarkDuplicates I=ERR188245_chrX.sorted.bam O=ERR188245_chrX.sorted.mkdup.bam M=ERR188245_chrX.metrics ASO=coordinate REMOVE_DUPLICATES=true
```

关于samtools的用法其实很多，但限于篇幅，我们只对最常用的几个命令进行了简单介绍，对于组学分析中的其他应用可以参考接下来各章的介绍。

## IGV可视化查看比对结果

虽然使用samtools的flagstat或者qualimap2可以从一个总体的情况得知整个fq的比对情况，但有时候，我们可能只是想看染色体上某一段区域，又或者还想直观的看编码区之类的比对情况，那这个时候就需要一个可视化的基因浏览器---IGV（Integrative Genomics Viewer）。
首先国际惯例，如何找到这个软件

打开bing，搜索IGV
![](image_mapping/26.png)

本次以桌面版为例
![](image_mapping/27.png)

![](image_mapping/28.png)

而后按照指示安装完成之后，我们来处理一下我们的bam文件，为导入到IGV里做准备

```
#如果还没对序列排序，记得先排序
samtools sort -@ 2 -o ERR188044_chrX.sorted.bam ERR188044_chrX.bam

#排好序之后，对bam文件建立index
samtools index -@ 2 ERR188044_chrX.sorted.bam ERR188044_chrX.sorted.bai

```

而后我们打开安装好的IGV，可以看到如下界面

![](image_mapping/29.png)

选择File--> Load from File--->加载想要查看的bam文件

导入成功后，可以选择染色体，由于我们的测序只测了chrX，故而选择chrX

![](image_mapping/30.png)

![](image_mapping/31.png)

![](image_mapping/32.png)

不断双击想查看的位置，即可放大该位置

![](image_mapping/33.png)

IGV工具是可视化bam文件的一个非常好的方法，好好利用可以事半功倍地帮助我们检查bam文件中的比对问题，更好地展示结果。

<!--chapter:end:0040-mapping_and_BAM_operation.Rmd-->

# 转录组数据分析 {#RNA_Seq}

RNA测序（RNA sequencing，RNA-Seq）是一种非常成熟的研究转录组学的技术，是目前使用最广泛的高通量测序技术之一。一个细胞所蕴含的全部遗传物质（DNA）即基因组，根据中心法则<sup>1</sup>，遗传信息由DNA通过转录作用流向RNA，这些RNA的总和被称为转录组 （transcriptome），研究转录组的方式方法及相关技术即转录组学（transcriptomics）。通过转录组测序可以解决多种生物学问题，例如寻找实验组和对照组的差异表达基因、目标研究对象在不同发育或者生物学过程中的基因表达时序性变化等。

## 什么是RNA-Seq？

RNA可以分为能够编码蛋白基因的信使RNA（mRNA）<sup>2</sup>和非蛋白编码RNA （non-coding RNA, ncRNA），例如人类基因组，含有约20000个蛋白编码基因和7000个非蛋白编码RNA基因。随着研究的深入，生命科学研究者对RNA的认识逐渐全面，陆续发现了生物体中多种类型的非编码RNA，有持家非编码RNA（house-keeping non-coding RNA）：在翻译过程中起转运作用的tRNA<sup>3</sup>、核糖体的组成成分rRNA<sup>4</sup> 、参与mRNA剪接的snoRNA（small nucleolar RNA）<sup>5</sup>等；还有能够起到调控作用的非编码RNA：长非编码RNA（long non-coding RNA, lncRNA）、miRNA（mircoRNA）<sup>6</sup>、小干扰RNA（small interfering RNA, siRNA）和环状RNA（circRNA）等。

研究人员通常会对mRNA和一些调控非编码RNA感兴趣，针对不同类型的RNA，采取的测序手段也不同，主要表现为样本建库策略的不同。测序仪通常只能对DNA序列进行测序，测序之前对样品里的目标待测RNA进行处理的过程称为“文库的制备”，简称建库（图3.1）。 
	
<img src="./image_RNASeq/RNA-seq-all.jpg" alt="RNA-seq-all" style="zoom:8%;" /> 图3.1 RNA测序建库的多种策略

用富集polyA方式可以获得mRNA的表达信息、也可以获得部分lncRNA（含有polyA 的lncRNA）的表达信息；通过去rRNA方式建库可以检测到mRNA、全部lncRNA、circRNA的表达信息；去线性建库则是专门为了检测circRNA的表达；短片端建库能够获得以miRNA为主的小RNA表达信息。选用何种建库方式，应结合研究目的来进行实验设计。

### 对mRNA测序

研究蛋白编码基因表达应采用富集poly-A的方式进行建库测序（图3.1）。利用真核生物mRNA都具备poly-A的特殊结构这一特性，对样本中含有poly-A的RNA进行富集。需要注意的是，部分lncRNA也含有poly-A结构，所以采取这一方式建库也可以检测到这部分lncRNA的表达。mRNA测序一般采取双端测序，测序读长150bp，数据量要求在6G clean reads左右。

建库分为多个步骤：

1. 用磁珠捕获含有poly-A结构的RNA；
2. 将RNA片段化，这是由于二代测序技术的限制只能对最长数百bp的DNA进行测序，而mRNA的长度平均为数千bp；
3. RNA反转录为小片段的双链cDNA，因为单链RNA的稳定性太差，且测序仪是针对DNA测序的；
4. 对cDNA的3'端加A，使之成为粘性末端，然后链接上barcode序列和统一的接头序列，在测序过程中是对多个样本同时测序，为了区分开来需要给不同的样品加上不同的barcode。

### 长非编码RNA-seq

长非编码RNA是一类长度大于200 nt的长非编码RNA，在不同物种中的保守性较差，曾经被认为是无用的RNA，目前被发现广泛参与基因表达调控的多种过程<sup>7</sup>。可根据其在基因组上的位置分为四类：

1. 与编码基因有重叠且转录方向一致的同义长非编码RNA（sense lncRNA）；
2. 与编码基因有重叠但在反义链上的反义长非编码RNA（antisense lncRNA）；
3. 由编码基因内含子转录产生的内含子长非编码RNA（intronic lncRNA）；
4. 以及位于两个编码基因之间非编码区的基因间区长非编码RNA（intergenic lncRNA, lincRNA）。

lncRNA的发挥多种调控功能，扮演信号分子、诱导因子、引导分子、支架分子等多种角色<sup>8</sup>。

对lncRNA 进行测序需要采用去rRNA的方法建库，以最大限度地保留lncRNA（图3.1）。与此同时，mRNA、snoRNA、snRNA、tRNA和cricRNA的表达也能在rRNA建库转录组测序中得到。与富集polyA方法不同的是，建库的第一步是去除样本中的rRNA，接下的步骤则与富集polyA方式建库差不多。lncRNA测序一般采取双端测序，测序读长150bp，数据量要求在10～12G clean reads。

### small RNA-seq 

microRNA广泛存在于动植中，是一类长度为22nt左右的小非编码RNA，通过抑制蛋白质翻译或者降解mRNA，在多种生物学过程中发挥调控作用。对microRNA测序需要做小RNA测序（small RNA-seq ），建库过程中需要回收小片段，这是与mRNA建库的主要不同之处。miRNA的功能涉及多种生物学过程，有潜力成为许多疾病包括癌症的标志物。建库起始样本可以用总RNA，也可以用分离纯化得到的small RNA。

1.基于small RNA本身对结构特征在3‘端和5’端连上接头序列，多数small RNA具有天然的磷酸化5‘端，且3‘端具有羟基基团，便于核酸序列的连接；
2.然后进行少量逆转录PCR扩增；
3.通过PAGE胶对特定大小的small RNA片段进行纯化，小RNA片段较短20～30nt，加上接头序列后长度在150bp左右；
4.对文库的片段大小、纯度和浓度进行质检。
5. 将得到的文库扩增后上机测序，测序读长50bp，数据量要求在10～20M clean reads。

### circRNA-seq

通常情况下，DNA和RNA是以线性形式存在的，有时候也以环状的形式出现，例如线粒体DNA和细菌DNA、类病毒和一些RNA病毒的单链环状RNA基因组。近年研究发现，真核生物细胞普遍且稳定存在环状的RNA，是mRNA剪接过程中形成的，主要通过吸附miRNA来实现转录水平的调控。circRNA能够类似“海绵”一样竞 争性结合miRNA或RNA结合蛋白，从而可能在生理和疾病过程中 发挥重要的功能。

去rRNA的方式，是目前最常用的方法，可以捕捉环形RNA的信息；另外，也可以通过去线性RNA的方式建库测序，核糖核酸酶R从RNA的自由3'端向5'端方向逐一水解线性RNA，烟草酸性磷酸酶和终止子外切酶能够从5'端向3'端方向逐一水解RNA，而环形RNA没有3'与5‘端和poly(A)，因此不会被降解；还可以利用环形RNA与线性RNA电泳迁移速度的不同来实现对环形RNA的特异性捕获，因为环形RNA会比等长的线性RNA迁移速度快，并且凝胶交联程度越高这种差别就会越大<sup>9</sup>。总的来说rRNA的方式建库具有更高的性价比，能够同时获得mRNA、lncRNA和circRNA的信息。


### 单细胞RNA-seq

前面转录组测序，研究对象都是对多个细胞混合的RNA进行测序，针对的是某一个组织、器官、甚至生物体（例如小型昆虫等），检测到的基因表达情况是所有细胞表达均值。而单细胞测序可以对每一个细胞单独测序，这对发育、肿瘤异质性、微小组织等研究十分重要，单细胞测序已成为目前热门的生命科学技术之一。

单细胞测序是目前的热门技术之一，单细胞测序不仅可以对样本中每个细胞进行转录组测序，还可以进行基因组测序、DNA甲基化测序和ATAC-seq测序。目前得到最广泛应用的单细胞测序平台是10X genomics单细胞平台和BD Rhapsody平台，分别基于DROP-seq技术<sup>10</sup>和Cyto-seq技术<sup>11,12</sup>（图3.2）。

<img src="./image_RNASeq/SC-RNA-seq-lib.jpg" alt="SC-RNA-seq-lib" style="zoom:20%;" />
图3.2 10X genomics平台和BD Rhapsody平台的单细胞RNA-seq测序

10X genomics平台与BD Rhapsody平台在单细胞RNA-seq测序中最大的不同在于微反应载体的不同。10X genomics芯片检测的细胞在液相中实现流动分选：

1. 大量连接着后续反应所需接头、barcode、UMI等序列的微磁珠在芯片管道中流动；
2. 流动的细胞与微磁珠相遇后被吸附上去；
3. 吸附着细胞的微磁珠与流动的油相遇形成油包水滴的乳浊液，亲水的微磁珠和吸附的细胞包裹在油包水的微液滴里，称为GEM（Gel bead in emulsion）;
4. 在GEM里完成细胞裂解、反转录、扩增等；
5. 每个细胞里扩增后的cDNA都带着特异的接头序列，随后进行测序。

BD Rhapsody平台采用蜂窝板技术进行单细胞分离和捕获：

1. 单细胞悬液流过含有大量微孔的蜂窝板使细胞落入微孔中；
2. 将微磁珠铺到蜂窝板上，使微孔中形成微磁珠与细胞的反应体系；
3. 在微磁珠里完成细胞裂解、反转录、扩增等。

两者后续的建库、测序是几乎一样的流程，单次捕获的细胞数量都可以达到很好的通量，在3,000至10,000之间，差距不大。

### 其他转录组测序

随着技术的发展，转录组测序也发展出了更多的测序技术。

#### 全长转录组测序

前文介绍的RNA测序都是基于二代测序技术平台，由于二代测序的技术限制，文库建立过程中需要将RNA片段化，在测序完成之后再对其进行拼接。近年来，基于单分子测序的三代测序不需要对样品进行PCR扩增处理，可以直接对RNA进行测序。例如nanopore纳米孔外切酶测序技术和SMRT实时单分子测序技术。Oxford Nanopore Technologies 公司采用的nanopore纳米孔外切酶测序技术基于电信号测序，核酸外切酶切割ssDNA时切下来的碱基会落入纳米孔，短暂地影响流过纳米孔的电流强度，由于不同碱基影响的电流强度变化不同，以此便可直接读取序列，测序读长得到了极大的提高，可达200 kb，但通量和准确率较低。Pacific Biosciences 公司的SMRT（single-molecule real-time sequencing）技术基于边合成变测序，以SMRT芯片为测序载体，DNA聚合酶、待测序列和不同荧光标记的4种dNTP在芯片上的ZMW（zero-mode waveguide）孔底部进行合成，根据荧光种类判断dNTP的类型，通量高且读长可达1Kb，但成本较高。SMRT测序开发的Iso-Seq（Isoform-sequencing），利用三代测序读长长的特点，不需打断转录本，直接测序，获得全长转录本。

使用三代测序技术进行RNA测序寻找样本之间的差异表达基因时，结果往往不理想，对低丰度基因的转录本容易产生漏检，且三代测序较二代测序而言成本较高，因此三代测序技术较少用于RNA测序。但三代测序技术优秀的读长，应用于基因组测序能够有效的降低拼接计算成本。

#### 空间转录组测序（Spatial Transcritome sequencing）<sup>13</sup>

普通的RNA测序，包括单细胞RNA测序都无法提供组织内部空间不同位置的转录组信息，空间转录组测序在获取转录组信息的同时还加入了空间位置信息。将待研究的组织制作为冰冻切片，转移到组织透化芯片上，不同组织区域的RNA信息释放到芯片上的小孔中，对这些RNA进行测序即可获得各个空间位置的转录组信息。空间转录组并不是单细胞转录组测序的升级，因为芯片上的小孔捕获的通常是多个细胞，二者能够形成较好的互补，可能会成为未来的热门技术。

#### 链特异RNA-Seq

在RNA测序的建库过程中，会丢失RNA链信息，即RNA是来自基因组上哪一条DNA链。然而在基因组中，有许多基因是重叠出现在同一个区域的正负链位置的。要想解决这一问题，就需要获得链特异的RNA-Seq数据，可以采取lillumina RNA ligation method、dUTP method、RT method。

此外，通过对RNA技术的改进可以进行转录起始位点的鉴定：GRO-Seq、NET-Seq和SLAM-Seq；翻译效率的测定：Ribosome footprint；RNA二级结构的测定：PARS、SHAPE-Seq和SHAPE-Map；以及RNA 结合蛋白位点的测定CLIP-seq 。

## RNA-seq的分析

有参转录组分析一般包括：测序数据的质量控制、构建参考基因组索引、将read比对到参考基因组、拼接新的转录本（可选）、基因表达的定量、差异表达基因的分析，以及对目标基因群进行注释和富集分析（图3.3）。	

<img src="./image_RNASeq/RNA-seq-analysis.jpg" alt="RNA-seq-analysis" style="zoom:8%;"/>
图3.3 有参转录组分析流程

转录组测序分析的常用软件如图3.3所示。

测序原始数据的质量评估常用FastQC进行分析； 

Trimmomatic、Cutadapt、Fastx-toolkit用于去除低质量片段和接头序列等；

BWA、Bowtie、Bowtie2、HISAT、HISAT2、STAR等软件用于构建参考基因组和序列比对；

组装转录本是一个可选项，常用软件为Cufflinks、StringTie；

对转录本的常用定量软件有HTSeq、Cuffquant+Cuffnorm、featureCount；

差异表达分析有cuffdiff、DESeq/DESeq2、edgeR；

得到的差异基因需要注释起功能，常用软件为clusterprofer、DAVID网站、Metascape网站等。

<img src="./image_RNASeq/RNA-seq-software2.jpg" alt="RNA-seq-software2" style="zoom:20%;" />
图3.3 有参转录组分析常用软件


### 测序数据的质量控制

测序原始数据是Fastq格式存储到文件，文件中包含序列的测序信息、本身碱基序列信息、碱基质量等内容。由于测序过程中存在很多或主观或客观的因素，例如样本污染或降解、接头污染以及测序过程中不可避免的测序误差等，都影响着测序数据的质量。对测序数据的质量控制可以减少数据噪音，保证结果的准确性。质量控制包括测序质量评估和高质量测序片段的获取。

#### 碱基质量

Fastq文件对每一个碱基质量都基于ASCII码进行了打分（图3.9）。

![ascll](./image_RNASeq/ascll.jpg)

图3.9 ASCII码表	

测序质量控制软件会通过碱基的Q值（Quality Score, *Q*）对碱基进行统计和过滤。

有两种格式Phred33和Phred64，分别代表碱基质量等于ASCII码值减去33或者64，例如：

Phred33：  *Phred("F") = 70 - 33 = 37*

Phred64 ： *Phred("F") = 70 - 64 = 6*

Q值是错误概率（Probability of incorrect base call, *P*）的对数：

Q=-10log<sub>10</sub> *P*

Q值为40则代表错误概率为0.0001；为30则代表错误概率为0.001；为20则代表错误概率为0.01；为10则代表错误概率为0.01。

#### 质量评估软件FastQC

在进行测序数据的正式分析之前，需要对样本的整体质量进行评估，包括碱基质量评估、接头序列检测、重复序列评估等。

FastQC（https://www.bioinformatics.babraham.ac.uk/projects/fastqc/）是常用的fastq质量评估软件（图3.4）。

<img src="./image_RNASeq/fastqc1.jpg" alt="fastqc1" style="zoom:48%;" />  

图3.4 FastQC网站

FastQC可以对每个位点碱基质量进行评估汇总、检测接头序列及重复序列，对GC含量分布、N碱基含量、长度分布进行统计，用网页展示结果。以下示例图片源于用FastQC对一个单端小RNA组测序样本的质量评估。

FastQC会给出一个测序数据总体的质量情况（图3.5）。包括:

1. 基本统计(Basic Statistics);
2. 每个位点的碱基质量（Per base sequence quality)
3. 每条reads的质量均值（Per sequence quality scores）
4. 每条reads中四种碱基出现频率（Per base sequence content）
5. reads每个位置的GC含量（Per sequence GC content）
6. 每个位点不明碱基N的含量（Per base N content）
7. 长度分布图（Sequence Length Distribution）
8. 序列的重复水平（Sequence Duplication Levels）
9. 突出的重复序列 （Overrepresented sequences）
10. 接头序列情况（Adapter Content）
11. 短序列重复片段（Kmer Content）

软件会对以上每一项进行评估，绿色对勾代表“pass”，黄色叹号代表“warn”，红色叉代表“fail”。

![fastqc2](./image_RNASeq/fastqc2.jpg)

图3.5 FastQC对一个RNA测序样本的总览

基本信息的统计能够快速了解样本的基本情况，例如文件类型、编码方式、总read数、序列长度等（图3.6）。

![fastqc2](./image_RNASeq/fastqc3.jpg)

图3.6 FastQC对RNA测序样本基本信息统计

每个位点的碱基质量统计，能够快速了解样本的整体质量（图3.7）。横轴代表碱基在reads上的位置；纵轴代表这个碱基的quality；Quality即为Fred值，计算公式-10*log10(p)，p为测错的概率，假设quality等于20，这个碱基出错的概率为0.01，假设quality等于30，这个碱基出错的概率为0.001；每一个碱基位置有一个箱型图，其中红线代表中位数，蓝线代表平均数；当然任意位置的下四分位数低于10或中位数低于25时FastQC软件会对此项评估为“warn”，当任意位置的下四分位数低于5或中位数低于20时FastQC软件会对此项评估为“fail”。

<img src="./image_RNASeq/fastqc4.jpg" alt="fastqc2" style="zoom:80%;" />

图3.7 FastQC对RNA测序样本的碱基质量

每条reads中四种碱基的统计显示碱基分布不均衡（图3.8）。一般情况下，A、T、C、G四种碱基的出现频率是均衡的，当任一位置的A/T比例与G/C比例相差超过10%时FastQC软件会对此项评估为“warn”，当任一位置的A/T比例与G/C比例相差超过20%时FastQC软件会对此项评估为“fail”。需要注意的是，评估为Fail不代表样品一定不能 用，要结合具体测序对象来分析。例如图3.7中的AT含量较高，导致评估为Fail，这是一个小RNA测序样本，小RNA中有大量的miRNA，而miRNA主要通过与mRNA富含AT碱基的3'非编码区结合，行使其调控功能，因此小RNA测序样本中AT含量高是正常现象。

<img src="./image_RNASeq/fastqc5.jpg" alt="fastqc2" style="zoom:80%;" />

图3.8 FastQC对RNA测序样本的碱基质量

#### 用质量控制软件获取高质量测序片段

对评估后确定数据质量合格的样品，进行进一步的分析。使用Trimmomatic、Cutadapt、Fastx-toolkit、NGSQC等去除数据中的低质量测序片段、接头序列等，以获得高质量测序片段，即clean reads。对于低质量的reads，例如Q值过低、含N过多的reads片段要进行切除或过滤，接头序列包括用于区分DNA片段来自哪个样本的barcode序列、DNA片段的PCR扩增序列，以及DNA片段与测序仪 lane结合的序列。需要切除这部分序列。

Trimmomatic采取滑动窗口的方式对reads质量进行评估，如果窗口碱基质量均值小于指定值，则将该read去除，还可以用于reads的修剪和接头的去除、去除reads 3‘/5’端指定长度，或者质量低于指定值的碱基。Cutadapt偏重对接头的处理，存在于reads内部或者两端的5'/3'接头的去除，设置接头错配率、接头是否含有indel以及在接头中设置通配碱基N等，去除含N过多的reads和低质量碱基。Fastx-toolkit可以对碱基质量进行过滤以及统计。

### 构建参考基因组索引

在上一步的分析中获取到的clean reads，需要将它们回帖到基因组上，在此之前，我们要建立一个基因组索引。对于有参考基因组的转录组分析，构建参考基因组索引是非常关键的一步。构建参考基因组这一步，在许多分析中，操作类似，比如之前章节介绍BWT算法时讲到的，以及后续ChIP-Seq，WGS分析中也会用到类似的操作。

RNA-Seq分析中参考基因组包括基因组DNA序列和基因组注释文件，可以从Ensemble、USCS等数据库获取。

（加一些网站图片）

#### GTF与GFF 文件

RNA-Seq中一个很重要的注释文件就是GTF文件或者是GFF文件。这个文件主要保存

其中基因组注释文件有两种格式，分别是GTF（General Transfer Format） 和GFF （ General Feature Format），那么这二者有何不同？其实GFF有若干个版本，GTF正是GFF文件的其中一个版本，一般认为GTF文件就是GFF 2.0版本的内容。

这两者只是一些格式细节上的不同，包含的信息内容上完全可以等价，也有很多工具可以提供两种格式的互相转换。

一个标准的GTF/GFF2.0文件需要包括9列内容（https://asia.ensembl.org/info/website/upload/gff.html）：

``` 
seqname    #序列名，一般为染色体名
source	   #来源，注释来源的软件名、数据库名等，没有则用“.”表示
feature    #特征类型，包括gene、mRNA、exon、CDS
start      #起始坐标位点
end        #终止坐标位点
score      #得分，该条注释信息可信度的打分，没有则用“.”表示
strand     #正负链，“+”表示正莲，“-”表示负莲
frame      #读码框，表示读码框的位置。当feature为CDS、start_codon、stop_codon时，frame值分别为0、1、2，0表示读码框在该位点进行读码，1表示读码框在该位点1个碱基后进行读码，2表示读码框在该位点2个碱基后进行读码。当feature为其他类型时，则用“.”表示。
attribute  #属性，包含众多属性。格式为“tag=value”，不同属性之间以分号相隔。

```

#### 构建参考基因组索引的软件

构建参考基因组索引的软件有：BWA（Fast and accurate short read alignment with Burrows-Wheeler transform. Heng Li and Richard Burbin），Bowtie（Ultrafast and memory-efficient alignment of short DNA sequences to the human genome），Bowtie2，HISAT，HISAT2。

此外，BLASR（Basic Local Alignment with Successive Refinement）主要用于将PacBio测序的reads和参考序列进行匹配，这是一个处理三代测序的软件。用sawriter命令建库、blasr进行序列比对。

### 序列比对

建立好参考基因组索引之后，测序得到的短reads可以据此进行基因组匹配，将高通量测序结果回溯基因组位置，这个过程叫做序列比对（reads mapping），将对象数量众多的reads（>100M reads pairs）比对到一条唯一且长度不短的参考基因组（>3Gbp），强调回溯的动作，需要较高的计算成本和巧妙的比对策略。这与在进化分析等工作中提到的双序列比对 （pairwise alignment）和多序列比对（multiple sequences alignment）不同，alignment的比对通量较低，更多的强调两条序列或者少数几条序列之间的比对。RNA比对用到的三种策略是Exon-first approach, seed-extend approach, Potential limitations of exon-first approaches。常用的算法是BWT算法和后缀树（Suffix tree），这一点我们在之前的章节已经有所介绍，这里就不再赘述了。

序列比对是获得每条测序片段在参考基因组上对应染色体上的位置坐标、正负链等信息。比对率能反映实验测序样品与参考基因组的相似关系，也反映了测序质量的高低。一般情况下，在80%以上，回帖多个位置的测序序列占总体百分比通常不超过10%。常用比对软件Tophat2、Bowtie2、STAR、HISAT2、RSEM等。

#### SAM文件与BAM文件

序列比对文件采取SAM（The Sequence Alignment/Map format）文件、BAM文件格式。Heng Li等人完成了SAM文件、BAM文件的标准制定，并开发了初代对软件。SAM文件由两部分组成：头部区和主体区，头部区以“@”开始，提供比对的总体信息，例如SAM格式版本、比对参考序列、比对使用的命令等；主体区是比对结果，每一行储存一个比对结果，共11个主列和1个可选列。

关于SAM文件与BAM文件的详细介绍与基本操作，也请翻看前面的章节。我们这里再次提出这个标题，只是想反复为读者强调，这个文件的重要性，以及强调概念无论是DNA还是RNA的比对结果，都是可以保存成对应的SAM/BAM文件的。

#### 序列比对软件

- Bowtie和Bowtie2

Bowtie（Ultrafast and memory-efficient alignment of short DNA sequences to the human genome）和Bowtie2都是常用的短序列比对软件，生成SAM格式的序列比对文件。Bowtie在小于50bp的reads比对中更精确更快，最长支持1000bp；而Bowtie2在大于50bp的reads比对中更精确更快，reads长度没有上限，支持空位比对、局部比对。

- BWA
BWA全称（Alignment with Burrows-Wheeler transform. Heng Li and Richard Burbin）。BWA有多个子命令，可以实现不同算法的比对。

上述3款软件都是针对DNA序列比对进行设计的，并不能直接应用于RNA-Seq的比对。一个最主要的原因就是因为真核生物的基因是间隔的，每两个外显子中间就会有一个内含子。最终成熟的mRNA是不包含内含子序列的，因此针对真核生物的RNA-Seq数据的比对，需要在上述3款软件的基础上加上一些限制条件与修正。最常用的有下面3款Tophat/Tophat2，HISAT/HISAT2, STAR。

- Tophat/Tophat2

Tophat的最新版Tophat2是基于Bowtie2的比对工具，与下游Cufflinks分析软件组合使用，优点是生成的文件内容丰富，不仅仅生成了比对结果，还对剪切位点等信息进行了输出。比对过程调用了Bowtie/Bowtie2, 大题策略是 先比对能比对上的reads，比对不上的reads根据可变剪切的方式拆开再比。该软件最大的缺点是处理不好假基因问题。(参考文献 TopHat: discovering splice junctions with RNA-Seq, TopHat2: accurate alignment of transcriptomes in the presence of insertions, deletions and gene fusions)。使用Tophat时，Bowtie或者Bowtie2，bowtie2-align, bowtie2-inspect, bowtie2-build和samtools，这些命令必须要在系统环境变量PATH中。Tophat能比对的最大reads长度时1024 bp，单端不能与双端混合，不同插入片段长度的双端不能混合。

- HISAT/HISAT2

HISAT（Hical Indexing for Spliced Alignment of Transcripts）和HISAT2(Graph-based genome alignment and genotyping with HISAT2 and HISAT-genotype, Daehwan Kim)是Tophat2的升级版本。利用数量众多的索引，覆盖整个基因组，使用小索引结合几种比对策略，以人类基因组为例，需要48,000个索引，每个索引代表～64，000 bp的基因组区域，从而实现高效比对，尤其是跨越多个外显子的比对，大大提升速度与index的构建方式。其下游分析软件为StringTie和Ballgown。HISAT2相比HISAT，考虑了SNP信息。

HISAT/HISAT2与Tophat/Tophat2出自同一个课题组，目前作者提倡使用HISAT2来替代之前的Tophat2流程。

- STAR

STAR(STAR: ultrafast universal RNA-Seq aligner，Alexander Dobin)的优势在于快，能够快速mapping，是ENCODE计划使用的比对软件。缺点在于占用内存比较大，以人类的参考基因组为例，比对时的运行内存需要28G~32G左右。STAR使用了Suffix Tree 的index：先把read切成若干小的seed，找到全基因组符合seed的位置；再通过打分算法，把邻近的全基因组符合的seed拼在一起，形成mapping结果。

如果比对任务非常多，数据量很大，我们推荐使用STAR这个比对软件得到最终的比对结果。

### 转录本组装

组装转录本是一个可选项，如果想挖掘测序数据中的新转录本，则需要做这一步分析。拼接软件根据参考基因组将测序处理得到的高质量测序片段比对到该参考基因组上，然后对比对上的片段进行转录本组装。Cufflinks、StringTie和Scripture都是常用的转录本组装软件。

Cufflinks可以依赖或者不依赖物种基因组注释文件进行转录本拼接。利用Tophat或HISAT2比对的结果来组装转录本。Cufflinks其实是一套软件，包括组装转录本的Cufflinks、合并gtf文件的Cuffcompare、比较转录本的Cuffcompare、定量转录本的Cuffquant、对多样本标准化的Cuffnorm，以及计算不同组差异表达的Cuffdiff。

（ Cufflinks套件示意图）

Cufflinks是根据Tophat或HISAT2比对结果，输入文件是排序后的BAM或SAM文件，据此进行序列分析，获得含有转录本序列信息和表达信息的GTF文件。但Cufflinks得到的GTF文件不包括起始密码子和终止密码子，是不标准的，称为transfrag转录片段。Cufflinks的输出文件包括表达量FPKM文件genes.fpkm_tracking、isoforms.fpkm_tracking，和GTF文件transcripts.gtf，包含序列名、来源、特征、起始坐标、终止坐标、得分、正负链、读码框、属性这九种信息。但Cufflinks命令只能对一个SAM/BAM文件进行分析，在处理多个样品时，可以使用cuffmerge将多个样品的transcripts.gtf文件合为一个更加全面的转录本注释文件。

StringTie是Cufflinks的升级版本，其下游常使用Ballgown软件分析差异表达。和 Cufflinks一样，输入文件是按坐标排序后的BAM文件，不能对具有多位点比对结果的reads进行过滤，否则会导致转录本序列不完整。进行转录本组装后可以用于基因测序或者与参考GTF/GFF3文件比较以寻找新转录本。但StringTie不直接提供表达量raw count文件，可以使用prepDE.py程序，根据GTF结果文件中的coverage信息，转换得到raw count数据，用于edgeR和DESeq2等其他差异表达软件的分析。

Scripture根据比对得到的spilce reads构建出连接图，采用统计法，分析连接序列与非连接序列比对区域的丰度信息，对可能的连接路径进行评分，依据得分情况选择可能的转录本，依据双端测序reads之间的距离，简介转录本或过滤非转录本。

### 表达定量

通过前面的序列比对分析，获得了能够map到各个基因的reads数，也就是原始的count数。但原始的count数并不能完全表征基因的表达情况，因为不同基因的长度不同，不同批次数据的测序量也不同，所以需要通过计算矫正测序深度和基因长度带来的影响，即对基因的表达进行标准化定量（*Manuel Garber et.al., Nat Methods, 2011）。

#### 基因表达定量方式RPKM、FPKM、TPM

例如，在同一个样本中，基因A和基因B的count数都是1000，而基因A的长度分别为100 bp和200 bp，我们不能认为基因A和基因B的表达水平是一样的；再比如，基因A在样本1、2中的count数分别为1000和2000，此时无法判断基因A在样本2的表达水平是样本1中的两倍，因为在测序实验过程不同样品的测序量不是完全一致的；由于基因本身长度的不同、不同样本测序量的差异，不能使用原始的count数来表征基因的表达水平。

基因的表达进行标准化定量包括多种方式，包括：

1. RPKM（Reads Per Kilobase per Million mapped reads）（Measurement of mRNA abundance using RNA-Seq data: RPKM measure is inconsistent among samples）、FPKM（Fragments Per Kilobase per Million mapped reads）；
2. TPM（Transcripts Per Million）
3. RPM(Reads per million mapped reads)
4. CPM（counts per million mapped reads）等。

各自的适用范围和优缺点不同，了解各自的原理才能在分析过程中选择最适合的定量方式:

```
RPM or CPM =( Number of reads mapped to gene x 10^6 )/ Total number of mapped reads
```

*RPKM=(Number of reads mapped to gene x 10^3 x 10^6) / (Total number of mapped reads x gene length in bp)*

*FPKM=RPKM/2=total reads/(mapped reads(millions)xtrancription length(KB))*

RPKM适用于单端测序。假设回贴到geneA 的 reads count为 CountA，geneA的exon总长度为Len(A) Kbp，总的测序量为D兆(million)reads，那么：

``` 
geneA RPKM = CountA / Len(A) / D * 10^9
```

FPKM适用于双端测序。RPKM与FPKM唯一的不同之处在第一个单词，reads即测序得到的读长片段，fragment则是指在双端测序中read1和read2在参考基因组上确定的片段。双端测序中，1个gene的FPKM应该等于RPKM / 2。

目前，应用最广泛的Illumina测序平台主要采用的是双端测序，因此FPKM也是目前最常见的基因表达定量方式。FPKM能够矫正gene长度以及测序深度对gene表达定量的影响，但不同样本的FPKM总和是不一致的，解决这个问题，可以使用TPM定量方式。

TPM定量将所有样本TPM总和统一标准化为10<sup>6</sup>，方便了不同样本批次之间的比较。

但RNA-Seq的定量有时候也会发生失败。因为RNA-Seq分析的前提是基于两个假设，即:
1. 绝大多数的gene不发生表达量的变化；
2. 特别高表达的gene不发生表达量的变化。

而且，如果仔细思考，你会发现普通的RNA-Seq定量计算采取的方式是样本内相对定量，定量值取决于基因本身的表达量和样本的表达总量的比值。所以，当上述假设不成立时，RNA-Seq的定量就会发很大的偏差。这个时候TPM可能会带来比FPKM/RPKM更大的偏倚（bias），所以从这个角度来看，并不会存在绝对的好与绝对的坏的定量矫正方法。不能一味地，人云亦云地认为TPM就是比FPKM更好的矫正办法。

当不满足上述两条假设时，我们往往需要通过绝对定量进行解决。这个时候，我们可以利用绝对定量的内参(spike-ins)进行绝对定量。最常见的办法是在做RNA-Seq实验的过程中就加入已知绝对摩尔数的内参序列，最常用的是ERCC spike-in，随后就可以根据ERCC spike-in的绝对物质的量来对基因进行定量。

另一个解决策略是选用管家基因（Housekeeping gene）对表达量进行矫正。管家基因是在不同的组织、器官、在不同的外界刺激中均有表达、参与最基础的生理过程、维持细胞的基本生理状态的基因，其表达量总体一般不发生大的变化。针对不同样本间的管家基因，也可以做一条类似于spike-in的标准曲线，通过这条标准曲线可以矫正数据，随后就可以正常进行差异表达分析。

但是无论是参入spike-in还是使用管家基因进行矫正，都可能会引入新的差异（variation），关于这一点我们一定要有个清醒的认识。

#### 表达定量软件
常用的表达定量软件有HTSeq、Cuffquant+Cuffnorm、featureCount。定量分析得到的Counts数据用于接下来的不同样品间的基因表达量差异分析。

HTSeq是用python编写的用于read计数的软件，用于有参考基因组的转录组测序数据的基因表达定量分析，需要SAM和基因组GTF文件。HTSeq软件根据SAM/BAM比对结果文件和基因结构注释GTF文件得到基因水平的counts表达量。HTSeq有有三种计算模式，ambigous表示read比对到多个基因上，no_feature表示read没有比对到基因组上。

（示意图）

Cuffquant是Cufflinks一套的基因表达定量软件，输入一个SAM/BAM文件进行表达量计算，生成一个二进制的结果文件。对多个 Cuffnorm 命令将多个二进制表达量结果进行标准化，给出count值或者FPKM值，与cuffdiff非常类似，但不进行差异化分析，结果可以用其他软件进行分析。

featureCount

### 表达差异分析

寻找差异表达的基本假设是样本中的大部分基因表达不变。基于这个假设，对样本中的基因表达做定量计算，寻找不同样本之间发生差异性表达的基因。而RNA-Seq定量的本质是相对定量，即测定指标的相对比例，如浓度、Fold change；这区别于绝对定量测定的是客观的数值等 ，例如温度、高度、长度等。

cuffdiff、cuffdiff2、DESeq、DESeq2 （Moderated estimation of fold change and dispersion for RNA-Seq data with DESeq2）、edgeR （Small-sample estimation of negative binomial dispersion, with applications to SAGE data）(edgeR: a Bioconductor package for differentical expression analysis of digital gene expression data) 都是常用的表达差异分析软件，此外imma::voom (voom: precision weights unlock linear model analysis tools for RNA-Seq read counts)也可用于差分析。

在差异表达分析过程中，常常会根据基因的差异表达情况绘制火山图：

（火山图）

针对差异表达基因，进行层次聚类（hierarchical clustering method），绘制聚类图：

（聚类图）

聚类采用两种思路，寻找最近的样本进行聚集，即聚类法 agglomerative；剥离出最远的样本的方法，即分割法divisive。

### 基因注释

GO数据库 (Gene Ontology, 基因本体论)是关于基因和蛋白质知识的标准词汇，对基因进行了三个维度的注释生物学过程 (Biological Process, BP)、分子功能 (Molecular Function, MF)和细胞成分(Cellular Component,CC),是所有基因的共有属性的描述。GO富集分析是常用的分析方法，它主要是给定一 个筛选后的gene集，对其进行功能注释，随后通过Fisher exact test或者Chi-Square test进行富集分析检验。

（有向无环图）

KEGG数据库是对基因进行信号通路、代谢等过程注释的数据库。

（代谢通路图）

在上一步的RNA-seq分析中获得了差异表达基因。要了解差异表达基因的功能，一般会对基因进行GO和KEGG pathway注释。很多情况下，研究者希望得到的信息是一群基因主要集中在了那些功能上，则需要对基因集进行GO和KEGG pathway的富集注释。例如在某些胁迫活着药物处理下，引起了机体内大量基因的表达变化，KEGG pathway富集分析可以提示这种处理下，有哪些通路发生了大量的表达基因表达变化。所以基因注释和富集分析是不一样的，注释解释的是单个基因有哪些功能、参与了哪些通路，而富集分析研究某一基因集在某一通路或者其他注释信息（BP，MF，CC）中是否富集。气泡图是在富集分析中常用的图：

（气泡图）

R语言clusterProfiler包和在线软件DAVID注释网站都是常用的基因注释和富集分析工具。其中clusterProfiler工具包是由南方医科大学的余光创老师用心打造的一个工具包。该工具包已经成功运行若干年，更新及时，与时俱进，深受业内好评，可以作为富集分析的一个重要工具进行使用。

## RNA-seq分析实例

在转录组研究工作中，至少设置两组样本，对照组和实验组，获取与实验组相关的某种疾病、表型或生命活动过程中具有重要作用的miRNA种类，预测靶标基因及其生物学功能。最好每组样品设置3个及以上生物学重复，以降低样品特异性带来的误差。

### 数据获取

首先从网络下载RNA-Seq数据和人类基因组及基因组注释文件。

示例采用GEO数据库中的转录组数据GSM1502498，GSM1502499，GSM1502502，GSM1502503，其中前两者为实验组，后两者为对照组。数据下载可以直接点击网页链接，也可以在linux服务器上用wget+链接自动获取。

*方法一 从网页链接直接下载*

下载链接：

- GSM1502498（https://trace.ncbi.nlm.nih.gov/Traces/sra/?run=SRR1573494）
- GSM1502499（https://trace.ncbi.nlm.nih.gov/Traces/sra/?run=SRR1573495）
- GSM1502502（https://trace.ncbi.nlm.nih.gov/Traces/sra/?run=SRR1573498）
- GSM1502503（https://trace.ncbi.nlm.nih.gov/Traces/sra/?run=SRR1573499）

(网页截图)

*方法二，使用命令行下载*

```shell
$wget 
```

这里选用的是人类样本，因此需要下载人类基因组和基因组注释文件。基因组文件可以从UCSC genome browser （https://genome.ucsc.edu/index.html）和 Ensembl（http://asia.ensembl.org/index.html）网站上获取。

(网页截图)

### 质量控制

从GEO数据库下载的数据文件格式为SRA，需要使用官方提供的SRA Toolkit进行转换，将sra文件转换为fastq格式文件，软件下载链接： https://github.com/ncbi/sra-tools/wiki/02.-Installing-SRA-Toolkit。

```shell
$fastq-dump SRR1573494.sra
```

使用FastQC做质量控制：

 ```shell
$fastqc SRR1573494.fq
 ```

使用cutadapt去除接头序列，过滤数据质量：

```shell
$cutadapt -j 6 --times 1 -e 0.1 -O 3 --quality-cutoff 25 -m 55 \
-a AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC \
-A AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTAGATCTCGGTGGTCGCCGTATCATT \
-o fix.fastq/test_R1_cutadapt.temp.fq.gz \
-p fix.fastq/test_R2_cutadapt.temp.fq.gz \
 raw.fastq/test_R1.fq.gz \
 raw.fastq/test_R2.fq.gz > fix.fastq/test_cutadapt.temp.log 2>&1 &
```

也可以使用fastx_toolkit去除接头序列，过滤数据质量：

```shell
$fastq_quality_filter -v -q 20 -p 80 -Q 33 -i SRR1573494.fastq -o SRR1573494_q20_p80.fq
```

### 建立参考基因组索引

#### HISAT2

使用`hisat2`构建基因组索引：

```shell
$hisat2_extract_splice_sites.py Homo_sapiens.GRCh38.101.gtf >genome.ss
$hisat2_extract_exons.py Homo_sapiens.GRCh38.101.gtf >genome.exon
$hisat2-build -p 20 Homo_sapiens.GRCh38.dna.toplevel.fa genome
$hisat2-build -p 20 --exon genome.exon --ss genome.ss Homo_sapiens.GRCh38.dna.toplevel.fa genome_tran
$hisat2-build ref_hg38.fa ref_hg38.fa > hisat2_build.log 2>&1 &
#download some resource
##SNP
http://hgdownload.cse.ucsc.edu/goldenPath/hg38/database/

##GTF

#make exon 
$hisat2_extract_exons.py hg38_refseq.gtf > hg38_refseq.exon &

#make splice site
$hisat2_extract_splice_sites.py hg38_refseq.gtf > hg38_refseq.ss &

#make snp and haplotype
$hisat2_extract_snps_haplotypes_UCSC.py ref_hg38.fa snp151Common.txt snp151Common &

#build index
$hisat2-build -p 6 --snp snp151Common.snp --haplotype snp151Common.haplotype --exon hg38_refseq.exon  --ss hg38_refseq.ss ref_hg38.fa ref_hg38.fa.snp_gtf > hisat2_build.log 2>&1 & 

# hisat2-build——hisat2构建索引的命令

# -p——使用多少个核，20代表使用20个核心

# Homo_sapiens.GRCh38.dna.toplevel.fa——从Ensembl数据库下载的人类基因组文件

# genome——将索引命名为genome
```

参数解释：

```
-p <int> default: 1 设置多线程运行
--snp <path> 输入一个包含SNP信息的文件，含5列数据：SNP ID、参考序列ID、SNP类型（single、deletion或insertion）、SNP位点（以第一个碱基位点为0计算）、变异碱基信息。
--haplotype <path> 单倍型信息文件，表明--snp参数指定的某些变异位点子啊要分析的样品中是单倍型的，和气变异位点碱基信息一致。含5列数据：Haplotype ID、参考序列ID、起始位点（以第一个碱基位点为0计算）、结束位点、逗号分隔的多个SNP ID。
--ss <path> 输入一个包含有剪接位点（Splicing Site）信息的文件。该文件可以利用HISAT2软件自带的hisat2_extract_splice_sites.py程序对编码蛋白基因结构注释GTF文件转换获得。
--exon <path> 输入一个含有外显子信息的文件。利用HISAT2软件自带的hisat2_extract_exons.py程序对编码蛋白基因结构注释GTF文件转换获得该文件。

```

#### STAR

还可以使用STAR构建基因组索引：

```shell
$STAR --runThreadN 12 --runMode genomeGenerate \
--genomeDir /home/menghaowei/ngs_course/reference/STAR_index \
--genomeFastaFiles /home/menghaowei/ngs_course/reference/STAR_index/ref_hg38.fa \
--sjdbGTFfile /home/menghaowei/ngs_course/reference/gtf/hg38_refseq_from_ucsc.rm_XM_XR.fix_name.gtf \
--sjdbOverhang 150 & 

```

### 序列比对

#### Tophat

使用Tophat将转录组数据的reads比对到参考基因组：

```shell
$tophat -r 50 -p 50 –G chrX.gtf  -o ERR188044 index/chrx.index ERR188044_chrX_1.fastq.fa ERR188044_chrX_2.fastq.fa
```

也使用Tophat2比对到参考基因组：

```shell
tophat2 -o ./test_tophat2 -p 6 \
-G /home/menghaowei/ngs_course/reference/gtf/hg38_refseq_from_ucsc.rm_XM_XR.fix_name.gtf \
/home/menghaowei/ngs_course/reference/bowtie2_index/ref_hg38.fa \
./fix.fastq/test_R1_cutadapt.fq.gz \
./fix.fastq/test_R2_cutadapt.fq.gz > test_tophat2/test_tophat2.log 2>&1 & 
```

#### HISAT2

也使用`hisat2`比对到参考基因组：

```shell
$hisat2 -p 12 \
-x /home/menghaowei/ngs_course/reference/hisat2_index/ref_hg38.fa \
-1 ./fix.fastq/test_R1_cutadapt.fq.gz \
-2 ./fix.fastq/test_R2_cutadapt.fq.gz \
-S ./bam/test_hisat2.sam > ./bam/test_hisat2.log 2>&1 &

#mapping
$hisat2 -p 6 \
-x /Users/meng/ngs_course/reference/hisat2_index/ref_hg38.fa.snp_gtf \
-1 ./fix.fastq/test_R1_cutadapt.fq.gz \
-2 ./fix.fastq/test_R2_cutadapt.fq.gz \
-S ./bam/test_hisat2.sam > ./bam/test_hisat2.log 2>&1 &

```

``` sh
$hisat2 -x genome -u 1000000 -p 24 -I 0 -X 500 --fr --min-intronlen 20 --max-intronlen 4000 -1 reads.1.fastq -2 read.2.fastq -U single.fastq -S result.sam
```

参数：

```
-x <hisat-idx> 设置索引数据文件前缀
-1 <m1> 双末端测序结果的第一个文件，若有多组数据，使用逗号将文件分隔，reads长度可以不一致
-2 <m2> 双末端测序结果第二个文件，顺序和-1参数对应。
-U <r> 单端数据文件，若有多组数据，使用逗号将文件分隔
--sra-acc <SRA accession number> 输入SRA登录号。多组数据之间用逗号分隔，HISAT将自动下载数据并识别数据类型，进行比对。参数大正常使用需要安装NCBI-NGS toolkit
-S <hit> 设置输出文件名。

```

#### STAR

也使用STAR比对到参考基因组：

```shell
STAR \
--genomeDir /home/menghaowei/ngs_course/reference/STAR_index \
--runThreadN 6 \
--readFilesIn ./fix.fastq/test_R1_cutadapt.fq.gz ./fix.fastq/test_R2_cutadapt.fq.gz \
--readFilesCommand zcat \
--outFileNamePrefix ./bam/test_STAR \
--outSAMtype BAM Unsorted \
--outSAMstrandField intronMotif \
--outSAMattributes All \
--outFilterIntronMotifs RemoveNoncanonical > ./bam/test_STAR.log 2>&1 & 
```

参数解释：

```
-b 默认输出SAM格式文件，该参数设置输出BAM格式
-h 默认输出不带头部信息的SAM文件，参数设定输出SAM文件带头部信息
-H 只输出头部信息
-S 默认输入是BAW文件，若是输入SAM文件，最好加这个参数

```

#### samtools操作SAM/BAM文件

``` sh
samtools view [options] <in.bam> | <in.sam> [region1 [...]]
$samtools view -bS adc.sam >abc.bam
$samtools view -b -S abc.sam -o abc.bam

提取比对到参考序列上的比对结果：
$samtools view -bF 4 abc.bam >abc.F.bam

提取paired reads中两条reads都比对到参考序列上的比对结果，只需要把两个4+8的值12作为过滤参数：
$samtools view -bf 4 abc.bam >abc.f.bam

提取BAM文件中比对到scaffold1上的比对结果，并保存到SAM文件格式：
$samtools view abc.bam scaffold1 >scaffold1.sam

提取能比对到scaffold1 30k到100 k区域到比对结果：
$samtools view abc.bam scaffold1:30000-10000 > scaffold1_30k-100k.sam

根据FASTA文件，将header加入到SAM或BAM文件中：
$samtools view -T genome.fasta -h scaffold1.bam >scaffold1.h.sam

```

### 转录组拼接 （需要增加解释）

####  Cufflinks

使用Cufflinks组装转录本：

```shell
$cufflinks -o ERR188044/cufflink ERR188044/accepted_hits_sorted.bam -p 50 -g chrX.gtf -b chrX.fa

```

使用Cuffmerge合并新的转录本:

```shell
#使用cuffmerge:
$cuffmerge -g Homo_sapiens.GRCh37.85.gtf -s hisat/human_genome.fa -p 40 -o merged.gtf assemblies.txt

#使用cuffcompare:
$cuffcompare -r Homo_sapiens.GRCh38.85.gtf -i 1.txt -o cuffcmp01

```

#### StringTie

使用StringTie组装转录本：

```shell

```

Cufflinks输入的必须是排序后的BAM或SAM文件，对于剪接性比对结果，记录中要有XS标签。“XS:A:-”标签表明reads比对到了负义链上，使用HISAT2软件对非链特异性测序的RNA-seq数据进行比对时，一定要添加--dta-cufflinks参数，从而使跨过内含子的剪接性比对结果中含有XS标签，否则cufflinks命令不能正确处理结果。

cufflinks的输出结果有genes.fpkm_tracking, isoforms.fpkm_tracking, transcripts.gtf。前两个时表达量FPKM结果文件，第三个是GTF文件，用于描述基因在染色体上的结构信息：序列名、来源、特征、起始坐标、终止坐标、得分、正负链、读码框、属性。不包含起始密码子和终止密码子，因此GTF不是标准的

``` sh
$cufflinks -p 4 -b genome.fasta -u -o sample1 -L sample1 tophat.ba。m
```

```
-o | --output-dir <string>  设置输出文件夹名称
-p | --num-threads 设置CPU线程数
-G | --GTF <reference_annotation.gtf.gff> 提供包含有基因结构信息的格式为GTF或GFF文件，计算文件中转录本的表达量。
-g | --GTF-guide 提供GFF文件，以此知道转录本组装。
```

cufflinks命令只能对一个SAM/BAM文件进行表达量分析，不同样品表达量不同，为了获得全面的基因注释信息，用cuffmerge将cufflinks命令生成的多个transcripts.gtf文件融合为一个更全面的转录本注释结果。

 ``` sh
$ cuffmerge -o ./merged_asm -p 4 -s genome.fasta assembly_GTF_list.txt
 ```

```
-o | --output-dir <string>  设置输出文件夹名称
-p | --num-threads 设置CPU线程数
-s | --ref-sequence <seq_dir> 基因组DNA序列
```

``` sh
对一个样品数据进行组装：
$stringtie sample.bam --rf -l sample1 -o sample1.gtf -p 4
对多个样本对GTF文件进行整合：
$stringtie --merge -o merge.gtf sample1.gtf sample2.gtf 
对一个样品的表达量进行分析
$stringtie sample1.demulpos.bam --rf -o sample1.gtf -p 8 -e -G genome.gtf

```

### 表达定量

#### HTSeq

使用HTSeq对基因表达进行定量：

```shell
htseq-count -f bam -r pos \
--max-reads-in-buffer 1000000 \
--stranded no \
--minaqual 10 \
--type exon --idattr gene_id \
--mode union --nonunique none --secondary-alignments ignore --supplementary-alignments ignore \
--counts_output ./count_result/test_count.tsv \
--nprocesses 1 \
./bam/test_hisat2.sort.bam  ./reference/gtf/hg38_refseq_from_ucsc.rm_XM_XR.fix_name.gtf > ./count_result/test_count.HTSeq.log  2>&1 & 
```

#### featureCount

使用featureCount对基因表达进行定量：

```shell
$featureCounts -t exon -g gene_id \
-Q 10 --primary -s 0 -p -T 1 \
-a ./reference/gtf/hg38_refseq_from_ucsc.rm_XM_XR.fix_name.gtf \
-o ./count_result/test_count.featureCounts \
./bam/test_hisat2.sort.bam \
./bam/test_hisat2.sort.2.bam > ./count_result/test_count.featureCounts.log  2>&1 & 
```

-a参数默认值为10，忽略掉比对到多个位置的reads信息，其结果有利于后续差异分析。输入的GTF文件不能包含可变剪接信息，否者HTSe会认为没个可变剪接都是单独的基因，导致能比对到多个可变剪接转录本傻姑娘的reads计算结果是ambiguous，不能计算到基因的count中。

ambigous表示read比对到多个基因上，no_feature表示read没有比对到基因组上。

```
# 非链特异性真核转录组测序数据
$htseq-count -f sam -r name -s no -a 10 -t exon -i gene_id -m union hisat2.sam genome.gtf >counts_out.txt

# 链特异行真核转录测序数据
$htseq-count -f sam -r name -s reverse -a 10 -t exon -i gene_id -m union hisat2.sam genome.gtf >count_out.gtf

# 非链特异原核生物转录组测序数据
$htseq-count -f sam -r name -s no -a 10 -t exon -i gene_id -m intercextion-strict bowtie2.sam genome.gtf >counts_out.txt
```

参数说明：

```
-f | --format default:sam 设置输入文件格式，sam或者bam
-r | --order default: name 设置输入文件排序方式，name或者pos。前者按reads名排，后者比对的参考基因组位置进行排序。当测序时间是双端测序是，输入文件按照pos排序，两端的比对结果在文件中不是紧邻的两行，程序会将reads对的第一个比对结果放入内存，知道读取到另一端read的比对结果，选pos可能会导致内存使用过多。其他表达量分析软件要求输入SAM/BAM文件是pos排序的，很多软件出处结果也是按照name排序，有所不同。
-s | --stranded default:yes 设置是否链特异性测序。值可以为yes,no,reverse.分别代表：非链特异性测序;单端yes表示read比对到基因的正义链上，双端测序表示read1比对到正义链上，reads比对到负义链傻姑娘；reverse表示双端测序与yes值相反的结果。
-a | --a default: 10 忽略比对质量低于此值的比对结果。
-t | --type default: exon 程序会对该指定的feature(GTF/GFF文件第三列)进行表达量计算，而GTF/GFF文件中其它的feature都会被忽略
-i | -idattr default:gene_id 设置feature ID 是由GTF/GFF文件第九列那个标签决定的，若GTF/GFF文件多行具有相同feature ID, 则它们来自同一个feature,程序会计算这些features的表达量之和赋给相应的feature ID。
-m | --mode deault: union 设置表达量计算模式。参数的值可以有union，intersection-strict, intersection-nonempty。原核生物用intersection-strict,真核生物用union模式。
-o | --samout 输出一个SAM文件，比对结果多一个XF标签，表示 read比对到了某个feature上。
-q | --quiet 不输出程序运行的状态信息和警告信息
```

#### cuffquant

用于对一个SAM/BAM文件进行表达量计算，生成一个二进制的结果文件。这部分计算比较消耗计算资源。

``` sh
$ cuffquant -o sample1 -p 4 -b genome.fasta -u genome.gtf sample1.sam
```

```
-o | --output-dir <string>  设置输出文件夹名称
-p | --num-threads 设置CPU线程数
-b | --frag-bias-correct <genome.fa> 知道Cufflinks运行偏差检测和校正算法（bias detection and correction algorithm），提高转录子丰度计算的精确性。
-u | --multi-read-coreect 让cufflinks更精确地比对到genome多个位点的reads
-library-type default:fr-unstranded 设置是否为链特异测序或其种类，默认为非链特异性的RNA-seq
```

### 差异分析

#### Cuffdiff

cuffdiff 用于基因表达差异性的显著性分析，若基因组较小可直接使用，基因组较大的可以先用cuffquant处理后再进行差异分析。

```
cuffdiff -L lample1,sample2 -p 4 -u -b genome.fasta genome.gtf sample1_rep1.sam,sample2_rep2.sam sample2_rep1.sam,sample2_rep2.sam
```

```
-o | --output-dir <string> default: ./ 设置输出文件夹目录
-L | --lables <lable1,lable2,...,lableN> default:q1,q2,...,qN 设置每一个样本的样品名
-p | --num-threads 设置CPU线程数
-T | --time-series  让cuffdiff按样品顺序进行比对
-u | --multi-read-correct initial estimation，好精确衡量比对到genome多个位点的reads
-b ｜ --frag-bias-correct 提供一个fasta文件来知道cufflinks运行的新的bias detection and correction algorithm。提高转录本丰度的计算。
```

使用cuffdiff进行差异分析：

```
cuffdiff -o cuffdiff -p 50 -L male,female -u chrX.gtf ERR188044/accepted_hits_sorted.bam,ERR188104/accepted_hits_sorted.bam,ERR188454/accepted_hits_sorted.bam ERR188234/accepted_hits_sorted.bam,ERR188273/accepted_hits_sorted.bam,ERR204916/accepted_hits_sorted.bam
```

#### DEseq

使用R语言DEseq包进行差异分析：

```R
library(DESeq2)
# count table 
count_df <- read.table(file = "./03.code_and_data/out_table/293T-RNASeq-Ctrl_vs_KD.STAR.hg38.featureCounts.FixColName.tsv",header = T,sep = "\t")
# filter 
colnames(count_df)
count_df.filter <- count_df[rowSums(count_df) > 20 & apply(count_df,1,function(x){ all(x > 0) }),]
# condition table
sample_df <- data.frame(
  condition = c(rep("ctrl",2), rep("KD",2)),
  cell_line = "293T"
)
rownames(sample_df) <- colnames(count_df.filter)
deseq2.obj <- DESeqDataSetFromMatrix(countData = count_df.filter, colData = sample_df, design = ~condition)
deseq2.obj
# -------------------------------------------------------->>>>>>>>>>
# directly get test result 
# -------------------------------------------------------->>>>>>>>>>
deseq2.obj <- DESeqDataSetFromMatrix(countData = count_df.filter, colData = sample_df, design = ~condition)
deseq2.obj
# test 
deseq2.obj <- DESeq(deseq2.obj)
# get result
deseq2.obj.res <- results(deseq2.obj)
deseq2.obj.res.df <- as.data.frame(deseq2.obj.res)
# -------------------------------------------------------->>>>>>>>>>
# step by step get test result 
# -------------------------------------------------------->>>>>>>>>>
deseq2.obj <- DESeqDataSetFromMatrix(countData = count_df, colData = sample_df, design = ~condition)
deseq2.obj
# normalization 
deseq2.obj <- estimateSizeFactors(deseq2.obj)
sizeFactors(deseq2.obj)
# dispersion
deseq2.obj <- estimateDispersions(deseq2.obj)
dispersions(deseq2.obj)
# plot dispersion
plotDispEsts(deseq2.obj, ymin = 1e-4)
# test 
deseq2.obj <- nbinomWaldTest(deseq2.obj)
deseq2.obj.res <- results(deseq2.obj)
```

#### edgeR

使用R语言edgeR包进行差异分析：

```R
library(edgeR)

# -------------------------------------------------------->>>>>>>>>>
# make obj 
# -------------------------------------------------------->>>>>>>>>>
# count table 
count_df <- read.table(file = "./03.code_and_data/out_table/293T-RNASeq-Ctrl_vs_KD.STAR.hg38.featureCounts.FixColName.tsv",header = T,sep = "\t")

# filter 
colnames(count_df)
count_df.filter <- count_df[rowSums(count_df) > 20 & apply(count_df,1,function(x){ all(x > 0) }),]

# condition table
group_info = c(rep("ctrl",2), rep("KD",2))

dge.list.obj <- DGEList(counts = count_df.filter, group = group_info)
dge.list.obj

# -------------------------------------------------------->>>>>>>>>>
# Normalization
# -------------------------------------------------------->>>>>>>>>>
# Normalization method: "TMM","TMMwsp","RLE","upperquartile","none"
dge.list.obj <- calcNormFactors(dge.list.obj,method = "TMM")
dge.list.obj$samples

dge.list.obj <- calcNormFactors(dge.list.obj,method = "TMMwsp")
dge.list.obj$samples

dge.list.obj <- calcNormFactors(dge.list.obj,method = "upperquartile")
dge.list.obj$samples

dge.list.obj <- calcNormFactors(dge.list.obj,method = "RLE") # DESeq2, cuffdiff
dge.list.obj$samples

dge.list.obj <- calcNormFactors(dge.list.obj,method = "none")
dge.list.obj$samples

# raw data plot MDS
plotMDS(dge.list.obj)

# -------------------------------------------------------->>>>>>>>>>
# make design matrix
# -------------------------------------------------------->>>>>>>>>>
design.mat <- model.matrix(~group_info)

# -------------------------------------------------------->>>>>>>>>>
# estimate dispersion
# -------------------------------------------------------->>>>>>>>>>
dge.list.obj <- estimateDisp(dge.list.obj,design.mat)
dge.list.obj$common.dispersion
dge.list.obj$tagwise.dispersion

# 1st common dispersion
dge.list.obj <- estimateCommonDisp(dge.list.obj)

# 2nd tagwise dispersion
dge.list.obj <- estimateTagwiseDisp(dge.list.obj)

# plot dispersion
plotBCV(dge.list.obj, cex = 0.8)

# plot var and mean
plotMeanVar(dge.list.obj, show.raw=TRUE, show.tagwise=TRUE, show.binned=TRUE)

# -------------------------------------------------------->>>>>>>>>>
# test with likelihood ratio test
# -------------------------------------------------------->>>>>>>>>>
dge.list.res <- exactTest(dge.list.obj)
DEGs.res <- as.data.frame(topTags(dge.list.res,n=nrow(count_df.filter),sort.by = "logFC"))

# MA plot
select.sign.gene = decideTestsDGE(dge.list.res, p.value = 0.001) 
select.sign.gene_id = rownames(dge.list.res)[as.logical(select.sign.gene)]
plotSmear(dge.list.res, de.tags = select.sign.gene_id, cex = 0.5,ylim=c(-4,4)) 
abline(h = c(-2, 2), col = "blue")

# -------------------------------------------------------->>>>>>>>>>
# test with likelihood ratio test
# -------------------------------------------------------->>>>>>>>>>
fit <- glmFit(dge.list.obj, design.mat)
lrt <- glmLRT(fit, coef=2)
DEGs.res.lrt <- as.data.frame(topTags(lrt,n=nrow(count_df.filter),sort.by = "logFC"))

```

### 火山图与聚类图绘制

#### 火山图

使用R语言ggplot2包绘制火山图

```R
require(ggplot2)

bmp(filename="M3 volcan plot.bmp",width = 400,height = 300)

##Highlight genes that have an absolute fold change > 2 and a p-value < Bonferroni cut-off
a <- read.table("M3-vol.txt",header=T,sep="\t")
P.Value <- c(a$pvalue)
FC <- c(a$log2)
df <- data.frame(P.Value, FC)
 
df$threshold = as.factor(abs(df$FC) > 1 & df$P.Value < 0.05)
#df$color_flag <- ifelse(df$FC > 1, ifelse(df$FC < -0.5))

##Construct the plot object
g = ggplot(data=df, aes(x=FC, y=-log10(P.Value), colour=threshold)) +
  
  geom_point(alpha=0.4, size=1.75) +
  xlim(c(-20, 20)) + ylim(c(0, 5)) +
  theme_set(theme_bw())+
  theme(panel.grid.major=element_line(colour=NA))+
  xlab("log2 fold change") + ylab("-log10 p-value")
g
dev.off()

rm(list=ls())
```

输入文件格式为：

```
log2	pvalue
2.04705	5.00E-05
1.17727	2.25E-03
2.08625	3.11E-02
1.66692	3.58E-02
-1.72558	4.24E-02
2.44106	4.26E-02
...`...
... ...
... ...
```

#### 聚类图

使用R语言gplots包绘制火山图

```R
library("gplots")

est <- read.table(file = "DEgene.txt", header = T, row.names=1)
tiff("DEgene.tiff", width = 1000, height = 1000, units = "px", res=80)
heatmap.2(as.matrix(est),  margins = c(13, 13),col=redgreen(100), scale = "row", dendrogram = "column",
         key = T, keysize=0.8, symkey = T, density.info = "none", trace = "none")
dev.off()

est <- read.table(file = "heatmap.txt", header = T, row.names=1)
svg(file="e3.svg", width = 100, height = 100)
heatmap.2(as.matrix(est),  margins = c(13, 13),col=redgreen(100), scale = "row", dendrogram = "column",
          key = T, keysize=0.8, symkey = T, density.info = "none", trace = "none")
dev.off()


```

输入文件格式为：

```
hsa-miR-6087	4.835286667	2.680141333
hsa-miR-663a	5.537003333	3.407306667
hsa-miR-6821-5p	3.699006667	2.02985
hsa-miR-1469	6.229766667	4.79053
hsa-miR-3665	4.710016667	3.276396667
hsa-miR-2861	4.070266667	2.670983333
hsa-miR-4466	3.904726667	2.54759
hsa-miR-1915-3p	3.367876667	2.018898
hsa-miR-6090	5.80658	4.459086667
...	...	...
...	...	...
...	...	...
```

#### GO注释

使用R语言clusterProfiler包进行GO注释:

```R
# ---------------------------------------------------------------------->>>>>>>
# GO analysis
# ---------------------------------------------------------------------->>>>>>>
rm(list=ls())

library(clusterProfiler)
library(tidyverse)

# laod table 
cuffdiff_res <- read_tsv("./03.code_and_data/cuffdiff_result/gene_exp.diff")

# rename colname
colnames(cuffdiff_res)
colnames(cuffdiff_res)[10] = "log2FC"
colnames(cuffdiff_res)

# filter 
cuffdiff_res.filter <- filter(cuffdiff_res, status == "OK")

# real sign
real_sign = rep("no",nrow(cuffdiff_res.filter))

select.FPKM <- (cuffdiff_res.filter$value_1 > 1 | cuffdiff_res.filter$value_2 > 1)
table(select.FPKM)

select.log2FC <- abs(cuffdiff_res.filter$log2FC) > 1
table(select.log2FC)

select.qval <- (cuffdiff_res.filter$q_value < 0.05)
table(select.qval)

real_sign[select.FPKM & select.log2FC & select.qval] <- "yes"
table(real_sign)

# select sign DEGs
cuffdiff_res.filter.DEG <- cuffdiff_res.filter[select.FPKM & select.log2FC & select.qval,]

# load annotation file
# BiocManager::install("org.Hs.eg.db")
library(org.Hs.eg.db)

# GO 
DEG.gene_symbol = as.character(cuffdiff_res.filter.DEG$gene_id)

erich.go.BP = enrichGO(gene = DEG.gene_symbol,
                       OrgDb = org.Hs.eg.db,
                       keyType = "SYMBOL",
                       ont = "BP",
                       pvalueCutoff = 0.5,
                       qvalueCutoff = 0.5)

erich.go.CC = enrichGO(gene = DEG.gene_symbol,
                       OrgDb = org.Hs.eg.db,
                       keyType = "SYMBOL",
                       ont = "CC",
                       pvalueCutoff = 0.5,
                       qvalueCutoff = 0.5)

erich.go.MF = enrichGO(gene = DEG.gene_symbol,
                       OrgDb = org.Hs.eg.db,
                       keyType = "SYMBOL",
                       ont = "MF",
                       pvalueCutoff = 0.5,
                       qvalueCutoff = 0.5)


dotplot(erich.go.CC)
dotplot(erich.go.BP)
dotplot(erich.go.MF)

# save image to file
pdf(file="./03.code_and_data/out_image/20200926-enrich.go.BP.Dotplot.pdf",width = 10,height = 6)
dotplot(erich.go.BP)
dev.off()

```

#### 4. KEGG注释

使用R语言clusterProfiler包进行KEGG注释:

```R

# ---------------------------------------------------------------------->>>>>>>
# KEGG analysis
# ---------------------------------------------------------------------->>>>>>>
# convert id
DEG.entrez_id = mapIds(x = org.Hs.eg.db,
                       keys = DEG.gene_symbol,
                       keytype = "SYMBOL",
                       column = "ENTREZID")

erich.kegg.res <- enrichKEGG(gene = DEG.entrez_id,
                             organism = "hsa",
                             keyType = "kegg")

barplot(erich.kegg.res)
```

## 其他RNA测序的分析简述

其他RNA测序的数据分析与普通RNA测序数据分析类似，例如质量检测、序列比对、表达定量和差异表达分析是所有RNA测序都需要做的分析。不同的地方在于鉴定是否属于这一类RNA的手段、定量的方法和一些下游分析，例如miRNA需要分析其靶基因，circRNA需要分析能够与之互作的miRNA。此外，单细胞RNA-seq的分析自基因表达矩阵后，与RNA-seq的分析会有较大的差异，一般会侧重于细胞的分群、分类、演化等分析。

### 长非编码RNA测序分析

去rRNA建库方式和富集polyA方式建库，这两种方式的RNA测序都能检测到长非编码RNA，前者能够获得全面的数据，而后者只能获得一部分的长非编码RNA数据，即含有polyA尾巴的类mRNA的lncRNA。

已知lncRNA的分析与mRNA是类似的，可以从基因组注释文件中获取已知lncRNA。也可以通过与长非编码RNA数据库比较，获得已知的lncRNA转录本。lncRNA相关的数据库有lncRNAdb、NONCODE、NRED、LNCIPedia等。lncRNAdb（http://www.lncrnadb.org/）只收录已经被实验验证的真核生物lncRNAs数据库；NONCODE（http://www.noncode.org/）是ncRNA相关注释数据库；NRED收录人和鼠的长非编码RNA数据；LNCipdedia（https://lncipedia.org/）是人类LincRNA转录序列和结构注释数据库。

<img src="./image_RNASeq/RNA-seq-lncRNA-analysis.jpg" alt="RNA-seq-lncRNA-analysis" style="zoom:8%;" />

而新lncRNA的预测分析则需要预测转录本的编码潜能和序列同源性等指标，主要包括：
1. 在拼接好的转录本中提取长度大于200nt的转录本；
2. 与其他非编码RNA数据库比对去除其他非编码RNA；
3. 与已知蛋白质序列比对去除与之高度相似的转录本；
4. 利用lncRNA鉴定软件评估潜在lncRNA转录本的编码能力，常用预测软件有PhyloCSF、CNCI、CPC、COME、PLEK、lncRNA-MFDl等；
5. 获取可能的新lncRNA转录本。

lncRNA数据分析中，表达定量和差异表达分析和mRNA的分析方法是类似的，但功能注释方法不同。包括直接注释和通过靶标基因注释两种方式：

1. 直接注释可以基于一些收录lncRNA功能信息的数据库进行注释分析，例如LncRNADisease（http://www.cuilab.cn/lncrnadisease）收录了人类疾病lncRNA数据、真核生物的LincRNA综合数据库LncRNAdb（http://www.lncrnadb.org/）收录了包括亚细胞定位和功能疾病等在内的系列结果信息、NONCODE（http://www.noncode.org/）数据库提供了 LincRNA的注释信息；
2. lncRNA一般通过调控蛋白编码基因的表达来发挥作用，主要有Cis调控和trans作用，Cis调控是指lncRNA可能会调控基因组上相邻位置的基因，trans作用可以预测其碱基互补，可以基于lncRNA在基因组上的位置特性进行预测。

（功能分析图）

### small RNA-seq 

small RNA-seq一般是为了获取miRNA的表达信息，miRNA广泛存在于动植物中，通过抑制蛋白质翻译或降解mRNA，在多种生物学过程中发挥着重要的调控作用。

<img src="./image_RNASeq/small-RNA-seq-analysis.jpg" alt="small-RNA-seq-analysis" style="zoom:8%;" />

small RNA-seq原始数据的处理与RNA-seq有所不同：
1. 在对原始数据进行质量控制后，基于miRNA的长度特性，利用Fastx-toolkit等工具对reads进行长度筛选；
2. 从miRBase中获取已知的miRNA成熟体及前体序列，用Bowtie等工具构建miRNA索引；
3. 将筛选后的reads比对到构建好的miRNA索引获取已知的miRNA；
4. 利用预测软件根据miRNA前体的二级结构特征预测潜在的新miRNA，例如待预测miRNA前体能否形成发卡结构，结构是否稳定等；
5. 得到所有miRNA的count表达矩阵后，差异表达分析就与前面的RNA-seq方法类似了。此外，mirDeep2工具提供了成套的新miRNA预测、miRNA定量等功能。

获得差异表达miRNA后，需要对这些miRNA的靶标基因进行预测。miRNA靶标基因预测软件有miRanda（http://www.microrna.org/microrna/home.do），Pictar，psRNATarget（ http://plantgrn.noble.org/psRNATarget/?function= 1），PITA，TargetScan, RNAHybrid，Tarbase，miRecords，MMIA等。此外，miRNA与靶基因的交互作用和通路内miRNA的协同与竞争作用收到较多的关注与研究

### circRNA测序分析

cirRNA常被认为是前体mRNA不正常剪接的结果，因此序列常包括两个以上的外显子。环状RNA断裂成线装RNA，测序会发现不能直接比对到基因组上，会跨越一个剪接信号GTAG，信号前后会比对到基因组上的不同位置。利用Tophat2、Bowtie1、 Bowtie2、 Samtools进行比对。

<img src="./image_RNASeq/circRNA-seq-analysis.jpg" alt="circRNA-seq-analysis" style="zoom:8%;" />

circBase （ http://www.circbase.org/）是一个通过收集和整合已经发布的circRNA数据构建的数据库，包括6个物种：人 (hg19)、小鼠(mm9) 、秀丽线虫(ce6)、黑腹果蝇 (dm3)、非洲 矛尾鱼 (latCha1)、印尼矛尾鱼 (latCha1)。circRNADb （ http://202.195.183.4:8000/circrnadb/circRNADb.php）是一个蛋白质编码注释的人类环状RNAs的综合数据库。CIRCpedia（ http://www.picb.ac.cn/rnomics/circpedia/）对人和小鼠组织和细胞系样品中环状RNA分子的可变反向剪接(可变环化)和可变剪接进行了归类。

### ceRNA分析

ceRNA并不是一种新发现的RNA，而是由于体内多种RNA之间的相互作用形成的一种现象，称为内源竞争性RNA。例如circRNA能够吸附miRNA，而miRNA能够作用于mRNA，此时circRNA与mRNA就形成了一种竞争的关系，这种RNA直接的竞争称为内源竞争RNA（ceRNA）。

<img src="./image_RNASeq/ceRNA.jpg" alt="ceRNA" style="zoom:9%;" />

1. miRNA是内源竞争RNA争夺的目标，除了mRNA和circRNA，部分具有类mRNA结构的lncRNA也能够与miRNA进行结合lncRNA与miRNA之间的作用，是miRNA与lncRNA的3‘非编码区结合，类似与miRNA与mRNA之间的作用。 miRcode（ Transcriptome-wide microRNA target prediction including lncRNAs，http://www.mircode.org/，Human）。
2. lncRNA与基因之间还有着Cis调控和反式作用等作用。（3）circRNA除了能与miRNA进行作用，与其宿主基因之间表达关系，与宿主基因转录的mRNA则源自同一个基因。

可见，生物体内的RNA之间有着千丝万缕的联系，有时候会竞争，有时候会协同作用。

### 单细胞RNA-seq

<img src="./image_RNASeq/SC-RNA-seq-analysis.jpg" alt="SC-RNA-seq-analysis" style="zoom:9%;" />



<!--chapter:end:0050-RNA_seq.Rmd-->

---
output:
  html_document: default
  word_document: default
---

- 我的一些想法与建议
1. 4.1.2 ChIP-seq 技术革新 这个部分放到最后，如果想要写的话，不必展开，做一个展望就好，给大家推荐几篇文章去进一步阅读即可。
2. 数据质控“使用FastQC对测序进行评估”这个部分，前面的章节已经写过了，可以略写，并写详细解释参考第X章；
3. “接头的去除” 这个部分和后面的去低质量的部分，我都建议增加cutadapt
4. “比对概念”比对概念可以略讲，之前的内容已经讲过了；
5. 以bowtie2为例的话，要把bowtie2的每一个参数都讲一下；
6. 以mm10为例，一般不用那些“chr1_GL456210_random”这种染色体，只用主要的染色体序列；
7. 所有的脚本，我建议都给出不用循环和用循环的两种方式，并在第一次出现的时候加以简单的说明；
8. 增加deeptools的分析流程，比如富集图，画出来的图是什么意思，以及代码；
9. MACS2要重点讲，程序的参数到output的每一列内容，都要解释一下；
10. motif分析，正向分析，反向分析都要包括；通过peak找motif，以及通过motif找binding protein


# ChIP-Seq和ATAC-Seq数据分析 {#ChIP_seq}

## ChIP-seq 简介

**ChIP-seq** (Chromatin immunoprecipitation followed by high-throughput sequencing) 即染色质免疫共沉淀高通量测序技术，把 **ChIP** 实验技术与第二代高通量测序技术相结合，可以用来寻找全基因组上检测与组蛋白、转录因子等互作的 DNA 区域，也就是我们常说的我感兴趣的转录因子在全基因组上结合在哪些区域、组蛋白修饰在全基因组上富集在哪些区域。这个方法有助于我们深入了解转录调控机制。

### ChIP-seq 实验

下一代高通量测序技术（next-generation sequencing, NGS）自 `2005` 年 **454 公司**首次推出第一款高通量测序仪**454 Genome Sequencers** [1, 2] 开始，一直是一个快速发展的领域，产生了一系列可用的文库构建流程和测序技术，将基因组水平的研究带入一个新的发展阶段。常用的高通量平台包括 `Illumina 公司的 Solexa 测序仪` , `Roche 公司的 454 测序仪` , `SOLID 公司的 (ABI)` 以及 `Thermo Fisher` 公司旗下的子公司 `Life Technologies` 的 `Ion Torrent的测序技术` 以及 `Pacific Biosciences` 公司的 `SMRT (DNA单分子实时测序技术)` 和 `Oxford Nanopore Technologies` 公司的`纳米孔单分子测序技术`（详情见 [2019-浅谈基因测序技术的发展及其在肿瘤中的应用](http://libproxy.hzau.edu.cn/rwt/CNKI/http/NNYHGLUDN3WXTLUPMW4A/KXReader/Detail?TIMESTAMP=637247240431171250&DBCODE=CJFQ&TABLEName=CJFDLAST2019&FileName=ZJTY201902090&RESULT=1&SIGN=dpZRZloduk0HVtKvSKWdjrojUNE%3d)）。这些技术在测序概念、通量和运行时间、获得的序列信息的长度和错误率等方面有所不同（详情见 [2015-High-Throughput Sequencing Technologies](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4494749/)）。

 `ChIP-seq` 是一项基于 [免疫沉淀（IP)](https://www.thermofisher.com/cn/zh/home/life-science/protein-biology/protein-biology-learning-center/protein-biology-resource-library/pierce-protein-methods/immunoprecipitation-ip.html) 的实验，利用高通量测序技术对一群细胞进行`免疫沉淀`鉴定全基因组上蛋白的结合位点（图 1）[8]，此项技术最早于 2007 年公开报道[3,4,5,6]。这里我们描述了最广泛使用 `Illumina` 测序平台的流程。流程使用与其他平台是相似的，但在文库的构建和测序步骤上略有不同。

![image-20200510162704888](./image_ChIPSeq/2009-NatureRevGenetics-ChIP-seq_pipeline.png)

> 图一

简要来说主要包括以下四个步骤：

1. **甲醛交联**：首先将染色质结合的蛋白质与 DNA 通过甲醛交联，从而可以得到蛋白质-DNA 复合物。为什么要做这一步呢？我们要研究蛋白与 DNA 之间的关系， 我们得保持他们当前的状态；不同物种、不同组织、不同细胞类型的交联时间都是不同的，只有恰当的交联的时间才能保证后续实验的顺利进行，交联时间太短，导致蛋白质-DNA聚合物松散；交联时间过长会导致蛋白质-DNA聚合物紧密，导致后面片段化十分困难、解交联麻烦等。
2. **获得染色质：**通过超声波将其随机打断或者酶解成一定长度范围内的染色质小片段（一般为 200-600 bp 左右）。因为我们当前二代测序的片段长度有限，所以一般选择打断在 200-600bp。
3. **免疫沉淀**：接下来，通过特异性抗体免疫沉淀出目标蛋白质-DNA 复合体，然后解交联，从而特异性地富集与目标蛋白结合的 DNA 片段。通过对目标蛋白的纯化与检测，选择特定长度的DNA片段，最后进行建库测序。
4. **文库准备：**测序文库的准备包括 `DNA 末端修复`、`测序接头的连接`。在复杂的情况下，比如在流式细胞仪上的同一个 `lane` 上运行多个样本。为了获得足够的测序量，对连接产物进行纯化和 PCR 扩增。PCR 扩增是产生 `bias` 的来源，因此 PCR 循环的次数应保持在最低限度。然后将文库加载到流式细胞仪上并进行测序。
5. **测序：** 打断的 DNA 片段的测序总是沿着 `5'-3'` 的方向进行。正向和反向接头被随机连接到双链 DNA 片段的两端。单端测序从正向接头或反向接头开始，而双端测序从两端开始。`reads` 的长度通常短于共孵育 DNA片段，因此只有片段末端被测序。

### ChIP-seq 技术革新

#### CUT&RUN

**CUT&RUN** （**Cleavage Under Targets and Release Using Nuclease**）是研究 DNA-蛋白质互作的一项革命性技术，无需用甲醛进行交联和免疫共沉淀。在这种方法中，初代使用**与 Protein A 结合的微球菌核酸酶**与所选择的抗体结合，并立即切割相邻的 DNA，然后释放与抗体靶向结合的 DNA，回收的 DNA 片段可直接进行 ChIP-qPCR 或者二代测序。该过程在原位进行，避免交联和增溶问题，减少了背景噪音，从而使得使用少量细胞在保证测序质量的前提下测序深度为平常 ChIP-seq 所需测序深度的十分之一。由于微球菌核酸酶激活时细胞核是完整的，CUT&RUN 可以检测目标位点周围的局部环境，使得 CUT&RUN 还能检测到转录因子的长距离 3D 互作位点。

![image-20200510204720478](./image_ChIPSeq/CUT_and_RUN_1.png)
 
## ChIP-seq 实验设计

### ChIP-seq对照的设计

为了准确地识别 ChIP-seq 样本中的富集区域，需要将 reads 分布与背景分布（即在进行抗体孵育之前的 DNA）进行比较，以控制潜在的偏差。ChIP-seq 实验最好的对照是在抗体孵育步骤之前对从打断后的染色质中纯化的 Input DNA 进行序列测定。其他`对照`可以使用不同的策略进行准备: 模拟 `IP` 遵循 `ChIP-seq` 实验流程的所有步骤，但不使用任何抗体。`非特异性 IP` 可以通过使用不与染色质结合的蛋白质的抗体来实现，比如：`免疫球蛋白G` (IgG)。然而，这两种方法都可以得到少量的低复杂度的共纯化DNA，而这并不能反映真实的背景分布。在研究`组蛋白修饰`时，一种能识别 `H3` 或 `H4` 的 `H3 泛抗体`或 `H4 泛抗体`是一种很好的选择, 因为捕获修饰时候同时捕获了潜在核小体分布。

### `bias` 的来源

`input` 样本是控制一些可能导致某些区域丰度异常高的 `biases` 所必需的。可能最重要的 `bias` 来源是在超声或消化过程中染色质的不均匀打断。致密的异染色质区是很难剪切的，并且与开放的常色质区域相比，即使在 `input` 样本中，也变得捕捉的量不足 。染色质的紧密的影响是线性的，例如：染色质越开放，文库中能捕捉到的量越高。此外，PCR 扩增产生的不均匀片段和 `bias` 将导致富含 GC 序列的过度表达。同样，背景分布将与基因组的 GC 含量呈正相关。这在哺乳动物细胞中尤为普遍，因为常染色质区被富集 `CpG 岛`。因此，在比较 `CpG` 富集的地区与其他拥有较少 `CpGs` 的区域时，应考虑到这一点。

`bias` 的另一个来源是对数据的计算处理过程。在基因组回比步骤，只有唯一比对上的 reads 才保留下来进行后续分析，导致在重复区域低覆盖度。最后，`在癌症样品和细胞系中，基因组与参考基因组有很大的不同`。在所研究的细胞系中被删除的区域将显示为缺失，而重复或扩增的区域会产生更多的 `reads`，并且看起来更富集。

为了解释这些 `biases`，将一个 ChIP-seq (或至少一组重复)与对照样本进行比较是至关重要的，对照样本将用于在 `Peak calling` 步骤中控制潜在的假阳性 `Peak` 。

### 抗体质量

由于 `ChIP-seq` 是一种基于抗体的免疫沉淀实验，其效率很大程度上取决于抗体的质量和特异性。因此选择一个好的抗体是至关重要的。例如，之前有报道说，大约三分之一的商业 ChIP-seq 抗体对组蛋白修饰不起作用。此外，同一蛋白质的单个抗体可能识别不同的表位，这些表位可能根据基因组位置的不同而暴露在不同的表位上（尤其是单克隆抗体）。例如，一种特定于某因子的抗体可能检测富集在启动子区，而另一种针对同一因子的抗体也可能检测富集在基因间间区。因此，建议对同一种蛋白的几种抗体进行检测并验证其特异性，例如，在 `Western blot` 分析中通过 `knock-out` 和 `knock-down` 来验证它们的特异性。

### 测序深度

为了在实验中捕获所有真正的结合位点，测序的 `reads` 数量是一个决定因素。所需的 `reads` 数取决于基因组的大小和感兴趣因子的结合模式（转录因子的窄峰和组蛋白修饰的宽峰）。这两个参数共同定义了基因组的有效大小，例如，需要覆盖的碱基对 (bp) 的数量。它还取决于 `Peak calling` 的灵敏度: 为了确定最高富集的峰(`input` > 30x)，大约三分之一的 `reads` 就足够了。一旦对样本进行测序，`饱和度分析`就可以显示是否在给定数量的`回比上的 reads` 下在样本中所有的的 `Peak是否`都被鉴定到。在黑腹果蝇中，转录因子和组蛋白修饰表明，在 1600万(`16 M`) 左右的 `reads` 处达到饱和 ；相反，在哺乳动物中，转录因子至少需要 `30M reads`，组蛋白修饰需要最少 `60M reads`。`Input` 样本需要测序至少和 `ChIP` 样本一样深，因为在这种情况下，也是需要覆盖整个基因组。

### 测序片段的长度与测序方式

测序 reads 相关的决定因素的是 reads 长度和单端或双端测序。单端和双端 reads 是从随机连接到 DNA 片段两端的一个或两个接头测序的结果。在大多数 ChIP-seq 研究中，reads 长度和测序类型不是关键的考虑因素，而目前标准的 `50-nt 单端测序`足以捕捉推断结合位点所需的大部分信息。通常，较长或双末端 reads 都有更高的机会唯一地回比到基因组，即使在轻微重复的区域也是如此。因此，可以覆盖更大比例的基因组，并且在比对过程中过滤掉较少的 reads。如果该因子被期望结合重复区域，建议使用尽可能长的 reads 和双末端测序。如果 reads 范围超出重复区域，这将增加进行唯一比对的几率。然而，重复区域仍然很难研究，即使是较长的或双末端 reads，它所带来的成本增加可能不会随着预期产量的增加而扩大。

### 样品重复的设置

重复样本可以呈现不同水平的变异。技术重复的范围从重新测序文库到在同一细胞培养的重复中进行 ChIP-seq。然而，为了评估生物的变异性和获得对已确定的结合区的置信度，`ChIP-seq 实验应该用生物学重复`（不同的细胞培养物或个体）。一般来说，建议至少重复三次，以获得合理可靠的结果，并强制统计模型成立（尽管许多模型已经适应了只有两次可用重复的情况）。对于每个条件，最低要求是对 ChIP 进行两次重复，对相应的 `input` 进行一次重复。如果数据要表现出很高的内在变异性，可能需要更多的重复，例如：当取自不同个体的样本时。

## ChIP-seq 数据分析流程
ChIP-seq 数据分析包括几个步骤（图 1.1B）。

得到原始序列文件后的第一步是执行标准的高通量数据质量控制。

1. 这一步确保数据质量高：没有污染以及文库复杂度高（`见第 3 节`）。
2. 原始的 reads 回比到研究物种的参考基因组上（`见第 4 节`）。
3. 随后可进行特异性 ChIP-seq 的质量控制，检查 ChIP-seq 样品中的富集情况，并排除过度碎片（`见第 5 节`）。
4. 接下来是 ChIP-seq 分析的核心，鉴定全基因上感兴趣的因子富集的区域，也叫 `Peak calling`（`见第 6 节`）。
5. 一旦确定了峰值区域，还可以评估需要峰值位置的特定 ChIP-seq 的质量控制措施（`见第 5 节`）。
6. 还有几乎每一步都需要涉及的数据可视化（`见第 7 节`）。
7. 尤其重要的是，在 `Peak calling` 之后，要确保预测的峰值准确地捕捉到结合模型。`Peak calling` 后的分析取决于实验设计与生物学问题。
8. 比如，如果在实验中有重复或多个条件下，那么下一步可能是样本之间的比较（`见第 8 节`）。

生物学重复将提供有关数据中的重现性和内在生物和技术变异性的信息。差异结合分析解决了哪一 `Peak` 区域在两种情况下显示出明显不同的丰度（例如：与观察到的相同条件的重复之间的变化相比，差异比预期的要大得多）。最后，`Peak` 区间或差异 `Peak` 可以被用来做各种下游分析，比如`基因组注释`、`GO分析`、`Pathway 分析`、`motif 查找`、`与其他基因组数据联合分析`。

![img](./image_ChIPSeq/chip_workflow_june2017_step4.png) 

### 代码运行环境的准备

```bash
mkdir bio_soft
cd bio_soft
mkdir my_soft  # 用于保存可执行文件

# 安装 conda 
# 官方链接：https://docs.conda.io/en/latest/
# For the installers "Anaconda" and "Miniconda," the default is 2.7.
# For the installers "Anaconda3" or "Miniconda3," the default is 3.7

wget -c https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
# 然后 source 环境变量 .bashrc 文件，使其生效
source ~/.bashrc

# 运行以下命令，使 conda 不自动激活 base 环境，因为我们自己环境还有不急于 conda 的
conda config --set auto_activate_base false

# 运行以下命令，可以看到是有一个叫做 base 的环境的
conda env list 

# 添加镜像源
# 将清华源官方链接中的信息添加到 .condarc 中
# https://mirror.tuna.tsinghua.edu.cn/help/anaconda/

# 安装下载数据软件 aspera，此不基于 conda 安装
wget https://download.asperasoft.com/download/sw/connect/3.9.8/ibm-aspera-connect-3.9.8.176272-linux-g2.12-64.tar.gz 
tar -xvf ibm-aspera-connect-3.9.8.176272-linux-g2.12-64.tar.gz
bash ibm-aspera-connect-3.9.8.176272-linux-g2.12-64.sh
echo 'export PATH=$PATH:~/.aspera/connect/bin/' >> ~/.bashrc # add to .bashrc env 
source ~/.bashrc

# 安装 SRAtools
# https://github.com/ncbi/sra-tools/wiki/02.-Installing-SRA-Toolkit
# https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/current/
wget --output-document sratoolkit.tar.gz http://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/current/sratoolkit.current-centos_linux64.tar.gz
tar -xvf sratoolkit.tar.gz
echo "PATH=$PATH:~/bio_soft/sratoolkit.2.10.5-centos_linux64/bin" >> ~/.bashrc
source ~/.bashrc

# 安装 FASTQC，质检 FASTQ 文件用
# https://www.bioinformatics.babraham.ac.uk/projects/download.html
wget https://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_v0.11.9.zip
unzip fastqc_v0.11.9.zip
chmod 755 fastqc
ln -s ~/bio_soft/FastQC/fastqc ~/bio_soft/my_soft/fastqc # 软链接到专门管理可执行文件夹中
source ~/.bashrc

# 安装 MultiQC，汇总所有质检结果
# https://multiqc.info/docs/
conda install -c bioconda -c conda-forge multiqc
ln -s /miniconda3/envs/ChIP_seq/bin/multiqc ~/bio_soft/my_soft/multiqc


# 安装 fastp
# https://github.com/OpenGene/fastp
wget http://opengene.org/fastp/fastp
chmod a+x ./fastp
echo 'PATH=$PATH:~/bio_soft/my_soft'  >> ~/.bashrc
source ~/.bashrc

# 安装 bowtie2
## 第一种
conda install -c bioconda bowtie2

## 第二种
wget https://github.com/BenLangmead/bowtie2/releases/download/v2.4.1/bowtie2-2.4.1-linux-x86_64.zip

unzip bowtie2-2.4.1-linux-x86_64.zip 
echo "PATH=$PATH:~/bio_soft/bowtie2-2.4.1-linux-x86_64" >> ~/.bashrc
source ~/.bashrc

# 安装 htslib
wget https://github.com/samtools/htslib/archive/1.10.2.zip
unzip 1.10.2.zip
mkdir htslib.1.10.2
cd htslib-1.10.2
autoheader
autoconf
./configure --prefix=/public/home/xrzhang/bio_soft/htslib.1.10.2
make
make install
echo "PATH=$PATH:~/bio_soft/htslib.1.10.2/bin" >> ~/.bashrc

# 安装 samtools 1.10 版本
## 第一种
conda install -c bioconda samtools

## 第二种
## https://www.htslib.org/download/
## samtools 说明书 http://www.htslib.org/doc/samtools.html
wget https://github.com/samtools/samtools/releases/download/1.10/samtools-1.10.tar.bz2
tar -jxvf samtools-1.10.tar.bz2
mkdir samtools.1.10
cd samtools-1.10
./configure --prefix=/public/home/xrzhang/bio_soft/samtools.1.10
make 
make install
echo "PATH=$PATH:~/bio_soft/samtools.1.10/bin" >> ~/.bashrc
source ~/.bashrc

# 安装 bedtools 2.29.1 版本
## https://bedtools.readthedocs.io/en/latest/content/installation.html
wget https://github.com/arq5x/bedtools2/releases/download/v2.29.1/bedtools-2.29.1.tar.gz
tar -xvf bedtools-2.29.1.tar.gz 
cd bedtools2/
make
echo "PATH=$PATH:~/bio_soft/bedtools2/bin" >> ~/.bashrc
source ~/.bashrc


# 安装 Picard
## 第一种
conda install -c bioconda picard

## 第二种
wget https://github.com/broadinstitute/picard/releases/download/2.23.0/picard.jar
# 以后移动到自己常用的 bin 目录下
java -jar picard.jar -h

# 创建我们此次所需要的环境
conda create -n ChIP_seq python=3.7 

conda activate ChIP_seq
conda install 
```

### 数据的下载

我们需要下载的示例数据集为文章 [Competition between DNA methylation and transcription factors determines bind- ing of NRF1.](https://www.nature.com/articles/nature16462) 中的，都为单端测序。

| Sample name        | GEO ID     | SRA ID     | raw reads  |
| ------------------ | ---------- | ---------- | ---------- |
| NRF1_CHIP_WT1      | GSM1891641 | SRR2500883 | 40,570,927 |
| NRF1_CHIP_WT_2     | GSM1891642 | SRR2500884 | 40,365,286 |
| H3K27AC_CHIP_WT1   | GSM1891651 | SRR2500893 | 41,972,346 |
| H3K27AC_CHIP_WT2   | GSM1891652 | SRR2500894 | 40,822,025 |
| NRF1_INPUT_WT      | GSM1891643 | SRR2500885 | 22,773,779 |
| NRF1_CHIP_TKO_1    | GSM1891644 | SRR2500886 | 32,306,980 |
| NRF1_CHIP_TKO_2    | GSM1891645 | SRR2500887 | 45,342,909 |
| H3K27AC_CHIP_TKO_1 | GSM1891653 | SRR2500895 | 50,829,570 |
| H3K27AC_CHIP_TKO_2 | GSM1891654 | SRR2500896 | 45,485,455 |
| NRF1_INPUT_TKO     | GSM1891646 | SRR2500888 | 24,937,026 |

这些数据被用来测试`转录因子结合对 DNA 甲基化`的敏感性，例如：测试 DNA 甲基化是否影响转录因子的结合。其基本假设是，如果在正常 `WT` 细胞中，一些转录因子在 DNA 甲基化时不能结合，那么在去除了甲基化的 `TKO细胞`时，就会出现新的结合位点。通过使用 `DNase-seq` 分析开放的染色质区域，与 WT 相比，我们可以确定 TKO 细胞中获得转录因子结合的新区域。`MOtif` 分析确定 `NRF1` 是对DNA甲基化敏感的潜在候选分子，我们在 WT 和 TKO 细胞中用 NRF1 的ChIP-seq 验证了这一点。

这里我们推荐一个在线网站：[SRA Explorer](https://sra-explorer.info/#)（https://sra-explorer.info/#），我们可以直接输入 `GSE30567`, `SRP043510`, `PRJEB8073`, `ERP009109` or `human liver miRNA` 这些信息来获取我们的数据链接。具体细节这里不做展示，大家可以自己去实践。

当我们将上面十个 SRR 号输入后，我们会得到下面几种结果：

![image-20200516144937351](./image_ChIPSeq/10_SRR.png)

可以清楚的看到，结果有好几种下载方式的链接或者命令。

- #### [Raw FastQ Download URLs](https://sra-explorer.info/#fastqURLs)：纯粹的下载 FASTQ 的链接。

![image-20200516150148716](./image_ChIPSeq/raw_fastq.png)

- #### [Bash script for downloading FastQ files](https://sra-explorer.info/#fastqURLs_bashCURL) ：通过软件 curl 来下载的命令。

![image-20200516150102230](./image_ChIPSeq/down_load_fq_bash.png)

- #### [Aspera commands for downloading FastQ files](https://sra-explorer.info/#fastqURLs_aspera)：通过软件 Aspera 来下载的命令。

> 这里有几个选项：
>
> 1、如果你是基于 linux 那么你得选择 linux，如果你是基于 OSX 系统那么就得选择这个
>
> 2、如果你想下载完后重新命令那么选择 Append `mv` command to rename downloaded files ，反之选择 Don't rename files。

![image-20200516150030006](./image_ChIPSeq/Aspera.png)

- #### [Cluster Flow FastQ download file (nice filenames)](https://sra-explorer.info/#fastqURLs_niceNames)：将会输出链接以及对应的名称

![image-20200516145959895](./image_ChIPSeq/Cluster.png)

- #### [bcbio project file for FastQ downloads (nice filenames)](https://sra-explorer.info/#fastqURLs_bcbio) 

![image-20200516145840008](./image_ChIPSeq/bcbio.png)

当然，你也可以下载 SRA 或者其他格式文件，但是我们一般需求都是从 FASTQ 开始。

下面我们开始下载本次所需数据，创建`01_down.sh` 脚本文件，然后运行 `bash 01_down.sh` （非并行，花了 40 分钟左右）即可。

```bash
#!/usr/bin/env bash
ascp -QT -l 300m -P33001 -i $HOME/.aspera/connect/etc/asperaweb_id_dsa.openssh era-fasp@fasp.sra.ebi.ac.uk:vol1/fastq/SRR250/005/SRR2500885/SRR2500885.fastq.gz .
ascp -QT -l 300m -P33001 -i $HOME/.aspera/connect/etc/asperaweb_id_dsa.openssh era-fasp@fasp.sra.ebi.ac.uk:vol1/fastq/SRR250/003/SRR2500883/SRR2500883.fastq.gz .
ascp -QT -l 300m -P33001 -i $HOME/.aspera/connect/etc/asperaweb_id_dsa.openssh era-fasp@fasp.sra.ebi.ac.uk:vol1/fastq/SRR250/004/SRR2500894/SRR2500894.fastq.gz .
ascp -QT -l 300m -P33001 -i $HOME/.aspera/connect/etc/asperaweb_id_dsa.openssh era-fasp@fasp.sra.ebi.ac.uk:vol1/fastq/SRR250/007/SRR2500887/SRR2500887.fastq.gz .
ascp -QT -l 300m -P33001 -i $HOME/.aspera/connect/etc/asperaweb_id_dsa.openssh era-fasp@fasp.sra.ebi.ac.uk:vol1/fastq/SRR250/003/SRR2500893/SRR2500893.fastq.gz .
ascp -QT -l 300m -P33001 -i $HOME/.aspera/connect/etc/asperaweb_id_dsa.openssh era-fasp@fasp.sra.ebi.ac.uk:vol1/fastq/SRR250/004/SRR2500884/SRR2500884.fastq.gz .
ascp -QT -l 300m -P33001 -i $HOME/.aspera/connect/etc/asperaweb_id_dsa.openssh era-fasp@fasp.sra.ebi.ac.uk:vol1/fastq/SRR250/006/SRR2500886/SRR2500886.fastq.gz .
ascp -QT -l 300m -P33001 -i $HOME/.aspera/connect/etc/asperaweb_id_dsa.openssh era-fasp@fasp.sra.ebi.ac.uk:vol1/fastq/SRR250/005/SRR2500895/SRR2500895.fastq.gz .
ascp -QT -l 300m -P33001 -i $HOME/.aspera/connect/etc/asperaweb_id_dsa.openssh era-fasp@fasp.sra.ebi.ac.uk:vol1/fastq/SRR250/006/SRR2500896/SRR2500896.fastq.gz .
ascp -QT -l 300m -P33001 -i $HOME/.aspera/connect/etc/asperaweb_id_dsa.openssh era-fasp@fasp.sra.ebi.ac.uk:vol1/fastq/SRR250/008/SRR2500888/SRR2500888.fastq.gz .
```

到这里我们可以看到前面这一部分都是相同的 `ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR250/`，然后接下来都是 `SRR` 号的最后一位数字即 `00+SRR号最后一位`，然后就是 `SRR号/SRR号.fastq.gz`。

```bash
#!/usr/bin/env bash

cat `cut -f1 SRR.list`|while read id;
do
    ascp -QT -l 300m -P33001 -i ~/.aspera/connect/etc/asperaweb_id_dsa.openssh era-fasp@fasp.sra.ebi.ac.uk:/vol1/fastq/${id:0:6}/00${id:0-1}/$id/${id}.fastq.gz ./
done
```

### 数据质控

由于我们测序下机刚得到的数据是含有接头序列，且碱基质量层次不齐，这会在很大程度上影响我们后续回比到基因上的过程，会导致回比率偏低等问题。所以我们一般在拿到数据后查看完质量后，就需要进行一定的修剪和过滤。在此部分将会陈述我们需要注意哪些质控的标准以及怎么去过滤。

一些软件为高通量测序数据提供了易于操作的质量控制。`FastQC` 是最常用的工具之一，它可以在 `FASTQ` 和其他来自多个测序平台的文件格式上运行。其他工具为数据处理提供了额外的功能，比如：`NGS QC Toolkit`（ 见 ref3 ）和 `fastx-toolkit` （[hannonlab.cshl.edu/fastx_toolkit/](http://hannonlab.cshl.edu/fastx_toolkit/)） 。

#### 使用FastQC对测序进行评估

与之前章节内容类似，我们这次再次强调FastQC是为了突出一些和ChIP-Seq数据分析有关的质量报告内容，读者灵活掌握即可。

- **每个位点的测序质量** 在许多测序 `runs` 中，由于测序化学的逐步降解，碱基识别（ `base calling` ）精度随着循环次数的增加而下降。此外，在第一个循环中也会出现轻微的质量下降和运行过程中的瞬时波动。这种系统的质量变化可以从每个测序周期的 `Q 值` 分布中看到。如果 `50%` 的 reads 显示 `Q < 25` ( 或在 `Q < 10` 占10%)，FastQC 会发出警告，表明基于质量的读数修整是值得推荐的。在本文中可以看到数据质量这部分是没有问题的，可能是上传的非原始下机数据而是过滤后的数据。

- **每个位点的碱基成分** 在 ChIP-seq 流程中，DNA 被打断成随机的片段。因此，核苷酸的组成在整个过程中应该是恒定的（ 图 3.1B ）。由于两条链的测序概率相等，G 和 C 将同等丰度，但将根据基因组的 GC 含量与 A 和 T 分开。

> 注意：不同的测序类型这部分并不是绝对的，也就是并非所有得到测序得到的 FASTQ 文件这部分都是 AT 重合、GC 重合的。比如在 DNA 甲基化测序这种对碱基处理后的 WGBS 这部分是不一样的，这里不予详细讨论。

- **每条 reads 的平均 GC 含量** 在一个复杂的 ChIP-seq 文库中，reads 是从大量富集的DNA片段中随机取样的。因此，每条 reads 的 GC 含量分布应成正态分布。偏差表示 reads 的 `biased` 或来自不同 `GC` 含量的有机体的污染。当针对接头序列进行过滤时，其中一些偏差会得到解决。

> 注意：富集的 DNA 片段反映了所研究的转录因子（ TF ）或组蛋白修饰的序列特异性。因此，在某些情况下，GC 含量可能会偏离均匀分布。例如：如果 TF 结合在 CpG岛 或低复杂性区域，如端粒。

- **其他质量指标** 在复杂的 ChIP-seq 文库中，大多数富集片段将是唯一的。高水平的重复 （ 即相同的高通量测序 reads ）表明存在富集偏差，例如由于起始物质数量不足而导致的 PCR 过度扩增。过量的自由引物表明，在文库准 备过程中，这些引物没有被有效地去除（见 **章节 1.1** ）。在此例中我们结合 CD 两图可以猜测 D 图中原始数据中的 GC 含量分布的异常很有可能是图 C 中过表达序列引起的，当我们修剪和过滤后，可以看到当没有过表达序列时候，GC 含量分布是正常的。
- 此外，如果 DNA 片段短于 reads 长度，则用于测序的接头将出现在 reads 上。由于 DNA 片段的平均长度为 200 bp，在短 reads 中接头应基本不存在，但在较长 reads 时，接头应开始出现在位置 70-100 bp 附近。在早期的测序周期中接头的高含量表明了文库的过度碎片化。默认情况下，FastQC 将搜索几个常用的 `Illumina` 接头。用户也可以提供自定义接头序列。

```bash
#!/usr/bin/env bash

# cd data
mkdir QC
ls *gz | xargs fastqc -t 10 -q -o QC 

cd QC
multiqc .
```

#### 根据报告对数据进行修剪和过滤

接下来，含有过度的接头序列和低质量的碱基将被过滤掉。这可以通过完全删除相应的 reads 来实现，从而在整个数据集中保持相等的读取长度，或者通过修剪它们来实现。

> 注意：对于样本的比较，样本具有相同的  reads 长度是很重要的。不同的 reads 长度意味着基因组的可回比的比例不同，这在比较分析中可能导致人为现象。

##### 接头的去除

- 如果富集的 DNA 片段小于 read 长度，则高通量测序 reads 将延伸到下游接头。由于所包含的接头序列将影响基因组比对，它们需要在基因组比对之前删除。
- 接头匹配的严格性依赖于几个参数，包括所需的最小重叠和最大错配。此步骤的低严格性可确保检测到大多数接头。不同的匹配模式指定在 reads 中允许的接头位置以及哪部分需要被去除。

##### 低质量的修剪

- reads 中的低质量序列可能会影响其基因组比对。大多数 reads 长度较短的 ChIP-seq 数据集不需要低质量的修剪。然而，如果在质检中大量的质量 `drop` 是可见的，reads 应该进行修剪或丢弃。
- 删除低质量序列的一种常见方法是在 Q 值低于给定阈值的第一个位置修剪每个 reads 的内容（通常 Q < 20）。或者，可以容忍单个低质量的位置，这样，只有当滑动窗口中的平均 Q 值低于给定阈值时，才会修剪 reads。
- 作为另一种选择，数据集中的所有 reads 都可以在低质量序列开始成簇出现之前的某一点上进行剪切。这避免了 reads 长度的差异，并允许集成具有不同测序长度的 ChIP-seq 数据集（比如在比较 50nt 和 100nt reads 时候，所有的 reads 应该都被修剪为 50nt）。

- 建议始终在修剪数据集上重新运行 FastQC 。此外，大多数工具返回修剪的 reads 数、删除的核苷酸和删除的 reads 。如果数据集之间出现很大的差异，则应重新检查样本的质量。如有必要，应调整修剪参数以使采样尽可能具有可比性。

- 质量修剪和过滤的常用工具是 **`Trim Galore`**、**`FLEXBAR`**、**`Trimmomatic`**、**`fastp`** 。

**fastp 过滤**

这里我们将用 fastp 来进行数据过滤。fastp 是基于 C++ 开发的，使用高效算法，且支持多线程，具有丰富的功能的软件。根据 reads 质量、长度过滤，自动查找并裁剪接头序列、对 reads 进行滑动质量裁剪、对双端数据进行碱基校正、分子标签 UMI 处理等。

```bash
#!/usr/bin/env bash

# mkdir clean_data
cd data

ls *gz | while read id;
do
  out=${id%%.*}
  fastp --thread 10 -i $id -o ../clean_data/${out}_clean.fastq.gz -h ../clean_data/${out}.html	 
done
```

> bsub -J fastp -n 10 -R span[hosts=1] -o %J.out -e %J.err -q normal "bash 03_trim.sh"

速度很快，参数也基本不需要改变。

![image-20200516201729763](./image_ChIPSeq/fastp.png)

fastp 也可以自动生成全自动的人性化报告，但是为了前后更好的对比，这里仍然使用 FASTQC 进行再一次质检。

```bash
#!/usr/bin/env bash

# cd clean_data
mkdir QC
ls *gz | xargs fastqc -t 10 -q -o QC 
multiqc .
```

![image-20200519171339719](./image_ChIPSeq/FASTQC.png)

FASTQC 质检结果。（A）测序 reads 每个位点的碱基质量值 Q 的分布。箱式图的上下须分别表示 10% 和 90%。背景颜色绿色、黄色、红色依次代表质量好、可接受、差。（B）测序 reads 每个位点的 ATCG 碱基的相对百分比折线图。（C）表示测序 reads 中是否有过表达序列，左边表示原始数据中的情况，右边表示进行修剪和过滤后的情况。（D）表示文库中所有 reads 的 GC 含量分布，蓝色表示预期的 GC 含量分布呈正态分布，红色表示文库中的 GC 含量分布情况。左边表示未修剪和过滤前，右边表示修剪和过滤后。

### 序列比对
**高通量测序回比到参考基因组上确定了共纯化的 DNA 片段的来源。**本节介绍参数设置的不同对比概念和注意事项，以及评估比对质量的措施。

基因组回比的目标是找到参考基因组中高通量测序 reads 的最可能的来源。除了大的基因组和大量的 reads，还因为 reads 和参考序列之间可能存在的不匹配而变得更加复杂。这些序列偏差可能是由于产生高通量测序 reads 过程中的扩增或测序错误引起的，也可能是由于参考基因组水平上的基因组变异或错误造成的。

#### 比对概念

由于 ChIP-seq reads 是直接从 DNA 片段衍生的，所以数据通常用连续短 read 比对软件比对。这些比对算法中的许多都采用了 “种子扩展 **seed-and-extend**” 的方法。在第一步中，该算法识别 **k-mer** 种子，即指定长度的 reads 片段，这些片段精确地映射到基因组中的给定位置（ `ref1` ）。依赖于算法，种子匹配必须是精确的，或者可以容忍一定数量的错配。在第二步中，使用动态规划在两个方向上扩展种子，以达到无间隙的最大可映射长度，并最终生成完全比对。

基于概念上的差异，可用的算法在比对准确性（ 灵敏度和精度 ）以及计算性能（ 运行时间和内存 ）方面有所不同。差异还受种子长度选择的影响，较短的种子可提高敏感性，而较长的种子可使搜索速度更快。

大多数算法分配一个质量分数来估计获得的比对的准确性（见第 4.2.4 节）。在某些情况下，此分数考虑到 reads 的碱基识别准确性（ 即 FASTQ 文件中的 Q 值）中来衡量错配。

#### 常用工具

目前常见的 ChIP-seq 比对工具主要为：Bowtie、Bowtie2、BWA。Bowtie2 和 BWA 能够通过跨区域（gapped alignment）考虑 indel（插入和缺失）比对，常用于长的 reads 和双端 reads 的比对。Bowtie 常用于短 reads 的比对。 

有各种各样的对齐工具，它们在概念、建立索引方法、计算性能和映射精度方面都有所不同（详细信息见 `ref1` ）。一个非常流行的用于 ChIP-seq 数据的工具是基于 “ 种子和扩展  **seed-and-extend** ” 的算法 Bowtie2，它提供了高精度和高速度（ `ref2` ）。由于其高效的索引编码，**Bowtie2** 的内存需求相对较小，支持其在普通笔记本电脑或台式计算机上的应用。此外，许多专门的应用程序都是为特定的用例而设计的。例如，**Bowtie2** 明确支持来自新兴的第三代测序方法的 reads 比对。另外，`ENCODE` 计划依赖于 **BWA** 算法，以高效和可重复的方式比对数百个 ChIP-seq 数据集（ `ref3` ）。

#### 参数和注意事项

- 错配
由于测序错误和单核苷酸变异，一些 reads 将不会完全匹配参考基因组。为了避免丢失这些 reads ，在比对过程中应该允许一定数量的错配。最佳阈值取决于样品的类型和实验类型。大多数比对算法允许指定每条 reads 比对的绝对错配数，或者指定相对于 reads 长度的不匹配频率（对于 **Bowtie2** 的参数设置 **4.3** 节）。

> 注意：对于高度突变的细胞（如癌细胞）的 ChIP-seq 实验，或当与低质量的参考基因组比对时，应该允许更多的错配。此外，一些平台显示出比其他平台高得多的错误率。例如，`Illumina` 测序通常引入的误差不到 0.1%，而第三代测序方法的错误率可能超过 10%（ `ref4` ）。

- 多重比对

多重比对，即比对到基因组中的多个位置的 reads ，在短的 reads 比对中呈现了相当大的挑战（ `ref5` ）。这种模棱两可的比对最常见的来源是重复区域，例如占人类基因组 10% 以上的 *`Alu`* 元素。重复区域也可以起源于片段甚至全基因组的复制，例如拟南芥。

引入了不同的概念来处理多重比对事件。按照保守的方法，许多工作流只保留唯一比对的 reads ，以便进行进一步的分析。或者，可以通过使用全部或仅使用一个随机选择的比对位置来考虑多个映射事件。

> 注意：当报告一个 reads 的多个比对位置时，比对的数量可能会大大高于 reads 的总数。

由于 ChIP-seq 中共纯化的 DNA 片段约为 200bp，如果有足够数量的 reads 唯一地排列在重复序列周围，那么在较短的重复区域内的结合位点仍将被捕获。如果初步分析表明与某种类型的重复序列结合，也可以对从 [**Repbase**](https://www.girinst.org/repbase/) 中提取的一致重复序列进行比对。这通常可以实现更高的覆盖率，并允许对重复序列的结合进行更精确的量化。在研究预期在重复区域结合的蛋白质时需要考虑的其他因素见 `章节 1`。

- 其他参数

**基因组版本** 大多数参考基因组存在多个版本。通常建议使用最新版本。对于大多数分析来说，考虑到常规染色体就足够了（例如人类中的 **chr1-22, X, Y** ）。删除任何 **`scaffolds`** ，因为这可能会导致比对模糊不清。

> 注意：如果所研究的生物体没有参考基因组序列，则 ChIP-seq 数据可以与近亲物种的基因组进行比对。在这种情况下，考虑到基因组序列的差异，允许更多的错配是可取的。或者，可以通过 ChIP-seq reads 的从头组装来重建结合位点（见 `ref6` ）。虽然结合位点在基因组中的位置尚不清楚，但这种方法允许进行某些下游分析，如 `Motif` 查找。此外，与单个 reads 相比，增加组装的结合位点的长度可以促进与密切相关的基因组序列的比对。将 ChIP-seq 和 `input` 样本中 reads 的数据组合在一起，可以组装更大的 `contigs`。
>
> 注意：在等位基因特异性结合的分析中，reads 中存在的杂合单核苷酸变异（ `SNVs` ）被用来区分给定染色体的父本或母本上的结合。通常，可以通过在 reads 比对中将 `SNV` 信息与错配项叠加在一起来评估这一点。可以考虑调整允许的错配数量，以捕获所有 reads 变异。然而，为了避免参考偏差，最近的一项研究将 ChIP-seq reads 直接比对到根据 `SNV` 信息重建的单倍体亲本染色体（ `ref6` ）

**Soft-clipping** 一些比对算法通过所谓的 `Soft-clipping` 来提高比对率。例如：在 reads 的任何一端的核苷酸都可以从比对中被排除。这对于绕过 reads 末端的低质量序列很有用，但也可以用来定位与未注释的基因组重排有交集的的 reads 。

**单末端与双末端 reads** 正如在 **第1.4章** 中更详细地解释的，早期大多数 ChIP-seq 实验使用单端测序，现在由于双端建库普遍相对单端便宜，而且准确度更高，目前一般采用双端建库。如果双末端 reads 可用，则应将两个一起进行比对，以提高比对精确度。从而与单端测序相比，双端唯一比对的比例增加。

- 输出格式
reads 比对信息通常存储在在 `BGZF` 压缩的 `BAM` 文件或相应的可读 `SAM` 对应文件中报告（ `ref7` ）。`header` 部分提供了有关原始 `fastq` 文件、比对软件的应用（包括参数的选择）和使用的参考基因组的详细信息。在比对部分中，每个比对由 reads的名称、序列和质量信息以及关于参考基因组中的比对坐标的信息来描述。扩展的 `CIGAR` 字符串描述比对上的 reads 比例、插入、缺失等信息。可选字段允许添加额外的标记，例如，报告基因组中某一给定 reads 的比对数量（多重比对）或 重复。
- `SAMtools` 是一个软件包，它提供了各种要处理 `SAM/BAM` 的实用程序（ `ref7` ）。特别地，排序和索引允许快速检索与特定基因组区域重叠的比对，而无需将所有比对信息加载到内存中。同样，[**Picard**](https://broadinstitute.github.io/picard/) 提供了一组命令行工具，包括一些用于预先过滤的选项。

#### 使用 Bowtie2 进行基因组比对
本节演示如何使用 `Bowtie2` 对 ChIP-seq 数据进行比对，然后是几个后续处理步骤。首先，从 **UCSC** 下载参考基因组（ 老鼠基因组 `mm10` ），然后使用 `Bowtie2` 建立索引。然后在示例 `FASTQ` 文件上运行 `Bowtie2` ，并对生成的 `BAM` 文件进行过滤、排序和索引。

`Bowtie2` 使用的是一种非常快速且节省内存的比对算法（ `ref2` ）。与上一版本不同的是，**Bowtie2** 不再提供参数来显示定义错配和多重比对的阈值。相反，**Bowtie2** 实现了一种评分方案，该方案将用户可配置的惩罚分配给 `gap` 和 `extension` 等。错配罚分由 `FASTQ` 文件中相应碱基的 `Q` 值加权（见 `章节 3.1` ）。如果比对总得分高于用户定义的阈值，则该比对被视为有效。比对分数在 `SAM/BAM` 文件的 `MAPQ` 文件中报告。更多详细信息见[ **Bowtie2** 说明书](http://bowtie-bio.sourceforge.net/bowtie2/manual.shtml)。

**Bowtie2** 生成的比对文件通常通过过滤给定的比对得分进行事后处理。一个常用的过滤标准是 `MAPQ > 20`，它通常保持唯一比对 reads 。可以使用 `Samtools`  执行过滤，如下所示。使用 **bedtools** 的 `bamToBed` 命令，可以很容易地从 `BAM` 文件生成 `BED` 文件（ 见 `第2.2.4章` ）。

一旦对 BAM 文件进行了排序和索引，就可以通过一些指标来评估数据质量。

**比对上的 reads 所占百分比** 即从初始 `FASTQ` 文件中 reads 能够成功地与参考基因组比对上的 reads 数应尽可能高，通常 `>70%` 。`比对率 < 50%` 的文库可能包含大量污染或其他缺陷，应将其排除。

BAM 文件中唯一比对 reads 起始位置的分比例可作为文库复杂性的度量。在 `input` 样本中， reads 应该分布在整个基因组中，然而在 ChIP-seq 样本中，它们应该聚集在某些地方。因此，在 ChIP-seq 样本中，唯一比对的 reads 开始的比例应该始终低于 `Input` 样本。此外，与组蛋白修饰相比，`TFs` 的这一部分有减少的趋势，反映了它们在不同位点的更有选择性的结合。ChIP-seq 示例通常显示大约 80% 的唯一reads 。
  
相对丰度过高的 reads ，使我们可以检查潜在的人为因素。此类重复的数量过高可能会降低文库的复杂性。

- 下载 mm10 基因组序列文件和注释信息

进入 UCSC https://genome-asia.ucsc.edu/cgi-bin/hgGateway?db=mm10&redirect=manual&source=genome.ucsc.edu，可以看到有几种方式下载，其中推荐用 `rsync` 下载。

**Download sequence and annotation data:**

- [Using rsync](https://genome-asia.ucsc.edu/goldenPath/help/ftp.html) (recommended)
- [Using FTP](ftp://hgdownload.soe.ucsc.edu/goldenPath/mm10/)
- [Using HTTP](http://hgdownload.soe.ucsc.edu/downloads.html#mouse)
- [Data use conditions and restrictions](https://genome-asia.ucsc.edu/goldenPath/credits.html#mouse_credits)
- [Acknowledgments](https://genome-asia.ucsc.edu/goldenPath/credits.html#mouse_credits)

然后我们进入到 UCSC 对应的小鼠 mm10 相关数据下载链接 [ftp://hgdownload.soe.ucsc.edu/goldenPath/mm10/bigZips/](ftp://hgdownload.soe.ucsc.edu/goldenPath/mm10/bigZips/) 中，下载 .fa 基因组序列文件。

```bash
# wget 下载
wget ftp://hgdownload.soe.ucsc.edu/goldenPath/mm10/bigZips/mm10.fa.gz

# rsync 下载，这个真的快，高达 10 M/s
rsync -avzP rsync://hgdownload.soe.ucsc.edu/goldenPath/mm10/bigZips/mm10.fa.gz .
```

下载完成后，我们可以看到其中包含的信息是很杂乱的，所以我建议下载各条染色体序列，然后合并成一个

```bash
> grep '>' mm10.fa 
>chr1
>chr10
>chr11
>chr12
>chr13
>chr14
>chr15
>chr16
>chr17
>chr18
>chr19
>chr1_GL456210_random
>chr1_GL456211_random
>chr1_GL456212_random
>chr1_GL456213_random
>chr1_GL456221_random
>chr2
>chr3
>chr4
>chr4_GL456216_random
>chr4_JH584292_random
>chr4_GL456350_random
>chr4_JH584293_random
>chr4_JH584294_random
>chr4_JH584295_random
>chr5
>chr5_JH584296_random
>chr5_JH584297_random
>chr5_JH584298_random
>chr5_GL456354_random
>chr5_JH584299_random
>chr6
>chr7
>chr7_GL456219_random
>chr8
>chr9
>chrM
>chrX
>chrX_GL456233_random
>chrY
>chrY_JH584300_random
>chrY_JH584301_random
>chrY_JH584302_random
>chrY_JH584303_random
>chrUn_GL456239
>chrUn_GL456367
>chrUn_GL456378
>chrUn_GL456381
>chrUn_GL456382
>chrUn_GL456383
>chrUn_GL456385
>chrUn_GL456390
>chrUn_GL456392
>chrUn_GL456393
>chrUn_GL456394
>chrUn_GL456359
>chrUn_GL456360
>chrUn_GL456396
>chrUn_GL456372
>chrUn_GL456387
>chrUn_GL456389
>chrUn_GL456370
>chrUn_GL456379
>chrUn_GL456366
>chrUn_GL456368
>chrUn_JH584304
```

```bash
# 分别下载各个染色体序列，然后选取合并
rsync -avzP rsync://hgdownload.cse.ucsc.edu/goldenPath/mm10/bigZips/chromFa.tar.gz .
gzip -d chromFa.tar.gz
tar -xvf chromFa.tar
# 只保留常用的染色体（ chr1-19,X,Y,M ）
rm chromFa.tar ./*random* ./chrUn*

# merge_fa.sh 写入以下内容
list_str=" "
for index in {1..19} X Y M
do
    list_str=${list_str}" "chr${index}.fa
done

cat $list_str > mm10_genome.fa
rm -rf chr*

```

- bowtie2-build 对基因组序列建立索引

```bash
bowtie2-build --threads 15 mm10_genome.fa ./mm10
```

- 建立完索引后我会看到了以下几个以 bt2 结尾的文件

```bash
mm10.1.bt2  mm10.2.bt2  mm10.3.bt2  mm10.4.bt2  mm10.rev.1.bt2  mm10.rev.2.bt2
```

- 回比 `04_align.sh` 

```bash
cd ~/qliu/ChIP-seq

for i in `ls clean_data/*gz`
do
sample=$(basename $i | sed 's/_clean.fastq.gz//g')
bowtie2 -x ../index/mm10_ucsc/mm10 -p 10 -U $i \
  | samtools view -h -@ 10 -bS -q 30 | samtools sort -@ 10 > align/${sample}.bam
done

nohup bash 04_align.sh &
```

```
-x：后面根之前 bowtie2-build 建立的索引的路径，mm10 为建立索引时的前缀
-p：表示使用多少线程
-U：表示单端
如果是双端数据则为：-1 fq1 -2 fq2
默认是 --end-to-end 全局比对模式；--local 表示局部比对
一般默认参数即可。
简要介绍以下上面的命令就是：bowtie2 比对默认输出 SAM 文件 → samtools 对 SAM 文件排序，过滤低质量的 reads，保留 uniq 的 reads，输出 BAM 文件 → 然后再对 BAM 文件进行排序。
```

#### end-to-end 与 --local 的区别

![end-to-end 与 local比对的区别](./image_ChIPSeq/local vs global alignment.jpg)

顾名思义全局比对就是头对头尾对尾，不对 reads 进行任何修剪，而局部比对，则会对 reads 进行 soft-clip 切除尾部或者头部来最大化比对分数，分值越高，即越相似。

不推荐对 ChIP-seq 数据使用局部比对模式进行比对，即用默认的全局比对 end-to-end 即可。

## 寻找富集的区域

寻找富集的区域也就是我们常说的`Peak calling`，这一步是 ChIP-seq 分析流程中的核心步骤，因为它能鉴定全基因组上被 `转录因子（TF）` 和 `组蛋白修饰` 结合的区域。本章介绍了不同类型的 `ChIP-seq` 信号以及这些信号如何影响 `Peak` 的识别。描述了大多数 `Peak callers` 通常的算法，介绍了一些现有的工具以及各自的特性。最后，提供了 `TF` 和 `组蛋白修饰` 类型的 ChIP-seq 数据 `Peak calling` 的示例代码

### ChIP-seq 信号类型

ChIP-seq 实验的目的是为了鉴定全基因组研究人员感兴趣的 `TF` 和 `组蛋白修饰` 的结合区域。这些结合位点显示高度的 reads 富集，即 `Peak`。正如 章节 1 和 章节 5 所介绍的，ChIP 样本的高通量测序是从两端随机进行的，并且不覆盖富集的 DNA 片段的完整长度。因此，正向和反向链的比对 reads 形成特征的双峰分布（ 图 6.1 ）。在待定所研究的蛋白质的类型上，ChIP-seq 信号的形状，因此也就是 `Peak callling` 算法有不同。

- 转录因子的 `sharp` 信号

**转录因子（TF）** 通常识别特定的 DNA 序列 `motifs`。因此，富集的 DNA 片段集中在 `motif` 周围，导致锐利的“尖峰”富集区（ 图 6.1A ）。`TFs` 显示同型结合的特征是紧密相邻的多个结合位点的簇，这些结合位点将表现为合并两个或更多个特定峰的更宽区域。

- 组蛋白修饰的 `Broad` 信号

**组蛋白修饰**通常跨好几个核小体，即不是特定定位在 DNA 序列上，而是取决于相邻 TF 的位置。因此，覆盖同一区域的 DNA 片段对应于几个松散定位于 DNA 上的核小体。结果，ChIP-seq 信号表现为可以达到几千个碱基的宽度的富集区（ 图 6.1B ）。

- RNA 聚合酶 II 的 `Mixed` 信号

**RNA聚合酶 II （ POLII ）**的定位被用作基因转录的标志。在某些情况下，`Pol II` 在基因启动子处暂停，表明调控转录起始水平。因此，ChIP-seq 信号可以表现为启动子处的 `Sharp` 信号（ 对应于起始或暂停 ）和基因 `Body` 内的 `braod` 信号（ 对应于转录延伸 ）的混合信号（ 图 6.1C ）。

### 通常的 `Peak calling` 算法

许多 `Peak caller` 遵循相同的框架，该框架沿着基因组滑动窗口，计算 ChIP 样本相对于 `Input` 样本中的 reads 的富集程度，并定义针对多次测试校正的显著性打分。

由于 `ChIP-seq` 实验流程包括大小选择步骤，DNA片段具有紧密的大小分布，通常在 **200bp** 左右，这表示数据的分辨率。然后，通过计算基因组中最富集区域内正向和反向链分布之间的距离，可以估计由单端测序产生的 reads 的原始片段大小（ 图 6.1 ）。当应用双端测序并且可以从 reads 重构片段时，使用平均片段大小。

> 图 6.1 不同类型的研究蛋白的 ChIP-seq 信号特性，实验设计、reads 密度、片段密度和 Peak 区域类型
>
> （ A ）转录因子的 `sharp` 信号
>
> （ B ）组蛋白修饰的 `Broad` 信号
>
> （ C ）RNA 聚合酶 II 的 `Mixed` 信号
>

![img](./image_ChIPSeq/chip_diff_type_signal.png)

>
> 注意：并不是所有的组蛋白修饰类型都是 宽峰的。
>
> 图片来源 [ENCODE Target-specific Standards](https://www.encodeproject.org/chip-seq/histone/)
>

![img](./image_ChIPSeq/peak_type.png)

>
> 建议深入阅读 ENCODE 分析：
>
> [Histone ChIP-seq Data Standards and Processing Pipeline](https://www.encodeproject.org/chip-seq/histone/)
>
> [Transcription Factor ChIP-seq Data Standards and Processing Pipeline](https://www.encodeproject.org/chip-seq/transcription_factor/)


#### reads 的富集

使用通常对应于估计片段大小的 `两倍` 的滑动窗口扫描基因组。对于每个窗口，对于 ChIP 和 Input 样本的 reads 都通过文库中的比对上的 reads 总数来进行均一化。然后使用这些数目来计算富集倍数。

#### 显著性
然后，可以使用泊松或负二项分布将均一化的 reads 数与来自零假设的背景模型进行比较，以计算显著性或 `P` 值。许多不同的模型已经被应用于 ChIP-seq 数据，以及完全不同的方法，例如机器学习，但是简单的模型已经被证明具有同样好的性能（ ref1 ）。

#### 多重检验校正
当多次应用统计检验时，即对于被检验的数千个基因组窗口，一些 `P` 值将只是偶然地通过阈值。因此，重要的是根据检验运行的次数来校正它们，即多重检验是正确的（ ref1 ）。这可以通过 `FDR（ false discovery rate ）` 来实现。如果提供了 `Input` 样本，则可以通过交换 ChIP 和 Input 样本以 `call` Input 中的 `Peak` 来计算经验 `FDR` 值。然后，通过 `Input` 样本中高于该分数的峰值总数除以 ChIP 样本中的数目，为 ChIP 样本中的每个峰值分数计算 FDR。`FDR` 或 `q-value` 也可以通过置换或随机抽样（ 例如使用 `Benjamini-Hochberg` ）从模型中估计出来（ ref2 ）。

#### 阈值的选择

通过不同 `Peak caller` 方法找到的 `Peak` 数量高度依赖于所使用的阈值和参数，因此应谨慎考虑。最重要的是将分析集中在一个等级的列表上。`Peak` 应根据评分或适合于评估 reads 富集程度的 `q-value` 等指标进行排序。普遍接受的 `p/q值` 阈值 `0.05` 不能很好地适用于对其进行检验的数千个区域的基因组数据，并且最小阈值 `10^-5` 至 `10^-30` 更适合 `ChIP-seq peaks`。富集倍数相对于 `Input` 样本中的信号不是对 `Peak` 进行排序的好方法（ (例如，相同的 2 倍富集可以来自 `2/1` 或 `10/5`，其中 ChIP 样品中的绝对计数，因此在第二部分中峰高是 5 倍 ）。然而，它可以用于设置最小阈值，2 倍被普遍接受，但是 5 倍更适合 `ChIP-seq Peak`（ `ref2` ）。同样，它仍然可以用于设置最小阈值，`5%` 是普遍接受的阈值，但 `1%` 更适合 `ChIP-seq Peaks`。更重要的是，选择阈值的困难可以通过在重复样本内或跨不同条件彼此比较 ChIP-seq 样本来克服，这将在第 8 章中讨论。

### 现有工具和注意事项

ChIP-seq 于2007年推出，随后几年开发了许多 `Peak caller` 工具（ `ref3` ）。包括迄今为止最流行的 `MACS` （ `ref4` ）以及在 **ENCODE** 流程（ `ref1` ）中的 `SPP` （ `ref5` ）。然而，那些 `Peak caller` 是在第一个 ChIP-seq 数据集上开发的，并且并不总是很好地适应当前的 ChIP-seq 数据集，这些数据集利用了最近的方法学改进，例如双末端测序，高测序深度，最重要的是，增加了实验分辨率。

#### 单末端与双末端文库

在 ChIP-seq 实验中，由于片段大小可以从单端数据中估计出来，因此使用双端比单端数据仅略微提高了寻找 `Peaks` 的性能（ `ref6` ）。大多数 ChIP-seq 数据集都是使用单端文库生成的，并且一些 `Peak caller` 不适用于双端数据。在比较双末端与单末端数据集时，双末端也可以被视为单末端输入（仅使用两个集合中的一个）。

#### 测序深度和文库复杂度

生成的第一个 ChIP-seq 数据集具有大约 2 - 5M （ M = Million = 1e6 ）条测序 reads （ `ref7` ），而最近的有大约 20 到 50M 的 reads，这导致十年来测序深度增加了10倍。良好的测序深度对于能够识别样品中所有真正的结合位点是至关重要的，并且可以通过执行饱和度分析来评估（ 见 `章节 6.6` ）。然而，由于到相同位置的 reads 比对也可以由 PCR 扩增人工产物产生，所以比对的 reads 总数不一定反映文库的复杂性（ 见 `章节 4` ）。因此，一些 `Peak caller` 在计算 reads 富集之前有去除重复的步骤。虽然这一策略对于其中重复主要是 PCR 人工产物的具有几百万条 reads 的数据集是有效的，但如今，高测序深度意味着比对到相同位置的更多 reads 实际上可能来自真正不同的DNA片段（ `ref6` ）（ **这里再一次表明作者觉得 ChIP-seq 分析不应该去重复** ）。因此，如果 ChIP-seq 文库具有良好的质量并且显示出高复杂性，我们不建议删除重复的 reads 再进行 `Peak calling` 。一些 `Peak caller` （ 例如：MACS2 ）现在可以基于使用测序深度和比对的基因组大小对真实重复项的估计来删除一小部分重复 reads 。

### 新一代的 Peak caller

最近开发的方法确实考虑了上面讨论的一些细节。MACS 的升级版 `MACS2` ，既能鉴定 `Broad Peaks` 又能鉴定 `Sharp Peaks` （ 示例代码见`章节 6.5` ）。**Peakzilla**（ `ref12` ）是专门开发用于在高分辨率下从转录因子 ChIP-seq 数据中鉴定 `Peak`（ 示例代码见`章节 6.4` ）。**HOMER** （ `ref13` ）, 最初设计为在 `Peak` 区域重新识别 `motif` 的工具（ 示例代码见 `章节 9` ）。也有其他类型的工具，如 **findPeaks**，用于鉴定不同类型的 ChIP-seq 的 `Peak` 。**JAMM**（ `ref14` ）使用重复的样本来提高 `Peak` 宽度的分辨率和精度。**GEM**（ `ref15` ）通过包括关于 `TF motif` 的信息作为附加输入来识别高分辨率的 `Peak` ，然而，我们更喜欢使用 `Motif` 信息来验证 `Peak`，而不是在识别步骤。已经专门开发了其他方法来比较不同的样本，在 **章节 8** 将对此进行讨论。

### Postprocessing

可以 `Post-processing` 处理步骤来去除在 `Peak calling` 过程中不能过滤的人为造成的 `Peak`。这样的 `Peak` 出现在基因组 `blacklisted` 区域中，这些区域在任何 `ChIP-seq` 数据集（ ChIP 和 Input ）中显示非常高的 reads 丰度，通常位于着丝粒和端粒，并已被 `ENCODE` 定义为几个物种（  见`章节 2.2.2` ）。我们还选择去除位于线粒体染色体（ **chrM** ）上的 `Peak`。

### `Peakzilla`：转录因子类型数据

**Peakzilla** 专为 `Sharp` 的 TF ChIP-seq 数据而设计，以便在高分辨率下 `call peak`，即解析由 **TF homotypic** 结合产生的紧密间隔的 `Peak summits`。**Peakzilla** 可以使用于没有对照 `control` 的 `ChIP-exo` 数据。简而言之，它使用来自高度富集区域的正向和反向 reads 的双重分布来估计片段大小。然后，它使用滑动窗口直接扫描沿基因组的 reads 的双重分布来对区域进行评分。为此，它首先计算 ChIP 样本中的 reads 数减去 control 样本中的 reads 数（ **通过文库中比对的 reads  总数进行归一化** ）。此方法允许比变化倍数更改更好的排序。然后，它用 `p-value` 对这个原始分数进行加权，`p-value` 值检查数据与预期的正向和反向 reads 的双高斯分布的匹配程度。这允许在不去除重复 reads 的情况下用 PCR 人工产物过滤掉位置，以及更好地识别准确的 `Peak summits` 位置。最后，通过交换 ChIP 和 control 样本计算经验 FDR，计算每个区域的富集倍数，并通过多重检验进行校正。默认情况下，它返回最小得分为 1 的峰值和 2 的富集倍数。唯一需要的输入是两个 ChIP 和 control 文件。

### `MACS2`：组蛋白修饰类型数据

`MACS` 是最早用来鉴定 ChIP-seq 数据的 `Peaks` 软件之一，并且仍然是最受欢迎的一种。最初，它被开发用来识别 `sharp` 的 `Peak`，但定义的 `Peak` 相对较宽。最新版本 `MACS2` 现在两者都可以鉴定。简而言之，它首先删除所有重复的 reads 。然后，使用来自高度富集区域的正向和反向 reads 的双重分布来估计片段大小。它将所有reads 扩展到估计的片段大小，并将 ChIP 和 Input 样本扩展到相同的测序深度，即根据样品间的测序深度来进行矫正（Normalization）。然后，它使用滑动窗口扫描沿基因组的片段分布，对区域进行评分。为此，它将 ChIP 中的富集程度与对照样本进行比较，并使用局部泊松分布计算显著性得分。最后，它使用 **Benjamini-Hochberg** 过程对多重检验进行校正。默认情况下，它返回最小 `q-value` 得分为 0.05 的 `Peak`。输入参数包括 ChIP 和 Input 文件的路径、文件格式、基因组大小、输出目录和样本名称。`--broad` 是用来鉴定 `broad peaks`。

虽然目前已经出现了非常多的寻找peak的软件，但是MACS2仍然是最为常用的一个。

### 饱和度分析

为了检查样品的测序深度是否足以识别大多数结合区域，建议进行饱和分析。它涉及对 reads 的数量进行随机二次取样，并计算使用这些子集识别的峰值数量。然后根据使用的 reads 数绘制峰值数量。如果峰的数量显示饱和并达到一个平台，那么样品的测序足够深。**NRF1** ChIP-seq 样本在 `2000万 reads` 时显示饱和（ 图 6.2 ）。


## ChIP-Seq数据的比较分析

ChIP-seq 数据的比较分析对于在重复实验之间或在不同的生理条件下比较感兴趣的蛋白质的结合是必不可少的。此章节将介绍通过 `Peaks` 之间取交集来快速比较和如何使用基于 `Peak`  reads 密度的定量的方法来研究差异结合。

### Peak 区域的交集
比较样本间 `Peak` 的一种简单的方法是简单的取交集。这导致了在两个样品中是否发现峰的 `binary view` ，提供了对不同样品之间的 `Peak` 区域的相似性的粗略估计。然而，这种方法本质上低估了相似性，因为 `Peak calling` 依赖于应用于区域排序列表上的置信阈值（  见`章节 6` ）。因此，一个样品中超过阈值的 `Peak` 在第二个样品中可能刚好低于阈值，即使它显示出相当的富集（ `ref1` ）。另一种选择是将来自第一个样本的高置信度 `Peaks` 与第二个样本中用较低置信阈值识别的所有 `Peak` 取交集（ `ref1/ ref2` ）。虽然在较小的程度上，`Peak` 的简单取交集也低估了样品之间的差异，因为即使两个样品中的一个 `Peak` 高于阈值，它仍然可以显示出非常不同的富集。

重复样本数不同，使用默认 `Peak` 阈值标识的 `Peak` 数量不同（ 7167 Vs 10232 ）。因此，分析是不对称的：`WT_1` 中 98% 的 `Peak` 与 WT_2 重合，但 WT_2 中只有 67% 的 `Peak` 与 WT_1 重合。然而，如果考虑到附加的富集区，WT_2 中的附加 `Peak` 可能已经很好地存在于 WT_1 中。当样品未饱和时，更深的测序也会增加重复交集数目。`Peak` 区域长度的差异会进一步扭曲结果，特别是如果接受任何重叠，比如 1bp 。

> 注：由于这些偏差，通常在 Venn 图中显示的峰重叠可能具有误导性，因为不重叠的峰不应被解释为特定于样品的峰。

尽管存在这些限制，我们可以在本示例中得出结论，WT 和 TKO 细胞中 NRF1 的两个重复实验似乎共享它们的大部分 `Peak` 区域。正如预期的那样，我们观察到 WT 和 TKO 之间重叠的峰值较少。然而，仍然有很大的重叠（ WT 76% 或者 TKO 45% )，这表明许多峰值是在不同条件之间共享的。

所有成对比较的结果热图允许我们检查哪些样本比其他样本更相似（ 图 8.1A ）。正如预期的那样，样本按条件进行聚类。此外，WT  `Peak` 似乎更经常与 TKO `Peak` 共享，而反之亦然，尽管这可能是由于 TKO 样本中的较高峰数而造成的伪像。

### Irreproducible Discovery Rate (IDR)

如上所述，ChIP-seq 分析中的每一个比较都强烈依赖于在 `Peak calling` 步骤中选择的阈值。因此，**ENCODE** 开发了不可复制的发现率（ `IDR` ），作为一种基于它们在重复之间的可重复性来识别真正 `Peak` 的标准（ `ref3` ）。其基本思想是，使用线性阈值生成的 `Peak list` 将包含真正的 `Peak` 和 `noise`。当列表中的 `Peak` 被排序时，例如在它们的富集倍数或显著性上，对于真正的 `Peak`，这些排序将很好地相关，而 `noise` 将显示不相关。IDR 使用统计方法来找到曲线中的点，在该点上，重复 `rank` 之间的关联的 `heterogeneity` 急剧增加。

> 注意：此方法也可用于来自不同 `Peak callers` 生成的相同样本的 `Peak list` 。在没有重复的情况下，这种方法可以帮助在单个样品中定义可靠的峰。
>
> **注意：IDR 不适用于组蛋白修饰数据，因为宽峰的交集不明确。**

### Peak calling for IDR
只要评分不会产生太多的关联，从而导致排名不明确。**IDR** 可以与任何对 `Peak` 进行排名的 `Peak caller` 的输出一起使用。在这里，我们展示了如何将 IDR 与 `peakzilla` 峰值一起使用。如前所述，为了使 IDR 工作，峰值列表必须同时包含真正的峰值和噪声，因此必须放宽峰值调用参数。

当比较重复时，需要一个统一的 `Peak` 集合作为参考集合。这既可以由 IDR 软件从单独识别的 `Peak` 区域创建，也可以由用户提供。对于后者，在 `Peak calling` 之前合并重复应该有助于识别所有可能的 `Peak` 区域，来自合并样本的 `Peak list` 通常用于 IDR 分析。

### 计算 IDR
下一步是运行 IDR 软件以鉴定可重现的 `Peak`。对于生物学重复，通常的阈值是 0.05，即最后 `list` 中高达 5% 不能被重现出来。技术重复应使用较低的阈值，因为它们的总体可变性较低。

IDR 的概念在很大程度上依赖于有两个好的重复。如果其中一个重复显示质量较差，例如如果 `IP` 不是有效的，IDR 将只记录非常少的可重现峰。对于这种情况，**ENCODE** 开发了一种拯救策略，方法是将两个重复汇集在一起，然后随机地将 reads 分成两个伪重复。这些并不代表真正的生物或实验变异，但用于对来自 DNA片段群体的reads 采样中的随机噪声进行建模。对于伪复制的 IDR 比较，为了降低了噪声，建议使用较低的阈值 （ 0.0025 ）。

### reads 密度的比较
在 reads 密度的水平上，评估样本之间的总体相似性的最简单的方法是全局地关联它们的 reads 密度。这可以通过计算整个基因组的标准化 reads 密度上的 `Pearson` 相关系数（ `PCC` ）来实现，无论是对于每个单独的碱基对（ `ref3` ），还是在沿着基因组的滑动窗口中。然而，由于 `Peak` 区域仅代表基因组的一小部分， reads 密度的高相关性将主要反映一致的背景信号，如 ChIP 和 Input 样本之间的高相关性所显示的（见 `表1` ）。

> 表1 reads 密度的 `Pearson` 相关系数（ PCC ）

| Sample1        | Sample2         | PCC  |
| -------------- | --------------- | ---- |
| NRF1_CHIP_WT_1 | NRF1_CHIP_WT_2  | 0.98 |
| NRF1_CHIP_WT_1 | NRF1_CHIP_TKO_1 | 0.97 |
| NRF1_CHIP_WT-1 | NRF1_INPUT_WT   | 0.96 |

> 沿着基因组的每个碱基对的 reads 密度的PCC（ 不包括两个样本中具有零 reads 的位置 ）。

为了具体比较 `Peak` 区域中的 reads 密度，可以仅在至少一个样本中包含 `Peak` 的区域内计算 `PCC` 值。还可以使用散点图在视觉上比较每个区域的标准化平均 reads 密度。这代表了 `Peak` 区域中信号的更定量比较，而不是 **8.1节** 中解释的重叠 `Peak` 区域的二元方法。

### 合并 `Peak` 区间
为了聚焦于包含高信号并且可能在不同样本之间存在差异的基因组窗口，我们在 `Peak` 区域内执行 reads 密度的比较。为此，我们将来自所有实验的 `Peak` 区域合并（ 可以针对所有可能的成对比较单独执行 ）。尽管这也依赖于 `Peak caller` 阈值，但它允许对所有 `Peak` 进行定量比较，包括仅存在于一个样本中的那些。

我们将合并区域与原始 reads 重叠，以计算每个样本中落入其中的 reads 数。这些原始 reads 数将直接用作下一节中识别差异 `Peak` 区域的输入。

由于 Peak 区域具有不同的大小，并且样本包含不同数量的比对 reads ，因此将每个 reads 计数标准化为该区域的大小和样本中比对 reads 的总数，以获得 `RPKM` 值（ reads per kilobase per million）。

我们现在可以可视化散点图中跨样本的 `Peak` 区域中的标准化 reads 数，并计算相关的 PCC 值。散点图为探索数据和得出结论提供了一种不带偏见的方式。为了更好地可视化数据的分布，RPKM 值以 log2 标准化。为了确认 WT 和 TKO 细胞之间 NRF1 结合的变化是可重复的，我们比较了重复之间的 TKO 和 WT 变化倍数。为此，我们向所有数据点添加一个伪计数（ 这里是0.1 ），以避免被0除，并以 log2 标准化，以获得以 0 为中心的正态分布。

我们观察到，WT 和 TKO 的重复样本的 reads 密度沿对角线排列，并且相关性很好（ PCC > 0.9 ）（ 图8.1 C ）。当比较 WT 和 TKO 样本时，reads 密度仍然相关，但小于重复之间的相关性（ PCC = 0.74 或 0.81 ）（图8.1D）。

此外，我们发现在 WT 样品中识别的所有峰在两种条件下都显示出相似的 reads 密度，因为 WT 样品中具有高 reads 密度的所有区域在 TKO 样品中也具有高 reads 密度并沿对角线排列（ 图8.1 D ）。相反，在 TKO 样本中识别的许多峰具有低 reads 数或不存在于 WT 样本中，通过图左上部分的数据点群体可视化。

> 注意：在曲线图的左下部分有很少或没有具有低 reads 数密度的点，这是由于我们只选择了在至少一个样本中被称为 `Peak` 的区域，因此显示了 reads 计数的最小富集。在图 8.1 C 中，对于 TKO 重复样品，左下角的点表示在 WT 样品中识别但在 TKO 样品中具有背景 reads 密度的峰。如果从成对比较中合并 `Peak` 区域，则它们不会出现。

由于两个重复都显示了在 TKO 样本中获得的 `Peak`，因此检查重复 1和重复 2中的这些 `Peak` 是否相同是很有趣的。这是通过比较 `delta-delta` 曲线图中的变化倍数来确认的，这表明在 WT 和 TKO 之间观察到的 reads 密度变化在两个重复之间高度一致（ PCC = 0.67 ）（`图 8.1 E`）。

### 差异结合分析
一旦散点图确认样品间存在差异 `Peak` ，统计方法可以定义共享 `Peak` 或差异 `Peak` 的组，用于进一步分析。差异结合分析主要有两种类型的工具（ `ref4` ）。第一种类型采用基于  reads 计数数据的定量方法来比较一种条件下的结合强度与另一种条件下的结合强度。第二种类型使用**隐马尔可夫模型**将基因组分割成`丢失、不变或获得`的区域。然而，这些工具不允许在这三种截然不同的状态之外进行定量描述。在这里，我们介绍了使用 `DESeq2` 和 `DiffBind` 进行定量分析的典型分析流程，`DiffBind` 为 ChIP-seq 分析提供了专门围绕 `DESeq2` 的封装。

在以下部分中，如果显示条件之间差异结合的 `Peak` 区域分别在 WT或 TKO 细胞中显示更多的 NRF1 结合，则它们被称为 “WT-specific ” 或 “ TKO-specific ”。相反，显示条件之间的结合（ 在任一方向上 ）变化小于2倍的 `Peak` 被称为 “shared Peaks” 。

#### 使用DESeq2进行分析
具有差异富集的 `Peak` 区域的鉴定在概念上类似于差异表达基因的鉴定，因为两者都依赖于 reads 数的比较。这使我们能够采用最初为 `RNA-seq` 数据分析而设计的成熟的统计方法，例如 `R/Bioconductor` 软件包 `DESeq2` （ `ref5` ）和 `edgeR`（ `ref6` ）。DESeq2 使用基于负二项的广义线性模型来检验零假设，即两个条件之间 reads 数的 `log2FC` 等于零。它可以分解为四个主要步骤（ 包含在 DESeq() 函数中）：

这个软件的统计学原理，我们在这个部分不再过多的介绍。在大多数peak不发生变化的情况下，DESeq2或者edgeR等RNA-Seq常用的差异表达分析软件都可以用来分析ChIP-Seq的差异peak信息。

#### Diffbind
**DiffBind** 是一个封装工具，它将 `R/Bioconductor` 软件包 DESeq、`DESeq2` 或 `edgeR` 应用于 ChIP-seq 数据（ 默认：DESeq2 ）。它提供了一个简单的流程，并在几个步骤中进行数据可视化，这允许检测重复一致性和条件之间的总体差异。它需要一个类似于 `ChIPQC` 的样本表 （ 参见附件中的 `NRF1_Sample_Sheet.csv` ），该样本表以 `data.frame` 或 `CSV` 格式总结有关样本所需的信息。

导入数据后，通过生成显示成对欧几里德距离的热图以及由此产生的样品的层次聚类，可以基于 `Peak` 位置检查样品的总体相似性（ 类似于 `8.1 节`中生成的热图 ）。

**DiffBind** 中的下一步定义将用于比较的一致 `Peak` 值集。函数 `dba.count()` 中的 `minOverlapp` 参数设置了 `Peak` 必须出现在给定数量的样本中才能包含到一致集合中的要求（ 默认值：2 ）。使用一致 `Peak` 集合处的富集（ 输入标准化 reads数 ）值重复成对距离的热图可视化通常将改善按样本类型的聚类。`minOverlay` 可以降低到 1，以包括所有 `Peak` ，这可能会增加噪音，但会减少假阴性。函数 `dba.contrast()` 的作用是：定义使用样本表中的哪一列进行比较。通过在 `block` 参数中指定混杂参数的列，可以考虑实验设置中的混杂参数。`minMembers` 参数设置每个比较组中所需的最小唯一样本数（ 默认：2 ）。运行差异结合分析的最后一个函数是 `dba.Analyze()` 。这里需要考虑的一个重要参数是 `bFullLibrarySize`，它决定是否将整个文库的大小用于标准化（ 默认值：TRUE ）。这对于预期全局变化的比较是可取的。相反，仅考虑峰值区域内的 reads 数（ `bFullLibrarySize = false` ）适用于预期不到一半的峰值将发生变化的比较。

> 注意：全局变化可能需要使用 `spike-in` 进行标准化（ `ref7 / ref8` ）。

**DiffBind** 可以使用函数 `dba.report()` 导出差异 `Peak` 并可视化结果。

从 **DiffBind** 获得的差异 `Peak` 上的 PCA 图 再次表明 WT 和 TKO 样品在重复之间紧密聚类，并且在条件之间很好地分离。`MA` 图显示了分析中每个 `Peak` 的 log2 转换的富集倍数变化与 log2 转换的平均富集（ `图 8.2 C` ）。在 FDR < 5% 的默认阈值下，DiffBind 鉴定到了 6946 个差异结合 `Peak` ；其中大多数在 TKO 细胞中表现出更强的结合。请注意，这个阈值比我们在第 `8.4.1` 节中的 DESeq2 分析中的阈值更宽松，反映在鉴定到更多数量的差异 `Peak` 。箱式图显示了与那些在 WT 细胞中显示明显的更多 （ + ）或更少（ - ）结合的 `Peak` 相比， log2 转化的富集在所有 `Peak` 中的分布（ `图 8.2 D` ）。在 NRF1 数据中，我们观察到所有 `Peak` 的 reads 密度都有很大的变化，表明全库大小标准化更适合于此数据集。最后，可以使用热图对每个差异 `Peak` 的每个重复的标准化富集进行可视化和聚类（  `图 8.2E` ）。这再次证实，大多数 `Peak` 在 TKO 中显示出更高的富集，并且重复之间具有相似的水平，因此聚在一起。

## 下游分析
本节介绍如何注释已鉴定的 `Peak` 的基因组序列，并注释到基因，然后对其进行功能特征分析。它还提出了解决所研究蛋白质的 DNA 序列特异性的初步步骤，并对如何将 ChIP-seq 与其他功能基因组学数据集成进行了展望。

### 结合基因组位置的序列特征

**转录因子 （ TF ）**结合位点的基因组 context 可以告知其在细胞中的潜在功能。ChIP-seq  Peak 的基因组分布可以在不同的间隔尺寸水平上进行评估，从全局对染色质类型（ 颜色 ）的分类到单个基因中的特定区域。

在大多数情况下，第一步是检查 ChIP-seq Peak 相对于注释基因的位置。然而，同样的方法也可以应用于其他基因组特征，例如重复区域，CpG 岛或增强子区域。

基因可分为编码蛋白基因、假基因和非编码 RNAs （ 称为基因生物型 ）。注释包括转录区域，但不包括前面的启动子，启动子通常被定义为转录起始位点（ TSS ）上游的 2kb 。基因本身分为内含子和外显子，如果是蛋白质编码基因，则进一步分为 5‘UTR、CDS 和 3’UTR 。基因组的其余部分被称为基因间区。

基因注释（ GTF 格式 ）可从 [**Ensembl**](http://asia.ensembl.org/index.html)、[**UCSC**](http://genome.ucsc.edu/) 或 [**NCBI**](https://www.ncbi.nlm.nih.gov/) 以及物种特定资源数据库（例如：[flybase](http://flybase.org/) 、[arabidopsis](https://www.arabidopsis.org/) ）。根据来源的不同，注释文件在布局和信息内容方面可能会有所不同。例如，**NCBI RefSeq** 注释仅包括一组简明的手动整理的转录本，而 **Ensembl** 报告了潜在的异构体的图谱，包括自动注释的转录本，而没有实验支持。**UCSC KnownGenes** 是另一个广泛使用的注释源，具有相当数量的转录本。对 `长非编码 RNA` （ `LncRNA` ）基因最全面的分析可以从 **PTANTOM** 项目中获得（ [**FANTOM**](http://fantom.gsc.riken.jp/) ）（ `ref1` ）。

基因组特征也可以通过 `R/Bioconductor` 注释包检索（ 详情见 [annotation](http://bioconductor.org/packages/devel/workflows/html/annotation.html) ）。 我们在 R 中提供替代代码，用于在脚本中进行基因组位置分析，见附加在线文件。

基因注释可能很难处理，因为许多特征是重叠的。这发生在基因水平上，每个基因的多个转录异构体进一步扩增。重叠注释可以通过基于关于蛋白质功能的先验假设来定义符号的层次结构来解决（ 例如：**`exon > 5' UTR > 3' UTR > intron > promoter > intergenic`** ）或通过使用其他类别（ 例如：ambiguous ）。当使用层次结构时，需要注意确保相关分布不是由于强加的层次结构，而是反映了明确分配的 `Peak` 的分布。

重叠注释的问题由于 ChIP-seq  Peak 可能非常宽而进一步恶化。解决这个问题的一种方法是只使用 TF Peak。对于较宽的区域，例如组蛋白修饰，可以考虑重叠的程度，使得例如需要 `>50%` 的 Peak 区域位于给定特征内。或者，可以通过与每个注释的重叠部分将区域指定给多个特征。以下代码显示了如何将 NRF1 和 H3K27ac Peak 分配给不同基因组特征的示例。它使用基于编码蛋白基因的 `Ensembl` 注释的小鼠基因组预处理文件（ mm10）（ 作为附加在线文件提供 ）。

### 距离基因的距离
TF 结合位点可以发生在启动子区域内（ TSS 的近端 ）或基因间区位置（TSS的远端 ）。为了区分位于 TSS 近端或远端的 Peak ，检查每个 Peak 与最近的 TSS 的距离，而与特定的目标基因分配无关。由于许多 TF 既结合近端点又结合远端点，因此到 TSS 的距离通常呈双模态分布（ `图 9.1C` ）。对于也可以具有位置偏好的组蛋白修饰，预期有不同的模型。例如，H3K27me3 修饰几乎只发生在启动子区，而 H3K4me3 修饰和 H3K4me1 修饰之间的平衡允许区分启动子和增强子区域（ `ref2` ）。

下面的代码计算每个 Peak 到最接近的 TSS 的距离。它使用基于所有编码蛋白基因转录本的 Ensembl 注释的小鼠基因组预处理文件（ mm10 ）。

### 功能分析

一种流行的下游分析是探索靶基因的功能。

#### 注释到靶基因
Peak 到基因的分配仍然是一项不平凡的任务，因为 TF 和增强子可以从非常长的差异激活它们的目标基因，小鼠中的基因被位于 1Mb 之外的增强子调控（`ref4`）。即使已经探索了几个概念来分配目标基因，最简单和最有效的方法是使用最近的 TSS（ `ref5` ）。理想情况下，重新开发的技术，如 **Capture Hi-C**（ `Chi-C` ) ( `ref6` )，可以用来推断可靠的关联，但数据的可用性和处理仍然是有限的。

#### 基因富集分析
以基因本体论（ **GO** ）的形式在许多物种上都可以获得对基因功能的全面描述（ `ref7` ）。GO被组织成三个不重叠的本体，它们描述蛋白质的生理作用（ 生物学过程：Biological Process ），分子活性（ 分子功能：Molecular Function ）或在细胞内的位置（ 细胞成分：Cellular Component）。此外，分配给蛋白质的每个 GO 术语都与一个 GO 号相关联，指定所分配的功能是例如通过实验验证的，还是仅仅从正交学中推断出来的。

基于GO注释，可以检验一系列基因特定功能的富集。对于每个GO `term`，将列表中与该 `term` 相关联的基因的部分与其总体出现进行比较，以识别明显过度表达的 `term`。显著性通常使用`超几何检验`的 p 值来计算。值得注意的是，GO 富集可能受到 `baseline` 选择的强烈影响，即是否对基因组中的所有基因或一组特定的 `control` 基因（ 即背景文件 ）进行富集检验。`通常应用的` control `集都是表达基因（ 例如根据 RNA-seq 数据 ）或具有共享的和差异的 ChIP-seq Peak 的基因`。用于 GO 分析的流行在线工具包括 **David** 以及用于可视化结果的 **REViGO**。

> 注意：与用于 `Peak calling` 的阈值选择类似（ 参见 第6.2.5章 ），应始终根据 p 值而不是变化倍数对富集的类别进行排序和选择。在报告或可视化围棋分析结果时，应避免任意选择GO terms。应提供完整的富集注释信息表作为补充信息。

#### 其它类型的基因富集分析
富集的概念可以扩展到在研究上下文中感兴趣的任何预定义的基因列表。例如，可以对目标基因进行检验以富集发育调节基因或某一蛋白质的相互作用伙伴。可以从已发表或数据库中检索参考文献列表，也可以手动编辑参考文献列表。

另一个流行的功能注释来源是 **KEGG** 数据库，它收集手动整理的生物学途经。最初为酶和代谢过程设计的 KEGG 现在包含了数百张手工绘制的 map，包括人类疾病和药物设计（ `ref8`）。**KEGG Mapper** 工具允许将基因列表映射到通路上，通路图可以根据用户定义的信息进行着色。最后，像 **g：profiler** 这样的工具将广泛的不同功能注释集成到一个联合资源中，以便能够对基因列表进行全面的功能解释。

### 序列分析

分析 `Peak` 区域下的 DNA 序列提供了对所研究蛋白质的 DNA 结合偏好或在相邻位置重复结合的潜在协同因子的洞察。

#### Motif 分析
**De novo motif discovery** motif 分析中的第一个策略是在没有先验假设的情况下搜索富含 Peak 区域的序列，也称为从头 motif 发现。搜索通常在围绕 `TF Peak summits` 或组蛋白修饰的整个区域的 `50-200bp` 的窗口中执行。大多数 Motif 发现工具都遵循基于 `word-based` 或基于 `profile-based` 的方法（ `ref9` ）。在例如在 `DREME`（ `ref10` ）中实现的基于 `word-based` 的方法中，所有可能的 `k-mer`（ 即长度为 k 的序列 ）都被穷举以生成在输入序列中以增加的频率出现的共识基序。相反，基于 `Profile-based` 的方法，如 `MEME`（ `ref10` ），迭代地优化序列比对以获得最佳评分 `motif`。最近，应用**深度学习**方法来发现 ChIP-seq 数据中的结合 `motif`（ `ref11` ）。

`Motifs` 在整个基因组中出现的频率很高。因此，任何富集的基序都应始终对照背景序列进行检验，要么由用户提供，要么由 `randomisation` 生成。这些背景序列的选择可能会强烈影响所发现的 `motif`。

**HOMER** 是一种可以通过命令行运行的流行工具。它将目标区域和背景区域的基因组坐标作为输入，或者生成具有匹配目标区域的 GC 含量的可能性的随机背景区域。**MEME-ChIP** （ `ref12` ）是一个所谓的集成工具，它结合了几种 `Motif` 发现算法。它可以作为在线工具运行，将目标区域和背景区域的 `FASTA` 序列作为输入，或使用随背景字母频率变化的随机控制。

> 注意：Motif 表示为位置权重矩阵（ PWM ），这些矩阵由多序列比对构建而成。PWM 报告 motif 中每个位置的每个核苷酸出现的概率，这可以被可视化为 **`Sequence logo`**。

**HOMER** 输出在目标序列中找到的 Motif 的排序列表（ `图 9.2A` ）。对于每个 motif，它表示序列（以 logo 表示 ）与背景序列相比，靶标中该 motif 的富集相对应的 p 值，以及已知 motif 中该 motif 的最佳匹配。在 NRF1 中，如预期的那样，发现与已知的NRF1 motif 匹配的从头识别的 motif 在 Peak 区域中最富集，大约 64%。

**已知 motif 搜索** motif 分析中的第二个策略是扫描已定义 motif 的Peak 区域，也称为已知 motif 搜索。许多 TF 的 motif 现在已经从体外（ 例如通过指数富集（ **SELEX** ）（ `ref13` ）或蛋白质结合矩阵（ **PBM** ）或体内（ 例如使用 ChIP-seq ) 实验获得，并且可以在公共数据库中获得（例如：**JASPAR** （ `ref14` ） 或者 **HOCOMOCO** （ `ref15` ））。已知基序的 PWMs 可用于扫描感兴趣的基因组区域以识别 motif （ 例如：使用 **MAST**（ `ref15` ） ）。为了选择有意义的 `Motif` 出现，需要应用 p 值阈值，我们建议根据 `motif` 的信息内容进行调整（ 例如： 根据 motif 的长度，相同的阈值将具有不同的严格性）。下面的代码显示了如何在我们的Peak 区域搜索已知的 NRF1 motif。

使用已知的 NRF1 motif 在特定阈值下，我们发现 73% 的 `Peak` 区域含有一个 `motif`。在 TF 的 ChIP-seq 数据中，带有 Motif 的  `Peak` 的比例通常在 `60-80%` 左右。一些非特异性峰可能是由实验偏差引起的，如 `crosslinking artefacts` 。可以将相同的代码调整为在 `Control` 区域上运行（ 使用命令 `shuffledBed` 生成 ）。可替换地，可以使用 `Peak` 的子选择，例如 TKO 特定的 `Peak` 与共享的 `Peak`。最后，可以使用**超几何检验**来统计评估 **targets 区**和 **control 区**的富集程度的比较（例如：使用 R 中的函数 `phyper` ）。同样的分析可以运行更多的 `motif`，甚至所有可能的 `k-mers`。与从头开始的 motif 发现方法相比，使用已知 motif 扫描 `Peak` 区域的优点是，该信息可以用于进一步的分析，例如探索不同 `Motif` 在特定区域中的组织和共生（ 例如，彼此之间的距离或方向 ）。此外，计算 `metaplot` 中的位置富集使我们能够可视化是否以及在何处在 `Peak` 周围富集了 `motif`。

#### 序列保守性

当具有额外物种的多个比对可用时，可以探索 Peak 或 motif 的保守性水平。为此，可以从 UCSC 基因组浏览器以 bigwig 格式下载 **PhastCons** 或 **PhyloP** 等保守性分数，并且可以使用 **bwtool** 或 **bedtools** 进行处理（ 见 `章节 9.4.1`）。

### 结合其他数据分析

基因组研究通常需要几种类型的实验来解决特定的生物学问题。此外，可以公开获得大量相关的基因组数据集。因此，ChIP-seq 数据与其他数据类型的结合分析是一种常见的分析。这种数据集成的一个示例可以在 NRF1 数据集的原始发布中找到。

#### 额外的 ChIP-seq 数据集
第一步通常是与其他 ChIP-seq 数据集集成，这可能包括 TF 和组蛋白修饰的数据组合。

> 注意：为了避免任何偏见和错误解释，强烈建议使用包括数据预处理（ 例如 reads 长度，修整 ）， reads 比对（ 例如索引，用于唯一 reads 的过滤阈值 ）和 `Peak calling` ( 例如算法、Peak 阈值 ）的类似流水线来处理每种类型的数据集（ 或重新处理公共数据）。

可视化和比较 TF 和组蛋白修饰的几个 ChIP-Sseq 数据集的流行方法是生成 Peak 区域中 reads 密度的热图。这种整合应该考虑到识别的 Peak 区域的不同性质：组蛋白修饰的信号通常较宽，并且 Peak 在 TF 信号周围。因此，建议对以特定位置为中心的区域进行比较分析，如 TF Peak summits 或 TSS，而不是合并所有富集区域。下面，我们提供代码为跨样本的 NRF1 共享和差异 Peak 区域生成这样的热图。有几种对用户友好的在线工具可用于根据测序数据生成热图和其他表达图（例如：deeptools2）。

密度热图显示在共享 Peak 和 TKO 特定 Peak 中的 Peak 周围的 reads 密度的分布（`图 9.2C` ）。它也可以从 第 8.3 章 的整个 Peak 列表中生成。

> 注意：重要的是要记住，尽管热图是很好的可视化工具，但它们不是表示数据的具体方式，因为颜色比例的细微变化可能会对人眼产生误导。在这里生成的密度热图的示例中，由于以相对较小的数字显示数千个区域，如果行不会按降序 RPKM 值排序，则具有低  reads 密度的一些区域在具有高 reads 密度的区域之间将不可见。此外，用户很容易以非线性步骤排列颜色标度以突出特定的特征，例如在我们的情况下，我们使用从白色到黑色的线性标度从 0 到10，并注释所有大于10 直到 100到黑色的附加值，因为密度值遵循下降的指数曲线。

#### 表达数据
将 ChIP-seq 与RNA-seq 或芯片数据的基因表达信息结合，允许我们研究 TF 的结合或组蛋白修饰的存在是否与其目标基因的表达相关。为此，可以将 Peak 区域的信号与假定的目标基因的表达水平进行比较。如果有几个条件可用，在所谓的 `delta-delta` 散点图中比较结合和基因表达的变化可能更具信息性（ 见 `章节 8.3.4` ）。请注意，由于可以将几个 Peak 分配给同一基因，因此某些基因表达值可能会多次出现。这可以通过取给定目标基因的所有相关 Peak 的最小、最大或平均信号来解决。

> 注意：这种分析对假阳性目标基因引入的噪音很敏感，当被分配到最接近的 TSS 的基因时。由于远端 Peak 可能比近端 Peak 更经常被错误分配，因此分别对近端和远端 Peak 进行下游分析是有用的（ 例如，≤ 2kb vs > 2kb ）。

#### 其他类型数据
最后，其他类型的基因组数据也可以整合到分析中，例如染色质可及性（ 例如 `DNase-seq` 或 `ATAC-seq` ）或 DNA 甲基化（ 例如 `WGBS-seq` 或 `RRBS-seq`)。这可以通过使用 `bwtool` 或 `bedtools` 在 Peak 区域上汇总信息来执行（ 见 `章节 9.4.1` ）。例如，可以在 Peak 区域上计算信号平均值或在峰值区域的相关子集中进行比较。与基因表达的比较类似，`delta-delta` 散点图可用于将结合的变化与染色质可及性或 DNA 甲基化的变化进行比较。

除了用于靶基因分配，来自高分辨率基于 `Hi-C` 的方法的数据也可以通过比较 ChIP-seq 结合的变化与包含差异 Peak 的基因组区域的相互作用谱的变化来集成。

<!--chapter:end:0060-ChIP_seq.Rmd-->

# 全基因组测序与全外显子组测序 {#whole_genome_sequencing}

## 全基因组测序(WGS)

### 实验设计（待补充）

### 样本量

### 覆盖度估算
假设构建的基因组文库无区域偏好性，测序片段来自于基因组各个区域的概率均等，则我们可以估计特定建库方式下，一定的library size的序列所能覆盖的基因组区域

已知目标基因组的长度为$G$，测序片段长度（read size）为$S$，library size为$N$，则某一条read来自于一个长度为$L$的基因组区段的概率为$\frac{L}{G}$

此时，设随机变量：

$$D=起始于一个长度为L的区段的reads数$$

则D服从二项分布：

$$D \sim Binomial(N,\frac{L}{G}) $$

令$L=S$，则起始于该长度为S的区段的reads，均覆盖该区段的最后一个碱基，即此时D就是该碱基位置的测序深度

我们知道，对于二项分布，当其实验次数$N\to \infty$，概率$P\to 0$时，二项分布近似于泊松分布，在这里，因为$S<<G$，则$P=\frac{S}{G} \to 0$，且$N$非常大，可以用泊松分布近似，即：

$$D \sim Possion(\lambda), 其中\lambda=N\frac{S}{G}$$

因此，我们获得了全基因组各碱基位点的测序深度的概率分布（概率质量分布PMF）估计，如下图（以$\lambda=40$为例）：

<p align='center'><img src=./image_WGS/snp-calling-estimate-depth-distribution.png/></p>

依据测序深度的概率分布，可以很容易推出测序深度大于指定阈值$d$的基因组区域比例：

$$P(D\ge d) = \sum_{i=d,...,\infty}P(D=i)$$

不过实际的基因组测序深度分布与泊松分布并不完全一致，由于GC偏好性等因素的影响，之前推导过程中依据的全基因组来源等概率的假设并不完全成立，从而使实际的分布相对于理论分布，存在明显的overdispersion（即$Var(D) > E(D)$）

![img](./image_WGS/snp-calling-estimate-depth-distribution.png) 

<p align='center'>Bentley et al, Nature, 2008</p>

![img](./image_WGS/snp-calling-possion-overdispersion.png) 

<p align='center'>Shen et al, Nature, 2008</p>

### SNV/SNP的数据前处理

#### 去除PCR重复

##### duplicate产生原因

![img](./image_WGS/GATK4-pipeline-remove-duplicates-reason-of-duplicates.jpg) 

- **PCR duplicates（PCR重复）**

PCR扩增时，同一个DNA片段会产生多个相同的拷贝，第4步测序的时候，这些来源于同！一！个！拷贝的DNA片段会结合到Fellowcell的不同位置上，生成完全相同的测序cluster，然后被测序出来，这些相同的序列就是duplicate

- **Cluster duplicates**

生成测序cluster的时候，某一个cluster中的DNA序列可能搭到旁边的另一个cluster的生成位点上，又再重新长成一个相同的cluster，这也是序列duplicate的另一个来源，这个现象在Illumina HiSeq4000之后的Flowcell中会有这类Cluster duplicates

- **Optical duplicates（光学重复）**

某些cluster在测序的时候，捕获的荧光亮点由于光波的衍射，导致形状出现重影（如同近视散光一样），导致它可能会被当成两个荧光点来处理。这也会被读出为两条完全相同的reads

- **Sister duplicates**

它是文库分子的两条互补链同时都与Flowcell上的引物结合分别形成了各自的cluster被测序，最后产生的这对reads是完全反向互补的。比对到参考基因组时，也分别在正负链的相同位置上，在有些分析中也会被认为是一种duplicates。

##### 用泊松分布解释duplicate问题

求解duplicate rate，相当于是在问这样一个问题：

> 对于已经建好的测序文库，其中有N种序列片段，每条片段长度均为l，每种片段的拷贝数为$k_i(i=1,...,N)$，文库大小（library size）为M，即：
>
> $$M=\sum_{i=1}^{N}k_i$$
>
> 现在，从这个文库M中随机抽取m条序列($m \ll M$)，进行测序
>
> 问：duplicate rate为多少？

先给大家一个结论：

$$duplicate\,rate \approx 1-\frac{\lambda N}{M}$$

其中$\lambda=Ml/G$，当原始文库确定（即测序对象G确定，且片段长度l和总文库大小M确定）时，$\lambda/M$是一个常数，此时$duplicate\,rate \approx 1-kN$，即此时duplicate rate只与原始文库中序列片段的种类数$N$有关，且是负相关

具体的推导过程，请阅读以下部分

解：

下面采用逆向思维来完成这个推导过程

假设，我们可以知道这$m$条序列中总共有$n$种片段，则我们可以很容易地求出目标duplicate rate $d$为：

$$d=1-\frac{n}{m} \tag{1}$$

那么，这个$n$为多少呢？

现在问题变成了：

> 从这个文库$M$中随机抽取$m$条序列($m \ll M$)，理论上我们能抽中多少种片段？

对于原始文库中的任意一种片段$i$，设以下随机变量：

$$
X_i = \left\{ 
  \begin{array}{ll}
    1 & 该片段被至少抽中一次 \\
    0 & 该片段未被抽中
  \end{array}
\right.
$$

注：当随机变量按照以上形式进行设定时，该随机变量的分布函数称为**示性函数**

则总共被抽中的片段种类为：

$$n=\sum_{i=1}^{N}X_i \tag{2}$$

我们需要求出$n$的期望，又

$$E(n)=E(\sum_{i=1}^{N}X_i)=\sum_{i=1}^{N}E(X_i) \tag{3}$$

则我们需要求出其中$E(X_i)$的通式

对于原始文库中的任意一种片段$i$，还可以设以下随机变量：

$$\theta_i=该种片段被抽中的次数$$

则$\theta_i$服从二项分布：$\theta_i \sim Binomial(m, \frac{k_i}{M})$

又由于$\frac{k_i}{M} \to 0$，且$m$也比较大，所以$\theta_i$服从泊松分布，即：$\theta_i \sim Possion(\lambda_i)$，其中$\lambda_i=\frac{m\cdot k_i}{M}$

则

$$
\begin{aligned}
&\quad E(X_i) \\
&= P(X_i=1) \\
&= P(\theta_i\ge 1) \\
&= 1-P(\theta_i=0) \\
&= 1-e^{-\lambda_i} \\
&= 1-e^{-m\cdot k_i/M}
\end{aligned}
\tag{4}
$$

这是我们在已知原始文库中该片段拷贝数$k_i$的情况下，能得出的结果，若我们不知道，则可以知道$k_i \sim Possion(\lambda)$，其中$\lambda=\frac{M\cdot l}{G}$，上式(4)就变成了

$$E(X_i)=E(1-e^{-m\cdot k_i/M})=\sum_{k=0}^{\infty} (1-e^{-m\cdot k_i/M})\cdot p_k \tag{5}$$

而且每种片段被抽中的可能性均满足(5)

所以

$$E(n)=\sum_{i=1}^{N}E(X_i)=N\cdot E(X_i)=N\cdot \sum_{k=0}^{\infty} (1-e^{-m\cdot k_i/M})\cdot p_k \tag{6}$$

所以

$$
\begin{aligned}
&\quad d \\
&=1-\frac{E(n)}{m} \\
&=1-\frac{N}{m}\sum_{k=0}^{\infty} (1-e^{-m\cdot k_i/M})\cdot p_k \\
&=1-\frac{N}{m}\sum_{k=0}^{\infty} (1-e^{-m\cdot k_i/M})\cdot \frac{\lambda^k}{k!}e^{-\lambda} \\
&=1-\frac{N}{m}+\frac{Ne^{-\lambda}}{m}\sum_{k=0}^{\infty} \frac{1}{k!}(\lambda e^{-m/M})^k
\end{aligned}
\tag{7}
$$

上式(7)中的$\sum_{k=0}^{\infty} \frac{1}{k!}(\lambda e^{-m/M})^k$（其中$\lambda e^{-m/M} \to 0$）近似指数函数$e^x$在$(0, f(0))$处的泰勒展开式：

$$e^x=\sum_{n=0}^{\infty} \frac{x^n}{n!} \tag{8}$$

因此，可以得到

$$
\begin{aligned}
&\quad d \\
&=1-\frac{N}{m}+\frac{Ne^{-\lambda}}{m}\sum_{k=0}^{\infty} \frac{1}{k!}(\lambda e^{-m/M})^k \\
&\approx1-\frac{N}{m}+\frac{Ne^{-\lambda}}{m}\cdot e^{\lambda e^{-m/M}} \\
&=1-\frac{N}{m}\left(1-e^{-\lambda}\cdot e^{\lambda e^{-m/M}}\right) \\
&=1-\frac{N}{m}\left(1-e^{\lambda (e^{-m/M}-1)}\right)
\end{aligned}
\tag{9}
$$

由于$m \ll M$，则$-m/M \to 0^-$，且由于$e^x$在$x=0$处的一阶泰勒公式为：$e^x=1+x+o(x)$，则此时$e^{-m/M} \approx 1-m/M$

则(9)可以化简为：

$$
\begin{aligned}
&\quad d \\
&\approx 1-\frac{N}{m}(1-e^{-\lambda m/M}) \\
&\approx 1-\frac{N}{m}[1-(1-\lambda m/M)] \\
&=1-\frac{N}{m}\frac{\lambda m}{M} \\
&=1-\frac{\lambda N}{M}
\end{aligned}
\tag{10}
$$

故，最终得到

$$d\approx 1-\frac{\lambda N}{M}$$

##### PCR bias的影响

1. DNA在打断的那一步会发生一些损失，主要表现是会引发一些碱基发生颠换变换（嘌呤-变嘧啶或者嘧啶变嘌呤），带来假的变异。PCR过程会扩大这个信号，导致最后的检测结果中混入了假的结果；

2. PCR反应过程中也会带来新的碱基错误。发生在前几轮的PCR扩增发生的错误会在后续的PCR过程中扩大，同样带来假的变异；

3. 对于真实的变异，PCR反应可能会对包含某一个碱基的DNA模版扩增更加剧烈（这个现象称为PCR Bias）。因此， 如果反应体系是对含有reference allele的模板扩增偏向强烈，那么变异碱基的信息会变小，从而会导致假阴。

![img](./image_WGS/GATK4-pipeline-remove-duplicates-1.png) 

##### 操作

![img](./image_WGS/GATK4-pipeline-remove-duplicates-3.png)

**1. 排序（SortSam）**

- 对sam文件进行排序并生成bam文件，将sam文件中同一染色体对应的条目按照坐标顺序从小到大进行排序
- GATK4的排序功能是通过`picard SortSam`工具实现的。虽然`samtools sort`工具也可以实现该功能，但是在GATK流程中还是推荐用picard实现，因为SortSam会在输出文件的头信息部分添加一个SO标签用于说明文件已经被成功排序，且**这个标签是必须的**，GATK需要检查这个标签以保证后续分析可以正常进行
- `https://software.broadinstitute.org/gatk/documentation/tooldocs/current/picard_sam_SortSam.php`

```bash
# 使用GATK命令
$ gatk SortSam -I mapping/T.chr17.sam -O preprocess/T.chr17.sort.bam -R database/chr17.fa -SO coordinate --CREATE_INDEX
# 使用picard命令
$ java -jar picard.jar SortSam \
      I=input.bam \
      O=sorted.bam \
      SORT_ORDER=coordinate
```

![img](./image_WGS/GATK4-pipeline-remove-duplicates-4.png)
如何检查是否成功排序？

```bash
$ samtools view -H /path/to/my.bam
@HD     VN:1.0  GO:none SO:coordinate
@SQ     SN:1    LN:247249719
@SQ     SN:2    LN:242951149
@SQ     SN:3    LN:199501827
@SQ     SN:4    LN:191273063
@SQ     SN:5    LN:180857866
@SQ     SN:6    LN:170899992
@SQ     SN:7    LN:158821424
@SQ     SN:8    LN:146274826
@SQ     SN:9    LN:140273252
@SQ     SN:10   LN:135374737
@SQ     SN:11   LN:134452384
@SQ     SN:12   LN:132349534
@SQ     SN:13   LN:114142980
@SQ     SN:14   LN:106368585
@SQ     SN:15   LN:100338915
@SQ     SN:16   LN:88827254
@SQ     SN:17   LN:78774742
@SQ     SN:18   LN:76117153
@SQ     SN:19   LN:63811651
@SQ     SN:20   LN:62435964
@SQ     SN:21   LN:46944323
@SQ     SN:22   LN:49691432
@SQ     SN:X    LN:154913754
@SQ     SN:Y    LN:57772954
@SQ     SN:MT   LN:16571
@SQ     SN:NT_113887    LN:3994
...
```

若随后的比对记录中的contig那一列的顺序与头文件的顺序一致，且在头信息中包含`SO:coordinate`这个标签，则说明，该文件是排序过的

**2. 标记重复（Markduplicates）**

- 标记文库中的重复
- `https://software.broadinstitute.org/gatk/documentation/tooldocs/current/picard_sam_markduplicates_MarkDuplicates.php`

```bash
gatk MarkDuplicates -I preprocess/T.chr17.sort.bam -O preprocess/T.chr17.markdup.bam -M preprocess/T.chr17.metrics --CREATE_INDEX

```

![img](./image_WGS/GATK4-pipeline-remove-duplicates-5.png)

### 碱基质量校正

#### 质量校正原理

Phred碱基质量值是由测序仪内部自带的base-calling算法评估出来的，而这种base-calling算法由于受专利保护，掌握在测序仪生成商手中，研究人员并不能了解这个算法的细节，它对于人们来说就是一个黑盒子

而测序仪的base-calling算法给出的质量评估并不十分准确，它带有一定程度的系统误差（非随机误差），使得实际测序质量值要么被低估，要么被高估

BQSR试图利用机器学习的方法来对原始的测序质量值进行校正

例如：

> 对于一个给定的Run，我们发现，无论什么时候我在测序一个AA 的子序列时，改子序列后紧接着的一个任意碱基的测序错误率总是要比它的实际错误率高出1%，那么我就可以将这样的碱基找出来，将它的原始测序错误率减去1%来对它进行校正

会影响测序质量评估准确性的因素有很多，主要包括序列组成、碱基在read中的位置、测序反应的cycle等等，它们以类似于叠加的形式协同产生影响，这些可能的影响因素被称作协变量 (covariable)

注意：BQSR只校正碱基质量值而不改变碱基组成，特别是对于那些质量值偏低的碱基，我们只能说它被解析成当前碱基组成的准确性很低，但是我们又无法说明它实际更可能是哪种碱基，所以干脆不改

那么，BQSR的工作原理是怎样的？

BQSR本质上是一种回归模型

前提假设：影响质量评估的因素只有reads group来源，测序的cycle和当前测序碱基的序列组成背景（这里将它上游的若干个连续位点的碱基组成看作它的背景，一般为2~6，BQSR中默认为6）

则基于这个前提假设，我们可以得出以下结论：

> 相同reads group来源，同处于一个cycle，且序列背景相同的碱基，它们具有相同的测序错误率，这样的碱基组成一个bin

则可以建立这样的拟合模型：

$$X_i=(RG_i,Cyc_i,Context_i) \quad \begin{matrix} f \\ \to \end{matrix} \quad y_i$$

其中，i表示当前碱基，$RG_i$表示碱基所属的Reads Group来源，$Cyc_i$表示该碱基所在的测序cycle，$Context_i$表示该碱基的序列组成背景，$y_i$表示该碱基的实际测序质量(emprical quality)

这三个分量可以直接通过输入的BAM文件的记录获得，那如何获得实际的实际测序质量呢？

可以通过BAM文件中的比对结果推出

用给定的大型基因组测序计划得到的人群变异位点作为输入，将样本中潜在变异位点与人群注释位点overlap的部分过滤掉，则剩下的那些位点，我们假设它们都是“假”的变异位点，是测序错误导致的误检

则实际测序质量为：

$$EQ=-10\log \frac{\#mismatch + 1}{\#bases + 2}$$

注意：emprical quality是以bin为单位计算出来的

这样，有了X和Y，就可以进行拟合模型的训练了，训练好的模型就可以用于碱基质量值的校正

上述只是BQSR的基本逻辑框架，在实际的实现细节上会稍有一些差别

#### 操作

**1. 建立较正模型**

质量值校正，这一步需要用到variants的known-sites，所以需要先准备好已知的snp，indel的VCF文件：

```bash
# 下载known-site的VCF文件，到Ensembl上下载
$ wget -c -P Ref/mouse/mm10/vcf ftp://ftp.ensembl.org/pub/release-93/variation/vcf/mus_musculus/mus_musculus.vcf.gz >download.log &
$ cd Ref/mouse/mm10/vcf && gunzip mus_musculus.vcf.gz && mv mus_musculus.vcf dbsnp_150.mm10.vcf
# 建好vcf文件的索引，需要用到GATK工具集中的IndexFeatureFile，该命令会在指定的vcf文件的相同路径下生成一个以".idx"为后缀的文件
$ gatk IndexFeatureFile -F dbsnp_150.mm10.vcf

# 建立较正模型
$ gatk BaseRecalibrator -R Ref/mouse/mm10/bwa/mm10.fa -I PharmacogenomicsDB/mouse/SAM/ERR118300.enriched.markdup.bam -O \
PharmacogenomicsDB/mouse/SAM/ERR118300.recal.table --known-sites Ref/mouse/mm10/vcf/dbsnp_150.mm10.vcf
```

**2. 质量值校准**

```bash
# 质量校正
$ gatk ApplyBQSR -R Ref/mouse/mm10/bwa/mm10.fa -I PharmacogenomicsDB/mouse/SAM/ERR118300.enriched.markdup.bam -bqsr \
PharmacogenomicsDB/mouse/SAM/ERR118300.recal.table -O PharmacogenomicsDB/mouse/SAM/ERR118300.recal.bam
```

### 使用GATK鉴定SNV/SNP位点

#### 变异位点基因型推断的数学原理

##### 单点基因型推断

问题描述

> 某一区域的比对结果如下：
> 
> ```
> REFERENCE: atcatgacggcaGtagcatat
> --------------------------------
> READ1:     atcatgacggcaGtagcatat
> READ2:         tgacggcaGtagcatat
> READ3:     atcatgacggcaAtagca
> READ4:            cggcaGtagcatat
> READ5:     atcatgacggcaGtagc
> ```
> 
> 该区域存在一个候选变异位点，且在上面的比对结果中用大写字母标出：该碱基位置共用5条reads成功比对上，其中有4条reads在该位置的碱基组成与参考基因组一致，为G，而只有一条read的碱基组成为A，与参考基因组不同，即G:A=4:1
> 
> 该个体该位点似乎是一个G/A杂合，因为按照最简单的杂合位点的定义标准，若一个位点中检出的碱基组成中，与参考不一致的碱基组成比例在20%~80%的范围内，就可是算作是一个杂合位点。显然，在本示例中，是满足这个条件的
> 
> 然后，仅依据碱基组成比例来作这个推断，显然是不够可靠的，因为支持其为G/A杂合的read只有一条，而该read可能来自：
> 
> - 实际存在的变异
> - 建库过程中引入的错误（PCR）
> - 测序过程中错误的碱基检测（base calling）
> - 比对错误
> 
> 因此，为了得到更为可靠的变异检测结果，我们应该综合考虑更多的信息，在给出给出对于位点genotype推断时，同时给出该推断的置信度
> 
> 那么，如何实现呢？

简单来说，就是基于各genotype($G_i$)的人群先验概率$P(G_i)$以及特定样本对应位点的测序结果$S$，推断其可能为各个$G_i$的后验概率$P(G | S)$，根据贝叶斯推断的方法，将后验概率最高的那种$G_i$作为其最终推断出的genotype，即

$$G=arg \max_{G_i} P(G_i|S)$$

而根据贝叶斯公式：

$$P(G_i|S)=\frac{P(S|G_i)\cdot P(G_i)}{P(S)}$$

由于测序数据确定，$P(S)$固定，可以省略，则$P(G_i|S) \sim P(S|G_i)\cdot P(G_i)$

另外$P(G_i)$是$G_i$基因型的人群频率，已经给出，所以要想指定$P(G_i|S)$，只需要额外算出$P(S|G_i)$即可

> 注：
> 
> 当只有少数样本时，可以从对应的大型人群重测序项目中获取基因型的人群频率，例如dbSNP
> 
> 当有多个样本构成一个人群时，可以从当前研究的人群测序数据中，根据allel频率推算出基因型频率（Hardy-Weinberg equilibrium (HWE)）。
> 
> 例如，对于某个以A/T形式存在的位点，A的频率为1%（$p=0.01, q=1-p=0.99$），则
> | AA($p^2$) | AT($2pq$) | TT($q^2$) |
> |:--- |:---|:---|
> |0.0001|0.0198|0.9801|

我们假设各个read相互独立，则$P(S|G_i)$就是各个read的$P(S_i | G_i)$的乘积，即

$$P(S|G_i)=\prod_i P(S_i | G_i)$$

则，下面只要分别算出各个$P(S_i | G_i)$，最后就能得到$P(G_i|S)$

那么，怎么算这个$P(S_i | G_i)$呢？

我们令

$$
G_i = \left\{
   \begin{array}{ll}
    G_0 & \textrm{基因型的两个allel与参考基因组都不同} \\
    G_1 & \textrm{基因型的两个allel中有一个与参考基因组都相同}\\
    G_2 & \textrm{基因型的两个allel均与参考基因组相同}
  \end{array} 
  \right.
$$

则

$$
\left\{
  \begin{array}{ll}
  P(S_i | G_0) = (1-\epsilon_i)^{1-I_i}\cdot\epsilon_i^{I_i} \\
  P(S_i | G_1) = \frac{1}{2}(1-\epsilon_i) \cdot \frac{1}{2}\epsilon_i=\frac{1}{4}(1-\epsilon_i)\epsilon_i \\
  P(S_i | G_2) = (1-\epsilon_i)^{I_i} \cdot \epsilon_i^{1-I_i}
  \end{array} 
\right.
$$

其中，$I_i$表示该read当前位点碱基组成是否与参考位点一致，若一致$I_i=1$，否则$I_i=0$

> 对上面的$P(S_i | G_i)$的公式，作一个简单的说明：
> 
> 以上的3个式子来源于下面的同一形式
> 
> $$P(S_i | G_i)=P(I_i=1)^{I_i}\cdot P(I_i=0)^{1-I_i}$$
> 
> 而不同genotype下，$P(I_i=1)$或$P(I_i=0)$因为表示测对和测错对应的事件不同，而得到最终不同的公式


上面是将三种可能基因型的$P(S_i | G_i)$分别表示出来，为了将它们合并在一个公式中得到更为简洁的表达方式，可采用下面的形式：

符号说明：

| Symbol | Description |
|:---|:---|
| $n$	| Number of samples |
| $m_i$	| Ploidy of the $i$-th sample ($1≤i≤n$)，即i样本的倍型 |
| $M$	| Total number of chromosomes in samples: $M=\sum_i m_i$ |
| $d_i$ | Sequencing data (bases and qualities) for the $i$-th sample |
| $g_i$ | Genotype (the number of reference alleles) of the $i$-th sample ( $0≤g_i≤m_i$ ) |
| $\phi_k$ | Probability of observing k reference alleles ( $\sum_{k=o}^M \phi_k=1$ ) |
| $Pr\{A\}$ | Probability of an event A |
| $L_i(\theta)$ | Likelihood function for the $i$-th sample: $L_i(\theta)=Pr\{d_i \mid \theta\}$ |

前提假设：

> - 不同位点间相互独立；
> - 对于同一个位点，不同reads的测序错误或mapping误差相互独立；
> - 只考虑二等位情况；

估计某个样本出现特定基因型g的概率：$L(g)=?$

![img](./image_WGS/snp-calling-mathmatical-theory.png)
对于某一个样本的某一个位点，有$k$条 reads 比对上，其中有$l$条 ($0 \le l\le k$) 序列在该位点的碱基组成与 reference 一致，剩余 $k-l$ 条与 reference 不同，其中第 $j$ 条上该碱基的测序错误率为 $\epsilon_j$，则该样本的基因型与ref一致的有 $g \in [0,m]$ 种（由于这里只考虑人的，则m取值为2，其中g=0表示该样本的基因型与ref一致的allel数为0，即与ref完全不同，例如在该位点可能的二等位为A/C，ref为A，则g=0说明该样本的genotype为C/C，同理，g=1或g=2分别表示该样本的基因型与ref一致的allel数为1或2，在上面举的例子中该样本的基因型就应该为A/C或A/A）的概率为

$$
	\begin{aligned}
	&\quad L(g) \\
	&= Pr(d \mid g) \\
	&= \prod_{i=1}^l Pr_i(A)\prod_{j=l+1}^k Pr_j(\overline A)  & (1)\\
	&= \prod_{i=1}^l [Pr_i(B , A)+Pr_i(\overline B , A)]\prod_{j=l+1}^k [Pr_j(B , \overline A)+Pr_j(\overline B , \overline A)] & (2)\\
	&= \prod_{i=1}^l [Pr_i(B,C) + Pr_i(\overline B,\overline C)] \prod_{j=l+1}^k [Pr_j(B,\overline C) + Pr_j(\overline B,C)] & (3)\\
	\end{aligned}
$$

> 其中，$m$ 是该物种的倍性，普通人是二倍体，因此一般 $m=2$
>
> 事件$A=\{测序碱基与\text{ref}一致\}$，则$\overline A=\{测序碱基与\text{ref}不一致\}$
>
> 事件$B=\{该碱基的测序是正确的\}$，则$\overline B=\{该碱基的测序是错误的\}$
>
> 事件$C=\{实际碱基与\text{ref}一致\}$，则$\overline C=\{实际碱基与\text{ref}不一致\}$

上面公式中，从(2)到(3)的推导涉及到最基本的逻辑常识，这里就不再赘述了

由于测序错误与基因组的组成无关，即$B \bot C$，因此上面的公式可以向下继续推导：

$$
	\begin{aligned}
	&=  \prod_{i=1}^l [Pr_i(C)Pr_i(B) + Pr_i(\overline C)Pr_i(\overline B)] \prod_{j=l+1}^k [Pr_j(\overline C)Pr_j(B) + Pr_j(C)Pr_j(\overline B)] & (4)\\
	&= \prod_{i=1}^l \left[ \frac{g}{m}(1-\epsilon_i) + \frac{m-g}{m}\epsilon_i \right] \prod_{j=l+1}^k \left[  \frac{m-g}{m}(1-\epsilon_j) +  \frac{g}{m}\epsilon_j\right] & (5)\\
	&= \frac{1}{m^k}\prod_{i=1}^l [g(1-\epsilon_i) + (m-g)\epsilon_i] \prod_{j=l+1}^k [(m-g)(1-\epsilon_j) + g\epsilon_j] & (6)
	\end{aligned}
$$

上面公式中，(4)到(5)的推导利用了：

$$
	\begin{aligned}
	&Pr(B)=1-\epsilon, \quad Pr(\overline B)=\epsilon & (7)\\
	&Pr(C)=\frac gm , \quad Pr(\overline C)=\frac{m-g}{m} & (8)
	\end{aligned}
$$

\(7\)公式很好理解，在这里就不作更多的解释

对公式(8)，下面作一下简单的解释：

> 由于上面的前提假设中就已经提到，只考虑双等位情况，ref allele即是双等位中的一种，则对于一个m倍体的个体，它该等位基因座上有m个等位基因，其中与ref allele一致的有g个，则剩下m-g个基因座上的allele与ref allele不一致
>
> 则，随机从这m个基因座中抽一个，其基因型与ref一致的概率为$Pr(C)=g/m$，与ref不一致的概率为$Pr(\overline C)=1-g/m=(m-g)/m$

##### 单体型推断

GATK进行SNP calling的核心算法为HaplotypeCaller，这个也是GATK中最核心的算法，理解了这个算法基本上就明白了GATK变异检测的原理

HaplotypeCaller它本质上是对贝叶斯原理的应用，只是相于同类算法它有点不同之处

算法思想概述：

> HaplotypeCaller首先是根据所测的数据，先构建这个群体中的单倍体组合（我认为这也是Haplotype这个名字的由来），由于群体中的单倍体是有多个的，所以最好是多个人一起进行HaplotypeCaller这样构建出来的单倍体组合会越接近真实情况
>
> 构建出单倍体的组合之后（每一个单倍体都有一个依据数据得出的后验概率值），再用每个样本的实际数据去反算它们自己属于各个单倍体组合的后验概率，这个组合一旦计算出来了，对应位点上的碱基型（或者说是基因型，genotype）也就跟着计算出来了：
>
> 计算每一个后候选变异位置上的基因型（Genotype）后验概率，最后留下基因型（Genotype）中后验概率最高的哪一个

下面进行详细地说明：

在HaplotypeCaller中变异检测过程被分为以下四个大的步骤

![img](./image_WGS/Algorithms-Bioinf-variants-calling-algorithmn-GATK-1.png)

**1. 确定候选变异区域（ActiveRegion）**

通过read在参考基因组上的比对情况，筛选出潜在的变异区域，这些区域在GATK中被称为ActiveRegion

**2. 通过对候选变异区域进行重新组装来确定单倍型**

对于每个ActiveRegion，GATK会利用**比对到该区域上的所有read**（如果有多个样本那么是所有这些样本的reads而不是单样本进行）构建一个类似于de Bruijn的图对ActiveRegion进行局部重新组装，构建出该区域中可能的单倍型序列。然后，使用Smith-Waterman算法将每个单倍型序列和参考基因组进行重新比对，重新检测出潜在的变异位点

**3. 依据所给定的read比对数据计算各个单倍型的似然值**

在步骤2的基础上，我们就得到了在ActiveRegion中所有可能的单倍型序列，接下来需要评估现有数据中对这些单倍型的支持情况

GATK使用PairHMM算法把原本比对于该区域中的每一条read依次和这些单倍型序列进行两两比对，这样我们就可以得出一个read-单倍型序列成对的似然值矩阵，例如以单倍型为列，以read为行，将矩阵记作$(a_{i,j})$

$$
\begin{array}{l|c|c|c|c}
\hline
0 & H_1 & H_2 & .. & H_m \\
\hline
r_1 & a_{11} & a_{12} & .. & a_{1m} \\
r_2 & a_{21} & a_{22} & .. & a_{2m} \\
.. & .. & .. & .. & .. \\
r_n & a_{n1} & a_{n2} & .. & a_{nm} \\
\hline
\end{array}
$$

则矩阵中的某一个元素$a_{ij}$表示在read i支持单体型为$H_j$的似然，即$P(r_i,H_j)=a_{ij}$

这个似然值矩阵很重要，因为在获得这个矩阵之后，GATK会在每一个潜在的变异位点上把这些似然值相加合并，计算等位基因的边缘概率，这个边缘概率实际上是每一个read在该位点上支持其为变异的似然值，即

$$P(H_i)=\sum_{j=1}^n P(r_j,H_i)$$

（* 在该步骤中，Pair-HMM这实际上是GATK中最为耗费计算资源的那部分了，GATK的加速也是常常以此为突破口——比如GPU加速或者把Pair-HMM模块烧录到FPGA芯片中，也有人从算法本身出发发表了关于如何更快计算Pair-HMM的文章：`https://journals.sagepub.com/doi/pdf/10.1177/1176934318760543` ）

（4）计算每一个样本在最佳单倍型组合下的基因型（Genotype）

在完成了步骤3之后，我们就知道了**每一条read在每个候选变体位点上支持每一种等位基因（Allele）的概率**了。那么，最后要做的就是通过这些似然值，计算出候选变异位点上最可能的样本基因型，也就是Genotype——这也是发现真正变异的过程。这就需要应用贝叶斯原理来完成这个计算了——GATK这也是到这一步才使用了该原理，通过计算就可以得到每一种Genotype的可能性，最后选择后验概率最高的那一个Genotype作为结果输出至VCF中

后面的分析中，对于每一个变异位点假设只有二等位形式——注意：这和一个ActiveRegion中存在多种单体型不矛盾，若一个ActiveRegion在群体中存在n个变异位点，在只考虑二等位形式的前提下，该区域具有的单体型总共有$2^n$种

下面来推导某个样本中的某一个变异位点最可能的SNP形式

该样本在该位点的genotype为G的后验概率为：

$$P(G \mid D) = \frac{P(G)P(D \mid G)}{\sum_i P(G_i)P(D \mid G_i)} \tag{1}$$

由于分母部分对于任何形式genotype都一样，即它是个定值，所以可以忽略，因此上面的公式可以简化成：

$$P(G \mid D) = P(G)P(D \mid G) \tag{2}$$

其中，$P(G)$为genotype为G的先验概率，理论上为样本来源的群体中allele为G的频率，这个一般需要前期给定，若不给定的话，GATK会默认每种G的频率均等

$P(D \mid G)$表示在已知样本genotype为G的前提下，对样本进行测序得到的测序数据为D（仅考虑该ActiveRegion范围内的）的条件概率，我们假设每条reads之间是相互独立的，所以

$$P(D \mid G)=\prod_j P(D_j \mid G)\tag{3}$$

其中，$D_j$表示该样本测序数据D中的第j条read

由于我们正常人都是二倍体，则对于某一条reads，它既可能来自于同源染色体1，记作$H_1$，也可能开自于同源染色体2，记作$H_2$，所以

$$
\begin{aligned}
&\quad P(D_j \mid G) \newline
&= P(D_j,H_1 \mid G) + P(D_j,H_2 \mid G) \newline
&= P(H_1 \mid G)P(D_j \mid H_1) + P(H_2 \mid G)P(D_j \mid H_2)
\end{aligned} \tag{4}
$$

由于理论上一条read来源于$H_1$还是$H_2$的概率是均等的，都为1/2，即$P(H_1 \mid G)=P(H_2 \mid G)=1/2$，所以

$$P(D_j \mid G)=\frac{P(D_j \mid H_1)}{2} + \frac{P(D_j \mid H_2)}{2} \tag{5}$$

因此(3)可以改写成

$$P(D \mid G)=\prod_j \left( \frac{P(D_j \mid H_1)}{2} + \frac{P(D_j \mid H_2)}{2}\right) \tag{6}$$

现在如果想算出$P(G \mid D)$，就差$P(D_j \mid H_n)$了，那么，如何算$P(D_j \mid H_n)$呢？

上面已经提到，$P(D_j \mid H_n)$表示的是由同源染色体$H_n$产生read $D_j$的条件概率，而每条同源染色体有它各自的单体型，所以这里可以把$H_n$理解为它对应的单体型，则$P(D_j \mid H_n)$可以理解为在特定单体型$H_n$的前提下，产生read $D_j$的条件概率


## 全外显子组测序（WES）

在这一章节中，我们将会对全外显子组（Whole Exome Sequencing， WES）进行介绍，包括其与全基因组测序的异同、技术特点及下游分析方向等，同时也包括实战代码的讲解。

### 简介

**外显子**

真核生物中编码蛋白质的基因由外显子（exon）和内含子（intron，非编码区域）组成，外显子又分为编码区域和UTR区域。转录过程中或转录后的RNA经过修饰剪切（splicing）作用，移除内含子、合并外显子，最终形成蛋白质。人类基因组中约1.1%为外显子，所有的外显子区域集合称为外显子组（exome）。80%的外显子序列长度少于200bp（Sakharkar，2004年）。研究发现，在外显子组中约85%的突变与疾病相关[1]。

![pic1](./image_WES/pic1.png)

前面的章节已经详细介绍了全基因组测序方法（Whole Genome Sequencing，WGS）与各类高通量测序技术。与全基因组测序相比，全外显子组测序针对外显子区域进行定序测序，是一种成本效益更佳的方法。相比于花费大量的计算资源和时间去分析整个人类基因组的30亿个碱基，全外显子组测序仅需测序约6000万个碱基，时间成本与计算成本都大幅度降低，更适用于个人基因信息的快速检测与大规模群体样本的基因分析。

![全基因组测序和全外显子组测序的覆盖范围对比](./image_WES/pic2.jpeg)

![不同测序方法的费用成本](./image_WES/pic3.png)

但近年来随着高通量测序技术的发展，测序成本大幅降低，成本已经不是研究机构的主要考量因素，全基因组测序也越来越多出现在科研项目中。 已有研究表明，全基因组测序的产出结果覆盖率高、测序深度稳定，可获得更全面可靠的基因序列，且在单核苷酸突变（SNP）检测方面更为灵敏[4]。

全基因组测序与全外显子组测序各有所长，实际中应当结合研究课题和实验设计选择最合适的测序方案[5]。人类全外显子占基因组不超过2%，却已经涵盖了近85%的已知疾病相关突变，全外显子测序是比全基因组测序更为经济高效的实验方法，适用于孟德尔疾病、肿瘤和复杂疾病等方向的研究。全外显子组测序目前广泛应用于医学临床研究和科研项目中，已经成为临床遗传疾病和罕见病的常规检测方法之一。如对超声异常或单基因遗传病疑似胎儿进行全显子组测序分析，可以快速预估生育风险，并通过早诊断和精准治疗来节省医疗费用[2]。而对于普通人群，分析个人基因组数据可以更科学地评估个体常见疾病风险和提供个人用药建议。

**全外显子组测序的优点：**

- 高深度(coverage)，全外显子组测序深度一般达到50~100X。全基因组测序深度一般为30X；
- 测序成本低；
- 资料存储空间需求小，仅~2%的基因组序列；
- 计算机资源需求不高，分析计算周期短；
- 分析出来的变异与表型直接关联，可解释性更强；

**全外显子组测序的缺点：**

- 只能检测外显子组区域的变异（SNP和Indel为主），无法检测外显子组区域以外的变异、拷贝数变异（copy number variation，CNV）和结构变异（structural variant，SV）；
- 测序深度受多方因素影响，测序深度不一致；
- 目前测序过程中定序长度一般大于200bp，而人类基因组大部分外显子的长度都小于200bp，造成浪费；
- 全外显组测序的实际产出的序列只有65%-75%是处于外显子组区域，但可以通过整体提高测序深度的方法来减弱“部分区域测序深度偏低“和“有效序列占比不高“等问题带来的偏差。

通过分析全外显子组测序结果可以得到突变位点信息，其中可能发现一些重要的致病突变，但也有相当多的一部分是未知意义的突变位点，其临床应用意义仍未探明。同时，虽然全外显子测序设计上涵盖近2万个基因（可以理解为外显子序列或转录本），但实际检测的结果全面与否，很大程度取决于前期样本提取实验中是否能尽可能地覆盖和捕获全部外显子组序列，因此对于全外显子的阴性检测结果，还需要进一步考虑是该基因无突变还是该基因未被检测。当然，突变位点注释和样本质量造成的局限性在全基因组测序中也无法避免，相信随着测序技术的不断优化迭代，越来越多数据库的更新迭代，这些问题会逐步得到解决。
在临床应用上，如果只需定向检测已知的致病位点，另一项更有针对性的靶向基因测序（targeted panel sequencing）方案或许是更好的选择。但全外显子组测序又有着更广泛的覆盖范围，能发现更多新的变异情况，因此，测序方案的选择需要根据患者实际需求而选择。

### 全外显子组测序的覆盖度与测序深度

测序深度代表了参考基因组每个区域被短序列覆盖的次数，测序深度越高，测序结果的识别就越准确，后续的统计分析也越可靠。由于全外显子组样本在上机测序前必须经过捕获（capture）和扩增（PCR amplification）两个步骤，这两个步骤在不同的区域有效率差别，有些外显子区域捕获效率高，有些区域捕获效率低，因此会造成全外显组测序结果测序深度不一致的问题。影响测序深度的因素包括：

- GC含量高的区域（如启动子或UTR）在捕获和扩增时会受到影响^；
- 低复杂度片段（如重复区域）和含有模糊碱基的区域捕获效率偏低；
- 进行PCR扩增的合适为70bp-200bp，零碎或过长的序列片段会受到影响。；
- 假基因的存在影响真实测序深度的计算；
- DNA的数量，如果DNA数量偏低，只能通多高次数PCR循环来达到后续测序所需的样本量，但这会导致大量PCR重复，影响后续数据分析的可信度；
- DNA的质量，如从石蜡包埋样本（FFPE）提取的DNA通常质量较差，某些区域的序列更易破碎，引入偏差；

^G、C碱基之间由3个氢键连接，稳定性较强，不易被打断，所以使得GC含量高的区域通常片段偏大。同时PCR时不易解旋，就算分开后，单股的GC含量高的序列也容易自身粘合形成二级结构。同时，PCR聚合酶可能对GC含量高的片段有偏好性[6]，影响PCR的效果。（这段备注放在与上一段同一页的页脚备注就好）

全外显组测序的探针也略有不同，除了常见的的全外显组探针产品，也可自行设计和定制。研究人员结合现有的参考序列数据和突变信息，可以设计和增加感兴趣区域的探针，也可在特定区域增加探针密度来提高捕获效率。但探针的设计需要综合考虑中靶率（On-target rate）、覆盖度（coverage）、均一性（uniformity）和重复率（Dup rate）等指标。

在不考虑测序成本的前提下，全基因组测序不需要经过捕获步骤，甚至可以不经过PCR扩增直接进行测序，其测序深度能更加稳定，序列分布更均匀，甚至能发现未曾被探针捕获的区域，覆盖的基因组区域更全【7】。

![在不同参考序列中的覆盖率](./image_WES/pic5.png)

> a)WES，WGS_wPCR（经过PCR）和WGS（未经PCR）的WGS所显示的每个GC%的参考基因组的编码外显子区域的平均读取深度，每个数值为五个样品的深度均值。
> b)WES和WGS（未经PCR）在不同参考序列中的覆盖率 【6】

### 全外显子组数据分析实战

全外显子组测序实验的整体工作流程如下:

1. 样品制备，核酸分离提纯；
2. DNA片段化；
3. DNA文库构建；
4. 使用探针靶向捕获外显子序列；
5. PCR扩增；
6. qPCR进行质量控制（若需）；
7. 测序；
8. 分析数据，突变检测；

好的样本制备实验能保证后续数据分析的准确度，两部分的工作相辅相成。本节我们将进入下机数据分析的实战环节，只要针对双端测序样本的外显子组下机数据分析，如果是单端测序，可以自行调整Trimmomatic和bwa代码变为单端测序模式，其余步骤不变。

所需软件：
- fastqc
- multiqc
- bwa
- samtools
- gatk （此处用gatk 4.1版本）
- Annovar

运行代码如下：

基本的处理思路是，下机序列经过数据质控后，比对到参考序列上找到最有可能的原位置，结合现有的常见突变位点信息进行筛选，过滤得到样本个体的突变位点信息，并存储在VCF（Variant Call Format）文件中。 利用ANNOVAR软件，同样地结合前人总结的突变信息（humandb/目录下）来注释和解析检测到的个体突变位点，并探索突变与个人生理状态和疾病发展的可能联系。

```bash
thread=1
ref=ref/references_hg38_v0_GRCh38.primary_assembly.genome.fa
data=data/
sample=WXS_example
gatk_db=ref/gatk/
annovar=/home/huaping/software/annovar/annovar/
###############
# fastq QC
################

#fastq-dump SRR8381428 --split-3
#fastqc -o fastqc/ ${data}/${sample}*.fq.gz
#bash check_phred.sh ${data}/${sample}_1.fq.gz

##Running Trimmomatic
##Paired End Mode:
##trimmomatic PE [-threads <threads] [-phred33 | -phred64] [-trimlog <logFile>] <input 1> <input 2> <paired output 1> <unpaired output 1> <paired output 2> <unpaired output 2> <option 1>...
time trimmomatic PE -phred33 ${data}/${sample}_1.fq.gz ${data}/${sample}_2.fq.gz ${data}/${sample}_1.clean.fq.gz ${data}/${sample}_1.clean.unpaired.fq.gz ${data}/${sample}_2.clean.fq.gz ${data}/${sample}_2.clean.unpaired.fq.gz MINLEN:20 LEADING:20 TRAILING:20 && echo "trim done	$(date "+%Y-%m-%d %H:%M:%S")"

mkdir -p fastqc/
fastqc -o fastqc/ ${data}/${sample}*clean.fq.gz &&
multiqc fastqc/${sample}*.zip -o fastqc &&  echo "QC done	$(date "+%Y-%m-%d %H:%M:%S")"

##gatk annotation files download

##################
##alignment
##################
mkdir -p BAM/
#bwa index -a bwtsw ${ref} &&
bwa mem -M -Y -R '@RG\tID:sample_1\tSM:sample\tLB:WES\tPL:Illumina' ${ref} ${data}/${sample}_1.clean.fq.gz ${data}/${sample}_2.clean.fq.gz | samtools view -Sb - > BAM/${sample}.bam && echo "alignment done	$(date "+%Y-%m-%d %H:%M:%S")"

#################
#sam file preprocessing - sort and markduplicate
#################
samtools sort -o BAM/${sample}.sorted.bam BAM/${sample}.bam &&
picard MarkDuplicates -Xmx64g I=BAM/${sample}.sorted.bam O=BAM/${sample}.sorted.markdup.bam M=BAM/${sample}.sorted.markdup.txt &&
picard BuildBamIndex -Xmx64g I=BAM/${sample}.sorted.markdup.bam && echo "markduplicate done	$(date "+%Y-%m-%d %H:%M:%S")"

#samtools faidx ${ref} &&
#picard CreateSequenceDictionary R=${ref} O=${ref/\.fa/}.dict &&

##########################
#BQSR
##########################
gatk BaseRecalibrator -R ${ref} -I BAM/${sample}.sorted.markdup.bam \
	--known-sites ${gatk_db}resources_broad_hg38_v0_Mills_and_1000G_gold_standard.indels.hg38.vcf.gz \
	--known-sites ${gatk_db}resources_broad_hg38_v0_Homo_sapiens_assembly38.known_indels.vcf.gz \
	--known-sites ${gatk_db}resources_broad_hg38_v0_hapmap_3.3.hg38.vcf.gz \
	--known-sites ${gatk_db}resources_broad_hg38_v0_Homo_sapiens_assembly38.dbsnp138.vcf \
	-O BAM/${sample}.BQSR.table
gatk ApplyBQSR -R ${ref} -I BAM/${sample}.sorted.markdup.bam -bqsr BAM/${sample}.BQSR.table -O BAM/${sample}.sorted.markdup.BQSR.bam && echo "BQSR done     $(date "+%Y-%m-%d %H:%M:%S")"

###########################
##Variant calling - haplotypecaller
##########################
mkdir -p VCF/
gatk HaplotypeCaller -R ${ref} -I BAM/${sample}.sorted.markdup.BQSR.bam -O VCF/${sample}.vcf && echo "variant calling done	$(date "+%Y-%m-%d %H:%M:%S")"


###########################
#Annotation -ANNOVAR
###########################
${annovar}table_annovar.pl VCF/${sample}.vcf ${annovar}humandb/ -buildver hg38 -out VCF/${sample} -remove -protocol refGene,cytoBand,exac03,avsnp147,dbnsfp30a -operation gx,r,f,f,f -nastring . -vcfinput -polish && echo "annotation done 	$(date "+%Y-%m-%d %H:%M:%S")"

```

### 测序数据的下游分析方向

经过上述的流程处理，带有注释结果的突变位点将存储在VCF文件中，具体格式介绍见前面章节。除了对突变位点进行注释外，还可以进一步有选择性地对突变位点/基因进行功能性分析和关联分析。在此简单介绍一下可行的研究方向和思路和可能会用到的数据库，数据库包括现有的文献数据库（如NCBI Pubmed）和生物数据库：

- 从位点/基因层面出发进行功能分析；
- 从基因层面出发进行通路分析，发掘与目标基因相关的代谢通路及其相互关系；
- 从样本层面出发，比较公开数据库中同类型人群的基因特征进行结果验证。同理，也可结合非公开的临床样本进行验证分析和实验分析；

#### 突变位点相关数据库查询

**OMIM**（Online Mendelian Inheritance in Man）https://omim.org/ 是比较全面、权威的人类孟德尔遗传数据库，主要关注表型（孟德尔遗传病为主）和基因型之间的关系。自1960年代初开始建立，并在1987年启动在线网站，实现免费公开查询。目前，OMIM数据库保持每日更新，存储记录了超过15,000个基因的信息（截至2020年9月）。OMIM数据库界面简洁清晰、内容全面、操作简便，是遗传学、基因组学和医学领域等领域的重要数据库。

**COSMIC** （Catalogue Of Somatic Mutations In Cancer，癌症体细胞突变数据库）https://cancer.sanger.ac.uk/cosmic 主要记录与癌症相关的体细胞突变（somatic mutation）信息，可供学术研究人员免费使用。数据库自2004年建立开始快速发展，目前储存了超过1000个全基因组序列信息，1.6万例样本信息和超过250万个突变位点（截至2020年9月）。COSMIC数据库主要来自科学文献中收集已被报道的癌症基因突变位点（Tier1: 具有与癌症相关的活动记录和突变证据，突变以促进致癌转化的方式改变基因产物的活性。），或者是来自大人群癌症研究的结果位点（Tier2：在癌症样本中检测到了大量该基因的突变但与癌症的相关意义未明确）。体细胞突变是指并非由遗传得到、个体在受精卵发育后发生的突变，通常情况下体细胞突变不会造成自身后代的遗传改变。体细胞突变不一定引起表型变化，但也可能引起多种疾病，包括癌症。

**ClinVar**  https://www.ncbi.nlm.nih.gov/clinvar/ 是NCBI主办的，与疾病相关的人类基因组变异数据库。它整合了dbSNP、dbVar、Pubmed、OMIM等多个数据库的遗传变异和临床表型信息。同时，每个研究机构都可以向其提交数据，并由专家团队对信息进行审核评级。按提交的注释信息和证据的可靠性，每个突变位点从高到低被评为4个星级，研究人员在查询相关位点时，可以结合注释信息、证据和专家评级综合考虑。Clinvar数据库体系依照疾病类别分成不同的数据库，并由熟悉该领域的专家团队来管理和审核，不断更新优化，形成一个标准的、可信的遗传变异-临床相关的数据库。

**BRCA Exchange** https://brcaexchange.org/ 整合了Clinvar和LOVD等数据库，专门针对乳腺癌易感基因BRCA1 和BRCA2（Breast cancer susceptibility gene 1/2）进行突变位点注释和记录，目前（截至2020年9月）有超过4万条位点记录。BRCA基因是目前研究比较深入的肿瘤易感基因，早期研究发现，女性BRCA突变携带者患乳腺癌和卵巢癌的风险大幅度提升。近年研究发现，结肠癌、胰腺癌、皮肤癌和男性前列腺癌等疾病的发生也与BRCA基因相关。基因序列中不同位置的突变会造成带来不同的影响和风险，BRCA基因无热点突变或热点区域，即基因上存在上万种突变的可能性，因此针对突变位点的注释数据库就变得非常重要，只有了解了该突变位点的风险，才能采取更有针对性预防或治疗措施。

![BRCA Exchange 数据库中现存超过4万条突变位点记录](./image_WES/pic10.png)

#### 数据库使用案例
以实战代码中找到的一个突变为例，利用OMIM 和 COMICS数据库进行进一步查找。

**根据结果VCF注释查找感兴趣的突变位点**
VCF文件中会突变所在位置（Func.refGene）、涉及的突变基因（Gene.refGene）以及功能变化（ExonicFunc.refGene），假如说从风险度比较高的突变开始查起，4号染色体的第81046034碱基从C变成了T，基因型GT=1/1，且被标注了“Func.refGene=exonic; Gene.refGene=BMP3; ExonicFunc.refGene=nonsynonymous_SNV“，即认为在BMP3基因的编码区上有非同义突变，由此可以去数据库中搜索基因BMP3的信息，查看突变是否与样本表征有相关关系。OMIM数据库中记录了基因功能、生化特征、基因关系图、相关文献等信息。右侧菜菜单栏还可以点击进入外部数据库，查看该基因的DNA 、蛋白质、临床资源、动物模型、细胞通路等信息。

![在OMIM数据中查找基因与表型的关系](./image_WES/pic5.png)

**根据感兴趣的基因查找相应突变位点**
以癌症研究为例，关键任务是找到疾病相关的突变基因。前期大量的科研人员已经发现和总结了一些与癌症相关的基因。 COSMIC数据库中的CGC（Cancer Gene Census，https://cancer.sanger.ac.uk/census )是整理好的癌症相关基因目录，可供查询和下载。在数据库中查找目标疾病的相关基因目录，并在结果VCF文件中看是否有相关基因突变位点。

![在COSMIC中查找与特定疾病相关的基因](./image_WES/pic6.png)

以结直肠癌（colorectal cancer）为例，从CGC中查找关键词“colorectal”得到723条记录。关注其中的MSH6基因，在VCF中查找相应基因可用代码 $grep -v "#" <VCF文件> |grep "MSH6"  共得到25条记录，意味着样本在MSH6基因上有25个突变位点，接下来就在一一查看突变信息和对表型的可能影响即可。

![在COSMIC中查找与特定疾病相关的基因](./image_WES/pic7.png)

在COSMIC数据库中直接查找基因可以获得更多的信息，还有编码蛋白质的3D模型。COSMIC-3D （https://cancer.sanger.ac.uk/cosmic3d/）
是交互式的网页，可以通过鼠标翻转和缩放蛋白质的三维结构，网页下方记录了错义突变的位置，点击措意突变的位置可以查看对应的小分子，估计结合位点，网页信息可以跳转蛋白质数据库PDB（Protein Data Bank）继续详细查看。

![在COSMIC数据库中查找基因](./image_WES/pic8.png)

![查看突变位点对蛋白质结构的影响](./image_WES/pic9.png)

### 通路分析

**KEGG**（Kyoto Encyclopedia of Genes and Genomes，京都基因与基因组百科全书） https://www.genome.jp/kegg/pathway.html 数据库把基因与细胞、物种进行关联，KEGG PATHWAY子数据库通过清晰明了的图表来表述基因和代谢物所参与的代谢通路，同时更全面地展现通路内部变化以及代谢通路之间的关系。数据库中将生物代谢通路划分为 6 类：细胞过程（Cellular Processes）、环境信息处理（Environmental Information Processing）、遗传信息处理（Genetic Information Processing）、人类疾病（Human Diseases）、新陈代谢（Metabolism）、生物体系统（Organismal Systems），在此基础上还继续按具体生命活动细分子通路，记录包含其通路代谢图和具体注释等信息。

![以MSH6为例在KEGG数据库中搜索相关通路](./image_WES/pic11.png)

**Metascape** https://metascape.org/gp/index.html#/main/ 是2015年12月首次发布，整合了GO、KEGG、UniProt和DrugBank等多个权威的数据资源，且每月更新其相关的40多个数据库，保证查询结果的时效性，是目前较为常用的通路富集和生物过程注释数据库。除了记录模式生物的通路信息，数据库还包含了蛋白质相互作用通路，可进行基因相关的蛋白质网络分析和药物分析。

![Metascape数据库可以同时查看多个基因的相关通路](./image_WES/pic12.png)

### 样本数据库寻找数据集进行验证或辅助分析
**TCGA**（The Cancer Genome Atlas）https://portal.gdc.cancer.gov/ 是美国国家癌症研究所(National Cancer Institute)和美国人类基因组研究所(National Human Genome Research Institute)共同监管的一个基于肿瘤病人样本的数据库项目，旨在借助高通量测序技术对癌症基因组进行读取和分析，帮助人类理解癌症，提高对癌症的预防、诊治能力。TCGA数据库包含丰富且规范的样本多组学数据和临床数据，包括mRNA表达、miRNA表达数据、拷贝数变异、DNA甲基化、突变位点等，研究人员还可通过申请获准下载原始下机数据，是癌症研究中非常重要的数据库。

![TCGA数据库](./image_WES/pic13.png)

**CCLE**（Cancer Cell Line Encyclopedia，癌症细胞系的百科全书）https://portals.broadinstitute.org/ccle 目前存储了1457种（截至2020年9月）癌症细胞系的免费公开基因组数据，旨在对大量癌症模型进行详细的遗传学和药理学表征分析，开发基因与药物效用相关的综合分析流程，同时在体外运用细胞系模拟癌症患者分层样本进行更多的肿瘤药理研究实验。







<!--chapter:end:0070-WGS.Rmd-->

# 常用数据分析的数学原理 {#statistics}

## 假设检验

## 线性回归

## 主成分分析

## 主坐标分析

## 聚类

## tSNE

在这一章节中，我们将会对t-SNE的算法做一个比较详尽的介绍。同时，也会在理论讲述的最后，给大家带来实战代码的讲解。

在具体讲解t-SNE之前，我们首先要了解两个信息论中的概念：信息熵和相对熵（K-L散度）。

### 信息熵与相对熵

#### 信息熵

1948年，美国科学家香农发表的论文《通信的数学理论》，奠定了信息论的理论基础。其定义的信息熵这一概念，实现了对“不确定性”的数学化度量。从定义上来看：信息熵是从总体上、从平均意义上表示信源$X$每一个符号（不论哪一个符号）所含有的平均信息量（或信源发送信息前，每一个符号的平均不确定性），见公式1。
$$
H(X)=-\sum_{i=1}^rp(a_i)logp(a_i)
\tag{1}
$$
其中，$p(a_i)$代表随机事件$X$为$a_i$时的概率。是不是感觉很抽象？没关系，接下来我们将举一个生活中十分常见的例子来帮助大家理解这个公式。

平时早晨出门前我们会习惯性的查看当天的天气预报，如果天气预报说“今天白天下雨的概率是百分之九十，晴天的概率是百分之十”，我们一般就会选择带伞出门，因为我们认为下雨的可能性非常大；如果天气预报说“今天白天下雨的概率是百分之五十，晴天的概率是百分之五十”，我们就会犹豫是否带伞，因为，今天有可能下雨，也有可能不下雨，并且无法判断到第大概率会出现哪一种情况；如果天气预报说“今天白天下雨的概率是百分之十，晴天的概率是百分之九十”，我们一般就会不带伞出门，因为我们认为下雨的可能性比较小，晴天的可能性非常大。显然，在第一条和第三条天气预报中，下雨这件事的不确定性程度较小，要么是大概率下雨，要么是大概率晴天，都有助于我们决策是否带伞。而第三条天气预报关于下雨的不确定性程度就大多了。而这种信源的平均不确定性就可以用信息熵来描述，假设三条新闻分别为$X_1,X_2,X_3$，他们所具有的的平均不确定性分别是：
$$
H(X_1)=-\sum_{i=1}^rp(a_i)logp(a_i)=-(0.9\times log0.9+0.1\times log0.1)=0.4689956\\
H(X_2)=-\sum_{i=1}^rp(a_i)logp(a_i)=-(0.5\times log0.5+0.5\times log0.5)=1\\
H(X_3)=-\sum_{i=1}^rp(a_i)logp(a_i)=-(0.1\times log0.1+0.9\times log0.9)=0.4689956
$$


由计算结果，我们可以直观看出$H(X_1)=H(X_3)<H(X_2)$。这也与我们平日里的经验认知相符，在平日里做决策时，往往是“几个事件旗鼓相当”情况下最难做出决定。因此，通过这个例子，大家是不是对信息熵这个概念有了比较直观的认识了？接下来我们将了解相对熵这个概念。

#### 相对熵

相对熵，又称K-L散度( Kullback–Leibler divergence)，是描述两个概率分布$P$和$Q$差异的一种方法。在信息论中，$D(P||Q)$表示当用概率分布$Q$来拟合真实分布$P$时，产生的信息损耗，其中$P$表示真实分布，$Q$表示$P$的拟合分布。有人将K-L散度称为K-L距离，认为K-L散度描述了不同分布之间的距离。但事实上，K-L散度并不满足距离的概念，因为度量距离应该满足对称性，而显然K-L散度并不对称，公式见2。
$$
D_{KL}(p||q)=\sum_{i=1}^np(x_i)(logp(xi)-logq(x_i))=\sum_{i=1}^np(x_i)log\frac {p(x_i)}{q(x_i)}
\tag{2}
$$
上面我们讲了好长一段的理论，大家可能感觉还是不是很直观，下面我举一个简单的例子带着大家直观的感受一下相对熵到第是怎样一回事。

假设，我们在火星上开展玉米种植试验，一个生长周期结束了，我们得到了玉米产量的数据，见图1。现在，我们需要把火星上的数据传送回地球，最好的结果就是按照数据原始的样貌进行传送。但是，假设现在数据传送的成本代价昂贵。虽然直接传送数据样貌最为准确，但是由于成本过于昂贵，我们难以承受这个代价。因此，我们就想，能不能使用一个模型来描述这些数据，这样只需传递模型和几个模型参数，我们就能得到玉米产量的大概分布，同时传送的成本也得以控制。

![假设数据的原始分布](./image_tSNE/原始分布.png)

假设，我们现在想用泊松分布和二项分布去近似原始数据，得到的结果见图2。

![模拟分布](./image_tSNE/模拟分布.png)

图2：原始分布，二项分布近似原始分布，泊松分布近似原始分布结果。

接着，我们利用相对熵（K-L散度）计算两种模型的信息损失量：
$$
D_{KL}(origin||binom)=\sum_{i=1}^np(x_i)log\frac {p(x_i)}{q(x_i)}=0.1597662
$$
$$
D_{KL}(origin||pois)=\sum_{i=1}^np(x_i)log\frac {p(x_i)}{q(x_i)}=0.201369
$$

所以，我们发现用二项分布近似原始分布的信息损失量比用泊松分布近似原始分布的信息损失量小，因此，当我们在考虑二项分布和泊松分布时，较优的一个选择是二项分布。

到这里，我们对信息熵和相对熵（K-L散度）这两个概念已经有了直观的认识，接下来，就进入本章的重点部分：t-SNE算法详解。

### t-SNE算法详解

#### t-SNE概述
t-SNE(t-distributed stochastic neighbor embedding，t分布-随机近邻嵌入)是一种非线性降维的算法，属于流形学习的范畴，可以把数据集中数据之间的高维欧式距离转变成条件概率来表示数据之间的相似度。

流形是局部具有欧几里得空间性质的空间。举个例子理解一下，例如比较经典的“瑞士卷”（见图3），数据是三维的，但其本质是一个二维流形。图中两个黑点之间的距离显然不能用欧式距离来衡量，如果用三维空间的欧氏距离来计算则它们的距离要比实际距离近得多，它们之间的实际距离应该是红色的这一条弧线。我们再举一个例子，如果你要测量北京到西安的距离，你可以拿一个缩小一定比例的地球仪，用卷尺经过地球仪表面上的这两点来测量它们之间的距离，然后再乘以相应的倍数，即可得到北京到西安的距离。同样的，你还可以把三维的地球仪展开成二维的地球，然后拿直尺直接测量北京到西安的距离。而这个三维地球仪到二维地图的展开，就属于流形学习，流形学习可以使欧式距离重新生效。

![瑞士卷](./image_tSNE/瑞士卷.png)

图3：“瑞士卷”

t-SNE算法的降维过程可以分为下面几个步骤：

1. 计算高维空间数据点的概率分布F1（欧式距离转换成高斯分布）；

2. 计算低维空间数据点的概率分布F2（用t分布随机初式化二维的点）；

3. 利用相对熵（K-L散度）衡量两种分布的差异，进行迭代，若F1与F2概率分布尽可能的接近则降维成功。

#### SNE算法原理

我们首先了解一下t-SNE的前身SNE的算法原理，因为这样我们会更加理解t-SNE相对于SNE带来的提升。我们以4个细胞，每个细胞有4个基因，构成一个$4\times 4$的矩阵为例（见表1），详细讲解一下SNE的每一步算法过程。

表1：$4\times 4$的矩阵，每一列代表一个基因，每一行代表一个细胞$FPKM_{i,j}$代表第i个细胞，第j个基因的表达值

|          | $gene_1$     | $gene_2$     | $gene_3$     | $gene_4$     |
| -------- | ------------ | ------------ | ------------ | ------------ |
| $cell_1$ | $FPKM_{1,1}$ | $FPKM_{1,2}$ | $FPKM_{1,3}$ | $FPKM_{1,4}$ |
| $cell_2$ | $FPKM_{2,1}$ | $FPKM_{2,2}$ | $FPKM_{2,3}$ | $FPKM_{2,4}$ |
| $cell_3$ | $FPKM_{3,1}$ | $FPKM_{3,2}$ | $FPKM_{3,3}$ | $FPKM_{3,4}$ |
| $cell_4$ | $FPKM_{4,1}$ | $FPKM_{4,2}$ | $FPKM_{4,3}$ | $FPKM_{4,4}$ |

**将欧式距离转化成概率分布**

根据我们假定的数据，每一个细胞都有四个基因表达值特征，我们可以根据此计算两两细胞之间的欧式距离。以$cell_1$为例，$cell_1$与$cell_2、cell_3、cell_4$之间的欧式距离计算见下：

$$
dis(cell_1,cell_2)=\sqrt{\sum_{x=1}^4(FPKM_{1,i}-FPKM_{2,i})^2}\\
$$

$$
dis(cell_1,cell_3)=\sqrt{\sum_{x=1}^4(FPKM_{1,i}-FPKM_{3,i})^2}
$$

$$
dis(cell_1,cell_4)=\sqrt{\sum_{x=1}^4(FPKM_{1,i}-FPKM_{4,i})^2}
$$

接着，我们用正态分布的公式转化$cell_1$ 与$cell_2、cell_3、cell_4$的距离：
$$
f(dis(cell_1,cell_2)) = \frac{1}{\sqrt{2\pi}\sigma}e^{-\frac{dis(cell_1,cell_2)^2}{2\sigma^2}}\\
f(dis(cell_1,cell_3)) = \frac{1}{\sqrt{2\pi}\sigma}e^{-\frac{dis(cell_1,cell_3)^2}{2\sigma^2}}\\
f(dis(cell_1,cell_4)) = \frac{1}{\sqrt{2\pi}\sigma}e^{-\frac{dis(cell_1,cell_4)^2}{2\sigma^2}}
$$
然后归一化，把距离变成概率:
$$
p_{cell_2|cell_1} = \frac {e^{-\frac{dis(cell_1,cell_2)^2}{2\sigma^2}}} {e^{-\frac{dis(cell_1,cell_2)^2}{2\sigma^2}}+e^{-\frac{dis(cell_1,cell_3)^2}{2\sigma^2}}+e^{-\frac{dis(cell_1,cell_4)^2}{2\sigma^2}}}\\
p_{cell_3|cell_1} = \frac {e^{-\frac{dis(cell_1,cell_3)^2}{2\sigma^2}}} {e^{-\frac{dis(cell_1,cell_2)^2}{2\sigma^2}}+e^{-\frac{dis(cell_1,cell_3)^2}{2\sigma^2}}+e^{-\frac{dis(cell_1,cell_4)^2}{2\sigma^2}}}\\
p_{cell_4|cell_1} = \frac {e^{-\frac{dis(cell_1,cell_4)^2}{2\sigma^2}}} {e^{-\frac{dis(cell_1,cell_2)^2}{2\sigma^2}}+e^{-\frac{dis(cell_1,cell_3)^2}{2\sigma^2}}+e^{-\frac{dis(cell_1,cell_4)^2}{2\sigma^2}}}\\
$$

同理，我们可以对每一个$cell_i$都算出以其为中心，其余$cell_j$与其距离的概率分布$p_{cell_j|cell_i},j\ne i$ 。例如，我们现在举的这个例子中，我们可以同样的算出：
$$
p_{cell_1|cell_2},p_{cell_3|cell_2},p_{cell_3|cell_2}\Rightarrow \sigma_{cell_2}\\
p_{cell_1|cell_3},p_{cell_2|cell_3},p_{cell_4|cell_3}\Rightarrow \sigma_{cell_3}\\
p_{cell_1|cell_4},p_{cell_2|cell_4},p_{cell_3|cell_4}\Rightarrow \sigma_{cell_4}
$$
对于这四个细胞，唯一的未知量就是$\sigma$，如果对于每一个细胞，我们都知道它的标准差，那么我们就能描述出高维空间上该细胞与其周围细胞的分布情况，如何估算每个细胞的$\sigma_{cell_i}$呢？这里我们就引入一个新的概念——困惑度（perplexity），这是一个基于信息熵计算出来的值。

**根据困惑度估计$\sigma$**

困惑度（perplexity）可以表示细胞的邻近个数，在t-SNE图上的直观反映是细胞点的分布是否紧凑，公式见3。perplexity设置越大，细胞分布越紧凑，一般情况下困惑度选择5-50。
$$
Prep(P_{cell_i})=2^{H(P_{cell_i})}\\
H(P_{cell_i})=-\sum_{j\ne i}p_{cell_j|cell_i}log(p_{cell_j|cell_i})
$$
于是，对于我们的示例来说，一旦我们定义了一个困惑度，也就是等式左边已经确定，那么唯一的未知量就是等式右边的$\sigma$，这样等式就变成了一个可解方程，我们就能计算得出每一个细胞特定的$\sigma$。这里，为了直观观察这一步骤的过程，我们还是以$cell_1$为例来看一遍如何计算$\sigma$：
$$
H(P_{cell_1})=-(p_{cell_2|cell_1}log(p_{cell_2|cell_1})+p_{cell_3|cell_1}log(p_{cell_3|cell_1})+p_{cell_4|cell_1}log(p_{cell_4|cell_1}))\\
Prep(P_{cell_1})=2^{H(P_{cell_1})}\Rightarrow 预设值：困惑度（perplexity）
$$
这样两个方程联立，我们就能解出$cell_1$的$\sigma_{cell_1}$，同理我们就能解出$\sigma_{cell_2}、\sigma_{cell_3}、\sigma_{cell_4}$ 。这样我们就完成了高维空间数据点概率分布的估计。

这里，根据我们之前介绍的信息熵，大家可以思考一下，在估计$\sigma$时，信息熵值的大小与$\sigma$具有怎样的关系？反应怎样的生物学意义？

提示：

1.信息熵越大，$\sigma$越小；

2.信息熵越大，代表$cell_i$临近的细胞个数越多。

**低维空间的正态分布近似**

当我们确定了高维数据的概率分布之后，利用正态分布初始化SNE的二维点，例如初始化低维数据点$x_1,x_2,x_3,x_4$分别对应高维空间上的$cell_1,cell_2,cell_3,cell_4$ 。我们同样可以计算类似的条件概率，以$x_1$为例：
$$
q_{x_2|x_1} = \frac {e^{-{dis(x_1,x_2)^2}}} {e^{-{dis(x_1,x_2)^2}}+e^{-{dis(x_1,x_3)^2}}+e^{-{dis(x_1,x_4)^2}}}\\
q_{x_3|x_1} = \frac {e^{-{dis(x_1,x_3)^2}}} {e^{-{dis(x_1,x_2)^2}}+e^{-{dis(x_1,x_3)^2}}+e^{-{dis(x_1,x_4)^2}}}\\
q_{x_4|x_1} = \frac {e^{-{dis(x_1,x_4)^2}}} {e^{-{dis(x_1,x_2)^2}}+e^{-{dis(x_1,x_3)^2}}+e^{-{dis(x_1,x_4)^2}}}\\
$$
同理，我们可以对每一个$x_i$都算出以其为中心，其余$x_j$与其距离的概率分布$Q_{x_j|x_i},j\ne i$ 。这样我们就在低维空间得到了我们样本点的概率分布，接下来，我们的目标就是希望高维空间和低维空间之间的分布尽可能的相同，这里我们就用到了之前讲解的相对熵（K-L散度）这一概念，计算过程见下（$i$最大值是4，只是因为我们举的例子只有4个细胞，实际情况$i$最大值等于细胞数目）：
$$
C=\sum_{i=1}^4D_{KL}(P_i||Q_i)=\sum_{i=1}^4 \sum_{j=1}^3 p_{j|i}log\frac {p_{j|i}}{q_{j|i}}
$$
这样我们的目标就是获得最小的$C$值，也就是获得最小的K-L散度，后面就是进行进行梯度优化，通过迭代，使低维空间的分布逼近高维空间的分布，最终确定SNE的二维点。一般默认梯度优化的迭代次数是1000。以上就是SNE的算法原理。


#### t-SNE相对于SNE的提升

上面的内容我们了解了SNE的算法原理，那么相对于SNE，t-SNE又做了哪些重要的优化呢？

**1. t-SNE解决了概率不对称问题**
 SNE高维情况：
 $$
 p_{j|i} = \frac {e^{-\frac{dis(i,j)^2}{2\sigma^2}}} {\sum_{k\ne i}e^{-\frac{dis(i,k)^2}{2\sigma^2}}}
 $$
 t-SNE高维情况：
 $$
  p_{ij}=\frac {p_{j|i}+p_{i|j}}{2n}
 $$

**2. t-SNE使用t分布作为降维后的概率分布**
SNE低维情况：
$$
q_{j|i} = \frac {e^{-{dis(i,j)^2}}} {\sum_{k\ne i}e^{-{dis(i,k)^2}}}
$$

t-SNE低维情况：
$$
q_{ij} = \frac {(1+{dis(i,j)^2})^{-1}} {\sum_{k\ne i}(1+{dis(i,k)^2})^{-1}}
$$

对于第一个优化我们直观上很好理解，因为，我们认为空间上两个点$(a,b)$的距离不论是$a\Rightarrow b$还是$b\Rightarrow a$都应该相等。那么我们为什么要用t分布来作为降维后的概率分布呢？它与正态分布有什么不同吗？

观察图4，在正态分布与t分布相交前，对于同一个概率值（y轴坐标），我们发现t分布的距离总是小于正态分布的距离（dis_1 < dis_2)；在正态分布与t分布相交后，对于同一个概率值（y轴坐标），我们发现t分布的距离总是大于正态分布的距离（dis_3 > dis_4)。所以由此我们可以了解到 t分布使得相近的细胞更加紧凑，较远的细胞更加疏远。换句话说，t-SNE倾向于保留数据中的局部结构。距离较远的两个细胞在t-SNE图上的表示可能失真。

![distribution](./image_tSNE/distribution.png)

图4：正态分布与t分布。

#### t-SNE的优缺点

**优点**

- 非常优秀的降维可视化方法

**缺点**
- 基本只用于可视化
- t-SNE倾向保留局部结构，有时候会“只见数木不见森林”
- t-SNE结果中距离没有太大意义，因为都是计算的概率
- t-SNE训练速度比较慢

**特点**
- 受初值影响

### R语言实战

这一部分我们就进入t-SNE实战环节，代码如下:

```R
# t-SNE需要使用Rtsne这一个包
library(Rtsne)
##加载t-SNE需要的数据
load("C:/Users/Jay/Desktop/t-SNE/data/GTEx.RData")
accession.df = read.csv(file="C:/Users/Jay/Desktop/t-SNE/data/GTEx_accession_table.csv")
accession.df
annotation.df = read.csv(file="C:/Users/Jay/Desktop/t-SNE/data/GTEx_v7_Annotations_SampleAttributesDS.txt",header = T,sep = "\t")
annotation.df
tissue_info = as.character(annotation.df$SMTS[match(accession_id_vec,annotation.df$SAMPID)])

##删除第一列基因名字，第二列描述信息
GTEx.TPM.gene.mat = GTEx.TPM.gene.mat[,c(-1,-2)]
##对每一行基因计算方差，筛选高变异的基因进行t-SNE运算，减少运算负担
SD.vector = apply(GTEx.TPM.gene.mat,1,FUN=function(x){sd(x)})
##依靠方差结果对GTEx.TPM.gene.mat数据进行排序
GTEx.TPM.gene.mat.sort = GTEx.TPM.gene.mat[order(SD.vector,decreasing = T),]
##查看尾部数据是否是变异较小的
tail(GTEx.TPM.gene.mat.sort)
##筛选前3000高变异基因
GTEx.TPM.gene.mat.log2.top3000 = GTEx.TPM.gene.mat.sort[1:3000,]

set.seed(20200503)
##行是观测，列是变量。如果把基因当做变量，那么每一列就是一个基因，每一行就是样本
##dims 输出的维度
##perplexity设置5-50
tSNE_res = Rtsne(t(GTEx.TPM.gene.mat.log2.top3000),dims = 3,perplexity = 10,pca = T)

##分别用生成t-SNE的三个维度进行可视化
library(ggplot2)
##首先把信息都综合到一个data.frame中
tSNE_res.df = as.data.frame(tSNE_res$Y)
colnames(tSNE_res.df) = c("tSNE1","tSNE2","tSNE3")
tSNE_res.df$tissue = tissue_info
##可视化tSNE1与tSNE2
ggplot(data = tSNE_res.df, aes(tSNE1,tSNE2,color=tissue)) + 
  geom_point()  + 
  geom_text(aes(label=tissue)) + 
  theme_bw()
##可视化tSNE1与tSNE3
ggplot(data = tSNE_res.df, aes(tSNE1,tSNE3,color=tissue)) + 
  geom_point()  + 
  geom_text(aes(label=tissue)) + 
  theme_bw()
##可视化tSNE2与tSNE3
ggplot(data = tSNE_res.df, aes(tSNE2,tSNE3,color=tissue)) + 
  geom_point()  + 
  geom_text(aes(label=tissue)) + 
  theme_bw()
```

<!--chapter:end:0080-statistics.Rmd-->

# 生物信息学平台的构建 {#build_up_platform}

## Windows、Linux和MacOS的选择

生信分析的平台主要分为个人电脑和服务器。服务器几乎全部使用Linux，发行版以Cent OS和Ubuntu Server为主，前者更多。个人电脑则Windows、Mac OS和Linux均有，本书主要介绍Windows和Linux的使用，而Mac OS的使用和Linux较为接近，仅有较少的差别。

而个人电脑操作系统的选择，在Windows 10推出WSL（Windows Subsystem for Linux）前以Linux和Mac最为方便。因为大多数开源生信软件仅会提供Linux版的二进制包或者是源代码。而源码编译安装的测试一般只在Linux下进行，Mac因为与Linux的接近而编译安装较为容易。Windows有着与Linux较大的差别，编译安装步骤常常存在很大的问题，无法简单使用软件开发者提供的编译流程。

但是WSL的出现使得在Windows下也可以获得十分接近Linux命令行环境的操作和兼容性体验。大多数人不用特别选择个人电脑的操作系统，原来使用Windows的只需要升级到Windows 10的最新版本即可。

WSL第一代使用了二进制翻译Linux API的方式建立了兼容层，兼容性已经较为优秀，但是在I/O密集型任务上存在效率问题，限制了生信分析的实际进行。WSL第二代则使用了轻量高效的虚拟机运行真正的Linux内核，具有高度的兼容性，也解决I/O密集型任务效率问题，可用于绝大多数生信分析的场景。操作系统不再成为限制生信分析的关键环节。

## Linux的一些基本概念

### Linux的环境变量

Linux下的可以通过修改`~/.bashrc`来设置用户环境变量，修改`/etc/.bashrc`来设置系统环境变量。绝大多数情况下修改系统环境变量即可。具体添加到`.bashrc`的内容可以参考下方的代码。第一行是在一个已有的环境变量中添加值（Linux中一个环境变量下的多个值以冒号分隔），第二行则是创建一个并赋值一个新的环境变量或是修改一个已有环境变量的值。

```bash
export PATH="/export/apps/JAVA/jdk1.8.0_111/bin:$PATH"
export JULIA_PKG_SERVER="https://mirrors.bfsu.edu.cn/julia/static"
```
修改完`.bashrc`文件后如果想到马上生效而不是重新启动命令行，可以使用`source`执行对应文件。比如设置用户环境变量时使用`source ~/.bashrc`即可。

### APT

apt（Advance Packaging Tool）是Debian系Linux发行版的默认包管理工具，于对包括系统本身在内的升级安装等管理操作。

**apt和apt-get命令**

`apt`是2014年正式发布的心得apt包管理工具的命令，相较于`apt-get`系列命令它更为简洁易用。

**apt取待的apt-get系命令**

| apt 命令 | 取代的命令 | 命令的功能 |
|:----- |:----- | ----- |
| apt install | apt-get install | 安装软件包 |
| apt remove | apt-get remove | 移除软件包 |
| apt purge | apt-get purge | 移除软件包及配置文件 |
| apt update | apt-get update | 刷新存储库索引 |
| apt upgrade | apt-get upgrade | 升级所有可升级的软件包 |
| apt autoremove | apt-get autoremove | 自动删除不需要的包 |
| apt full-upgrade | apt-get dist-upgrade | 在升级软件包时自动处理依赖关系 |
| apt search | apt-cache search | 搜索应用程序 |
| apt show | apt-cache show | 显示装细节 |

**新的apt命令**

| 新的apt命令 | 命令的功能 |
| ----- | ----- |
| apt list | 列出包含条件的包（已安装，可升级等） |
| apt edit-sources | 编辑源列表 |

**apt镜像设置**

apt默认的镜像在国内的访问速度是较慢的，所以设置一个国内的镜像是必要的。这里推荐北京外国语大学的开源软件站。其帮助信息完善，Ubuntu的镜像设置帮助文档地址为(https://mirrors.bfsu.edu.cn/help/ubuntu/)。

可以在文档中选择你具体使用的Ubuntu版本以获取对应的软件源地址。备份原先的软件源配置文件后即可更改配置文件。修改完成后执行`sudo apt update`命令刷新索引既可生效。

![image](./image_platform/4bcc5c9c-49e7-465a-91f8-4e1ed8512e7c.png)

### yum

yum（Yellow dog Updater, Modified）使用RedHat系（Red Hat、Cent OS、Fedora）发行版的默认包管理工具。

**常用yum命令**

| 命令 | 功能 |
| ----- | ----- |
| yum install | 安装软件包 |
| yum update | 更新软件包 |
| yum check-update | 检查是否有可用更新 |
| yum remove | 删除指定的软件包 |
| yum list | 显示软件包的信息 |
| yun search | 查找软件包的信息 |
| yum info | 显示指定软件包的信息 |
| yum clean | 清理过期缓存 |

**yum镜像**

我们依然十分推荐北外的相关镜像，访问（https://mirrors.bfsu.edu.cn/help/centos/ ）就可以进入CentOS镜像的帮助页面，选择你的系统版本即可获得详细的镜像配置文件内容和详细的指引。

![image](./image_platform/4023954c-93ad-4f0d-a221-b5b3762f5f14.png)


## Windows命令行环境搭建

Windows和Linux、Mac OS在操作上有着较大区别，但是掌握特点后也可以很好地完成任务。

### 环境变量

环境变量是在操作系统中一个具有特定名字的对象，它包含了一个或者多个应用程序所将使用到的信息。比如日常我们最初接触的Path环境变量。当你在命令行输入程序名称而不包括完整路径时，系统除了在当前目录下查找还会在Path环境变量中的路径进行查找。还有一些软件会用环境变量存储少部分主要设置项的值，比如Julia语言的官方编译器以环境变量JULIA_NUM_THREADS来设置线程数。

Windows的环境变量主要分为：系统、用户、进程（只在当前进程中生效）。设置位置包括系统的“高级设置”（具体内容存储于注册表中）和PowerShell的系统和用户配置文件。系统高级设置的环境变量可以被系统内运行的所有软件读取，而PowerShell配置文件的环境变量只在启动PowerShell时生效。

### Windows高级设置修改环境变量

首先，我再次推荐还没有升级到Windows10的尽快升级。如果你已经是Windows10了，直接在任务栏搜索框中输入“高级设置”，搜索结果中就会有“查看系统高级设置”的结果，点击后就进入到系统高级设置了。如果你还没有升级到Windows10，那么右击“计算机”选择“属性”，弹出窗口内可以找到“高级设置”的入口。

高级设置的窗口内就可以看到环境变量设置的入口。

![image](./image_platform/bfa4fe1a-87f9-49ef-993d-f475efb42382.png)

在弹出窗口中就可以选择对应的的用户或者系统环境变量进行新建、编辑或删除环境变量了。

![image](./image_platform/7dedbf76-f75e-42f6-b06d-b71ce194456f.png)

#### 编辑环境变量

比如这里选择用户变量的Path然后选择“编辑”，就会弹出对应的编辑窗口。“新建”就是添加一个新的路径到Path环境变量中；“编辑”为修改当前Path环境变量下的某个路径；“浏览”则可以通过“浏览文件夹”窗口选择路径；“删除”则可以删除已有的；“上移”和“下移”调整具体路径的优先度，下方的优先度更高；“编辑文本”则是在一个输入框编辑，各个路径之间以英文分号分隔，一般情况并不适用主要用在完全复制一个用户的单个环境变量的多个值时。

![image](./image_platform/67c80585-5b6e-4d27-8f15-feab73fdbbd0.png)

#### 新建环境变量

在环境变量设置窗口对应区域点击“新建”按钮即可新建用户或系统环境变量。变量值可以有多个，每个变量值之间用英文分号分隔。两个“浏览”按钮分布使用浏览窗口选择目录或文件。

![image](./image_platform/d099007d-fed0-4bb2-b983-500d9c36af27.png)

新建或编辑完环境变量并确认后，回到”环境变量“确认后就修改完成。初期相关读取环境变量的程序即可生效。如果仍未生效，则注销用户后重新登陆即可。

### PowerShell配置文件设置环境变量

Windows中的PowerShell包括系统内置的Windows PowerShell和可自行安装的PowerShell Core，个人推荐安装PowerShell Core。

![image](./image_platform/1230650c-9088-4283-8dd8-81f43bf30c6a.png)

不论你启动Windows PowerShell还是PowerShell Core（Windows PowerShell可以右击开始按钮的菜单启动，PowerShell Core安装后会在应用程序列表中出现），都可以用变量查看配置文件路径。`$profile.CurrentUserAllHosts`用于查看用户配置文件，只作用于当前用户。`$profile.AllUsersAllHosts`用于查看系统配置文件，作用域当前系统的所有用户。

![image](./image_platform/905328cc-a557-45a4-9792-eebf4e47f9d2.png)

![image](./image_platform/35fc36d7-1daa-4713-8c9d-94231f3a25da.png)

当然在修改配置文件之前需要对PowerShell的执行策略进行更改，否则配置文件是无法被载入的。右击开始按钮在菜单中选择“Windows PowerShell (管理员)”，弹出窗口中执行`Set-ExecutionPolicy RemoteSigned`命令。

查找到配置文件路径后就可以就通过编辑配置文件添加或修改环境变量。

```bash
$env:TEST="D:\\"
$env:TEST=$env:TEST+";E:\\"
$env:Path=$env:Path+";F:\\"

```

上面是一个例子，第一行新建了一个名为TEST的环境变量，并设置其值为"D:\\"，如果TEST环境变量已存在，则会覆盖原值。第二行在原值基础上添加一个值"E:\\"。所以第三行我们也以类似的方法在现有的Path环境变量下添加一个值，以防覆盖原有的值。修改完配置文件后只要重启PowerShell即可生效。

## WSL

微软官方文档的解释很好的解释了WSL（Windows Subsystem for Linux）为何。

> 适用于 Linux 的 Windows 子系统可让开发人员按原样运行 GNU/Linux 环境 - 包括大多数命令行工具、实用工具和应用程序 - 且不会产生传统虚拟机或双启动设置开销。

### 安装WSL

安装WSL前请先将Windows10更新到最新版。然后以管理员权限启动PowerShell，依序执行以下两个命令后重新启动计算机。

#### 启用“适用于 Linux 的 Windows 子系统”可选功能

```bash
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
```

#### 启用“虚拟机平台”可选功能

```bash
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```

#### 设置WSL2为默认版本

以管理员权限启动PowerShell，执行以下命令。

```bash
wsl --set-default-version 2
```

#### 安装发行版

访问(https://aka.ms/wslstore)，启动应用商店对应页面选择一个你中意的发行版即可，或者直接在应用商店搜索`Linux`，可以找到更多发行版。

![Microsoft Store 中的 Linux 分发版的视图](https://docs.microsoft.com/zh-cn/windows/wsl/media/store.png)

#### 创建账户和密码

安装完成发行版后首次启动时会要求你创建用户名和密码。

![Windows 控制台中的 Ubuntu 解包](https://docs.microsoft.com/zh-cn/windows/wsl/media/ubuntuinstall.png)

### Windows Terminal

> Windows 终端可启用多个选项卡（在多个 Linux 命令行、Windows 命令提示符、PowerShell 和 Azure CLI 等之间快速切换）、创建键绑定（用于打开或关闭选项卡、复制粘贴等的快捷方式键）、使用搜索功能，以及使用自定义主题（配色方案、字体样式和大小、背景图像/模糊/透明度）。

在应用商店搜索`Windows Terminal`后安装即可。

![](./image_platform/ce36916b-bbee-4d15-8a3e-193a0e1ae26e.png)

## OpenSSH for Windows

SSH命令是链接服务器很重要的工具。Linux和Mac都是自带且启动SSH命令的，但是Windows长期以来都不自带SSH命令，直到Windows 10。Windows 10最新版目前自带OpenSSH客户端和服务器端，但是默认情况下都不启用。在任务栏搜索框中输入“可选功能”，结果中会出现“添加可选功能”，点击即可进入。也可以通过“Windows设置→应用→可选功能”进入。

![](https://images-cdn.shimo.im/ZZob1QhLKmoyhnlk/Snipaste_2018_09_09_21_16_25.png!original)

![](./image_platform/c575c9fa-1e74-4fc5-99e4-465792565047.png)

点击“添加功能”进入到添加功能的页面，选择“OpenSSH客户端”，点击“安装”按钮即可开始安装，不长的一段时间后就安装完毕了。

![](https://images-cdn.shimo.im/2PrwPwoL75oUjCsd/Snipaste_2018_09_09_21_20_52.png!original)

## Anaconda and bioconda

Anaconda是Anaconda公司开的一个Python发行版，集成的除了Python本体外还包括大量科学计算的常用模块和Anaconda公司开发的Python模块和环境管理器conda。conda管理器的对环境和包管理的易用性要超过Python本地自带的功能，而且还可以管理非Python的模块（Perl、Java、R……）。对于生信分析人员，Bioconda这个conda源更是收入了大量生信分析软件，大大降低了生信软件的安装复杂度，一条命令即可，不需要手动编译和root权限。

在你已经添加了相应软件源的情况下，安装包只要用下面的命令即可(这里演示的是IPython的安装)。

```bash
conda install ipython
```

Anaconda的管理器默认会从Anaconda公司的官方服务器下载模块，而且默认只有一个default源。其他一些常用源像Bioconda也需要用户自己添加。这个时候手动添加所有常用源的国内镜像就十分有必要。

### Anaconda的安装

这些镜像网站本身也会提供Anaconda的安装包。直接从镜像站下载安装包就免去官网下载可能的卡顿。需要特别提到的是，镜像站除了提高标准版的Anaconda安装包外还会提供Miniconda的安装包。这是一个精简的版本，体积相比标准版要小不少，只包括Python和conda管理器，包需要自行通过`conda`和`pip`安装。在一些磁盘有限的情况下可以选择Miniconda。

Anaconda给Mac提供的是pkg和sh安装包，给Windows提供的是exe安装包，而给Linux只提供sh安装包。pkg和exe双击安装即可，而sh安装包需要通过命令行执行。即可通过图形界面启动sh安装包，很多设置也要在随之启动的终端下进行。

在这里也要特别提醒的是安装过程中pkg和exe安装过程中会有一部让你设置是否要将Anaconda的路径加入到环境变量中，一定要勾上。而sh安装的最后一部也会询问是否进行初始化（init），要记得输入`yes`。这些选上之后，只要重启终端环境变量即可生效，就可以正常使用conda管理和相关的包。

### Anaconda镜像的设置

目前国内最完善的公开Anaconda镜像就是清华大学的镜像(https://mirrors.bfsu.edu.cn/anaconda/ )， 不过国内部分地区访问清华大学镜像有时候不稳定，可以考虑使用北京外国语大学的镜像(https://mirrors.bfsu.edu.cn/help/anaconda/ )，其由清华开源软件协会负责维护内容基本保持一致，但是访问的稳定性很多时候更为优秀。帮助信息提到的存放`.condarc` 配置文件的用户目录，在Linux下使用`cd ~`命令进入；在Windows下使用`cd $env:USERPROFILE`命令进入，或者在资源管理地址栏输入`%USERPROFILE%`后回车进入。

我们依然推荐你通过上面的链接详细查阅他们的帮助信息，写入在`custom_channels`范围的镜像地址在使用时只有指定c参数才会生效。例如如果按帮助页面的信息设置Anaconda配置文件，使用`conda install seqkit`命令会按照失败，需要使用`conda install -c bioconda seqkit`命令。

![image](./image_platform/b2a4b20d-cbc1-451d-aa93-760b5274fe37.png)

### Anaconda环境的管理

为了防止不同的依赖之间相互冲突造成bug，除了最核心的常用组件，通常会为了每一类项目单独建立一个独立的环境。使得不同项目之间的模块可以版本不同。比如优势需要不同版本的Python或者R。

**创建环境**

你可以指定环境的名称，后面再赶上环境中一个或几个包的版本，也可以只有名称没有其他参数。这时新建的环境里就不会预装任何包

```bash
conda create -n py2 python=2
```

指定环境名称的创建方式会把环境相关文件放在Anaconda的安装目录下，但是有时候你需要将环境相关文件放在制动的路径。这个时候你就可以通过`p`参数来指定conda环境的路径。比如下面就是一个指定环境目录为`/home/test_conda`并指定环境中的Python版本号为3.4。

```bash
conda -p /home/test_conda python=3.4
```

**删除环境**

我们同样可以通过参数来指定特定名称或路径的环境。

```bash
conda remove -n py2 --all
conda remove -p /home/test_conda --all
```

### mamba

本书在这里还要特别提到一个C++的conda管理器实现：mamba。Anaconda千好万好，但是却有一个很致命的问题：计算依赖和扫描各个源的速度都较慢。当你已安装的包较多时，计算依赖和扫描源的时间都会不短。这个时候mamba就是一个拯救者的角色。通过C++的高效性，加上计算依赖和扫描源时的多线程并行，可以让原本耗时巨大的安装过程时间缩短十倍到几十上百倍。所以这里建议大家在安装完成Anaconda的第一时间就安装mamba。

安装mamba也很方便，直接通过`conda install -c conda-forge mamba`命令即可。安装完成后，所有出现`conda`命令的地方把单词替换成`mamba`即可。

## Jupyter

Jupyter是一个非盈利开源项目，2014年从IPython项目诞生。从诞生依赖不断发生，基于网页支持跨几乎所有编程语言的交互式数据分析与科学计算。最早的项目是IPython Notebook，随着发展改名Jupyter Notebook。而现在Jupyter项目的核心是JupyterLab。如果你之前是Jupyter Notebook的用户，迁移到JupyterLab的学习成本很低。第一眼看上去最大的变化可能就是多标签和侧边栏。当然由于相对于Jupyter Notebook，JupyterLab的历史还短一些，一些主题和个别扩展还不支持JupyterLab。但是随着JupyterLab正式版来到2.X时代，扩展生态已经相当发达。

### 安装JupyterLab

安装JupyterLab非常简单，Pypi和Anaconda都有收录。这里再度建议大家使用C++实现的conda管理器mamba进行安装

```bash
pip install jupyterlab # pypi安装
conda install jupyterlab # anaconda安装
mamba install jupyterlab # mamba安装
```

### 内核安装

JupyterLab安装时只支持Python，如果需要支持其他语言，需要自己安装相应的内核。例如R语言需要安装R包`IRkernel`，然后在R交互模式中使用`IRkernel::installspec()`命令注册内核到JupyterLab。而Julia语言则需要安装Julia包`IJulia`，然后通过`build IJulia`命令来注册内核。

### 本地和远程使用

JupyterLab的本地启动十分简单，启动一个终端（Windows下可以选择PowerShell，或者通过Windows Terminal使用某个终端），切换到你需要进行分析的目录。Jupyter只可以读取启动时的目录及其子目录下的文件。当进入到需要的目录是，在终端中使用`jupyter lab`命令就可以启动JupyterLab。默认浏览器这时会自动启动，并打开JupyterLab的页面。

而远程使用服务商的应用会复杂一些。需要先在本地的终端中使用`ssh`命令将服务器的客户端的某特定端口映射到本地计算机。执行完下面的命令后，会登录远程服务器，再使用`jupyter lab`即可启动远程服务器上的JupyterLab。在本地浏览器中访问`127.0.0.1:1234`即可链接服务器的8888端口。（username是你在服务器上的用户名，serverip为服务器IP地址。1234为希望的本地端口，8888则为远程服务器的端口。）

```bash
ssh username@serverip -L 127.0.0.1:1234:127.0.0.1:8888
```

这里还需要提醒大家，有时候因为服务器上已经有其他用户，或者你之前启动了一个JupyterLab还未关闭，远程端口可能不会是8888。所以这里其实更推荐大家，先用ssh登录远程服务器（可以使用某些ssh软件比如MobaXtrem，也可以用`ssh`命令）启动JupyterLab，通过启动时的提示信息查看端口号，由此更改下面映射命令中远程服务器端口。

## R and Rstudio	
R语言也是生信分子中一个极为重要的编程语言。R语言官方的软件源CRAN中有着大量数据分析和生信领域的相关包。Bioconductor项目更是集中了大多数生信领域的R包。

### R-base的安装和CRAN镜像设置

R-base的安装包可以通过CRAN的镜像站点获得(https://mirrors.bfsu.edu.cn/CRAN/ )，Windows和Mac根据你自己的操作系统点击链接，可以进入获取二进制安装包的页面。

![](image_platform/68cfe7a0-c604-448b-ba4e-b5d4d7662919.png)

![](image_platform/5ec3d53f-9a6b-46f4-978c-25d005b35ea4.png)

![](image_platform/6da0a303-f5d0-4cc3-96a4-3601c649742e.png)

Linux用户的话，有管理员权限的话建议使用系统的包管理器安装。如果没有管理员权限也不要紧，使用Anaconda即可。使用`conda install -c conda-forge r-base`命令就可以完成R-base的安装。

而CRAN的镜像设置需要进入R的用户home目录，可以在R的交互模式下通过命令`path.expand("~")`获取。

![](image_platform/9abb65cf-e93e-4722-a9f7-3c346e09c565.png)

获取R语言环境的home路径后，进入到该路径。查看路径下是否已经存在`.Rprofile`，如果没有则新建一个空白的即可。随后在`.Rprofile`文件末尾加入`options("repos" = c(CRAN="https://mirrors.bfsu.edu.cn/CRAN/"))`，保存后会在新启动的R环境中生效。

### Rtools

Bioconductor和CRAN上提供的R包绝大部分都提供Windows平台下的二进制包，安装过程无需编译。但因为二进制包的更新一般晚于源码包的更新，且个别R包不提供二进制包，所有还是存在需要编译安装的情况。这个时候就需要R官方所提供的编译器集合Rtools。

访问（https://cran.r-project.org/bin/windows/Rtools/）即可获得安装包。要注意的是要根据自己系统的位数选择对应的安装包，以及Rtools页面提供的目前是Rtools40，仅适用于R 4.0及更新的版本。如果你还在使用R 3.X的版本，需要访问历史版本页面（https://cran.r-project.org/bin/windows/Rtools/history.html）下载对应的版本。

![](image_platform/e67610e2-b16a-4c9d-ae9d-e8bbd0698714.png)

安装完Rtools后仍需修改R环境变量配置文件以使R能够识别的Rtools的路径，在需要时调用相关编译器。可以参照上一节中的`path.expand("~")`获取R的用户home目录，然后在该目录下编辑`.Renviron`文件，添加下面的内容。

```r
PATH="D:\\Program Files\\rtools40\\usr\\bin;${PATH}"
# 上面分号前的内容是Rtools安装目录下编译器所在路径，
# 应根据Rtools安装目录进行修改。
# 分号后的内容是表面是代表之前已有的PATH环境变量内容，
# 以免覆盖原有环境变量内容。
```

设置完R环境变量后应该保存文件，然后重启R的交互环境。然后在交互环境中使用语句`Sys.which("make")`验证是否设置成功，如果成功则会出现Rtools目录的`make.exe`的路径。如果设置成功，以后在出现源码包版本高于二进制包版本或R包吴源码包版本的情况，R就会提醒你是否进行编译安装。你可以使用语句

`install.packages("Rcpp", type = "source")`源码编译安装`Rcpp`包测试一下。

![](image_platform/d3b3bee0-3edf-4c48-b876-19fce8883633.png)


## Julia

Julia是一门很新的语言，2018年8月8日才正式发布1.0版。算是迈入了相对成熟的阶段。它是一门动态类型语言，语法规则简单，类似Python；它编译运行，运行效率很高，类似C++/C；对正则支持良好，类似Perl……

Julia对并行和分布式也支持良好，比如一个多线程的for循环只要像下面一样在原有的for循环代码上简单地加上`@threads`宏。

```julia
Threads.@threads for i = 1:1000
    ago_sdf = cm_df[i,:]
end
```

当然，它也非尽善尽美，仍然存在不足：

1. 生物信息学领域生态相对不足。虽然BioJulia项目已经初具规模，提供了不少高质量的Julia包，但是和有着长久积累的R和Python而言还差异巨大。
2. 因为需要进行编译，所以运行前存在“预热”时间，并不适合本身运行时间就很短的任务，否则反而有可能导致效率下降。

### Julia基础环境搭建

#### Julia的安装

Julia语言的安装相对来说是很友好的：Mac下提供了二进制安装包，Linux下提供了解压后即可用的压缩包，Windows下则同时提供了两类安装包。下载的地址，国外的用户建议直接上官网（https://julialang.org/downloads/），而国内用户我们依然建议使用已经推荐了很多次的北外镜像（https://mirrors.bfsu.edu.cn/julia-releases/bin/）。

使用二进制安装包或解压可用的安装包安装后，要记住把Julia可执行程序的所在目录添加到环境变量PATH中。比如现在我的Julia安装在`D:\Program Files\Julia-1.5.2`中，需要添加到环境变量PATH中的就是`D:\Program Files\Julia-1.5.2\bin`。具体的添加方法请查看本章前面的部分。

#### Julia的REPL

Julia带有一个交互式命令行环境REPL（read-eval-print loop），它内置于`julia`可执行文件中。其允许简单快捷地执行Julia语句，同时具有可搜索的历史记录、tab补全功能、help和shell模式以及一些实用的快捷键。只要不带参数地执行`julia`可执行文件（Julia可执行程序的所在目录添加到环境变量PATH中后，在终端中执行`julia`命令即可）或着双击执行`julia`可执行文件就可以启动REPL。

Julian模式：REPL的默认操作模式，可以快捷执行Julia语句。

pkg模式：包管理模式，在默认模式下光标位于行开头时输入]（英文右侧方括号）进入。

shell模式：命令模式，在该模式下可使用系统命令。

help模式：帮助模式，可以在该模式下查看各种帮助信息。例如可以在help模式下使用`if`命令查看if语句的帮助信息，使用`@time`查看`@time`宏的帮助信息。

#### Julia的设置

Julia的各种自定义设置都是通过环境变量进行的。其有两类方式进行修改。一是通过更改系统或当前用户的环境变量进行，Julia的线程数环境变量`JULIA_NUM_THREADS`和Julia仓库路径环境变量`JULIA_DEPOT_PATH`等少数环境变量只能通过此种方式进行修改。二是通过修改Julia参考路径下的`config`目录下的`startup.jl`文件内容设置其他大部分Julia设置环境变量。例如Julia包服务器地址环境变量`JULIA_PKG_SERVER`就可以通过在添加语句进行设置。例如可以在该文件中添加一行`ENV["JULIA_PKG_SERVER"] = "https://mirrors.bfsu.edu.cn/julia/static"`将包服务器设置为北外开源镜像站的地址。特别提醒，仓库路径也是存放二进制依赖、包原始文件、包预编译文件等属于当前用户的Julia环境数据。所以如果你想自定存放这些文件的地方就只能通过系统环境变量或者当前用户环境变量设置环境变量`JULIA_DEPOT_PATH`的值。如果不进行自定义设置，则仓库路径为当前用户的用户目录下的`.julia`目录。

#### Julia包的管理

Julia的使用REPL的pkg模式进行包管理。在pkg模式下，`add`命令按照包，`up`命令升级包，`rm`命令卸载包，`status`查看已安装包的状态。例如可以在pkg模式下用`add IJulia`命令安装IJulia包。

#### 开发环境配置

Julia的开发环境主要有三种，JupyterLab、Visual Studio Code和基于Julia的Pluto。

**JupyterLab的Julia环境配置**

Julia本体安装完成后，再安装IJulia包，IJulia包安装好后，执行`build IJulia`目录进行初始化即可将Julia内核添加至JupyterLab。

![](image_platform/851ad659-2dd4-41f8-aa76-97f13e1a53c3.png)

**Visual Studio Code的Julia环境配置**

Visual Studio Code可以通过安装Julia扩展快捷地获得对Julia的支持。安装后还需要修改VS Code设置中的`julia.executablePath`设置项，设置`julia`可执行文件的完整路径。

![](image_platform/53848068-fc53-4edc-ba71-dbfb487ce804.png)

![](image_platform/c80e763e-4e12-4cf1-9723-491c00946aa5.png)

**Pluto环境设置**

Pluto是一个基于Julia的轻量、易用且具有反应式特性（当改变一个函数或变量时，Pluto会自动更新所有受影响的Cell。）的交互式notebook。安装Pluto只要通过pkg模式安装`Pluto`包即可。启动则在REPL默认模式下使用以下命令即可。

```julia
import Pluto
Pluto.run()
```

## Perl

Perl作为一个生信分析领域上有着大量积累的脚本语言，你完全可以不用学习从头编写Perl脚本，但是很可能你会需要使用别人的Perl脚本，或者使用一些基于Perl的生信分析软件。所以掌握Perl环境的搭建就是很有必要的。

感谢十分强大的Anaconda以及收录了大部分生信相关Perl模块的Bioconda和conda-forge软件源，对于我们来说搭建Perl环境是相对很简单的。首先你要确认你按照本书之前的部分为Anaconda添加了Bioconda和conda-forge源。那么就可以简单地在终端中使用`conda install -c conda-forge perl`命令安装Perl。当然如果你所使用的分析软件或者Perl脚本如果不依赖第三方模块，其实也可以直接使用Linux和MacOS自带的Perl。

安装Perl第三模块会稍稍麻烦点，因为Bioconda和conda-forge收录的模块的名字形式稍稍和Perl官方源略有不同。你可以使用网站（https://anaconda.org/）进行搜索，比如查找bioperl模块可以搜索`bioperl`，就可以找到相应的模块名称和安装命令。

![](image_platform/8b0517b5-57cc-449a-886a-035b4b529dcc.png)

![](image_platform/4be6947e-fe2f-449e-9b47-8d2830221e1f.png)


## 其他内容

<!--chapter:end:0090-build_up_bioinfo_platform.Rmd-->

