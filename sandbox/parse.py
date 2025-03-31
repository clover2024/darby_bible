import json
import re
import os

def extract_book_order(file_path):
    """
    提取圣经文本文件中书卷的原始顺序
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用正则表达式匹配所有书卷名称，包括带数字前缀的书卷和多单词书卷名称（如Song of Solomon）
    book_pattern = re.compile(r'\n\n(\d+\s+[A-Za-z]+(?:\s+of\s+[A-Za-z]+)?|[A-Za-z]+(?:\s+of\s+[A-Za-z]+)?) \d+\n\n', re.DOTALL)
    book_matches = book_pattern.findall(content)
    
    # 去重并保持原始顺序
    book_order = []
    for book in book_matches:
        if book not in book_order:
            book_order.append(book)
    
    return book_order

def parse_bible_file(file_path):
    """
    解析圣经文本文件，将其转换为结构化的JSON格式
    修复之前的解析问题：
    1. 确保识别所有书卷，包括带数字前缀的书卷和多单词书卷名称（如Song of Solomon）
    2. 正确区分每章中的各节经文
    3. 保持原有的书卷顺序
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取书卷的原始顺序
    book_order = extract_book_order(file_path)
    print(f"提取到 {len(book_order)} 个书卷的原始顺序")
    
    # 创建数据结构来存储解析后的圣经内容
    bible_data = {}
    
    # 使用正则表达式匹配书卷章节和经文
    # 匹配模式：书名 章号，后面跟着经文内容直到下一个书卷章节或文件结束
    # 修改正则表达式以匹配多单词书卷名称（如Song of Solomon）
    book_chapter_pattern = re.compile(r'\n\n((?:\d+\s+)?[A-Za-z]+(?:\s+of\s+[A-Za-z]+)?) (\d+)\n\n(.*?)(?=\n\n\n|\n\n(?:\d+\s+)?[A-Za-z]+(?:\s+of\s+[A-Za-z]+)? \d+\n\n|$)', re.DOTALL)
    book_chapters = book_chapter_pattern.findall(content)
    
    # 用于跟踪已处理的书卷章节
    processed_chapters = set()
    
    for book_name, chapter_num, chapter_content in book_chapters:
        # 跳过已处理的书卷章节
        if (book_name, chapter_num) in processed_chapters:
            continue
        
        processed_chapters.add((book_name, chapter_num))
        
        if book_name not in bible_data:
            bible_data[book_name] = {}
        
        # 使用直接的行解析方法，更可靠地分隔经文
        verses = parse_verses_direct(chapter_content)
        
        bible_data[book_name][chapter_num] = verses
    
    return bible_data, book_order

def parse_verses_direct(chapter_content):
    """
    改进的经文解析方法，能够处理数字后直接跟符号的特殊格式经节
    """
    verses = {}
    
    # 清理章节内容
    chapter_content = chapter_content.strip()
    
    # 按行分割内容
    lines = chapter_content.split('\n')
    
    current_verse = None
    current_text = ""
    
    for line in lines:
        line = line.strip()
        if not line:  # 跳过空行
            continue
            
        # 修改正则表达式，匹配数字后直接跟符号的情况（如8*、8(、8[、8{）
        # 新的模式匹配：数字后可以直接跟空格或特殊符号
        verse_match = re.match(r'^(\d+)(?:\s+|[*(\[{])(.*)$', line)
        if verse_match:
            # 如果已经有当前经文，保存它
            if current_verse is not None and current_text:
                verses[current_verse] = re.sub(r'\s+', ' ', current_text).strip()
            
            # 开始新的经文
            current_verse = verse_match.group(1)
            
            # 如果匹配到的是特殊格式（数字后直接跟符号），需要将符号包含在经文内容中
            if not verse_match.group(0).startswith(current_verse + ' '):
                # 找出数字后的第一个字符
                first_char_after_num = verse_match.group(0)[len(current_verse)]
                current_text = first_char_after_num + verse_match.group(2)
            else:
                current_text = verse_match.group(2)
        else:
            # 继续当前经文
            if current_verse is not None:
                current_text += " " + line
    
    # 保存最后一节经文
    if current_verse is not None and current_text:
        verses[current_verse] = re.sub(r'\s+', ' ', current_text).strip()
    
    return verses

def main():
    # 解析圣经文本文件
    print("开始解析圣经文本文件...")
    bible_data, book_order = parse_bible_file('./resources/Darbible.txt')
    
    # 创建输出目录
    # os.makedirs('/home/ubuntu/bible_app_improved', exist_ok=True)
    
    # 将解析后的数据保存为JSON文件
    with open('./bible_data.json', 'w', encoding='utf-8') as f:
        json.dump(bible_data, f, ensure_ascii=False, indent=2)
    
    # 保存书卷顺序
    with open('./book_order.json', 'w', encoding='utf-8') as f:
        json.dump(book_order, f, ensure_ascii=False, indent=2)
    
    # 打印一些统计信息
    print(f"总共解析了 {len(bible_data)} 卷书")
    print(f"书卷顺序: {book_order}")
    
    # 检查每卷书的章节和经文数量
    for book_name in book_order:
        if book_name not in bible_data:
            print(f"警告: {book_name} 在数据中不存在")
            continue
            
        chapter_count = len(bible_data[book_name])
        print(f"{book_name}: {chapter_count} 章")
        
        # 打印第一章的经文数量和前3节经文作为示例
        if chapter_count > 0:
            first_chapter = sorted(bible_data[book_name].keys(), key=int)[0]
            verses = bible_data[book_name][first_chapter]
            verse_count = len(verses)
            print(f"  第 {first_chapter} 章: {verse_count} 节经文")
            
            if verse_count > 0:
                verse_keys = sorted(verses.keys(), key=int)
                for i in range(min(3, len(verse_keys))):
                    verse_num = verse_keys[i]
                    verse_text = verses[verse_num]
                    print(f"    {verse_num}: {verse_text[:50]}..." if len(verse_text) > 50 else f"    {verse_num}: {verse_text}")

if __name__ == "__main__":
    main()
