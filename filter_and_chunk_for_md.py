import re
import argparse
import os

def preprocess_md_file(file_path, min_chunk_length=200):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    content = re.sub(r'\n{3,}', '\n\n', content)
    content = content.strip()

    # 按 OneNote 标志切分文档
    one_note_pattern = re.compile(r'(分区.*?\n\n.*?\n\n\d{4}年\d{1,2}月\d{1,2}日\n\n\d{1,2}:\d{2})', re.DOTALL)
    chunks = re.split(one_note_pattern, content)
    chunks = [chunk for chunk in chunks if chunk.strip()]

    # 合并过于简短的分片
    merged_chunks = []
    current_chunk = ""
    for chunk in chunks:
        if current_chunk:
            combined_chunk = current_chunk + "\n\n" + chunk
            if len(combined_chunk) >= min_chunk_length:
                merged_chunks.append(combined_chunk)
                current_chunk = ""
            else:
                current_chunk = combined_chunk
        else:
            if len(chunk) >= min_chunk_length:
                merged_chunks.append(chunk)
            else:
                current_chunk = chunk
    if current_chunk:
        merged_chunks.append(current_chunk)

    return merged_chunks

def extract_date_from_chunk(chunk):
    # 匹配 2024年6月5日 这种格式
    match = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})日', chunk)
    if match:
        year, month, day = match.groups()
        return f"{year}{int(month):02d}{int(day):02d}"
    return "unknown_date"

def save_chunks_to_files(chunks, output_dir, prefix="chunk"):
    os.makedirs(output_dir, exist_ok=True)
    for idx, chunk in enumerate(chunks, 1):
        date_str = extract_date_from_chunk(chunk)
        filename = f"{prefix}_{idx:03d}_{date_str}.md"
        file_path = os.path.join(output_dir, filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(chunk)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preprocess Markdown files.")
    parser.add_argument('-i', '--input', required=True, help="Path to the input Markdown file.")
    parser.add_argument('-o', '--output_dir', required=True, help="Directory to save the chunked files.")

    args = parser.parse_args()

    md_file_path = args.input
    output_dir = args.output_dir

    processed_chunks = preprocess_md_file(md_file_path)
    save_chunks_to_files(processed_chunks, output_dir)
