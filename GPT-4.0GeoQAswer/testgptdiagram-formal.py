import base64
import requests
import os
from openai import APIError
import time
import csv
import pandas as pd

# OpenAI API Key
api_key = ""


prompt={}
excelfile=['./train.xlsx','./test.xlsx','./dev.xlsx']
for fpath in excelfile:
    df=pd.read_excel(fpath)
    for index,row in df.iterrows():
        prompt[row.iloc[10]]=row.iloc[8]
        # print(row.iloc[10],row.iloc[8])

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
# image_path = "0a7ff15d-0275-4bd6-a5e3-7e35ba4d3737.png"


def slover(text,image_path):
  while True:
    try:
      # Getting the base64 string
      base64_image = encode_image(image_path)

      headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
      }

      payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
          {
            "role": "system",
            "content": [
              {
                "type": "text",
                "text": f"这个题目只需要给出下面题的最终的一个数值结果，不需要给出分析过程"
              }

            ]
          },
          {
            "role": "user",
            "content": [
              {
                "type": "text",
                "text": text
              },
              {
                "type": "image_url",
                "image_url": {
                  "url": f"data:image/jpeg;base64,{base64_image}"
                }
              }
            ]
          }
        ],
        # "max_tokens": 300
      }

      response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

      return response.json()["choices"][0]['message']['content']
    except APIError as e:
      print("请求超时，正在尝试重新发送...")
      time.sleep(10)  # 等待一段时间后重试
      continue

try:
    with open('str_exp_new2.csv',encoding='utf-8') as file, open("gpt-4-vision-preview-diagram-formal.txt", 'a', encoding='utf-8') as f:
        reader=csv.reader(file)
        for row in reader:
            id=row[0]
            question=row[2]
            image_path=os.path.join('./image',id+'.png')
            # print(image_path)
            # prom = prompt[int(id)]
            answer=slover(question,image_path)
            print(f'习题{id},答案{answer}')
            # answers.append(answer)
            f.write(f"{id}: {answer}\n")

except FileNotFoundError:
    print("File not found!")
except Exception as e:
    print(f"An error occurred: {e}")
