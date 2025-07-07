

1.

构架调整。深层注释，专注与精细化的蛋白注释

-

原型：

-

输入：同源搜索，简单提示。anc2vec嵌入

2.

数据筛选，Information accretion: IA.txt

○

输入GO是weight最小的5000条，预测的是GO是weight最大的5000条。改进，

选用一级GO或者，

○

蛋白共10万条，一条蛋白平均1- 2条GO，样本极度不平衡

3.

效果：

○

BInaryF1Score接近0，Recall差。

改进：

1.

调参（focal loss的γ从2变成3

2.

添加蛋白相互作用。

问题：

问题

改进

1.

数据严重不

IA选大一点。多爬

平衡

取蛋白

Learning from Imbalanced Classes - Silicon
Valley Data Science (svds.com)

