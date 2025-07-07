

测序数据表征
在这项研究中，我们评估了逻辑回归 （LR）、支持向量机 （SVM）、随机森林 （RF） 和卷积

神经网络 （CNN） 对抗生素环丙沙星、头孢噻肟、头孢他啶和庆大霉素的 AMR 预测。

我们可以证明，这些模型可以通过标签编码、独热编码和频率矩阵混沌博弈表示（FCGR编

码）对全基因组测序数据进行有效预测AMR。我们在大型AMR数据集上训练了这些模型，并在

独立的公共数据集上对其进行了评估。通常，RF 和 CNN 的性能优于 LR 和 SVM，AUC 高达

0.96。此外，我们能够识别出每种抗生素与AMR相关的突变。

来自 <https://academic.oup.com/bioinformatics/article/38/2/325/6382301?login=false>

抗菌素耐药性的基因组预测的方法及流程

我们描述了基因组测序，因为它与预测临床分离株和样本中的抗菌素耐药性有关。我们详细阐

述了执行此测试的当前方法和工作流程，并总结了临床环境中基因组耐药性预测的现状。为了

突出这一方面，我们纳入了 3 个医学相关的微生物示例：结核分枝杆菌、金黄色葡萄球菌和

淋病奈瑟菌。最后，我们讨论了临床微生物学实验室中基于基因组的耐药性检测的未来。

来自 <https://academic.oup.com/clinchem/article/66/10/1278/5904416>

1.

组装方法选择:A metacomparison of multiple de novo assemblers found that no
single program was superior regarding multiple quality metrics (i.e.,
longest contig, number of contigs, N50 (the shortest contig length needed to
cover 50% of the genome), indicating that multiple tools could be used for
each specific study (15,).

2.

(经典的)这种测序技术的一个缺点是，微生物染色体和大质粒很可能被组装成数百个支

架，在长重复的基因组区域出现组装断裂;然而，越来越多的专业程序正在出现，这些程

序试图从未组装的短读长数据（例如，PlasmidSeeker 和 plasmidSPAdes）中鉴定和注释质

粒区域

3.

（平台技术对质粒基因组装的影响）质粒传播的 ARG 和染色体定位的 ARG 的区分对于
识别 ARG 的水平基因转移潜力和感染控制非常重要 （23，）。实现这一优势需要注意

的是，在基因组 DNA 提取方案中需要付出相当大的努力才能不剪切

DNA （21，）。Oxford Nanopore MinION系统的一个主要优点是，可以在测序运行进行

时分析读数，从而提供极快的周转时间，这为该技术在床旁诊断环境中的实用性提供了

潜在的希望（24,25，）。相反，Illumina测序的主要优点是具有成本效益，文库制备

