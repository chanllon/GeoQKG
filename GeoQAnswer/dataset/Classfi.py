import re
import csv
# 输入的数据集
data = """
# Paste your data here
"""

# 找出特定样式的数据函数
def find_pattern(pattern, data):
    matches = re.findall(pattern, data)
    return matches

# 正则表达式模式
patterns = {
    "n1 + n2": r'\(\(([^()]+)\)\+([^()]+)\)',
    "n1 - n2": r'\(\(([^()]+)\)\-([^()]+)\)',
    "n1 * n2": r'\(\(([^()]+)\)\*([^()]+)\)',
    "n1 / n2": r'\(\(([^()]+)\)\/([^()]+)\)',

}

# 查找数据
express = {}
keys = ["n1 + n2", "n1 - n2", "n1 * n2","n1 / n2"]  # 替换为您想要的键值

for key in keys:
    express[key] = []

with open('./geo3k/str_exps.csv', encoding='latin1',newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        for pattern_name, regex_pattern in patterns.items():
            match=re.search(regex_pattern,row[1])
            if match:
                # matches = find_pattern(regex_pattern, row[1])
                print(f'匹配模式为：{pattern_name}')
                express[pattern_name].append(row[0])
print(express)

for i in express.keys():
    print(f"{i}的数量为：{len(express[i])}")

            # print(f"Matches for {pattern_name}:")
csv_file = 'calssdata.csv'
expresstoid={"n1 + n2":0, "n1 - n2":1, "n1 * n2":2,"n1 / n2":3}
# # 将词典数据保存到 CSV 文件中
# with open(csv_file, 'w', newline='') as file:
#     writer = csv.writer(file)
#     # writer = csv.DictWriter(file, fieldnames=express.keys())
    # 写入词典数据
    # for i in express.keys():
    #     for j in express[i]:
    #         writer.writerow([j,expresstoid[i]])

print(f"数据已保存到文件 {csv_file}")


