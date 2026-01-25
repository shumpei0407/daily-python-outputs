"""YouTube文字起こし・要約サービス（完全無料版）"""
from datetime import datetime

import streamlit as st

from services.youtube import get_video_info, validate_youtube_url
from services.transcriber import Transcriber
from services.summarizer import Summarizer

# ページ設定
st.set_page_config(
    page_title="YouTube文字起こし・要約",
    page_icon="📝",
    layout="wide"
)

# サイドバー
with st.sidebar:
    st.header("使い方")
    st.markdown("""
    1. YouTube URLを入力
    2. 「処理開始」をクリック
    3. 文字起こしと要約が生成されます
    4. ダウンロードボタンで保存

    ---

    **文字起こし方法**
    - YouTube字幕（優先）
    - Whisper音声認識（字幕がない場合）

    **要約**
    - Ollama（ローカルLLM）で生成

    ---

    **必要な準備**
    - Ollamaをインストール
    - `ollama pull gemma2` でモデル取得
    """)

    st.divider()

    # Ollamaモデル選択
    ollama_model = st.selectbox(
        "要約モデル",
        ["llama3.2", "gemma2", "qwen2.5", "mistral"],
        help="Ollamaで使用するモデルを選択"
    )

    # Whisperモデル選択
    whisper_model = st.selectbox(
        "Whisperモデル（字幕がない場合）",
        ["base", "small", "medium", "tiny"],
        help="tiny: 最速 / base: バランス / small: 高精度 / medium: 最高精度"
    )

# メインUI
st.title("📝 YouTube 文字起こし・要約サービス")
st.caption("完全無料 - Ollama + faster-whisper でローカル処理")

# URL入力
url = st.text_input(
    "YouTube URL",
    placeholder="https://www.youtube.com/watch?v=..."
)

# 処理開始ボタン
if st.button("処理開始", type="primary"):
    # URL検証
    is_valid, result = validate_youtube_url(url)
    if not is_valid:
        st.error(result)
    else:
        video_id = result

        # 動画情報取得
        with st.spinner("動画情報を取得中..."):
            video_info = get_video_info(video_id)

        # 動画情報表示
        col1, col2 = st.columns([1, 2])
        with col1:
            if video_info["thumbnail_url"]:
                st.image(video_info["thumbnail_url"], use_container_width=True)
        with col2:
            st.subheader(video_info["title"])
            st.caption(f"チャンネル: {video_info['author_name']}")

        # 処理実行
        transcriber = Transcriber(whisper_model=whisper_model)
        summarizer = Summarizer(model=ollama_model)

        # 進捗表示用
        status_container = st.empty()
        progress_bar = st.progress(0)

        def update_status(message: str):
            status_container.info(message)

        try:
            # 文字起こし
            progress_bar.progress(10)
            update_status("文字起こしを取得中...")

            transcript_result = transcriber.get_transcript(
                video_id,
                progress_callback=update_status
            )

            progress_bar.progress(50)
            update_status(f"文字起こし完了（{transcript_result.method}, {transcript_result.language}）")

            # 要約生成
            progress_bar.progress(60)
            update_status(f"要約を生成中（{ollama_model}）...")

            summary = summarizer.generate_summary(
                transcript_result.text,
                video_info["title"]
            )

            progress_bar.progress(100)
            status_container.success("処理完了！")

            # 結果表示
            st.divider()

            tab1, tab2 = st.tabs(["📄 文字起こし", "📋 要約"])

            with tab1:
                st.markdown(f"**取得方法**: {transcript_result.method} / **言語**: {transcript_result.language}")
                st.text_area(
                    "文字起こしテキスト",
                    transcript_result.text,
                    height=400
                )

                # ダウンロードボタン
                filename_base = video_info["title"][:50].replace("/", "_").replace("\\", "_")
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                st.download_button(
                    label="📥 文字起こしをダウンロード (.txt)",
                    data=transcript_result.text,
                    file_name=f"{filename_base}_transcript_{timestamp}.txt",
                    mime="text/plain"
                )

            with tab2:
                st.markdown(summary)

                # 要約ダウンロード
                summary_with_header = f"""# {video_info["title"]}

**URL**: {url}
**文字起こし方法**: {transcript_result.method}
**要約モデル**: {ollama_model}
**生成日時**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

{summary}
"""
                st.download_button(
                    label="📥 要約をダウンロード (.md)",
                    data=summary_with_header,
                    file_name=f"{filename_base}_summary_{timestamp}.md",
                    mime="text/markdown"
                )

        except Exception as e:
            progress_bar.empty()
            status_container.empty()
            st.error(f"エラーが発生しました: {str(e)}")
            st.exception(e)
