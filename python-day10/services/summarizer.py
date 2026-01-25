"""要約生成モジュール（Ollamaローカル LLM連携）"""
import ollama


SUMMARY_PROMPT = """あなたは動画コンテンツの要約を行う専門家です。
以下はYouTube動画「{title}」の文字起こしです。
この内容を以下の形式で要約してください。

## 概要
（3-5文で動画の主題と結論を説明）

## 重要ポイント
（5つ以内の箇条書きで、最も重要な情報を抽出）

## 詳細メモ
（必要に応じて補足情報やキーワードをまとめる）

---

文字起こし:
{transcript}
"""


class Summarizer:
    def __init__(self, model: str = "gemma2"):
        """
        Args:
            model: Ollamaモデル名（gemma2, llama3.2, qwen2.5など）
        """
        self.model = model

    def generate_summary(self, transcript: str, title: str) -> str:
        """
        文字起こしから要約を生成

        Args:
            transcript: 文字起こしテキスト
            title: 動画タイトル

        Returns:
            str: Markdown形式の要約
        """
        # Ollamaのコンテキスト制限対策: 長すぎる場合は分割して処理
        max_chars = 12000  # 約3000トークン相当（ローカルLLM向け）
        if len(transcript) > max_chars:
            return self._summarize_long_text(transcript, title, max_chars)

        prompt = SUMMARY_PROMPT.format(
            title=title,
            transcript=transcript
        )

        response = ollama.generate(
            model=self.model,
            prompt=prompt
        )

        return response['response'].strip()

    def _summarize_long_text(self, transcript: str, title: str, max_chars: int) -> str:
        """長いテキストを分割して要約"""
        chunks = self._split_text(transcript, max_chars)
        chunk_summaries = []

        for i, chunk in enumerate(chunks):
            chunk_prompt = f"""以下はYouTube動画「{title}」の文字起こしの一部（パート{i+1}/{len(chunks)}）です。
このパートの内容を簡潔に要約してください。重要なポイントを箇条書きで3-5個挙げてください。

文字起こし:
{chunk}

要約:
"""
            response = ollama.generate(
                model=self.model,
                prompt=chunk_prompt
            )
            chunk_summaries.append(response['response'].strip())

        # 分割要約を統合
        combined = "\n\n---\n\n".join(chunk_summaries)
        final_prompt = f"""以下はYouTube動画「{title}」の分割要約です。
これらを統合して、以下の形式で最終的な要約を作成してください。

## 概要
（3-5文で動画の主題と結論を説明）

## 重要ポイント
（5つ以内の箇条書きで、最も重要な情報を抽出）

## 詳細メモ
（必要に応じて補足情報やキーワードをまとめる）

---

分割要約:
{combined}
"""

        response = ollama.generate(
            model=self.model,
            prompt=final_prompt
        )

        return response['response'].strip()

    def _split_text(self, text: str, max_chars: int) -> list[str]:
        """テキストを指定サイズで分割"""
        chunks = []
        current_chunk = ""

        # 文単位で分割（句点で区切る）
        sentences = text.replace("。", "。\n").replace(". ", ".\n").split("\n")

        for sentence in sentences:
            if len(current_chunk) + len(sentence) > max_chars:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                current_chunk += sentence

        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks if chunks else [text]
