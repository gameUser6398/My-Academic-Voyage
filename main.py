import datetime
import time
import os
import json
from tqdm import tqdm
from client import EntityRelationClient
from analyzer import EntityRelationAnalyzer
from neo4j import GraphDatabase

# 配置信息
API_KEY = 'asdfasdfasdf' # "asdfasdfasfd"
BASE_URL = "https://chat.ecnu.edu.cn/open/api/v1"

CHUNKS_DIR = "./chunk_of_2025"  # 切分后的数据目录
LOG_DIR = "./output_of_2025"  # 日志及切分结果目录
ENTITIES_RELATIONS_DIR = "results" # 整合后结果目录
NEO4J_URI = "bolt://localhost:17687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "My_trajectory_0705"

def read_chunks():
    """一次读取所有切分文件"""
    chunks = []
    for filename in os.listdir(CHUNKS_DIR):
        if filename.endswith(".md"):     ################## 只处理markdown文件
            file_path = os.path.join(CHUNKS_DIR, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                chunk = f.read()
                chunks.append((filename, chunk))
    
    return [] # filter_chunks_need_process(chunks)

def load_batch_data(structured_file_path):
    """从单个_structured.json文件加载批次数据"""
    with open(structured_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # 处理实体
    entities_data = data.get("entities", [])
    if isinstance(entities_data, dict) and entities_data.get("parsed", True):
        entities_list = entities_data.get("entities", []) if "entities" in entities_data else []
    elif isinstance(entities_data, list):
        entities_list = entities_data
    else:
        entities_list = []

    # 处理关系
    relations_data = data.get("relations", [])
    if isinstance(relations_data, dict) and relations_data.get("parsed", True):
        relations_list = relations_data.get("relations", []) if "relations" in relations_data else []
    elif isinstance(relations_data, list):
        relations_list = relations_data
    else:
        relations_list = []
    
    # 获取chunk_id作为时间戳
    chunk_id = data.get("entities", {}).get("chunk_id", data.get("relations", {}).get("chunk_id", "unknown"))
    
    return {
        "entities": entities_list,
        "relations": relations_list,
        "chunk_id": chunk_id
    }  

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

"""def create_neo4j_graph(integrated_data):
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    def create_entities(tx, entities):
        for entity in entities:
            tx.run("MERGE (e {name: $name, type: $type})",
                   name=entity["name"], type=entity["type"])

    def create_relations(tx, relations):
        for relation in relations:
            tx.run("MATCH (h {name: $head}), (t {name: $tail}) "
                   "MERGE (h)-[r:RELATION {type: $relation_type}]->(t)",
                   head=relation["head"], tail=relation["tail"], relation_type=relation["type"])

    with driver.session() as session:
        session.execute_write(create_entities, integrated_data["entities"])
        session.execute_write(create_relations, integrated_data["relations"])

    driver.close()"""


class Neo4jManager:
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        self.batch_properties = {}  # 用于存储批次属性

    def merge_batch_data(self, batch_data, batch_id):
        """合并批次数据到现有图谱"""

        # 存储批次属性，为时间戳预留
        chunk_timestamp = batch_data.get('chunk_id', datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))

        with self.driver.session() as session:
            # 1. 合并实体节点
            session.execute_write(self._merge_entities, batch_data['entities'], batch_id, chunk_timestamp)
            
            # 2. 合并关系
            session.execute_write(self._merge_relations, batch_data['relations'], batch_id, chunk_timestamp)
            
            # 3. 更新批次信息
            session.execute_write(self._update_batch_info, batch_id, chunk_timestamp)

    def _merge_entities(self, tx, entities, batch_id, chunk_timestamp):
        """合并实体节点 - 支持多标签"""
        for entity in entities:
            entity_type = entity.get('type', 'Unknown').replace(" ", "_").replace("-", "_")
            # 确保标签名符合Neo4j规范
            
            tx.run(f"""
                MERGE (e:{entity_type} {{name: $name}})
                ON CREATE SET 
                    e.type = $type,
                    e.created_at = datetime(),
                    e.batches = [$batch_id],
                    e.timestamps = [$chunk_timestamp]
                ON MATCH SET 
                    e.batches = CASE WHEN NOT $batch_id IN e.batches THEN e.batches + $batch_id ELSE e.batches END,
                    e.timestamps = CASE WHEN NOT $chunk_timestamp IN e.timestamps THEN e.timestamps +$chunk_timestamp ELSE e.timestamps END
            """, name=entity['name'], type=entity['type'], 
                batch_id=batch_id, chunk_timestamp=chunk_timestamp, )

    def _merge_relations(self, tx, relations, batch_id, chunk_timestamp):
        """合并关系"""
        for relation in relations:
            tx.run("""
                MATCH (h {name: $head}), (t {name: $tail})
                MERGE (h)-[r:RELATION {type: $relation_type}]->(t)
                ON CREATE SET 
                    r.created_at = datetime(),
                    r.batches = [$batch_id],
                    r.timestamps = [$chunk_timestamp]
                ON MATCH SET 
                    r.batches = CASE WHEN NOT $batch_id IN r.batches THEN r.batches + $batch_id ELSE r.batches END,
                    r.timestamps = CASE WHEN NOT $chunk_timestamp IN r.timestamps THEN r.timestamps + $chunk_timestamp ELSE r.timestamps END
            """, head=relation['head'], tail=relation['tail'], 
                  relation_type=relation['type'], batch_id=batch_id, chunk_timestamp=chunk_timestamp)
    
    def setup_neo4j_styles(self):
        """设置Neo4j浏览器中的节点样式"""
        
        style_commands = {
            "生物分子": {
                "color": "#2E8B57",  # 深绿色
                "border_color": "#1F5F3F",
                "text_color": "#FFFFFF",
            },
            "生物医学概念": {
                "color": "#3CB371",  # 中等绿色  
                "border_color": "#2F8B57",
                "text_color": "#FFFFFF",
            },
            "生物技术": {
                "color": "#20B2AA",  # 浅绿色
                "border_color": "#1C9A93", 
                "text_color": "#FFFFFF",
            },
            "生物信息工具": {
                "color": "#FF6347",  # 番茄红
                "border_color": "#E55039",
                "text_color": "#FFFFFF", 
            },
            "深度学习概念": {
                "color": "#DC143C",  # 深红色
                "border_color": "#B22222",
                "text_color": "#FFFFFF",
            },
            "项目活动": {
                "color": "#A9A9A9",  # 深灰色
                "border_color": "#808080", 
                "text_color": "#FFFFFF",
            },
        }
        
        print("\n=== Neo4j Community浏览器样式配置 ===")
        # 生成样式配置的JSON文件
        self._generate_style_config_file(style_commands)
        
        return style_commands

    def _generate_style_config_file(self, style_commands):
        """生成Neo4j Desktop可导入的样式配置文件"""
        
        # Neo4j Desktop样式配置格式
        desktop_style = {
            "node": {},
            "relationship": {}
        }
        
        for label, style in style_commands.items():
            desktop_style["node"][label] = {
                "color": style["color"],
                "border-color": style["border_color"], 
                "text-color-internal": style["text_color"],
            }
        
        # 保存样式配置
        style_file_path = os.path.join(ENTITIES_RELATIONS_DIR, "neo4j_styles.json")
        os.makedirs(os.path.dirname(style_file_path), exist_ok=True)
        
        with open(style_file_path, 'w', encoding='utf-8') as f:
            json.dump(desktop_style, f, ensure_ascii=False, indent=2)
        
        print(f"\n样式配置已保存到: {style_file_path}")
        print("您可以在Neo4j Desktop中导入此样式配置文件")

    def _update_batch_info(self, tx, batch_id, chunk_timestamp):
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
        if not network_stats:
            return
        
        # 获取所有节点名称
        all_nodes = set()
        for metric_name, node_values in network_stats.items():
            if isinstance(node_values, dict):
                all_nodes.update(node_values.keys())
        
        print(f"发现 {len(all_nodes)} 个节点需要更新指标")

           # 为每个节点更新指标
        for node_name in all_nodes:
            # 从各个指标字典中获取该节点的值
            degree_centrality = network_stats.get('degree_centrality', {}).get(node_name, 0.0)
            betweenness_centrality = network_stats.get('betweenness_centrality', {}).get(node_name, 0.0)
            closeness_centrality = network_stats.get('closeness_centrality', {}).get(node_name, 0.0)
            in_degree_centrality = network_stats.get('in_degree_centrality', {}).get(node_name, 0.0)
            out_degree_centrality = network_stats.get('out_degree_centrality', {}).get(node_name, 0.0)
            
            # 确保所有值都是数字类型
            degree_centrality = float(degree_centrality) if degree_centrality is not None else 0.0
            betweenness_centrality = float(betweenness_centrality) if betweenness_centrality is not None else 0.0
            closeness_centrality = float(closeness_centrality) if closeness_centrality is not None else 0.0
            in_degree_centrality = float(in_degree_centrality) if in_degree_centrality is not None else 0.0
            out_degree_centrality = float(out_degree_centrality) if out_degree_centrality is not None else 0.0
            
            try:
                tx.run("""
                    MATCH (n:Entity {name: $name})
                    SET n.degree_centrality = $degree_centrality,
                        n.betweenness_centrality = $betweenness_centrality,
                        n.closeness_centrality = $closeness_centrality,
                        n.in_degree_centrality = $in_degree_centrality,
                        n.out_degree_centrality = $out_degree_centrality,
                        n.updated_at = datetime()
                """, 
                name=node_name,
                degree_centrality=degree_centrality,
                betweenness_centrality=betweenness_centrality,
                closeness_centrality=closeness_centrality,
                in_degree_centrality=in_degree_centrality,
                out_degree_centrality=out_degree_centrality)
            except Exception as e:
                print(f"更新节点 {node_name} 失败: {e}")
   
    
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

        
def main():

    os.makedirs(LOG_DIR, exist_ok=True)  # 确保日志目录存在

    # 初始化客户端
    client = EntityRelationClient(API_KEY, BASE_URL, model="ecnu-plus", log_dir=LOG_DIR)
    chunks = read_chunks()

    # ----------------------------------------
    # 处理每个chunk，进行实体识别和关系提取
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
    # 更新 Neo4j 节点和关系
    neo4j_manager = Neo4jManager()
    
    USE_BATCH_MERGE = input(f"是否使用批量合并{LOG_DIR}中的数据？(y/n): ").strip().lower() == 'y'
    
    if USE_BATCH_MERGE:
        print("\n=== 使用逐批次合并模式 ===")
        # 逐批次合并到Neo4j
        for filename in tqdm(os.listdir(LOG_DIR)):
            if filename.endswith("_structured.json"):
                file_path = os.path.join(LOG_DIR, filename)
                try:
                    batch_data = load_batch_data(file_path)
                    if batch_data["entities"] or batch_data["relations"]:
                        # 使用文件名作为batch_id
                        batch_id = filename.replace("_structured.json", "")
                        neo4j_manager.merge_batch_data(batch_data, batch_id)
                    else:
                        print(f"⚠ 跳过空批次: {filename}")
                except Exception as e:
                    print(f"✗ 批次合并失败: {filename}, 错误: {e}")
        
        # 为了分析指标，仍需要获取整体数据
        integrated_data = integrate_entities_relations()
    
    else:
        print("\n=== 使用整体合并模式 ===")
        # 整体合并
        try:
            integrated_data = integrate_entities_relations()
            print(f"整合完成: {len(integrated_data['entities'])} 个实体, {len(integrated_data['relations'])} 个关系")
            
            # 整体合并到Neo4j
            batch_id = f"integrated_batch"
            # 对于整体合并，我们不传递具体的时间戳
            batch_data_for_merge = {
                "entities": integrated_data["entities"],
                "relations": integrated_data["relations"],
                "chunk_id": ""  # 整体合并时没有单一chunk_id
            }
            neo4j_manager.merge_batch_data(batch_data_for_merge, batch_id)
        
        except Exception as e:
            print(f"整合创建失败: {e}")
            neo4j_manager.close()
            return

    # ---------------------------------------------------
    # 更新分析指标
    try:
        analyzer = EntityRelationAnalyzer(integrated_data)
        metrics = analyzer.generate_summary_report()
        neo4j_manager.update_analysis_metrics(metrics)
    except Exception as e:
        print(f"分析指标更新失败: {e}")
    
    # 轨迹分析（可选）
    # if enable_trajectory_analysis:

    #     trajectory_results = analyzer.temporal_analysis(get_historical_data())



    neo4j_manager.close()

if __name__ == "__main__":
    main()
