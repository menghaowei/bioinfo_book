#!/usr/bin/env python3
"""One-time recorded editorial corrections, run after migrate_sources.py.
Normal build/CI NEVER runs this migration script or overwrites author text.
"""
from pathlib import Path
import re,json
ROOT=Path(__file__).resolve().parents[1]
changes=[]
def edit(slug,old,new,reason):
 p=ROOT/'manuscript'/slug
 s=p.read_text()
 if old not in s: raise ValueError(f'Missing expected source: {slug}: {old[:70]}')
 s=s.replace(old,new);p.write_text(s)
 changes.append({'file':str(p.relative_to(ROOT)),'reason':reason,'before':old,'after':new})

f='01-learning-and-study-design.md'
edit(f,'2006年Illumina公司开发了第二代测序技术（Next Generation Sequencing，NGS），随着NGS技术的推广','随着第二代测序技术（Next Generation Sequencing，NGS）的发展和推广','避免把二代测序的发明归于单一公司和单一年份')
f='03-sequencing-and-data-formats.md'
edit(f,'其实，二代测序比较常见的有罗氏454测序，Illumina等。但目前最为常用的NGS技术就是illumina测序技术，它能够保证在几十个小时内产生几百G甚至上T的测序数据，完全能够满足高通量测序的通量要求。并且其测序准确程度也是完全能够保证。我在这里很决断的说，在目前高通量测序的科研领域，Illumina测序绝对是主导地位的，几乎没有其他的公司可以撼动它。因此，我们这篇文章就Illumina测序的原理做一个比较详细的介绍，希望对大家入门生物信息学有所帮助。','二代测序的发展过程中出现过 Roche 454、Illumina 等不同技术路线。本节以 Illumina 的边合成边测序为例，解释文库、簇和测序循环如何产生 reads。图中的 X Ten 属于原稿写作时期的仪器示例；不同平台的通量、读长和流动槽结构应查对应型号的说明书。','删除过时的市场与性能绝对断言，保留历史示例')
edit(f,'**flowcell** 是指Illumina测序时，测序反应发生的位置，1个flowcell含有8条lane','**flowcell**（流动槽）是测序反应发生的位置；lane 数目随仪器和流动槽型号变化','flowcell 的 lane 数不是固定值')
edit(f,'**lane** 每一个flowcell上都有8条泳道，用于测序反应，可以添加试剂，洗脱等等','**lane**（泳道）是流动槽内的反应区域，具体结构取决于平台','同上')
edit(f,'**reads** 指测序的结果，1条序列一般称为1条reads','**read** 指一次读取获得的序列，复数为 reads','单复数术语')
edit(f,'**双端测序** 只一条序列可能比较长如500bp，我们可以两端每端各测150bp','**双端测序** 指从同一插入片段的两端分别读取，例如一个 500 bp 的插入片段两端各读 150 bp','双端测序定义')
edit(f,'**junction** 上面说的双端测序，中间会留有200bp测不到的东西，我们叫junction','**未读取区间** 在上述例子中，中间还有约 200 bp 未被两端的 reads 覆盖；这段区间不称为 junction。RNA 比对中的 splice junction 通常指剪接连接位点','纠正 junction 误用')
edit(f,'这就是一台illumina最新的XTen测序仪','Illumina X Ten 测序仪（原稿历史示例）','图注去时效断言')
edit(f,'这就是flowcell，图中透明的部分就是lane，每一个lane中整齐排列了无数个tile，只可惜我们肉眼看不到','流动槽、泳道与扫描区域示意（原稿平台示例）','图注规范')
edit(f,"由于Illumina测序策略本身的问题，导致其测序长度不可能太长，目前最好的X Ten也就是双端各150bp，所以不可能直接拿整个基因组去测序，所以在测序的时候需要先打断成一定长度的片段，这个根据需要用不同的策略，一般测人的基因组，我们是将其打断成300 ~ 500bp的长度。这个是根据跑胶控制的。","短读长测序每次只能读取有限长度，因此需要先把待测核酸制成适合平台的文库。下面以片段化的 DNA 文库为例：先把较长的 DNA 打断，再通过片段筛选控制长度分布。原稿以 300—500 bp 的插入片段举例；实际范围应按建库方案、读长和研究目的确定。",'避免把历史平台读长作为所有平台上限')
edit(f,"测序的过程反而简单了不少。就是来一个primer，然后加入特殊处理过的A，T，C，G四种碱基。特殊的地方有两点，一个是脱氧核糖3号位加入了叠氮基团而不是常规的羟基，保证每次只能够在序列上添加1个碱基；另一方面是，碱基部分加入了荧光基团，可以激发出不同的颜色。","测序时，聚合酶沿模板延伸引物，加入带有可逆终止基团的核苷酸，使一轮反应主要延伸一个碱基。仪器根据荧光信号判断本轮加入的碱基，再解除终止并进入下一轮。不同代际平台的荧光编码和化学体系有所不同，不能都理解为四种碱基各自发出一种颜色。",'按 Illumina 官方 SBS 说明纠正化学与荧光表述')
edit(f,'特殊处理的脱氧核糖核酸，引用自：http://www.oezratty.net/，图中的核糖的羟基应该换成-N2的叠氮基团。','下图保留原稿的核苷酸示意图，原图来源：http://www.oezratty.net/。具体可逆终止基团以对应化学体系为准；原稿关于“−N2 叠氮基团”的说明不成立。','纠正化学基团错误，保留原图与来源')
edit(f,'随后加入试剂，将脱氧核糖3号位的—N2改变成—OH，然后切掉部分荧光基团，使其在下一轮反应中，不再发出荧光。如此往复，就可以测出序列的内容。','成像后，解除可逆终止并清除本轮检测信号，使下一轮可以继续延伸。循环进行，即可从信号序列推断碱基序列。','同上')
edit(f,'测序时，经过长时间的PCR，会有不同步的情况。','测序循环中，不同模板分子的延伸可能逐渐失去同步（phasing 或 pre-phasing）。这里的测序延伸不等于反复进行 PCR。','区分簇扩增与 SBS 测序循环')
edit(f,'所有基于荧光淬灭原理的测序仪都有类似的问题，比如目前用过自主知识产权的华大智造测序仪，也是有类似的问题。','实际读长还受化学稳定性、信号质量和解码方法等因素影响，不能把所有平台归为“荧光淬灭原理”。','删除不正确的平台原理泛化')
# Replace two inaccurate long-read paragraphs, retaining conceptual depth and scope.
p=ROOT/'manuscript'/f;s=p.read_text();a=s.index('前文介绍的RNA测序都是基于二代测序技术平台');b=s.index('\n## ',a)
old=s[a:b].rstrip()
new='''前文的短读长 RNA-seq 通常先把 RNA 转成 cDNA，再进行文库构建。长读长技术可以减少把一个转录本拆成许多短片段后再推断结构的困难，因此特别适合理解转录本异构体。

PacBio 的 SMRT 测序观察聚合酶合成 DNA 时的荧光信号。Iso-Seq 分析的是由 RNA 逆转录得到的全长 cDNA，不能称为直接 RNA 测序。Oxford Nanopore 则根据核酸链通过纳米孔时的电流变化推断序列，既有 cDNA 测序，也有直接 RNA 测序；其常用平台不依靠外切酶逐个切下碱基再读取。

长读长、准确度、通量和定量性能需要结合具体平台、化学版本和建库方案讨论，不能用原稿时期的单一数值概括。PacBio、Nanopore 和直接 RNA 测序的进一步比较、示例数据与练习待完善。

参考：[Oxford Nanopore 技术说明](https://nanoporetech.com/platform/technology)；[PacBio RNA 测序说明](https://www.pacb.com/products-and-services/applications/rna-sequencing/)。'''
edit(f,old,new,'根据两家平台官方说明纠正长读长/直接 RNA 机制')

