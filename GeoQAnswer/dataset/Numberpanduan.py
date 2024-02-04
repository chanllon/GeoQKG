import csv
import json
import re


def tokenize_sentence(sentence):
    # 定义正则表达式模式
    pattern = r"[\w']+|[.,!?;]"

    # 使用正则表达式分词
    tokens = re.findall(pattern, sentence)
    return tokens


# 读取第二个文件到字典中
geo_en_text_dict = {}
with open('./geo3k/geo_en_text.csv', encoding='latin1', newline='') as output:
    file2 = csv.reader(output)
    for row in file2:
        geo_en_text_dict[row[0]] = row[1]

geo3ktext = []
with open('./geo3k/str_exps.csv', encoding='latin1', newline='') as csvfile:
    file1 = csv.reader(csvfile)
    for row in file1:
        id = row[0]
        if id in geo_en_text_dict:
            text = geo_en_text_dict[id]
            seg = tokenize_sentence(text)
            segtxt = ' '.join(seg)
            geo_item = {
                "id": id,
                "original_text": text,
                "segmented_text": segtxt,
                "equation": row[1],
                "ans": row[4]
            }
            geo3ktext.append(geo_item)

print(geo3ktext)


from sklearn.model_selection import train_test_split

# 假设 formatted_data 是你已经格式化好的数据
train_data, test_data = train_test_split(geo3ktext, test_size=0.2, random_state=42)
train_data, val_data = train_test_split(train_data, test_size=0.25, random_state=42)


# 存储为JSON文件
with open('./geo3ktext/trainset.json', 'w',encoding='utf-8') as train_file:
    json.dump(train_data, train_file)

with open('./geo3ktext/validset.json', 'w',encoding='utf-8') as val_file:
    json.dump(val_data, val_file)

with open('./geo3ktext/testset.json', 'w',encoding='utf-8') as test_file:
    json.dump(test_data, test_file)
