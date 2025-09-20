#　-*- coding: utf-8 -*-
import sys
import os
import re
import struct
import binascii
import numpy as np
# -------------------------------------------------------
import pandas as pd
import matplotlib.pyplot as plt
import re
# # -------------------------------------------------------
INPUT_CSV  = "./AIME_1983_2024_judge_11x11_pass_c.csv"          # 既存CSV (Question, NewQ, Answer など)
OUTPUT_CSV = "./AIME_1983_2024_judge_11x11_pass_c_split.csv"    # 出力CSV (新列を追加)

def normalize_text(s: str) -> str:
    if not isinstance(s, str):
        return ""
    return s.replace("\r\n", "\n").replace("\r", "\n")

def keyword_to_flexible_pattern(keyword: str) -> str:
    """
    見出しキーワードを柔軟にマッチできる正規表現へ変換
    - スペースは \s* に
    - ハイフンは [-\s]* に（Step-by-Step/Step by Step の揺れを吸収）
    - 大文字小文字は後段の IGNORECASE で無視
    """
    # いったんエスケープ
    k = re.escape(keyword)
    # エスケープ済みの空白とハイフンを柔軟化
    k = k.replace(r"\ ", r"\s*").replace(r"\-", r"[-\s]*")
    return k

def compile_heading_regex(keyword: str) -> re.Pattern:
    """
    見出し行を検出するためのパターンを作る。
    例: "1. **New Problem Statement**:" / "New Problem Statement" / "New Problem Statement:" など
    """
    kp = keyword_to_flexible_pattern(keyword)
    pattern = rf"""
        ^                                   # 行頭
        \s*                                  # 前置空白
        (?:\d+\s*[\.\)]\s*)?                 # 先頭の「1.」「1)」など任意
        \**\s*                               # 先頭の ** の任意個
        .*?{kp}.*?                           # キーワードを含む（前後に他文字あってもOK）
        \**\s*                               # 末尾の ** の任意個
        :?\s*                                # 末尾のコロン任意
        $                                    # 行末
    """
    return re.compile(pattern, re.IGNORECASE | re.MULTILINE | re.VERBOSE)

def find_section_span(text: str, keyword: str) -> tuple[int, int] | None:
    """
    見出し行の span を返す。見つからなければ None。
    """
    regex = compile_heading_regex(keyword)
    m = regex.search(text)
    if not m:
        return None
    return m.span()

def extract_section(text: str, keyword: str, next_keywords: list[str]) -> str:
    """
    見出し keyword を含む行の直後から、次の見出し（next_keywords のいずれか）直前までを抽出。
    なければ末尾まで。
    """
    text = normalize_text(text)
    here = find_section_span(text, keyword)
    if not here:
        return ""

    _, end_heading = here  # 見出し行の末尾インデックス
    # 次見出しの開始位置候補を全部探す
    candidates = []
    for nk in next_keywords:
        r = compile_heading_regex(nk)
        m = r.search(text, pos=end_heading)
        if m:
            candidates.append(m.start())

    next_start = min(candidates) if candidates else len(text)
    body = text[end_heading:next_start].strip()
    return body

def split_newq(newq_text: str) -> dict:
    titles = {
        "new_problem": "New Problem Statement",         # 例: "1.New Problem Statement", "New Problem Statement:"
        "mods":        "Description of Modifications",
        "steps":       "Step-by-Step Solution",          # "Step by Step Solution" もマッチ
        "answer":      "Final Answer",
    }
    order = ["new_problem", "mods", "steps", "answer"]

    def next_for(key):
        idx = order.index(key)
        following = order[idx+1:]
        return [titles[k] for k in following]

    parsed = {
        "NewProblem":  extract_section(newq_text, titles["new_problem"], next_for("new_problem")),
        "Modifications": extract_section(newq_text, titles["mods"], next_for("mods")),
        "Steps":       extract_section(newq_text, titles["steps"], next_for("steps")),
        "FinalAnswer": extract_section(newq_text, titles["answer"], next_for("answer")),
    }
    parsed["FinalAnswer"] = parsed["FinalAnswer"].strip().strip("`* \n\r\t")
    return parsed

def main():
    df = pd.read_csv(INPUT_CSV, encoding='cp932')

    if "NewQ" not in df.columns:
        raise ValueError("'NewQ' 列が見つかりません。")

    new_problem_col = []
    mods_col = []
    steps_col = []
    final_col = []

    for txt in df["NewQ"].fillna(""):
        parts = split_newq(txt)
        new_problem_col.append(parts["NewProblem"])
        mods_col.append(parts["Modifications"])
        steps_col.append(parts["Steps"])
        final_col.append(parts["FinalAnswer"])

    df["NewProblemStatement"] = new_problem_col
    df["DescriptionOfModifications"] = mods_col
    df["StepByStepSolution"] = steps_col
    df["FinalAnswer_extracted"] = final_col

    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    print(f"Done. Wrote: {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
# # -------------------------------------------------------
# # -------------------------------------------------------

