"""文字起こしモジュール（YouTube字幕API + faster-whisperフォールバック）"""
import os
from dataclasses import dataclass
from typing import Callable, Optional

from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp


@dataclass
class TranscriptionResult:
    """文字起こし結果"""
    text: str
    method: str  # "youtube_api" or "whisper"
    language: str


class Transcriber:
    def __init__(self, temp_dir: str = "temp", whisper_model: str = "base"):
        """
        Args:
            temp_dir: 一時ファイル保存ディレクトリ
            whisper_model: Whisperモデルサイズ（tiny, base, small, medium, large）
                - tiny: 最速、精度低め
                - base: バランス良い（推奨）
                - small: 精度高め
                - medium/large: 高精度だがメモリ消費大
        """
        self.temp_dir = temp_dir
        self.whisper_model = whisper_model
        self._whisper = None  # 遅延ロード
        os.makedirs(temp_dir, exist_ok=True)

    def _get_whisper_model(self):
        """Whisperモデルを遅延ロード"""
        if self._whisper is None:
            from faster_whisper import WhisperModel
            # CPU使用（GPU利用時は device="cuda" に変更）
            self._whisper = WhisperModel(
                self.whisper_model,
                device="cpu",
                compute_type="int8"
            )
        return self._whisper

    def get_transcript(
        self,
        video_id: str,
        progress_callback: Optional[Callable[[str], None]] = None
    ) -> TranscriptionResult:
        """
        文字起こしを取得（自動フォールバック付き）
        1. YouTube字幕APIを試行
        2. 失敗時はWhisperにフォールバック
        """
        if progress_callback:
            progress_callback("YouTube字幕を確認中...")

        # まずYouTube字幕APIを試行
        try:
            result = self._get_from_youtube_api(video_id)
            if progress_callback:
                progress_callback(f"YouTube字幕を取得しました（{result.language}）")
            return result
        except Exception as e:
            if progress_callback:
                progress_callback(f"字幕が見つかりません。Whisperで音声認識を開始します...")

        # Whisperにフォールバック
        return self._get_from_whisper(video_id, progress_callback)

    def _get_from_youtube_api(self, video_id: str) -> TranscriptionResult:
        """YouTube字幕APIから文字起こしを取得"""
        api = YouTubeTranscriptApi()

        # 利用可能な字幕をリスト
        transcript_list = api.list(video_id)

        # 日本語 → 英語の優先順位
        preferred_languages = ['ja', 'en']

        # 手動字幕を優先
        for lang in preferred_languages:
            for t in transcript_list:
                if t.language_code == lang and not t.is_generated:
                    data = t.fetch()
                    text = " ".join([item.text for item in data])
                    return TranscriptionResult(
                        text=text,
                        method="youtube_api",
                        language=t.language_code
                    )

        # 自動生成字幕
        for lang in preferred_languages:
            for t in transcript_list:
                if t.language_code == lang and t.is_generated:
                    data = t.fetch()
                    text = " ".join([item.text for item in data])
                    return TranscriptionResult(
                        text=text,
                        method="youtube_api",
                        language=f"{t.language_code}(自動生成)"
                    )

        # どれでもいいから最初の字幕を取得
        for t in transcript_list:
            data = t.fetch()
            text = " ".join([item.text for item in data])
            lang_info = f"{t.language_code}(自動生成)" if t.is_generated else t.language_code
            return TranscriptionResult(
                text=text,
                method="youtube_api",
                language=lang_info
            )

        raise Exception("字幕が見つかりませんでした")

    def _get_from_whisper(
        self,
        video_id: str,
        progress_callback: Optional[Callable[[str], None]] = None
    ) -> TranscriptionResult:
        """faster-whisperで音声認識（ローカル実行・無料）"""
        audio_path = None

        try:
            # 音声をダウンロード
            if progress_callback:
                progress_callback("音声をダウンロード中...")

            audio_path = self._download_audio(video_id)

            if progress_callback:
                progress_callback("Whisperモデルを読み込み中...")

            model = self._get_whisper_model()

            if progress_callback:
                progress_callback("Whisperで文字起こし中（ローカル処理）...")

            # faster-whisperで文字起こし
            segments, info = model.transcribe(
                audio_path,
                beam_size=5,
                language=None,  # 自動検出
                vad_filter=True  # 無音部分をスキップして高速化
            )

            # セグメントを結合
            text_parts = []
            for segment in segments:
                text_parts.append(segment.text)

            full_text = " ".join(text_parts)

            return TranscriptionResult(
                text=full_text,
                method="whisper(local)",
                language=info.language if info.language else "auto"
            )

        finally:
            # 一時ファイルを削除
            if audio_path and os.path.exists(audio_path):
                os.remove(audio_path)

    def _download_audio(self, video_id: str) -> str:
        """yt-dlpで音声をダウンロード"""
        url = f"https://www.youtube.com/watch?v={video_id}"

        # 一時ファイルパスを生成
        output_path = os.path.join(self.temp_dir, f"{video_id}.%(ext)s")

        ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio/best',
            'outtmpl': output_path,
            'quiet': True,
            'no_warnings': True,
            'extract_audio': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            # 実際のファイルパスを取得
            if info.get('requested_downloads'):
                return info['requested_downloads'][0]['filepath']
            # フォールバック: 拡張子を推測
            for ext in ['m4a', 'webm', 'mp3', 'mp4']:
                path = os.path.join(self.temp_dir, f"{video_id}.{ext}")
                if os.path.exists(path):
                    return path

        raise Exception("音声のダウンロードに失敗しました")
