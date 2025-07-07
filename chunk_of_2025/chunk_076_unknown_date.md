

抗生素耐药性转移 （HGT-ARG） 预测
使用具有假定 ARG 的 HGT 边缘来构建特定于 ARG 的 HGT 网络。为了避免
过度拟合，我们删除了 645 个 KO，这些 KO 与 ARG-miner 数据库中的任
何基因共享 50% 的序列相似性。然后，我们使用 RF、Lasso 和 GCN 框架
使用与二进制 HGT 预测器相同的超参数来预测二进制 ARG-HGT 网络。图3C
和图3C中描述的分离株来源。表 S5 中列出的 S13 是根据其在 NCBI 或
PATRIC 中的记录手动整理的。我们训练了一组 RF（用于多类分类的一余二
元分类器）来区分不同 ARG 类的转移，使用参数 （max_features =
“auto”， min_samples_leaf = 3， min_samples_split = 4，
n_estimators = 5000，class_weight = “balanced”） 在通过网格搜索
方法（“GridSearchCV”： cv = 5） （69).每个射频预测器的重要性特征
由“.feature_importances”提取。为了检查ARG的网络特性（图S14），我
们使用CD-HIT v4.6.8（-c 0.5 -s 0.8）对假定的ARG进行聚类。每个聚类
的最长最短路径是使用 NetworkX 的 “.shortest_path_length” 函数的
输出计算的。
我们进一步应用这些RF预测因子来预测我们收集的基因组与来自大肠杆菌
（41）、淋病奈瑟菌（43）和鲍曼不动杆菌（42）的三组单物种分离株之间
的ARG转移（表S7）。使用上述方法计算原始基因组数据集与这些基因组之
间的HGT联系。提取DNA的共享区域，并注释共享区域中的推定ARGs。每个单
物种分离数据集被用作测试数据。从训练集中删除具有相同物种名称的基因
组和/或在 16S rRNA 中序列相似度超过 97% 的基因组。对于每个 ARG 类
别，选择一组平衡的、随机的负 ARG 特定 HGT 边进行评估。

来自 <https://www.science.org/doi/10.1126/sciadv.abj5056>

模型评估
使用sklearn.metrics.roc_curve函数根据假阳性率和真阳性率之间的关系
计算ROC曲线。精确召回率曲线由
sklearn.metrics.precision_recall_curve函数 [sklearn （69）
v0.22.2] 计算。使用 sklearn.metrics.auc 函数计算的曲线下面积用作衡
量预测模型准确性的指标。通过减少多数类样本的数量来平衡用于评估的测
试数据。

来自 <https://www.science.org/doi/10.1126/sciadv.abj5056>

