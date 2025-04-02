import csv
import re

def extract_book_info(file_path):
    verses_data = []
    current_book = None
    current_chapter = None
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            
            # 提取书卷名称 - 修正为BIBLEBOOK标签
            book_match = re.search(r'<BIBLEBOOK\s+\w+="[^"]+"\s+bname="([^"]+)"', line)
            if book_match:
                current_book = book_match.group(1)
                print(f"找到书卷: {current_book}")
                continue
            
            # 提取章节号码
            chapter_match = re.search(r'<CHAPTER cnumber="(\d+)"', line)
            if chapter_match:
                current_chapter = chapter_match.group(1)
                continue
            
            # 提取经文（只有当已经找到书卷和章节时才处理）
            if current_book and current_chapter:
                verse_match = re.search(r'<VERS vnumber="(\d+)">(.*?)</VERS>', line)
                if verse_match:
                    verse_number = verse_match.group(1)
                    content = verse_match.group(2).strip()
                    verses_data.append([
                        current_book,
                        current_chapter,
                        verse_number,
                        content
                    ])
    
    return verses_data

def create_bible_csv():
    # 输入和输出文件路径
    xml_file = 'eng-darby.osis.xml'
    csv_file = 'bible.csv'

    print("开始提取数据...")
    verses_data = extract_book_info(xml_file)
    print(f"提取完成，共找到 {len(verses_data)} 节经文")

    print("开始写入CSV文件...")
    with open(csv_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['book', 'chapter', 'verse', 'content'])
        writer.writerows(verses_data)

if __name__ == '__main__':
    create_bible_csv()
    print("CSV文件已生成完成！") 