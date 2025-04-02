import csv
import json
from collections import defaultdict

def create_bible_json():
    # 创建嵌套的默认字典来存储数据
    bible_data = defaultdict(lambda: defaultdict(dict))
    
    # 读取CSV文件
    print("开始读取CSV文件...")
    with open('bible.csv', 'r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            book = row['book']
            chapter = row['chapter']
            verse = row['verse']
            content = row['content']
            
            # 将数据添加到嵌套字典中
            bible_data[book][chapter][verse] = content
    
    print("开始写入JSON文件...")
    # 将defaultdict转换为普通字典并写入JSON文件
    with open('bible_data.json', 'w', encoding='utf-8') as json_file:
        # 使用普通字典，确保JSON格式正确
        regular_dict = {
            book: {
                str(chapter): {
                    str(verse): content
                    for verse, content in verses.items()
                }
                for chapter, verses in chapters.items()
            }
            for book, chapters in bible_data.items()
        }
        
        # 写入JSON文件，设置缩进使其易读
        json.dump(regular_dict, json_file, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    create_bible_json()
    print("JSON文件已生成完成！") 