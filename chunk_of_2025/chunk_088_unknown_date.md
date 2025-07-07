

命令行工具 (nih.gov)，分为datasets（下载工具）和dataformat（格式转变工具）

通过conda使用CLI工具
conda activate ncbi_datasets

1.

2.

下载基因组元数据
datasets summary genome taxon 'sharks' --assembly-source refseq --as-json-lines | dataformat tsv genome --fields accession,assminfo-name,annotinfo-name,annotinfo-
release-date,organism-name

注意：将数据从datasets管道传输到dataformat时始终使用--as-json-lines
来自 <https://www.ncbi.nlm.nih.gov/datasets/docs/v2/how-tos/genomes/get-genome-metadata/>

下载基因组数据
datasets download genome accession GCF_000001405.40 --filename human_GRCh38_dataset.zip
来自 <https://www.ncbi.nlm.nih.gov/datasets/docs/v2/how-tos/genomes/download-genome/>

3.

下载大型基因组数据包 (nih.gov)

通过软件使用CLI工具

区别在于，下载后chmod +x datasets dataformat，然后使用./dataset 而不是dataset

示例
./datasets download genome taxon 1773 --filename 'Mycobacterium_tuberculosis_genomes_dataset.zip' --dehydrated

Python调用系统命令的四种方法（os.system、os.popen、commands、subprocess）-CSDN博客

下载NCBI的SRA数据 详细教程 - 知乎 (zhihu.com)

从 Entrez 搜索结果中下载 SRA 序列 (nih.gov)

