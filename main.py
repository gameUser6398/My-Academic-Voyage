import datetime
import time
import os
import json
from client import EntityRelationClient
from analyzer import EntityRelationAnalyzer
from neo4j import GraphDatabase

# 配置信息
API_KEY = 'sk-a23c5b2ae86a4a668e05729d435be035' # "sk-a23c5b2ae86a4a668e05729d435be035"
BASE_URL = "https://chat.ecnu.edu.cn/open/api/v1"

CHUNKS_DIR = "./chunk_of_2024"  # 切分后的数据目录
LOG_DIR = "./output_of_2024"  # 日志及切分结果目录
ENTITIES_RELATIONS_DIR = "results" # 整合后结果目录
NEO4J_URI = "bolt://localhost:17687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "My_trajectory_0705"

def read_chunks():
    chunks = []
    for filename in os.listdir(CHUNKS_DIR):
        if filename.endswith(".md"):     ################## 只处理markdown文件
            file_path = os.path.join(CHUNKS_DIR, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                chunk = f.read()
                chunks.append((filename, chunk))
    
    return filter_chunks_need_process(chunks)

def filter_chunks_need_process(chunks):
    need_process_chunks = []
    for filename, chunk in chunks:
        stru_file = os.path.join(LOG_DIR, f"{filename.replace('.md', '')}_structured.json")
        
        if not os.path.exists(stru_file):
            need_process_chunks.append((filename, chunk))
            continue
        if json.loads(open(stru_file).read()).get("status") != "success":
            need_process_chunks.append((filename, chunk))
    return need_process_chunks


def integrate_entities_relations():
    all_entities = []
    all_relations = []
    entity_names = set()
    relation_tuples = set()

    for filename in os.listdir(LOG_DIR):
        if filename.endswith("_structured.json"):   # 只处理结构化日志文件
            file_path = os.path.join(LOG_DIR, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

                # 处理实体
                entities_data = data.get("entities", [])
                if isinstance(entities_data, dict) and entities_data.get("parsed", True):
                    entities_list = entities_data.get("entities", []) if "entities" in entities_data else []
                elif isinstance(entities_data, list):
                    entities_list = entities_data
                else:
                    entities_list = []
                
                for entity in entities_list:
                    if isinstance(entity, dict) and entity.get("name") not in entity_names:
                        all_entities.append(entity)
                        entity_names.add(entity["name"])
                
                # 处理关系
                relations_data = data.get("relations", [])
                if isinstance(relations_data, dict) and relations_data.get("parsed", True):
                    relations_list = relations_data.get("relations", []) if "relations" in relations_data else []
                elif isinstance(relations_data, list):
                    relations_list = relations_data
                else:
                    relations_list = []
                
                for relation in relations_list:
                    if isinstance(relation, dict):
                        relation_tuple = (relation.get("head"), relation.get("type"), relation.get("tail"))
                        if all(relation_tuple) and relation_tuple not in relation_tuples:
                            all_relations.append(relation)
                            relation_tuples.add(relation_tuple)

    # 确保目录存在
    integrated_path = os.path.join(ENTITIES_RELATIONS_DIR, os.path.basename(CHUNKS_DIR), "integrated_entities_relations.json")
    os.makedirs(os.path.dirname(integrated_path), exist_ok=True)

    integrated_data = {
        "entities": all_entities,
        "relations": all_relations
    }
    with open(integrated_path, "w", encoding="utf-8") as f:
        json.dump(integrated_data, f, ensure_ascii=False, indent=4)
    return integrated_data

def create_neo4j_graph(integrated_data):
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    def create_entities(tx, entities):
        for entity in entities:
            tx.run("MERGE (e:Entity {name: $name, type: $type})",
                   name=entity["name"], type=entity["type"])

    def create_relations(tx, relations):
        for relation in relations:
            tx.run("MATCH (h:Entity {name: $head}), (t:Entity {name: $tail}) "
                   "MERGE (h)-[r:RELATION {type: $relation_type}]->(t)",
                   head=relation["head"], tail=relation["tail"], relation_type=relation["type"])

    with driver.session() as session:
        session.execute_write(create_entities, integrated_data["entities"])
        session.execute_write(create_relations, integrated_data["relations"])

    driver.close()


class Neo4jManager:
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        self.batch_properties = {}  # 用于存储批次属性

    def merge_batch_data(self, batch_data, batch_id):
        """合并批次数据到现有图谱"""
        print(f"\n=== 合并批次数据 {batch_id} ===")  # 对应structured.json中的filename

        # 存储批次属性，为时间戳预留
        self.batch_properties[batch_id] = {
            # 'timestamp': datetime.datetime.now().isoformat(),  # 这是当前合并时间
            'batch_id': batch_data["chunk_id"],    # 对应chunk_id
            'entity_count': len(batch_data['entities']),
            'relation_count': len(batch_data['relations'])
        }

        with self.driver.session() as session:
            # 1. 合并实体节点
            session.execute_write(self._merge_entities, batch_data['entities'], batch_id)
            
            # 2. 合并关系
            session.execute_write(self._merge_relations, batch_data['relations'], batch_id)
            
            # 3. 更新批次信息
            session.execute_write(self._update_batch_info, batch_id)

    def _merge_entities(self, tx, entities, batch_id):
        """合并实体节点"""
        for entity in entities:
            tx.run("""
                MERGE (e:Entity {name: $name})
                ON CREATE SET 
                    e.type = $type,
                    e.created_at = datetime(),
                    e.batches = [$batch_id]
                ON MATCH SET 
                    e.batches = CASE WHEN NOT $batch_id IN e.batches THEN e.batches + $batch_id ELSE e.batches END
            """, name=entity['name'], type=entity['type'], batch_id=batch_id)

    def _merge_relations(self, tx, relations, batch_id):
        """合并关系"""
        for relation in relations:
            tx.run("""
                MATCH (h:Entity {name: $head}), (t:Entity {name: $tail})
                MERGE (h)-[r:RELATION {type: $relation_type}]->(t)
                ON CREATE SET 
                    r.created_at = datetime(),
                    r.batches = [$batch_id]
                ON MATCH SET 
                    r.batches = CASE WHEN NOT $batch_id IN r.batches THEN r.batches + $batch_id ELSE r.batches END
            """, head=relation['head'], tail=relation['tail'], 
                  relation_type=relation['type'], batch_id=batch_id)
    def _update_batch_info(self, tx, batch_id):
        """更新批次信息(预留)"""
        # 这里可以添加更多批次级别的信息更新
        pass
    
    def update_analysis_metrics(self, metrics):
        """更新分析指标到节点"""
        print("\n=== 更新分析指标 ===")
        
        with self.driver.session() as session:
            # 更新网络分析指标
            session.execute_write(self._update_network_metrics, metrics.get('network_stats', {}))
            
            # 更新社区检测结果
            session.execute_write(self._update_community_info, metrics.get('communities', {}))
    
    def _update_network_metrics(self, tx, network_stats):
        """更新网络分析指标"""
        for node_name, metrics in network_stats.items():
            tx.run("""
                MATCH (n:Entity {name: $name})
                SET n.degree_centrality = $degree_cent,
                    n.betweenness_centrality = $betweenness_cent,
                    n.closeness_centrality = $closeness_cent,
                    n.in_degree_centrality = $in_degree_cent,
                    n.out_degree_centrality = $out_degree_cent,
                    n.updated_at = datetime()
            """, name=node_name, **metrics)
    
    def _update_community_info(self, tx, communities):
        """更新社区检测结果"""
        for node_name, community_id in communities.items():
            tx.run("""
                MATCH (n:Entity {name: $name})
                SET n.community = $community_id,
                    n.updated_at = datetime()
            """, name=node_name, community_id=community_id)
    
    def close(self):
        """关闭Neo4j连接"""
        if self.driver:
            self.driver.close()
   
    def generate_neo4j_queries(self):
        """生成常用的Neo4j查询语句"""
        queries = {
            "查看所有节点和边": "MATCH (n)-[r]->(m) RETURN n, r, m",
            
            "按实体类型分组统计": """
                MATCH (n:Entity)
                RETURN n.type as entity_type, count(n) as count, collect(n.color)[0] as color
                ORDER BY count DESC
            """,
            
            "度中心性TOP10": """
                MATCH (n:Entity)
                RETURN n.name, n.type, n.degree_centrality, n.degree
                ORDER BY n.degree_centrality DESC
                LIMIT 10
            """,
            
            "社区内节点": """
                MATCH (n:Entity)
                WHERE n.community = 0
                RETURN n.name, n.type, n.degree_centrality
                ORDER BY n.degree_centrality DESC
            """,
            
            "按颜色可视化": """
                MATCH (n:Entity)
                RETURN n.name, n.type, n.color, n.degree_centrality
            """,
            
            "关系类型统计": """
                MATCH ()-[r:RELATION]->()
                RETURN r.type as relation_type, count(r) as count
                ORDER BY count DESC
            """,
            
            "高度中心性节点的邻居": """
                MATCH (n:Entity)
                WHERE n.degree_centrality > 0.1
                MATCH (n)-[r]-(neighbor)
                RETURN n.name as central_node, collect(neighbor.name) as neighbors
            """
        }
        
        print("\n=== Neo4j常用查询语句 ===")
        for description, query in queries.items():
            print(f"\n{description}:")
            print(query)
        
        return queries
    
    
    def close(self):
        """关闭Neo4j连接"""
        if self.driver:
            self.driver.close()
        
def main():

    os.makedirs(LOG_DIR, exist_ok=True)  # 确保日志目录存在

    # 初始化客户端
    client = EntityRelationClient(API_KEY, BASE_URL, model="ecnu-plus", log_dir=LOG_DIR)
    chunks = read_chunks()

    # 处理每个chunk并保存
    successful_files = []
    failed_files = []

    for filename, chunk in chunks:
        try:
            result = client.process_chunk_with_save(filename, chunk)
            if result["entities"] and result["relations"]:
                successful_files.append(filename)
                print(f"✓ 成功处理: {filename}")
            else:
                failed_files.append(filename)
                print(f"⚠ 部分失败: {filename}")
        except Exception as e:
            failed_files.append(filename)
            print(f"✗ 处理失败: {filename}, 错误: {e}")
        finally:
            time.sleep(3)  # 避免 API 调用过于频繁

    print(f"\n处理完成: 成功 {len(successful_files)} 个, 失败 {len(failed_files)} 个")
    if failed_files:
        print(f"失败文件: {failed_files}")

    # ---------------------------------------------------
    # 整合实体和关系
    try:
        integrated_data = integrate_entities_relations()
        print(f"整合完成: {len(integrated_data['entities'])} 个实体, {len(integrated_data['relations'])} 个关系")
    except Exception as e:
        print(f"整合创建失败: {e}")
        return 
    
    # ---------------------------------------------------
    # 更新 Neo4j 节点和关系
    neo4j_manager = Neo4jManager(NEO4J_URI, (NEO4J_USER, NEO4J_PASSWORD))
    analyzer = EntityRelationAnalyzer(integrated_data)
    
    batch_id = f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    neo4j_manager.merge_batch_data(integrated_data, batch_id, datetime.now())
    
    # ---------------------------------------------------
    # 更新分析指标
    metrics = analyzer.generate_summary_report()
    neo4j_manager.update_analysis_metrics(metrics)
    
    # 轨迹分析（可选）
    # if enable_trajectory_analysis:
    #     trajectory_results = analyzer.temporal_analysis(get_historical_data())

    # 提示查询命令
    neo4j_manager.generate_neo4j_queries()

    neo4j_manager.close()