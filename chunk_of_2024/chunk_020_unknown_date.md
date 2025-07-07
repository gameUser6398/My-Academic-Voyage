

1.

Uniprot蛋白分布、经IC筛选后的蛋白分布（长尾分布）。

○

○

○

GO level几级、数量分布

阿斯顿发斯蒂

偏好/歧视，前期训练不好

2.

不平衡解决方法

○

○

○

DCGAN蛋白质嵌入生成模型

通过输入；；反复调试，

SMOTE合成少数过采样

chroma扩散模型

3.

深度学习模型

○

○

○

○

基于预训练的蛋白质标征

基于基因本体论的功能标准

卷积线性、

功能提升。

1.

2.

3.

模型构架

loss-train-step 损失不断上升，大到e16。梯度爆炸

验证集上loss增大，f1-score增大

self-
Attention-

simple：

4.

self-
Attention-
complex

只从序列

accuracy最低，

accuracy增加，

loss最低，score

score减小，loss

最低

减小，

稀疏性会

影响吗？

torch.cat([prot_embed,
label_embed], dim = 1)

loss最大，score

loss上升，score

把label加入后，

最大

上升

对不平衡有缓解

作用

score上升

self-
Attention-
conv

torch.bmm(prot_embed,
label_embed) #
(batch_size, 1024, 256)

self-atttenion学的慢。

关键问题是把loss降下去

1.

2.

3.

4.

learn rate 0.001再小点

独立验证集，随机拆分可能对于label有什么偏差。

激活函数

平均池化

