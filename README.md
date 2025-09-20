# プロジェクト名
松尾研LLM2025コンペで、LLMモデルを学習させるためのデータセットを作成
本コンペではHLE(Humanity Last Exam)という超難問の解答精度の向上を競う。
HLEの問題のうち40%は数学の難問であり数学の解答精度向上が鍵である。
既存の数学データセットAIMEをベースに合成データ作成手法により問題の難化を図る。

## 特徴
AIME_Synthesis.py: 11分野各1問x11分野

AIME_Judge.py: 元の問題と新問題の整合性確認

AIME_ExtractQ.py: NewQからQuestionを抽出

AIME_ExtractSA.py: <Question>から解法と解答を得る

AIME_dataset.7z: 既存数学データセットAIME

## 動作環境
- OS / Python / CUDA / OpenAIなど

## インストール


