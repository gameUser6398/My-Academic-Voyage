

平台： http://119.3.41.228/PLM-ARG/index.php

论文： https://academic.oup.com/bioinformatics/article/39/11/btad690/7443986?login=false#427816784

源码： https://github.com/Junwu302/PLM-ARG

PLM-ARG 将基因序列或预测的 ORF 作为输入和输出，包括抗性类别（如果查询被归类为 ARG）和相应的概率

一.

数据集策划

我们使用 EMBOSS 工具 Transeq 将所有具有 DNA 序列格式的 ARG 转换为 UniPort FASTA 蛋白质序列格式。然后，我们通过用 CD-

HIT 聚类所有序列并丢弃具有 100% 同一性和相同长度的重复项来删除重复的 ARG。最后，根据其授予的抗生素药物类别分配 ARG 的

耐药性类别，并根据 WHO 获取、观察、储备、抗生素评估分类和使用监测 （AWaRe） 分类系统
（ https://apps.who.int/iris/rest/bitstreams/1374989/retrieve） 进行手动校正。

来自 <https://github.com/Junwu302/PLM-ARG>

❖

ARG的认定

四种方法：CARD和MEGARes（5.2.0 版）、Resfams（1.2 版）和DeepARG

用于将查询的蛋白质确定为 ARG 的阈值设置为每种方法的默认阈值。

•
•
•

•

DeepARG predicted proteins with a probability >0.8 as ARGs.
Resfams considered proteins with an E-value <1e–10 were regarded as ARGs.
For the RGI, proteins with perfect or strict hits were regarded as ARGs.
RGI一种由 CARD 和 MEGARes 推荐的基于序列比对的方法

❖

PLM-ARG-DB数据描述

28 579个ARG组成，包括26 391个标有27个明确耐药类别的ARG，以及2188个标有模糊类别“multi-drug”

或"antibiotic without defined classification "的ARG。

优先级：CARD > ResFinder > MEGARes > AMRFinderPlus > ARGMiner > HMD -ARG-DB

具体而言，

•

•

•

•

•

•

PLM-ARGDB 包含来自 CARD 的 4790 个 ARG（即 CARD 中 100% 的蛋白质）、

来自 ResFinder 的 859 个 ARG（占 ResFinder 中蛋白质的 27.94%）、

来自 MEGARes 的 2044 个 ARG（占 MEGARes 中蛋白质的 30.01%）、

来自 AMRFinderPlus 的 444 个 ARG（占 AMRFinderPlus 中蛋白质的 7.43%）、

来自 ARGMiner 的 9863 个 ARG（占 ARGMiner 中蛋白质的 66.34%）

来自 HMD-ARG-DB 的 10 579 个 ARG（占 HMD-ARG-DB 中蛋白质的 61.30%）。

排除模糊类别的ARG，我们观察到大多数ARGs（22 015,77.03%）仅对一种抗生素类别具有耐药性。相比之下，大约四分之一的

ARGs（4376,15.31%）对多种抗生素类别产生耐药性

类别❖

二.

模型评估

对于多标签分类，各项指标是在单一类别上计算的

验证集来自uniprot：taxonomy： 'Bacteria [2]' AND keyword： 'Antibiotic resistance [KW-0046]' AND reviewed： yes

三.

案例研究：增强UniProt数据库中的抗性注释
我们利用我们开发的 PLM-ARG 对 UNIPROT 数据库中未经审查的 ARG 进行优先级排序，并扩展了它们的抗性类别注释（参见 补充
材料).在73 938个未经审查的ARG中，PLM-ARG分别预测了38 996个（52.74%）和13 902个（18.8%），概率值区间为0.9 -1和
0.5-0.9（图5A）。其中，52 898个ARGs（概率值>0.5），46 343个ARGs（87.61%）可以被指定为明确的阻力类别。排名前三的耐
药类别是肽、β-内酰胺和四环素（图 5B）。这些已鉴定的ARGs中的大多数（93.84%）仅被授予一类抗生素。作为一个典型的例
外，大环内酯类、林可酰胺类和链球菌敏 （MLS） 的抗菌光谱和机制是相似的，对三类抗生素中的一种产生耐药性的基因也对其
他两类抗生素产生耐药性。在我们的预测结果中也观察到了这种现象（图5C）。我们可以看到，2993 个基因被分配了至少一个
MLS 类别，92.38% 的基因对所有三类抗生素都具有耐药性。分配给73 938个未经审查的ARG的具体阻力类别及其预测概率值已在 附
表S2.

此外，我们计算了 73 938 个未经审查的 ARG 与我们的 PLM-ARGDB 之间的同一性，发现其中 64.77% 的相似度为 <40%，它们被定义

为遥远的同源 ARG。我们发现，这些遥远的同源ARG中有58%可以用PLM-ARG预测。值得注意的是，29.67%的ARGs具有<20%的相似性。

这些结果进一步证明了PLM-ARG在ARG识别方面的强大能力（图5D）。类别分类也具有很高的可靠性。例如，UniProt蛋白A0A010ZRL4

