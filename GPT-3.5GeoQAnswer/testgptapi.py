# API_key= "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"
import csv
import os
import time
from openai import OpenAI,APIError
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


def slover(content):
    while True:
        try:
            client = OpenAI()

            completion = client.chat.completions.create(
                model="gpt-3.5-turbo-16k-0613",
                messages=[
                    {"role": "system", "content": "下面每个题目只需要给出下面题的最终的一个数值结果，不需要给出分析过程"},
                    {"role": "user", "content": content }
                ]
                # max_tokens=50  # 设置最大令牌数量
            )
            return completion.choices[0].message.content
        except APIError as e:
            print("请求超时，正在尝试重新发送...")
            time.sleep(10)  # 等待一段时间后重试
            continue

try:
    with open('../GPT4.0/geo_en_text.csv',encoding='utf-8') as file, open("gpt-3.5-turbo-16k-0613result1.txt", 'a', encoding='utf-8') as f:
        reader=csv.reader(file)
        for row in reader:
            id=row[0]
            question=row[1]
            answer=slover(question)
            print(f'习题{id},答案{answer}')
            # answers.append(answer)
            f.write(f"{id}: {answer}\n")

except FileNotFoundError:
    print("File not found!")
except Exception as e:
    print(f"An error occurred: {e}")