f='04-quality-control-and-alignment.md'
edit(f,'2：双末端比对的一条','2：同一模板的各片段满足比对软件定义的正确配对条件（proper pair）','SAM FLAG 0x2')
edit(f,'8：是paired-end或mate pair中的一条，且无法比对到参考序列上','8：另一片段（mate）未比对到参考序列','SAM FLAG 0x8')
edit(f,'第五列是比对质量，MAPQ，即比对结果的可信度，从0到60，数值越高越好，一般认为大于等于20都是可信的。','第五列是比对质量 MAPQ，用 Phred 标度表达比对位置错误的概率。SAM 规范并未将取值限制为 0—60；255 表示没有可用的比对质量。具体算法、上限和过滤阈值依赖比对软件及分析目的，不能把 MAPQ≥20 当作普遍的可信保证。','SAMv1 规范')
edit(f,'38s432N38M，表示前三个碱基被剪切掉了，然后432个碱基被绕过，38个碱基可能是match或者是mismatch的','例如 `3S38M432N38M` 表示先软剪切 3 个碱基，再比对 38 个碱基、跳过参考上的 432 个碱基、再比对 38 个碱基；`M` 同时包含匹配与错配，`S` 必须大写','修复不一致的 CIGAR 示例')

f='06-rna-seq.md'
edit(f,'*FPKM=RPKM/2=total reads/(mapped reads(millions)xtrancription length(KB))*','$$\n\\mathrm{FPKM}_i=\\frac{F_i}{L_i\\,(\\mathrm{kb})\\times N_F\\,(\\mathrm{million})}\n$$\n\n其中 $F_i$ 为分配到基因或转录本 $i$ 的 fragment 数，$N_F$ 为所采用统计口径下的总 fragment 数。','修复 FPKM 定义与单位')
edit(f,'geneA RPKM = CountA / Len(A) / D * 10^9','geneA RPKM = CountA / Len(A) / D','原稿 Len(A) 已为 kb，D 已为 million，不再乘 10^9')
edit(f,'双端测序中，1个gene的FPKM应该等于RPKM / 2。','FPKM 与 RPKM 的分子和分母使用不同的计数单位，不能普遍写成 FPKM=RPKM/2。若每个 fragment 的两端都被计为 reads，分子和分母都会同比变化。','纠正重复出现的二倍关系')
edit(f,'TPM定量将所有样本TPM总和统一标准化为$10^{6}$，方便了不同样本批次之间的比较。','TPM 先将计数除以长度，再使每个样本内的总和为 $10^6$。它描述样本内的相对丰度，不会自动消除组成偏差或批次效应，也不能替代差异表达模型所需的 counts。\n\n$$\n\\mathrm{TPM}_i=10^6\\frac{C_i/L_i}{\\sum_j C_j/L_j}\n$$','区分相对丰度与统计模型输入')
edit(f,'因为RNA-Seq分析的前提是基于两个假设，即:','例如，部分跨样本归一化方法依赖表达变化的总体分布，不能把下面两条当作所有 RNA-seq 方法都必须满足的统一前提：','归一化假设的适用范围')
edit(f,'参与mRNA剪接的snoRNA（small nucleolar RNA）','参与mRNA剪接的snRNA（small nuclear RNA）','纠正 snRNA 与 snoRNA 混淆')
edit(f,'利用真核生物mRNA都具备poly-A的特殊结构这一特性','利用多数真核 mRNA 具有 poly(A) 尾的特性','避免“所有 mRNA”绝对断言')
# Generated, working figure cross-references replace ambiguous old hard-coded numbers.
p=ROOT/'manuscript'/f;s=p.read_text()
imgs=list(re.finditer(r'!\[([^\]]*)\]\(([^)]+)\)\{#(fig-[^}]+)\}',s))
figs={}
for m in imgs:
 for key in ['rna-seq-all','sc-rna-seq-lib','rna-seq-analysis','rna-seq-software2']:
  if key in m[2]:figs[key]=m[3]
