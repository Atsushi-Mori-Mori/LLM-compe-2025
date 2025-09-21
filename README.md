# プロジェクト名
松尾研LLM2025コンペで、LLMモデルを学習させるためのデータセットを作成
本コンペではHLE(Humanity Last Exam)という超難問の解答精度の向上を競う。
HLEの問題のうち40%は数学の難問であり数学の解答精度向上が鍵である。
既存の数学データセットAIMEをベースに合成データ作成手法により問題の難化を図る。

## プログラム及びデータ概要
AIME_Synthesis.py: 11分野各1問x11分野<br>
AIME_Judge.py: 元の問題と新問題の整合性確認<br>
AIME_ExtractQ.py: NewQからQuestionを抽出<br>
AIME_ExtractSA.py: <Question>から解法と解答を得る<br>
AIME_dataset.7z: 既存数学データセットAIME<br>

## 入力データセット
AIMEの1983年から2023年(+2024年Part2 まで)を網羅した約933問から選択
https://huggingface.co/datasets/di-zhang-fdu/AIME_1983_2024
圧縮ファイルAIME_dataset.7zに含まれるファイル<br>
----------------------------------------------<br>
AIME_1983_2024_Qp01.csv: 解析、10問<br>
AIME_1983_2024_Qp02.csv: 確率、10問<br>
AIME_1983_2024_Qp03.csv: 幾何、10問<br>
AIME_1983_2024_Qp04.csv: 集合、10問<br>
AIME_1983_2024_Qp05.csv: 数列、10問<br>
AIME_1983_2024_Qp06.csv: 組合せ、10問<br>
AIME_1983_2024_Qp07.csv: 代数、10問<br>
AIME_1983_2024_Qp08.csv: 複素数、10問<br>
AIME_1983_2024_Qp09.csv: 離散数学、9問<br>
AIME_1983_2024_Qp10.csv: 数論、10問<br>
AIME_1983_2024_Qp11.csv: 三角関数/その他(対数等)、9問<br>
----------------------------------------------<br>

## 動作環境
- OS / Python / CUDA / OpenAIなど

## インストール


