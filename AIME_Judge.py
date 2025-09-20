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
input_file = 'AIME_1983_2024_question_h.csv'
math_df = pd.read_csv(input_file)
# math_df = pd.read_csv(input_file, encoding='cp932')
fname = input_file[:-15]
fnumb = input_file[-5:-4]

# プロンプト処理
max_retry = 3
judge_full_list = []  # JudgeQ列用（判定全文）
judge_result_list = []  # Jresult列用（PASS/FAILだけ）

for k in range(len(math_df)):
    problem_text = math_df['Question'][k]
    new_problem_text = math_df['NewQ'][k]
    answer_text = str(math_df['Answer'][k])

    summary_prompt = (
        "The following [problems] and [answers] are original math problems and answers included in AIME.\n"
        "The following [modified problems] is modified math problems based on the [problems].\n"
        "Your tasks:\n"
        "1. Identify all differences between Original and Modified.\n"
        "2. Verify if Modified Problem still logically leads to the same Final Answer.\n"
        "5. Your output must be written in Japanese.\n"
        "4. Output:\n"
        "[Differences]\n"
        "...\n"
        "[Feasibility Check]\n"
        "...\n"
        "[Judgment]\n"
        "PASS or FAIL\n"
        f"[problem]\n{problem_text}\n[modified problems]\n{new_problem_text}\n[answer]\n{answer_text}"
    )
    response_text = ""
    for attempt in range(max_retry):
        summary_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a brilliant mathematics problem verification expert."},
                {"role": "user", "content": summary_prompt}
            ],
            max_completion_tokens=800
        )
        content = summary_response.choices[0].message.content
        if content and content.strip():
            response_text = content.strip()
            break  # 成功したらループを抜ける

    if not response_text:
        response_text = "[回答なし]"

    # JudgeQ列（全文）
    judge_full_list.append(response_text)

    # Jresult列（PASS/FAIL抽出）
    m = re.search(r'\bPASS\b|\bFAIL\b', response_text, re.IGNORECASE)
    if m:
        judge_result_list.append(m.group(0).upper())
    else:
        judge_result_list.append("UNKNOWN")

# DataFrameに列追加
math_df['JudgeQ'] = judge_full_list
math_df['Jresult'] = judge_result_list

# 出力
output_file = fname + '_judge_' + fnumb + '.csv'
math_df.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"保存完了: {output_file}")
# # -------------------------------------------------------
# # -------------------------------------------------------
