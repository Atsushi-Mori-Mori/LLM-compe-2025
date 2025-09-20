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
mf_lists = [
    './01a_Qp1/AIME_1983_2024_Qp01.csv',
    './01a_Qp1/AIME_1983_2024_Qp02.csv',
    './01a_Qp1/AIME_1983_2024_Qp03.csv',    
    './01a_Qp1/AIME_1983_2024_Qp04.csv',    
    './01a_Qp1/AIME_1983_2024_Qp05.csv',    
    './01a_Qp1/AIME_1983_2024_Qp06.csv',    
    './01a_Qp1/AIME_1983_2024_Qp07.csv',    
    './01a_Qp1/AIME_1983_2024_Qp08.csv',    
    './01a_Qp1/AIME_1983_2024_Qp09.csv',    
    './01a_Qp1/AIME_1983_2024_Qp10.csv',    
    './01a_Qp1/AIME_1983_2024_Qp11.csv'    
    ]
me_lists = [
    "- Analytic elements (limits, differentiability, optimization with derivatives, integral constraints, convexity/inequality arguments) \n",
    "- Probabilistic elements (probability, expected value, conditional probability, random variable scenarios, case analysis)\n",
    "- Geometric elements (coordinate geometry or transformations, similarity/congruence, power of a point, loci or area/length relations) \n",
    "- Set-theoretic elements (set-builder constraints, unions/intersections, mapping or injective/surjective conditions, invariants on subsets) \n",
    "- Sequence elements (recurrences, monotonicity and boundedness, partial sums or telescoping, convergence/divergence criteria) \n",
    "- Combinatorial elements (counting with cases, bijections, Pigeonhole Principle, inclusion–exclusion, invariants or extremal arguments) \n",
    "- Algebraic elements (systems of equations/inequalities, algebraic identities and factorizations, substitutions, AM–GM or Cauchy–Schwarz) \n",
    "- Complex-number elements (Argand-plane geometry, modulus/argument constraints, De Moivre’s formula, roots of unity, symmetry in conjugates) \n",
    "- Discrete-mathematics elements (graph degree/paths constraints, parity/recurrence on discrete states, invariants on moves, simple DP-style reasoning) \n",
    "- Number-theoretic elements (modular arithmetic, gcd/lcm relations, divisibility and Diophantine constraints, CRT-based case analysis) \n",
    "- Trigonometric elements (angle-sum and product identities, transformations, periodicity/phase constraints, auxiliary-angle or substitution tricks) \n"
]
ca_lists = ["（解析）","（確率）","（幾何）","（集合）","（数列）","（組合せ）","（代数）","（複素数）","（離散数学）","（数論）","（三角関数）"]
# プロンプト処理
# for f in range(0,1,1):
for f in range(len(mf_lists)):
    # for j in range(0,2,1):
    for j in range(len(me_lists)):
        math_df = pd.read_csv(mf_lists[f])
        max_retry = 2
        mc_list = []
        for k in range(len(math_df)):
            problem_text = math_df['Question'][k]
            answer_text = str(math_df['Answer'][k])
            math_elements = me_lists[j]
            summary_prompt = (
                "The following [problems] and [answers] are math problems and answers included in AIME.\n"
                "Your task is to produce a **new, more complex problem** that satisfies all of the following requirements:\n"
                "[Core Objective]\n"
                "1. **The final answer MUST remain exactly the same** as the original problem. Do NOT change it under any circumstances.\n"
                "2. Increase the number of reasoning steps significantly compared to the original problem.\n"
                "3. Introduce additional complexity by adding conditions such as:\n"
                f"{math_elements}\n"
                "- Extra intermediate variables or parameters\n"
                "- Multi-stage transformations, substitutions, or constraints\n"
                "- Additional layers of calculation or logical reasoning\n"
                "4. Any new conditions you add must be **essential** for solving the problem — not decorative.\n"
                "The solver must use them to reach the final answer.\n"
                "5. The problem should remain mathematically coherent and natural, without obvious artificial padding.\n"
                "6. Your output must be written in English only.\n"
                "[Prohibited Actions]\n"
                "- Do NOT alter the final numerical or algebraic answer.\n"
                "- Do NOT remove any original essential condition.\n"
                "- Do NOT introduce irrelevant story details that are unrelated to the mathematics.\n"
                "- Do NOT include the Final Answer in the **Step-by-Step Solution** in order to use it as <think> tags.\n"
                "- In the Step-by-Step Solution, do NOT explicitly state the final numeric or algebraic result.\n"
                "- End the Step-by-Step Solution with a sentence such as: \"The final computation result is omitted here.\" instead of the actual answer.\n"
                "[Output Format]\n"
                "1. **New Problem Statement** – rewritten and made more complex, incorporating the additional elements.\n"
                "2. **Description of Modifications** – explain exactly what was added or changed to increase difficulty.\n"
                "3. **Step-by-Step Solution** – a clean, well-structured list of logical steps without unnecessary headings, suitable for inclusion inside <think> tags, and ending with the placeholder sentence described above.\n"
                "4. **Final Answer** – exactly the same as the original final answer.\n"
                f"[problem]\n{problem_text}\n[answer]\n{answer_text}"
            )
            response_text = ""
            for attempt in range(max_retry):
                summary_response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are an expert creator of advanced mathematics problems."},
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
        math_df['NewQ'] = mc_list
        math_df['NewC'] = ca_lists[f]+"x"+ca_lists[j]
        if f == 0 and j == 0:
            mathall_df = math_df.copy()
        else:
            mathall_df = pd.concat([mathall_df, math_df],axis=0).reset_index(drop=True)
# # -------------------------------------------------------
# 出力
output_file = './AIME_1983_2024_question.csv'
mathall_df.to_csv(output_file, index=False, encoding='utf-8-sig')
print(f"保存完了: {output_file}")
# # -------------------------------------------------------
# # -------------------------------------------------------
# # -------------------------------------------------------

