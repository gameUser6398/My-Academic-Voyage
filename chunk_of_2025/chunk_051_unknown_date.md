

ARGNet：使用深度神经网络从序列中可靠地识别和分类抗生素耐药性基因 |微生物组 |全文 (biomedcentral.com)

1.

1.

2.

3.

四种模型（ARGNet-LSaa，ARGNet-Ssaa……）对应四种序列输入。继承DeepARG。

自动编码器和 CNN 分类器

独热编码

ARGNet-LSaa：

1.

自回归autoencoder

•

•

•

•

•

目的：区分ARG与non-ARG

鉴别：重建损失与阈值

训练：ARGs，无监督。混合全长序列和 90%、80%、70% 和 60% 全长序列的minibatch中进行训练。

自动编码器有 28 个一维卷积层（编码器中有 14 个，解码器中有 14 个），编码器和解码器中有 6 个最大池化层。

梯度消失或爆炸，使用了ResBlock

