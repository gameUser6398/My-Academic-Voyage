from datetime import datetime
import json
import os
import re
from openai import OpenAI


class EntityRelationClient:
    def __init__(self, api_key, base_url, model="ecnu-plus", 
                 entity_prompt_path='./prompt_entity_recognization.txt',
                 relation_prompt_path='./prompt_relation_recognization.txt',
                 log_dir='./logs'):
        
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.model = model

        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)

        self.entity_system_message = self.load_system_prompt(entity_prompt_path)
        self.relation_system_message = self.load_system_prompt(relation_prompt_path)

    def load_system_prompt(self, system_prompt_path):
        """加载系统提示词文件"""
        with open(system_prompt_path, 'r', encoding='utf-8') as f:
            system_prompt = f.read()
        return {'role': 'system', 'content': system_prompt}

    def extract_entities(self, chunk):
        """实体识别任务"""
        messages = [self.entity_system_message]
        user_message = f"请从以下文本中提取相关实体：\n{chunk}"
        messages.append({'role': 'user', 'content': user_message})

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"实体识别 API 调用出错: {e}")
            return None
        
    def extract_relations(self, chunk, entities=None):
        """关系提取任务"""
        messages = [self.relation_system_message]
        
        if entities:
            user_message = f"已识别的实体：{entities}\n\n请从以下文本中提取这些实体之间的关系：\n{chunk}"
        else:
            user_message = f"请从以下文本中提取实体间的关系：\n{chunk}"
        
        messages.append({'role': 'user', 'content': user_message})

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"关系提取 API 调用出错: {e}")
            return None
    
    def save_log(self, filename, entities_result, relations_result, raw_entities=None, raw_relations=None):
        """将数据保存到日志文件"""
        timestamp = datetime.now().isoformat()
        base_name = os.path.splitext(filename)[0]  # 移除文件扩展名

        # 保存结构化数据
        structured_data = {
            "timestamp": timestamp,
            "filename": filename,
            "entities": entities_result,
            "relations": relations_result,
            "status": "success" if entities_result and relations_result else "partial_success"
        }

        structured_path = os.path.join(self.log_dir, f"{base_name}_structured.json")
        with open(structured_path, 'w', encoding='utf-8') as f:
            json.dump(structured_data, f, ensure_ascii=False, indent=4)

        # 保存原始数据
        raw_data = {
            "timestamp": timestamp,
            "filename": filename,
            "raw_entities": raw_entities,
            "raw_relations": raw_relations
        }

        raw_path = os.path.join(self.log_dir, f"{base_name}_raw.json")
        with open(raw_path, 'w', encoding='utf-8') as f:
            json.dump(raw_data, f, ensure_ascii=False, indent=4)

        return structured_path, raw_path
    
    def parse_response(self, response_text, response_type="entities"):
        """解析API响应"""
        if not response_text:
            return None
        
        # 移除 ```json 和 ``` 标记
        cleaned_text = re.sub(r'```json\s*', '', response_text)
        cleaned_text = re.sub(r'\s*```', '', cleaned_text)
        cleaned_text = cleaned_text.strip()
        
        try:
            return json.loads(cleaned_text)
        
        except json.JSONDecodeError:
             # 如果仍然无法解析，输出错误信息
            print(f"警告: {response_type}响应不是有效JSON格式，保存原始文本")
            return {"raw_text": response_text, "parsed": False}


    # def parse_response(self, response_text, response_type="entities"):
    #     """解析API响应 - 更robust的版本"""
    #     if not response_text:
    #         return None
        



    #     # 尝试多种清理方法
    #     parsing_methods = [
    #         self._extract_json_from_markdown,
    #         self._extract_json_by_braces,
    #         self._clean_simple_format
    #     ]
        
    #     for method in parsing_methods:
    #         try:
    #             cleaned_text = method(response_text)
    #             if cleaned_text:
    #                 parsed_data = json.loads(cleaned_text)
    #                 return parsed_data
    #         except json.JSONDecodeError:
    #             continue
        
    #     # 所有方法都失败，保存原始文本
    #     print(f"警告: {response_type}响应无法解析为JSON，保存原始文本")
    #     return {"raw_text": response_text, "parsed": False}
    
    def _extract_json_from_markdown(self, text):
        """从markdown代码块中提取JSON"""
        # 匹配 ```json ... ``` 或 ``` ... ```
        pattern = r'```(?:json)?\s*([\s\S]*?)\s*```'
        match = re.search(pattern, text, re.IGNORECASE)
        return match.group(1).strip() if match else None
    
    def _extract_json_by_braces(self, text):
        """通过大括号提取JSON内容"""
        # 找到第一个{和最后一个}
        first_brace = text.find('{')
        last_brace = text.rfind('}')
        
        if first_brace != -1 and last_brace != -1 and first_brace < last_brace:
            return text[first_brace:last_brace+1]
        return None
    
    def _clean_simple_format(self, text):
        """简单清理格式"""
        # 移除常见的非JSON前缀后缀
        text = text.strip()
        # 移除可能的markdown标记
        text = re.sub(r'^```(?:json)?\s*', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\s*```\s*$', '', text)
        return text.strip()

    # 注意与process_chunk的区分
    def process_chunk_with_save(self, filename, chunk):
        """处理chunk并立即保存结果"""
        print(f"处理文件: {filename}")
        
        # 实体识别
        raw_entities = self.extract_entities(chunk)
        entities_result = self.parse_response(raw_entities, "entities")
        
        # 即时保存实体结果
        if raw_entities:
            entities_backup_path = os.path.join(self.log_dir, f"{os.path.splitext(filename)[0]}_entities_backup.txt")
            with open(entities_backup_path, "w", encoding="utf-8") as f:
                f.write(raw_entities)
        
        # 关系提取
        raw_relations = self.extract_relations(chunk, raw_entities)
        relations_result = self.parse_response(raw_relations, "relations")
        
        # 即时保存关系结果
        if raw_relations:
            relations_backup_path = os.path.join(self.log_dir, f"{os.path.splitext(filename)[0]}_relations_backup.txt")
            with open(relations_backup_path, "w", encoding="utf-8") as f:
                f.write(raw_relations)
        
        # 保存最终结果
        structured_path, raw_path = self.save_log(
            filename, entities_result, relations_result, raw_entities, raw_relations
        )
        
        return {
            "entities": entities_result,
            "relations": relations_result,
            "structured_path": structured_path,
            "raw_path": raw_path
        }

    def process_chunk(self, chunk):
        """向后兼容的方法"""
        entities = self.extract_entities(chunk)
        relations = self.extract_relations(chunk, entities)
        return entities, relations