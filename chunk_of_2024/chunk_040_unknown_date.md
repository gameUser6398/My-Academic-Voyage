

cl:
第4章 热带气旋预报

Hurricast框架中将不同类型的数据进行组合以进行预测的方法是采用了三个步骤的方法。首先，从每个重新分析地

图序列中提取一维特征表示（嵌入）。其次，将这个一维嵌入与统计数据进行连接，形成一个一维向量。最后，

使用梯度提升树XGBoost模型对选定的特征进行训练，进行预测。

cl:

cl:
输入数据有两种，图分析结果、统计数据。先用CNN提取图，拉平成一维，再和统计数据拼接。经过Transformer

cl:

