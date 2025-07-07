

生物学数据库可以大致分成两大类：泛用的，专用的。前者比如INSDC的几大数据库

（NCBI、EMBL），UniProt蛋白库，Pfam蛋白家族库等等。后者主要是某个研究领域特异

的，比如毒力蛋白的库、耐药基因的库、合成基因簇的库、toxin - antitoxin的库等等。那些

泛用的库自然就会用到。领域特异的库用到哪些，完全取决于你自己的研究内容。

数据储存方式(cid:1710)多样，而且实际上也经常会同时使用(cid:1710)多种储存方式。比如NCBI，要同时满

足关键词搜索、序列比对搜索、库间关系搜索、打包下载的功能，那肯定就要同时使用文件

包、关系型数据库、文本搜索引擎、blast索引库这几种方式。

01、Uniprot

网址：https://www.uniprot.org

数据:各物种基因组测序完成后得到的全基因蛋白质序列，并包含了(cid:1710)多来自文献中的蛋白及

其功能信息。由Swiss-Prot、TrEMBL和PIR-PSD三大子数据库构成尤其是Swiss-prot 子数据

库，库中蛋白质信息都是手工核对过的 ，非冗余， 有详细注释信息的蛋白数据。

•

EBI（ European Bioinformatics Institute）：欧洲生物信息学研究所（EMBL-EBI）是欧洲

生命科学旗舰实验室EMBL的一部分。位于英国剑桥欣克斯顿的惠康基因组校园内，是世界上

基因组学领域最强地带之一。

•

SIB（the Swiss Institute of Bioinformatics）：瑞士日内瓦的SIB维护着ExPASy（专家蛋白

质分析系统）服务器，这里包含有蛋白质组学工具和数据库的主要资源。

•

PIR（Protein Information Resource）：PIR由美国国家生物医学研究基金会（NBRF）于

1984年成立，旨在协助研究人员识别和解释蛋白质序列信息。

通过EMBL，GenBank，DDBJ等公共数据库得到原始数据，处理后存入UniParc的非冗余蛋

白质序列数据库。UniProt作为数据仓库，再分别给UniProtKB，Proteomes，UNIRef提供

可靠的数据集。其中在UniProtKB数据库中Swiss-Prot是由TrEMBL经过手动注释后得到的高

质量非冗余数据库，也是我们今后常用的蛋白质数据库之一。

