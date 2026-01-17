"""Ollama (ローカルLLM) 連携モジュール"""
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"  # 軽量で日本語もそこそこ対応


def check_ollama_running() -> bool:
    """Ollamaが起動しているか確認"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False


def generate_with_ollama(prompt: str) -> str:
    """Ollamaでテキスト生成"""
    if not check_ollama_running():
        raise ConnectionError("Ollamaが起動していません。Ollama.appを起動してください。")

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "num_predict": 2000,
            }
        },
        timeout=120
    )

    if response.status_code != 200:
        raise Exception(f"Ollama API エラー: {response.status_code}")

    return response.json().get("response", "")


def generate_summary(transcript: str, title: str) -> str:
    """文字起こしから要約を生成"""
    prompt = f"""以下はYouTube動画「{title}」の文字起こしです。
この内容を日本語で3〜5文で要約してください。
重要なポイントを押さえつつ、わかりやすく説明してください。

文字起こし:
{transcript[:4000]}

要約:"""

    return generate_with_ollama(prompt)


def generate_key_points(transcript: str, title: str) -> str:
    """重要ポイントを抽出"""
    prompt = f"""以下はYouTube動画「{title}」の文字起こしです。
この動画の重要ポイントを3〜5個、箇条書きで抽出してください。
各ポイントは簡潔に1〜2文でまとめてください。

文字起こし:
{transcript[:4000]}

重要ポイント:"""

    return generate_with_ollama(prompt)


def generate_quiz(transcript: str, title: str) -> str:
    """復習クイズを生成"""
    prompt = f"""以下はYouTube動画「{title}」の文字起こしです。
この内容に基づいて、復習用のクイズを3〜5問作成してください。

以下のフォーマットで出力してください:
Q1. [質問文]
A1. [回答]

Q2. [質問文]
A2. [回答]

質問は動画の重要な内容を確認できるものにしてください。

文字起こし:
{transcript[:4000]}

クイズ:"""

    return generate_with_ollama(prompt)
