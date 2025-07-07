

generate_embd.py

从h5文件中提取id和embd，分别存放为all_ids.npy all_embds.npy

arr = np.asarray(protein_name).

同样尝试了embd_Series.csv储存

注意：to_csv的字符串类型。csv明显比npy文件小，信息丢失

select_train_embd.py

加载已嵌入的蛋白向量、功能显示（0，1）

如何把np.array([np.array[True, False……], np.array[], ….)变成np.array([1,0,……….])

