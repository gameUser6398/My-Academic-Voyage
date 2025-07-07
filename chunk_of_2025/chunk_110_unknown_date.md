

1.

SOTA全称是state of the art，是指在特定任务中目前表现最好的方法或模

型。Benchmark和baseline都是指最基础的比较对象。你论文的motivation来自于想超越

现有的baseline/benchmark，你的实验数据都需要以baseline/benckmark为基准来判断

是否有提高。唯一的区别就是baseline讲究一套方法，而benchmark更偏向于一个目前最

高的指标，比如precision，recall等等可量化的指标。举个例子，NLP任务中BERT是目

前的SOTA，你有idea可以超过BERT。那在论文中的实验部分你的方法需要比较的

baseline就是BERT，而需要比较的benchmark就是BERT具体的各项指标。

链接： https://www.zhihu.com/question/433986039/answer/1618236738

2.

Logits在深度学习中通常是指模型的输出层的原始未经处理的分数或得分，特别是在
分类问题中。这些原始分数可以被视为模型对每个类别的置信度或概率的度量，但它们

并不直接表示概率。具体来说，Logits是模型对每个类别的线性输出，还未经过softmax

或sigmoid等激活函数的处理。

来自 <https://yiyan.baidu.com/>

1.

