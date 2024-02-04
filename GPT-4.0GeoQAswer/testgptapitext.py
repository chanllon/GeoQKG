# API_key= "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"
import csv
import os
import time
from openai import OpenAI,APIError
import pandas as pd

# from openai.error import APITimeoutError
# !pip install tiktoken
# import tiktoken

# MODEL_NAME = "gpt-3.5-turbo-16k-0613"
# encoder = tiktoken.encoding_for_model(MODEL_NAME)
#
# def calculate_and_display_token_count(input_text: str):
#     encoded_text = encoder.encode(input_text)
#     token_count = len(encoded_text)
#
#     print(f"输入的文本: '{input_text}'")
#     print(f"对应的编码: {encoded_text}")
#     print(f"Token数量: {token_count}")
#
#
# calculate_and_display_token_count(input_text='测试Token大小')

os.environ["OPENAI_API_KEY"] = ""


prompt={}
excelfile=['./train.xlsx','./test.xlsx','./dev.xlsx']
for fpath in excelfile:
    df=pd.read_excel(fpath)
    for index,row in df.iterrows():
        prompt[row.iloc[10]]=row.iloc[8]
        # print(row.iloc[10],row.iloc[8])

# print(prompt[0])

def slover(content):
    while True:
        try:
            client = OpenAI()

            completion = client.chat.completions.create(
                model="gpt-4-0314",
                messages=[
                    {"role": "system", "content": f"Please provide a only the final numerical result."},
                    {"role": "user", "content": content }
                ],
                # max_tokens=10  # 设置最大令牌数量
            )
            return completion.choices[0].message.content
        except APIError as e:
            print("请求超时，正在尝试重新发送...")
            time.sleep(10)  # 等待一段时间后重试
            continue

try:
    with open('../GPT4.0/geo_en_text.csv',encoding='utf-8') as file, open("gpt-4-0314-noprompt.txt", 'a', encoding='utf-8') as f:
        reader=csv.reader(file)
        for row in reader:
            id=row[0]
            question=row[1]
            # print(id)
            # prom=prompt[int(id)]
            # print(prom)
            answer=slover(question)
            print(f'习题{id},答案{answer}')
            # answers.append(answer)
            f.write(f"{id}: {answer}\n")

except FileNotFoundError:
    print("File not found!")
except Exception as e:
    print(f"An error occurred: {e}")