for old,key in [('图3.1','rna-seq-all'),('图3.2','sc-rna-seq-lib'),('图3.3','rna-seq-analysis')]:
 if key in figs:s=s.replace(old,'@'+figs[key])
s=s.replace('转录组测序分析的常用软件如图3.3所示。','转录组测序分析的常用软件见下图。')
p.write_text(s)

f='08-wgs-and-wes.md'
edit(f,r'P(S_i | G_1) = \frac{1}{2}(1-\epsilon_i) \cdot \frac{1}{2}\epsilon_i=\frac{1}{4}(1-\epsilon_i)\epsilon_i',r'P(S_i | G_1) = \frac{1}{2}(1-\epsilon_i) + \frac{1}{2}\epsilon_i=\frac{1}{2}','二等位对称错误教学模型：杂合子的似然是混合而非乘积')
edit(f,'则\n\n$$\n\\left\\{','这里采用二等位、对称翻转错误的简化教学模型；实际四碱基测序错误模型不能直接套用这些式子。\n\n则\n\n$$\n\\left\\{','标清简化模型假设')
edit(f,r'P(G \mid D) = P(G)P(D \mid G)',r'P(G \mid D) \propto P(G)P(D \mid G)','省略归一化常数后必须使用正比号')
old='''> HaplotypeCaller首先是根据所测的数据，先构建这个群体中的单倍体组合（我认为这也是Haplotype这个名字的由来），由于群体中的单倍体是有多个的，所以最好是多个人一起进行HaplotypeCaller这样构建出来的单倍体组合会越接近真实情况
>
> 构建出单倍体的组合之后（每一个单倍体都有一个依据数据得出的后验概率值），再用每个样本的实际数据去反算它们自己属于各个单倍体组合的后验概率，这个组合一旦计算出来了，对应位点上的碱基型（或者说是基因型，genotype）也就跟着计算出来了：
>
> 计算每一个后候选变异位置上的基因型（Genotype）后验概率，最后留下基因型（Genotype）中后验概率最高的哪一个'''
new='''HaplotypeCaller 在候选变异区域进行局部重组装，生成候选单倍型，并评估 reads 对这些单倍型的支持。这里的单倍型是一个区域内的序列组合，并不等于“单倍体个体”。在常用的 GATK 胚系多样本流程中，每个样本先独立生成 gVCF，随后进行联合分型；不能把这两个阶段理解为先把整个人群的 reads 混在一起运行 HaplotypeCaller。'''
edit(f,old,new,'按 GATK 官方文档区分局部组装与联合分型')
edit(f,'（如果有多个样本那么是所有这些样本的reads而不是单样本进行）','（在这里讨论的按样本生成 gVCF 流程中，使用当前样本的 reads）','同上')
edit(f,r'$P(r_i,H_j)=a_{ij}$',r'$P(r_i\mid H_j)=a_{ij}$','read–haplotype 似然为条件概率')
edit(f,'这个似然值矩阵很重要，因为在获得这个矩阵之后，GATK会在每一个潜在的变异位点上把这些似然值相加合并，计算等位基因的边缘概率，这个边缘概率实际上是每一个read在该位点上支持其为变异的似然值，即\n\n$$P(H_i)=\\sum_{j=1}^n P(r_j,H_i)$$','这个矩阵描述每条 read 在每个候选单倍型条件下的似然。软件随后把单倍型层面的证据映射到候选等位基因，并计算基因型似然。不能把跨 reads 的似然直接相加，写成单倍型的概率；下面在条件独立假设下使用似然乘积进行教学推导。具体聚合规则应以所使用的 GATK 版本实现为准。','删除错误的跨 reads 求和概率公式')
edit(f,'其中，$P(G)$为genotype为G的先验概率，理论上为样本来源的群体中allele为G的频率，这个一般需要前期给定，若不给定的话，GATK会默认每种G的频率均等','其中，$P(G)$ 是基因型 $G$ 的先验概率，不能与单个等位基因的频率混为一谈。工具对先验的处理取决于模型和参数，不能假定 GATK 默认给所有基因型相同先验。','修正先验解释')

# Make display-math labels unique throughout the book, retaining original tags as comments.
for p in (ROOT/'manuscript').glob('*.md'):
 s=p.read_text();n=[0];slug=p.stem
 def math(m):
  n[0]+=1;inner=m[1].strip();tags=re.findall(r'\\tag\{([^}]+)\}',inner)
  inner=re.sub(r'\\tag\{[^}]+\}','',inner).strip()
  inner=inner.replace('\\newline',r'\\')
  label=f'eq-{slug}-{n[0]:03d}'
  comment='\n\n<!-- Original equation tag: '+','.join(tags)+' -->' if tags else ''
  return '\n\n$$\n'+inner+'\n$$ {#'+label+'}'+comment+'\n\n'
 s=re.sub(r'\$\$([\s\S]*?)\$\$',math,s)
 p.write_text(s)
(ROOT/'editorial/corrections.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2)+'\n')
print(f'Applied {len(changes)} recorded corrections; preserved original source snapshots.')
