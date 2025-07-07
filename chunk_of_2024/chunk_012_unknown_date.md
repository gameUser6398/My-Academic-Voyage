

理想图：

背景知识：
How is protein family membership assigned in UniProtKB? | UniProt help | UniProt

我们使用的是Uniprotkb提供的蛋白家族数据，它整合了蛋白质家族数据库、序列分析工具、科学文献、序列相

似性搜索工具等多种资源。

它利用InterPro及其成员数据库将UniProtKB蛋白分配给家族。

UniProtKB中蛋白质家族的完整列表以及属于每个家族的条目可见：
https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/docs/similar.txt

1.

利用API获取家族信息
程序化访问资源：How can I access resources on this website programmatically? | UniProt help |
UniProt
Programmatic access - Retrieving entries via queries | UniProt help | UniProt
搜索字段：UniProtKB query fields | UniProt help | UniProt

返回字段：UniProtKB return fields | UniProt help | UniProt

示例：https://rest.uniprot.org/uniprotkb/search?query=accession:P05067&fields=protein_families

