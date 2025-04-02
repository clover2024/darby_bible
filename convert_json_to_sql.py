import json

def create_bible_sql():
    # SQL建表语句
    create_table_sql = '''
CREATE TABLE IF NOT EXISTS bible_verses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book TEXT NOT NULL,
    chapter INTEGER NOT NULL,
    verse INTEGER NOT NULL,
    content TEXT NOT NULL
);
'''
    
    # 打开输出文件
    with open('bible.sql', 'w', encoding='utf-8') as sql_file:
        # 写入建表语句
        sql_file.write(create_table_sql + '\n')
        
        # 读取JSON文件
        with open('bible_data.json', 'r', encoding='utf-8') as json_file:
            bible_data = json.load(json_file)
            
        # 生成插入语句 - 使用双引号包裹字符串值
        insert_template = 'INSERT INTO bible_verses (book, chapter, verse, content) VALUES ("{}", {}, {}, "{}");\n'
        
        # 遍历所有书卷
        for book, chapters in bible_data.items():
            for chapter, verses in chapters.items():
                for verse, content in verses.items():
                    # 处理内容中的双引号（如果有的话）
                    content = content.replace('"', '""')
                    book = book.replace('"', '""')
                    # 生成插入语句
                    insert_sql = insert_template.format(
                        book,
                        chapter,
                        verse,
                        content
                    )
                    sql_file.write(insert_sql)

if __name__ == '__main__':
    create_bible_sql()
    print("SQL文件已生成完成！") 