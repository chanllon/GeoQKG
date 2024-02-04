import os
import json
import csv
import re

import pandas as pd

##Path
root_directory = 'text_logic_forms.json'
csv_file_path = "Geo_Logic_form_language1.csv"

delete_first_list = ['RightAngle','Right','Isosceles','Equilateral','Regular', 'Red','Blue','Green','Shaded']

#Latex
def convert_latex_to_plain_text(latex_code,delete_list):
    # 将\frac{}{}转换为分数形式
    latex_code = re.sub(r'\\frac{([^{}]*)}{([^{}]*)}', r'\1/\2', latex_code)
    # 将^{}转换为上标形式
    latex_code = re.sub(r'\^{([^{}]*)}', r'**\1', latex_code)
    # 将\sqrt{}转换为平方根形式
    latex_code = re.sub(r'\\sqrt{([^{}]*)}', r'√\1', latex_code)

    # 匹配带有"angle"或"Angle"后接空格和字母/数字的子字符串，并进行替换
    latex_code = re.sub(r'(angle|Angle)\s+([a-zA-Z0-9]+)', r'Angle(A_\2)', latex_code)

    # 构建正则表达式模式，匹配delete_list中的元素后的括号
    delete_pattern = r'\b(?:' + '|'.join(re.escape(word) for word in delete_list) + r')\b\((.*?)\)'
    # 使用正则表达式替换匹配到的部分为括号内的内容
    latex_code = re.sub(delete_pattern, r'\1', latex_code)

    return latex_code

# logic_form.json-to-csv
def read_logic_form_files(root_dir,csv_file_path):
    for root, dirs,_ in os.walk(root_dir):
        for dir in dirs:
            fi_path = os.path.join(root, dir)
            for r, files,_ in os.walk(fi_path):
                for f in files:
                    f_path=os.path.join(r, f)
                    for rot,_,ff in os.walk(f_path):
                        for file in ff:
                            if file == 'logic_form.json':
                                file_path = os.path.join(rot, file)
                                with open(file_path, 'r', encoding='utf-8') as json_file:
                                    data = json.load(json_file)
                                    text = []
                                    for text_logic_form in data["dissolved_text_logic_form"]:
                                        if text_logic_form != "":
                                            text_logic_form = convert_latex_to_plain_text(text_logic_form,delete_first_list)
                                            text.append(text_logic_form)
                                    for diagram_logic_form in data["diagram_logic_form"]:
                                        if diagram_logic_form != "":
                                            diagram_logic_form = convert_latex_to_plain_text(diagram_logic_form,delete_first_list)
                                            text.append(diagram_logic_form)
                                    # 检查CSV文件是否已存在
                                    csv_exists = False
                                    try:
                                        with open(csv_file_path, "r", newline="") as csv_file:
                                            csv_exists = True
                                    except FileNotFoundError:
                                        csv_exists = False

                                    # 将文本列表转为一个包含整个列表的字符串
                                    text_list_str = '["' + '", "'.join(text) + '"]'

                                    # 打开CSV文件并写入数据
                                    with open(csv_file_path, "a", newline="") as csv_file:
                                        csv_writer = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL)

                                        # 如果CSV文件不存在，写入表头
                                        if not csv_exists:
                                            csv_writer.writerow(["ID", "TextList"])

                                        # 将ID和文本列表字符串写入CSV文件的新行
                                        csv_writer.writerow([f, text_list_str])

    return root_dir

#GroQA
def read_geo_logic_form_file(json_file_path, csv_file_path):
    # 打开JSON文件并读取数据
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

        # 提取'id'和'text_logic_forms'字段的数据
        id_list = list(data.keys())
        print(data.keys())
        text_logic_forms = []
        Segmened_texts = []
        for id in id_list:
            text = data[id]['text_logic_forms']
            text_logic_forms.append(text)
            # 数据2：在数据1的基础上去掉括号和逗号
            seg_text = ""
            for item in text:
                seg_text= "{}{}".format(seg_text, item.replace('(', ' ').replace(')', ' ').replace(',', ''))
            Segmened_texts.append(seg_text)
        print(Segmened_texts[0])
        # 检查CSV文件是否已存在
        csv_exists = False
        try:
            with open(csv_file_path, "r", newline="") as csv_file:
                csv_exists = True
        except FileNotFoundError:
            csv_exists = False

        # # 将文本列表转为一个包含整个列表的字符串
        # text_list_str = '["' + '", "'.join(text_logic_forms) + '"]'
        with open(csv_file_path, "a", newline="", encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL)
            # 如果CSV文件不存在，写入表头
            if not csv_exists:
                csv_writer.writerow(["ID", "TextList",'Segmened_text'])

        for item in range(len(id_list)):
            # 打开CSV文件并写入数据
            with open(csv_file_path, "a", newline="", encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL)
                # 将ID和文本列表字符串写入CSV文件的新行
                csv_writer.writerow([id_list[item], text_logic_forms[item],Segmened_texts[item]])

    return json_file_path


# read_logic_form_files(root_directory,csv_file_path)

#Geo
# read_geo_logic_form_file(root_directory,csv_file_path)

####################################################################################################
#diff

# df1 = pd.read_csv('str_exp.csv', encoding='latin1')
# list1 = df1.iloc[:, 0].tolist()
# str_exp =df1.iloc[:, 1].tolist()
# vars = df1.iloc[:, 2].tolist()
# df2 = pd.read_csv('Geo_Logic_form_language1.csv', encoding='latin1')
# list2 = df2.iloc[:, 0].tolist()
# TextList = df2.iloc[:, 1].tolist()
# Segmened_text =df2.iloc[:, 2].tolist()
# def difference(list1, list2):
#     return [item for item in list1 if item not in list2]
# dif_list = difference(list1, list2)

#
# with open('Geo_Logic_form_language.csv', 'a', newline='', encoding='latin1') as csvfile:
#     writer = csv.writer(csvfile)
#     for i in range(len(list1)):
#         if list1[i] in dif_list:
#             continue
#         else:
#             j = 0
#             while j <len(list2):
#                 if list1[i] == list2[j]:
#                     break
#                 j += 1
#             if j < len(list2):
#                 writer.writerow([list2[j],TextList[j],Segmened_text[j]])

#####################################################################################
# Delete Find logic

# df = pd.read_csv('str_exp_new.csv', encoding='latin1')
# def count_digits(s):
#     # '180','360','60','90','30'
#     s = re.sub(r'\b(180|360|60|90|30|2|45)\b', '', s)
#     return len(set(re.findall(r'\d', s)))
#
#
# df['count_col2'] = df.iloc[:, 1].apply(count_digits)
# df['count_col3'] = df.iloc[:, 2].apply(count_digits)
#
# mask = df['count_col2'] > df['count_col3']
#
# df.loc[mask, df.columns[0]].to_csv('new_file.csv', index=False)
#
# df1 = pd.read_csv('new_file.csv', encoding='latin1')
# list = df1.iloc[:, 0].tolist()
# df = pd.read_csv('Geo_Logic_form_language.csv', encoding='latin1')
# no_find_rows = df[~df.iloc[:, 1].str.contains('Find')]
# target_values = no_find_rows.iloc[:, 0].values
#
# df = df[~df.iloc[:, 0].isin(target_values)]
# df = df[~df.iloc[:, 0].isin(list)]
# df.to_csv('Geo_Logic_form_language.csv', index=False)

