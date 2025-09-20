#　-*- coding: utf-8 -*-
import sys
import os
import re
import struct
import binascii
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# -------------------------------------------------------
import cv2
import json
from PIL import Image  # Pillowライブラリをインポート
from openai import OpenAI
import openai
# # -------------------------------------------------------

# # APIキー
client = openai.OpenAI(api_key="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
# CSV読み込み
math_df = pd.read_csv('./AIME_1983_2024_judge_11x11_pass_b.csv', encoding='cp932')

# プロンプト処理
max_retry = 2
mc_list = []

for k in range(len(math_df)):
    # problem_text = math_df['NewQ'][k]
    problem_text = math_df['Question'][k]
    solution_text = math_df['NewS'][k]
    answer_text = str(math_df['Answer'][k])
    summary_prompt = (
        "以下の<problem>は、AIMEをベースに作成した数学の問題です。\n"
        "この数学の問題の解答を考え、その解法と解答を日本語で答えてください。\n"
        "解答は、Answer=(解答)で答えるようにしてください。\n"
        "※日本語で回答してください。\n"
        f"<problem>\n{problem_text}"
    )

    response_text = ""
    for attempt in range(max_retry):
        summary_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a brilliant mathematical expert."},
                {"role": "user", "content": summary_prompt}
            ],
            max_completion_tokens=2000
        )
        content = summary_response.choices[0].message.content
        if content and content.strip():
            response_text = content.strip()
            break  # 成功したらループを抜ける

    if not response_text:
        response_text = "[回答なし]"  # 明示的に空を記録

    mc_list.append(response_text)

# DataFrameに追加
math_df['LLM_answer'] = mc_list

# 出力
output_file = './AIME_1983_2024_judge_11x11_pass_b_answered.csv'
math_df.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"保存完了: {output_file}")
# # -------------------------------------------------------
# # -------------------------------------------------------

