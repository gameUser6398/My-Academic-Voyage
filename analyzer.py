import json
import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter, defaultdict
import seaborn as sns
import numpy as np

import datetime

import re
from neo4j import GraphDatabase
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates


import matplotlib.font_manager as fm
font_path = "/usr/share/fonts/google-noto-cjk/NotoSerifCJK-Bold.ttc"


NEO4J_URI = "bolt://localhost:17687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "My_trajectory_0705"

class EntityRelationAnalyzer:
    def __init__(self, json_file_path_or_data):
        """初始化分析器"""
        # 实体类型颜色配置
        self.entity_colors = {
            "生物分子": "#2E8B57",      # 深绿色
            "生物医学概念": "#3CB371",   # 中等绿色
            "生物技术": "#20B2AA",      # 浅绿色
            "生物信息工具": "#FF6347",   # 番茄红
            "深度学习概念": "#DC143C",   # 深红色
            "项目活动": "#A9A9A9",      # 深灰色
            "其他": "#D3D3D3"           # 浅灰色
        }
        
        try: 
            if isinstance(json_file_path_or_data, str) and json_file_path_or_data.endswith('.json'):
                if os.path.isfile(json_file_path_or_data):
                    with open(json_file_path_or_data, 'r', encoding='utf-8') as f:
                        self.data = json.load(f)
            elif isinstance(json_file_path_or_data, dict):
                self.data = json_file_path_or_data
            else:
                raise ValueError("输入参数必须是JSON文件路径或字典")
        except Exception as e:
            print(f"初始化EntityRelationAnalyzer错误: {e}")
            raise e

        
        self.entities = self.data['entities']
        self.relations = self.data['relations']
        self.G = self._build_graph()
        

    def _get_type_color(self, entity_type):
        """为不同实体类型分配颜色"""
        return self.entity_colors.get(entity_type.upper(), '#95A5A6')  # 默认灰色
    
    def _build_graph(self):
        """构建NetworkX图"""
        G = nx.DiGraph()
        
        # 添加节点时包含类型信息
        for entity in self.entities:
            G.add_node(
                entity["name"], 
                type=entity["type"],
                color=self._get_type_color(entity["type"]),
                labels=['Entity', entity["type"].replace(' ', '_')]  # 多标签信息
            )
        
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

        plt.rcParams['font.family'] = fm.FontProperties(fname=font_path).get_name()
        plt.rcParams['axes.unicode_minus'] = False
        
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
        plt.rcParams['font.family'] = fm.FontProperties(fname=font_path).get_name()
        plt.rcParams['axes.unicode_minus'] = False

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

    def analyze_type_interactions(self):
        """分析不同类型实体间的交互模式"""
        type_interactions = {}
        
        for relation in self.relations:
            head_type = self._get_entity_type(relation["head"])
            tail_type = self._get_entity_type(relation["tail"])
            relation_type = relation["type"]
            
            key = (head_type, tail_type, relation_type)
            type_interactions[key] = type_interactions.get(key, 0) + 1
        
        return type_interactions

    def _get_entity_type(self, entity_name):
        """获取实体类型"""
        for entity in self.entities:
            if entity["name"] == entity_name:
                return entity["type"]
        return "Unknown"


