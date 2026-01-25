"""YouTube URL解析・動画情報取得モジュール"""
import re
from typing import Optional
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


def get_video_info(video_id: str) -> dict:
    """
    動画情報を取得（oembed API使用）

    Returns:
        dict: {
            "title": str,
            "author_name": str,
            "thumbnail_url": str
        }
    """
    try:
        url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {
                "title": data.get("title", "タイトル取得失敗"),
                "author_name": data.get("author_name", "不明"),
                "thumbnail_url": data.get("thumbnail_url", "")
            }
    except Exception:
        pass
    return {
        "title": "タイトル取得失敗",
        "author_name": "不明",
        "thumbnail_url": ""
    }


def validate_youtube_url(url: str) -> tuple[bool, str]:
    """
    YouTube URLを検証

    Returns:
        tuple[bool, str]: (有効かどうか, エラーメッセージまたは動画ID)
    """
    if not url or not url.strip():
        return False, "URLを入力してください"

    video_id = extract_video_id(url)
    if not video_id:
        return False, "有効なYouTube URLを入力してください"

    return True, video_id
