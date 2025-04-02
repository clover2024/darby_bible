import json
import csv

def create_bible_csv():
    # 打开CSV文件
    with open('bible.csv', 'w', encoding='utf-8', newline='') as csv_file:
        # 创建CSV写入器
        csv_writer = csv.writer(csv_file)
        
        # 写入表头
        csv_writer.writerow(['book', 'chapter', 'verse', 'content'])
        
        # 读取JSON文件
        with open('bible_data.json', 'r', encoding='utf-8') as json_file:
            bible_data = json.load(json_file)
        
        # 遍历所有书卷并写入数据
        for book, chapters in bible_data.items():
            for chapter, verses in chapters.items():
                for verse, content in verses.items():
                    csv_writer.writerow([
                        book,
                        chapter,
                        verse,
                        content
                    ])

if __name__ == '__main__':
    create_bible_csv()
    print("CSV文件已生成完成！") 