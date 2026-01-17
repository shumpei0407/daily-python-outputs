"""学びノート生成モジュール"""
from datetime import datetime
from .youtube import get_youtube_content
from .llm import generate_summary, generate_key_points, generate_quiz


def format_quiz_as_markdown(quiz_text: str) -> str:
    """クイズをMarkdown形式（折りたたみ）に変換"""
    lines = quiz_text.strip().split('\n')
    result = []
    current_q = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith('Q') and '.' in line:
            if current_q:
                result.append("")
            current_q = line.split('.', 1)[1].strip() if '.' in line else line
            result.append(f"### {line.split('.')[0]}. {current_q}")
        elif line.startswith('A') and '.' in line:
            answer = line.split('.', 1)[1].strip() if '.' in line else line
            result.append(f"<details><summary>答えを見る</summary>\n\n{answer}\n\n</details>")

    return '\n'.join(result)


def generate_learning_note(url: str, progress_callback=None) -> tuple[str, str]:
    """
    YouTube URLから学びノートを生成

    Args:
        url: YouTube URL
        progress_callback: 進捗状況を通知するコールバック関数

    Returns:
        tuple[str, str]: (Markdownノート, 動画タイトル)
    """
    def update_progress(message: str):
        if progress_callback:
            progress_callback(message)

    # Step 1: YouTube情報取得
    update_progress("YouTube動画の情報を取得中...")
    content = get_youtube_content(url)

    title = content["title"]
    transcript = content["transcript"]
    language = content["language"]

    # Step 2: 要約生成
    update_progress("要約を生成中...")
    summary = generate_summary(transcript, title)

    # Step 3: 重要ポイント抽出
    update_progress("重要ポイントを抽出中...")
    key_points = generate_key_points(transcript, title)

    # Step 4: クイズ生成
    update_progress("復習クイズを生成中...")
    quiz = generate_quiz(transcript, title)
    quiz_formatted = format_quiz_as_markdown(quiz)

    # Step 5: Markdown組み立て
    update_progress("ノートを作成中...")
    today = datetime.now().strftime("%Y-%m-%d")

    markdown = f"""# 今日の学びノート

## 動画情報
- **タイトル**: {title}
- **URL**: {url}
- **字幕言語**: {language}
- **作成日**: {today}

---

## 要約

{summary}

---

## 重要ポイント

{key_points}

---

## 復習クイズ

{quiz_formatted}

---

*このノートはYouTube学びノートメーカーで自動生成されました*
"""

    return markdown, title


def save_note(markdown: str, title: str, output_dir: str = "output") -> str:
    """ノートをファイルに保存"""
    import os
    import re

    os.makedirs(output_dir, exist_ok=True)

    # ファイル名に使えない文字を除去
    safe_title = re.sub(r'[\\/*?:"<>|]', '', title)[:50]
    today = datetime.now().strftime("%Y%m%d")
    filename = f"{today}_{safe_title}.md"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(markdown)

    return filepath