class TemporalAnalyzer:
    def __init__(self, neo4j_uri, neo4j_auth):
        self.driver = GraphDatabase.driver(neo4j_uri, auth=neo4j_auth)
    
    def parse_timestamp(self, timestamp_str):
        """解析时间戳字符串，返回datetime对象"""
        if not timestamp_str or timestamp_str == "":
            return None
        
        # 支持多种时间戳格式
        patterns = [
            r'(\d{4})-(\d{2})-(\d{2})',  # 2024-03-02
            r'(\d{4})(\d{2})(\d{2})',    # 20240302
            r'(\d{4})-(\d{2})',          # 2024-03
            r'(\d{4})(\d{2})',           # 202403
        ]
        
        for pattern in patterns:
            match = re.match(pattern, timestamp_str)
            if match:
                groups = match.groups()
                if len(groups) == 3:
                    year, month, day = groups
                    return datetime.datetime(int(year), int(month), int(day))
                elif len(groups) == 2:
                    year, month = groups
                    return datetime.datetime(int(year), int(month), 1)
        
        return None
    
    def get_temporal_entities(self):
        """获取所有带时间戳的实体"""
        query = """
        MATCH (e:Entity)
        WHERE e.timestamps IS NOT NULL AND size(e.timestamps) > 0
        RETURN e.name as entity_name, e.type as entity_type, e.timestamps as timestamps, e.batches as batches
        ORDER BY entity_name
        """
        
        with self.driver.session() as session:
            result = session.run(query)
            return [dict(record) for record in result]
    
    def get_temporal_relations(self):
        """获取所有带时间戳的关系"""
        query = """
        MATCH (h:Entity)-[r:RELATION]->(t:Entity)
        WHERE r.timestamps IS NOT NULL AND size(r.timestamps) > 0
        RETURN h.name as head_entity, t.name as tail_entity, r.type as relation_type, 
               r.timestamps as timestamps, r.batches as batches
        ORDER BY head_entity, tail_entity
        """
        
        with self.driver.session() as session:
            result = session.run(query)
            return [dict(record) for record in result]
    
    def analyze_monthly_evolution(self):
        """分析实体的月度演化"""
        entities = self.get_temporal_entities()
        relations = self.get_temporal_relations()
        
        # 按月份组织数据
        monthly_data = defaultdict(lambda: {'entities': set(), 'relations': set()})
        
        # 处理实体
        for entity in entities:
            for timestamp_str in entity['timestamps']:
                dt = self.parse_timestamp(timestamp_str)
                if dt:
                    month_key = dt.strftime('%Y-%m')
                    monthly_data[month_key]['entities'].add(entity['entity_name'])
        
        # 处理关系
        for relation in relations:
            for timestamp_str in relation['timestamps']:
                dt = self.parse_timestamp(timestamp_str)
                if dt:
                    month_key = dt.strftime('%Y-%m')
                    relation_tuple = (relation['head_entity'], relation['relation_type'], relation['tail_entity'])
                    monthly_data[month_key]['relations'].add(relation_tuple)
        
        return dict(monthly_data)
    
    def create_temporal_graph_snapshots(self):
        """创建时间图快照"""
        monthly_data = self.analyze_monthly_evolution()
        
        snapshots = {}
        for month, data in monthly_data.items():
            G = nx.DiGraph()
            
            # 添加实体节点
            for entity in data['entities']:
                G.add_node(entity)
            
            # 添加关系边
            for head, rel_type, tail in data['relations']:
                if head in G.nodes and tail in G.nodes:
                    G.add_edge(head, tail, relation_type=rel_type)
            
            snapshots[month] = G
        
        return snapshots
    
    def visualize_temporal_evolution(self, save_path="temporal_evolution.png"):
        """可视化时间演化"""
        snapshots = self.create_temporal_graph_snapshots()
        
        # 创建子图
        n_months = len(snapshots)
        cols = min(3, n_months)
        rows = (n_months + cols - 1) // cols
        
        plt.rcParams['font.family'] = fm.FontProperties(fname=font_path).get_name()
        plt.rcParams['axes.unicode_minus'] = False
        
        fig, axes = plt.subplots(rows, cols, figsize=(5*cols, 4*rows))
        if n_months == 1:
            axes = [axes]
        elif rows == 1:
            axes = [axes]
        else:
            axes = axes.flatten()
        
        for i, (month, G) in enumerate(sorted(snapshots.items())):
            ax = axes[i] if i < len(axes) else None
            if ax is None:
                continue
                
            pos = nx.spring_layout(G, k=1, iterations=50)
            
            # 绘制节点
            nx.draw_networkx_nodes(G, pos, ax=ax, node_color='lightblue', 
                                 node_size=500, alpha=0.7)
            
            # 绘制边
            nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.5, arrows=True, 
                                 arrowsize=20, arrowstyle='->')
            
            # 绘制标签
            nx.draw_networkx_labels(G, pos, ax=ax, font_size=8, font_family='Noto Serif CJK JP')
            
            ax.set_title(f'{month}\n({len(G.nodes)} entities, {len(G.edges)} relations)')
            ax.axis('off')
        
        # 隐藏多余的子图
        for i in range(len(snapshots), len(axes)):
            axes[i].axis('off')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def get_entity_temporal_trajectory(self, entity_name):
        """获取特定实体的时间轨迹"""
        query = """
        MATCH (e:Entity {name: $entity_name})
        RETURN e.name as entity_name, e.type as entity_type, e.timestamps as timestamps, e.batches as batches
        """
        
        with self.driver.session() as session:
            result = session.run(query, entity_name=entity_name)
            record = result.single()
            if record:
                return dict(record)
            return None
    
    def analyze_entity_flow(self):
        """分析实体流动模式"""
        entities = self.get_temporal_entities()
        
        # 统计实体在不同时间点的出现
        entity_timeline = defaultdict(list)
        
        for entity in entities:
            entity_name = entity['entity_name']
            timestamps = []
            
            for timestamp_str in entity['timestamps']:
                dt = self.parse_timestamp(timestamp_str)
                if dt:
                    timestamps.append(dt)
            
            if timestamps:
                timestamps.sort()
                entity_timeline[entity_name] = timestamps
        
        # 分析流动模式
        flow_patterns = {
            'persistent': [],  # 持续出现的实体
            'emerging': [],    # 新出现的实体
            'disappearing': [] # 消失的实体
        }
        
        all_months = set()
        for timestamps in entity_timeline.values():
            for dt in timestamps:
                all_months.add(dt.strftime('%Y-%m'))
        
        sorted_months = sorted(all_months)
        
        for entity_name, timestamps in entity_timeline.items():
            entity_months = set(dt.strftime('%Y-%m') for dt in timestamps)
            
            if len(entity_months) >= len(sorted_months) * 0.8:  # 出现在80%以上的月份
                flow_patterns['persistent'].append(entity_name)
            elif min(entity_months) in sorted_months[-3:]:  # 最近3个月才出现
                flow_patterns['emerging'].append(entity_name)
            elif max(entity_months) in sorted_months[:3]:  # 只在前3个月出现
                flow_patterns['disappearing'].append(entity_name)
        
        return flow_patterns
    
    def generate_temporal_report(self):
        """生成时间分析报告"""
        monthly_data = self.analyze_monthly_evolution()
        flow_patterns = self.analyze_entity_flow()
        
        report = {
            'monthly_summary': {},
            'flow_patterns': flow_patterns,
            'trend_analysis': {}
        }
        
        # 月度汇总
        for month, data in monthly_data.items():
            report['monthly_summary'][month] = {
                'entity_count': len(data['entities']),
                'relation_count': len(data['relations']),
                'entities': list(data['entities'])
            }
        
        # 趋势分析
        months = sorted(monthly_data.keys())
        entity_counts = [len(monthly_data[month]['entities']) for month in months]
        relation_counts = [len(monthly_data[month]['relations']) for month in months]
        
        report['trend_analysis'] = {
            'months': months,
            'entity_growth': entity_counts,
            'relation_growth': relation_counts,
            'total_entities': sum(entity_counts),
            'total_relations': sum(relation_counts)
        }
        
        return report
    
    def close(self):
        """关闭连接"""
        if self.driver:
            self.driver.close()


