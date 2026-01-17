"""YouTube文字起こし取得モジュール"""
import re
from typing import Optional, Tuple
from youtube_transcript_api import YouTubeTranscriptApi
import requests


def extract_video_id(url: str) -> Optional[str]:
    """YouTubeのURLから動画IDを抽出"""
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]{11})',
        r'(?:youtube\.com/shorts/)([a-zA-Z0-9_-]{11})',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def get_video_title(video_id: str) -> str:
    """動画タイトルを取得（oembed API使用）"""
    try:
        url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json().get("title", "タイトル取得失敗")
    except Exception:
        pass
    return "タイトル取得失敗"


def get_transcript(video_id: str) -> Tuple[str, str]:
    """
    動画の文字起こしを取得（youtube-transcript-api v1.x対応）

    Returns:
        Tuple[str, str]: (文字起こしテキスト, 使用した言語)
    """
    api = YouTubeTranscriptApi()

    try:
        # 利用可能な字幕をリスト
        transcript_list = api.list(video_id)

        # 日本語 → 英語の優先順位で探す
        preferred_languages = ['ja', 'en']

        # 手動字幕を優先
        for lang in preferred_languages:
            for t in transcript_list:
                if t.language_code == lang and not t.is_generated:
                    data = t.fetch()
                    text = " ".join([item.text for item in data])
                    return text, t.language_code

        # 自動生成字幕
        for lang in preferred_languages:
            for t in transcript_list:
                if t.language_code == lang and t.is_generated:
                    data = t.fetch()
                    text = " ".join([item.text for item in data])
                    return text, f"{t.language_code}(自動生成)"

        # どれでもいいから最初の字幕を取得
        for t in transcript_list:
            data = t.fetch()
            text = " ".join([item.text for item in data])
            lang_info = f"{t.language_code}(自動生成)" if t.is_generated else t.language_code
            return text, lang_info

        raise Exception("字幕が見つかりませんでした。")

    except Exception as e:
        raise Exception(f"字幕の取得に失敗しました: {str(e)}")


def get_youtube_content(url: str) -> dict:
    """
    YouTubeのURLからコンテンツ情報を取得

    Returns:
        dict: {
            "video_id": str,
            "title": str,
            "transcript": str,
            "language": str,
            "url": str
        }
    """
    video_id = extract_video_id(url)
    if not video_id:
        raise ValueError("有効なYouTube URLを入力してください")

    title = get_video_title(video_id)
    transcript, language = get_transcript(video_id)

    return {
        "video_id": video_id,
        "title": title,
        "transcript": transcript,
        "language": language,
        "url": url
    }
