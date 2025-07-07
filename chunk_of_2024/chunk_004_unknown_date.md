

7月17日

刘：CAFA 5 - T5 Embeds + Ensemble+ zero_predic | Kaggle

1.

2.

3.

训练框架，torch

tensorboard。 多条曲线，阴影曲线干嘛

CAFA阅读。获取label——go term

7月18日

刘：CAFA 5 - T5 Embeds + Ensemble+ zero_predic | Kaggle

1.

2.

词嵌入+CNN = 多分类（500）预测

输入数据：

labels_vect存放在train-targets-top500.npy里，模型选取了500个最常见的label（GOterm）预测

3.

加载数据：
test_dataset = ProteinSequenceDataset(datatype="test", embeddings_source = embeddings_source)
test_dataloader = torch.utils.data.DataLoader(test_dataset, batch_size=1, shuffle=False)
All subclasses should overwrite :meth:`__getitem__`, supporting fetching a data sample for agiven key.
来(cid:14362) <https://pytorch.org/docs/stable/_modules/torch/utils/data/dataset.html#Dataset>

ProteiNet   PyTorch+EMS2/T5/ProtBERT Embeddings | Kaggle合理怀疑上面抄袭