def main():
    """主函数"""
    while True:
        print("\n请选择分析模式：")
        print("1. JSON 文件分析")
        print("2. Neo4j 数据库分析")
        print("0. 退出")
        choice = input("请输入选项编号: ").strip()

        if choice == "1":
            json_file_path = input("请输入JSON文件路径（例如：/path/to/integrated_entities_relations.json）: ").strip()
            try:
                analyzer = EntityRelationAnalyzer(json_file_path_or_data=json_file_path)
            except Exception as e:
                print(f"加载JSON失败: {e}")
                continue

            while True:
                print("\nJSON分析可用操作：")
                print("1. 生成综合分析报告")
                print("2. 实体统计分析")
                print("3. 关系统计分析")
                print("4. 网络拓扑分析")
                print("5. 社区检测分析")
                print("6. 分析类型间交互")
                print("0. 返回主菜单")
                op = input("请选择操作: ").strip()
                if op == "1":
                    analyzer.generate_summary_report()
                elif op == "2":
                    analyzer.entity_statistics()
                elif op == "3":
                    analyzer.relation_statistics()
                elif op == "4":
                    analyzer.network_analysis()
                elif op == "5":
                    analyzer.community_detection()
                elif op == "6":
                    interactions = analyzer.analyze_type_interactions()
                    print("类型间交互统计：")
                    for k, v in interactions.items():
                        print(f"{k}: {v}")
                elif op == "0":
                    break
                else:
                    print("无效选项，请重试。")

        elif choice == "2":
            temporal_analyzer = TemporalAnalyzer(NEO4J_URI, (NEO4J_USER, NEO4J_PASSWORD))
            while True:
                print("\nNeo4j分析可用操作：")
                print("1. 生成时间分析报告")
                print("2. 可视化时间演化")
                print("3. 分析实体流动模式")
                print("4. 查询实体时间轨迹")
                print("0. 返回主菜单")
                op = input("请选择操作: ").strip()
                if op == "1":
                    report = temporal_analyzer.generate_temporal_report()
                    print(f"时间分析完成，共分析 {len(report['monthly_summary'])} 个月份的数据")
                elif op == "2":
                    temporal_analyzer.visualize_temporal_evolution("temporal_evolution.png")
                    print("时间演化可视化已保存到 temporal_evolution.png")
                elif op == "3":
                    flow_patterns = temporal_analyzer.analyze_entity_flow()
                    print(f"持续实体: {len(flow_patterns['persistent'])} 个")
                    print(f"新兴实体: {len(flow_patterns['emerging'])} 个")
                    print(f"消失实体: {len(flow_patterns['disappearing'])} 个")
                elif op == "4":
                    entity_name = input("请输入要查询的实体名称: ").strip()
                    traj = temporal_analyzer.get_entity_temporal_trajectory(entity_name)
                    if traj:
                        print(traj)
                    else:
                        print("未找到该实体或无时间轨迹。")
                elif op == "0":
                    temporal_analyzer.close()
                    break
                else:
                    print("无效选项，请重试。")
        elif choice == "0":
            print("退出程序。")
            break
        else:
            print("无效选项，请重试。")

if __name__ == "__main__":
    main()