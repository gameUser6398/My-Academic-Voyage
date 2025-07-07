import json
import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter, defaultdict
import seaborn as sns
import numpy as np

import matplotlib.font_manager as fm
font_path = "/usr/share/fonts/google-noto-cjk/NotoSerifCJK-Bold.ttc"
plt.rcParams['font.family'] = fm.FontProperties(fname=font_path).get_name()
plt.rcParams['axes.unicode_minus'] = False

class EntityRelationAnalyzer:
    def __init__(self, json_file_path_or_data):
        """初始化分析器"""
        if os.path.isfile(json_file_path_or_data):
            with open(json_file_path_or_data, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        else:
            self.data = json_file_path_or_data
        
        self.entities = self.data['entities']
        self.relations = self.data['relations']
        self.G = self._build_graph()
        
        
        # 实体类型颜色配置
        self.entity_colors = {
            "生物分子": "#FF6B6B",      # 红色
            "生物医学概念": "#4ECDC4",   # 青色
            "生物技术": "#45B7D1",      # 蓝色
            "生物信息工具": "#96CEB4",   # 绿色
            "项目活动": "#FFEAA7",      # 黄色
            "其他": "#DDA0DD"           # 紫色
        }
    
    def _build_graph(self):
        """构建NetworkX图"""
        G = nx.DiGraph()
        
        # 添加节点
        for entity in self.entities:
            G.add_node(entity['name'], type=entity['type'])
        
        # 添加边
        for relation in self.relations:
            G.add_edge(relation['head'], relation['tail'], 
                      relation_type=relation['type'])
        
        return G
    
    def entity_statistics(self):
        """实体统计分析"""
        print("=== 实体统计分析 ===")
        
        entity_types = [entity['type'] for entity in self.entities]
        type_counts = Counter(entity_types)
        
        print(f"总实体数: {len(self.entities)}")
        print("\n实体类型分布:")
        for entity_type, count in type_counts.most_common():
            print(f"  {entity_type}: {count}")
        
        # 可视化
        plt.figure(figsize=(12, 8))
        types, counts = zip(*type_counts.most_common())
        
        # 使用配置的颜色
        colors = [self.entity_colors.get(t, "#999999") for t in types]
        bars = plt.bar(types, counts, color=colors)
        
        plt.title('实体类型分布', fontsize=16, fontweight='bold')
        plt.xlabel('实体类型', fontsize=12)
        plt.ylabel('数量', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        
        # 添加数值标签
        for bar, count in zip(bars, counts):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                    str(count), ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig('entity_type_distribution.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return type_counts
    
    def relation_statistics(self):
        """关系统计分析"""
        print("\n=== 关系统计分析 ===")
        
        relation_types = [relation['type'] for relation in self.relations]
        relation_counts = Counter(relation_types)
        
        print(f"总关系数: {len(self.relations)}")
        print("\n关系类型分布:")
        for rel_type, count in relation_counts.most_common():
            print(f"  {rel_type}: {count}")
        
        # 可视化关系类型分布
        plt.figure(figsize=(10, 6))
        rel_types, counts = zip(*relation_counts.most_common())
        plt.pie(counts, labels=rel_types, autopct='%1.1f%%', startangle=90)
        plt.title('关系类型分布')
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig('relation_type_distribution.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return relation_counts
    
    def network_analysis(self):
        """网络拓扑分析"""
        print("\n=== 网络拓扑分析 ===")
        
        # 基本网络统计
        print(f"节点数: {self.G.number_of_nodes()}")
        print(f"边数: {self.G.number_of_edges()}")
        print(f"平均度: {sum(dict(self.G.degree()).values()) / self.G.number_of_nodes():.2f}")
        
        # 各种中心性分析
        degree_centrality = nx.degree_centrality(self.G)
        betweenness_centrality = nx.betweenness_centrality(self.G)
        closeness_centrality = nx.closeness_centrality(self.G)
        
        # 入度和出度分析
        in_degree_centrality = nx.in_degree_centrality(self.G)
        out_degree_centrality = nx.out_degree_centrality(self.G)
        
        # 打印TOP10
        print("\n度中心性TOP10:")
        top_degree = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
        for node, centrality in top_degree:
            print(f"  {node}: {centrality:.3f}")
        
        print("\n介数中心性TOP10:")
        top_betweenness = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
        for node, centrality in top_betweenness:
            print(f"  {node}: {centrality:.3f}")
        
        print("\n紧密中心性TOP10:")
        top_closeness = sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
        for node, centrality in top_closeness:
            print(f"  {node}: {centrality:.3f}")
        
        return {
            'degree_centrality': degree_centrality,
            'betweenness_centrality': betweenness_centrality,
            'closeness_centrality': closeness_centrality,
            'in_degree_centrality': in_degree_centrality,
            'out_degree_centrality': out_degree_centrality
        }
    
    def community_detection(self):
        """社区检测分析"""
        print("\n=== 社区检测分析 ===")
        
        G_undirected = self.G.to_undirected()
        
        try:
            import community as community_louvain
            communities = community_louvain.best_partition(G_undirected)
        except ImportError:
            communities_iter = nx.community.greedy_modularity_communities(G_undirected)
            communities = {}
            for i, community in enumerate(communities_iter):
                for node in community:
                    communities[node] = i
        
        community_counts = Counter(communities.values())
        print(f"检测到 {len(community_counts)} 个社区")
        
        # 打印社区的节点(nodes > 20)
        community_nodes = defaultdict(list)
        for node, community_id in communities.items():
            community_nodes[community_id].append(node)
        
        for community_id, nodes in community_nodes.items():
            if len(nodes) > 20:
                print(f"\n社区 {community_id} ({len(nodes)} 个节点):")
                print(f"  {', '.join(nodes[:5])}{'...' if len(nodes) > 5 else ''}")
        
        return communities
    
    def generate_summary_report(self):
        """生成综合分析报告"""
        print("\n" + "="*50)
        print("综合分析报告")
        print("="*50)
        
        entity_stats = self.entity_statistics()
        relation_stats = self.relation_statistics()
        network_stats = self.network_analysis()
        communities = self.community_detection()
        
        print("\n=== 关键洞察 ===")
        
        top_entity_type = max(entity_stats, key=entity_stats.get)
        print(f"1. 最主要的实体类型: {top_entity_type} ({entity_stats[top_entity_type]} 个)")
        
        top_relation_type = max(relation_stats, key=relation_stats.get)
        print(f"2. 最主要的关系类型: {top_relation_type} ({relation_stats[top_relation_type]} 个)")
        
        top_central_node = max(network_stats['degree_centrality'], 
                             key=network_stats['degree_centrality'].get)
        print(f"3. 网络中心节点: {top_central_node}")
        
        print(f"4. 检测到 {len(set(communities.values()))} 个知识社区")
        
        return {
            'entity_stats': entity_stats,
            'relation_stats': relation_stats,
            'network_stats': network_stats,
            'communities': communities
        }
    def compute_metrics(self):
        pass

def main():
    """主函数"""
    # 配置文件路径
    json_file_path = input("请输入JSON文件路径（例如：/path/to/integrated_entities_relations.json）: ").strip()
    

    # 创建分析器（可以不提供Neo4j连接进行本地分析）
    analyzer = EntityRelationAnalyzer(
        json_file_path_or_data=json_file_path
    )
    
    # 生成分析报告
    results = analyzer.generate_summary_report()
    
    # 写入Neo4j（如果配置了连接）
    # analyzer.write_to_neo4j()

    print("\n分析完成！")


if __name__ == "__main__":
    main()