"""第1回: 素のLLMに1回だけ質問するスクリプト。

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask            # 質問を省略すると、講座に固有の質問をする

ツールも会話履歴も持たない「素の」呼び出し。
講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
（講座の実際とは違う）ことを確かめよう。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

import argparse
import time

from google import genai
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


def ask(conversation) -> str:
    client = genai.Client(api_key=get_api_key())

<<<<<<< HEAD
    # TODO(第1回 演習): response.usage_metadata から
    #   入力トークン数と出力トークン数を表示してみよう（Copilotに頼んでよい）
    usage = response.usage_metadata
    print(f"入力トークン数: {usage.prompt_token_count}")
    print(f"出力トークン数: {usage.candidates_token_count}")
=======
    # 応答時間の計測を開始
    start_time = time.perf_counter()

    # 会話履歴全体をモデルに渡す
    response = client.models.generate_content(
        model=MODEL,
        contents=conversation,
    )

    # 応答時間の計測を終了
    elapsed_time = time.perf_counter() - start_time

    print(f"[応答時間] {elapsed_time:.2f}秒")

    # 入力・出力トークン数を表示
    usage = response.usage_metadata

    if usage is not None:
        print(f"[入力トークン数] {usage.prompt_token_count}")
        print(f"[出力トークン数] {usage.candidates_token_count}")
        print(f"[合計トークン数] {usage.total_token_count}")
>>>>>>> 13f260f9495648160d3ec74359842724e37f9f7e

    return response.text


def main() -> None:
    parser = argparse.ArgumentParser(description="素のLLMに質問する")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    args = parser.parse_args()

    print(f"[model] {MODEL}")

    # 会話履歴を保存する
    conversation = []

    # 最初の質問
    question = args.question

    try:
        # 質問を繰り返し受け付ける
        while True:
            print(f"[質問] {question}\n")

            # ユーザーの質問を履歴に追加する
            conversation.append({
                "role": "user",
                "parts": [{"text": question}],
            })

            # 会話履歴全体をモデルに渡す
            answer = ask(conversation)
            print(answer)

            # モデルの回答を履歴に追加する
            conversation.append({
                "role": "model",
                "parts": [{"text": answer}],
            })

            # 次の質問を受け付ける
            question = input(
                "\n続けて質問してください（終了するには exit）: "
            )

            # 空のままEnterを押した場合は質問し直す
            if not question.strip():
                print("質問を入力してください。")
                continue

            # exitで終了する
            if question.lower() == "exit":
                break

    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()