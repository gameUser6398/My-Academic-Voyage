

"Embed_then_GOannotations.py"
代码来自： https://docs.bioembeddings.com/v0.2.3/notebooks/goPredSim.html

目的：使用Bert嵌入向量+KNN对未知序列进行蛋白质注释

本质：序列相似性

bio_embeddings.extract.unsupervised_utilities的源代码

-

pairwise_distance_matrix_from_embeddings_and_annotations (cid:2124)配对距离

distances_dataframe = DataFrame(instrinsic_pairwise_distances.pairwise_matrix,
                                index = instrinsic_pairwise_distances.queries,
                                columns= instrinsic_pairwise_distances.references)
(50条消息) sklearn.metrics.pairwise_distances_lonelykid96的博客-CSDN博客

-

get_k_nearest_neighbours (cid:2124)最近邻居及距离

-

RI的值：(50条消息) 无监督聚类评价指标，RI、ARI、MI、NMI等_nmi和ari_踮踮脚尖看远方的博客-CSDN博客

"GOannotations_knn.py"
代码来自：
https://docs.bioembeddings.com/v0.2.3/notebooks/pairwise_distances_and_nearest_neighbours.html

"Visual_sequSpace_embd1.py"
目的：嵌入一些序列并尝试不同的想法，看看嵌入是否能够聚类不同的序列

向量能直接加减？

