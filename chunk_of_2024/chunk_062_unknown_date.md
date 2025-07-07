

视频来源：

我居然3小时学懂了深度学习神经网络入门到实战，多亏了这个课程，看不懂你打我！！！

GAN/RNN/CNN神经网络/人工智能/计算机视觉/深度学习/AI机器学习_哔哩哔哩_bilibili

（对应的文章深度学习（2）基础2 -- 分类：得分函数&&损失函数(损失、正则化惩罚项、梯度

下降、学习率)&&概率__(*^▽ ^*)_的博客-CSDN博客）

文章来源：

CNN笔记：通俗理解卷积神经网络_cnn卷积神经网络_v_JULY_v的博客-CSDN博客

正则化方法一篇就够了_使用正则化_星画天的博客-CSDN博客

神经网络——最易懂最清晰的一篇文章_illikang的博客-CSDN博客

训练框架

model =
loss_function =
optimizer = torch.optim.SGD(model.parameters(), )

for data, targets in data_loader:
outputs = model(data)
loss = loss_function(outputs, targets)

optimizer.zero_grad()
loss.backward()
optimizer.step()

