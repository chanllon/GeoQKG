import csv
import json
geo3k=[]
with open('/home/dxl/Represention_learning/KGMEU/dataset/gps/Inter-GPS_datas_200.csv', encoding='latin1',newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        geo_item={
            "id": row[0],
            "original_text": row[3],
            "segmented_text": row[4],
            "equation": row[1],
            "ans": row[2]
        }
        geo3k.append(geo_item)

from sklearn.model_selection import train_test_split

# 假设 formatted_data 是你已经格式化好的数据
train_data, test_data = train_test_split(geo3k, test_size=0.2, random_state=42)
train_data, val_data = train_test_split(train_data, test_size=0.25, random_state=42)


# 存储为JSON文件
with open('./gps/trainset.json', 'w',encoding='utf-8') as train_file:
    json.dump(train_data, train_file)

with open('./gps/validset.json', 'w',encoding='utf-8') as val_file:
    json.dump(val_data, val_file)

with open('./gps/testset.json', 'w',encoding='utf-8') as test_file:
    json.dump(test_data, test_file)