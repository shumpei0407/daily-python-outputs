"""YouTube学びノートメーカー - Streamlit UI"""
import streamlit as st
from services.note_generator import generate_learning_note, save_note

st.set_page_config(
    page_title="YouTube学びノートメーカー",
    page_icon="📚",
    layout="wide"
)

st.title("📚 YouTube学びノートメーカー")
st.markdown("""
YouTubeの動画URLを入力すると、自動で学習ノートを作成します。
- 📝 動画内容の要約
- 💡 重要ポイントの抽出
- ❓ 復習クイズの生成
""")

st.divider()

# URL入力
url = st.text_input(
    "YouTube URL を入力",
    placeholder="https://www.youtube.com/watch?v=..."
)

col1, col2 = st.columns([1, 4])
with col1:
    generate_btn = st.button("📝 ノート生成", type="primary", use_container_width=True)

# 生成処理
if generate_btn and url:
    progress_container = st.empty()
    status_text = st.empty()

    def update_status(message: str):
        status_text.info(message)

    try:
        with st.spinner("処理中..."):
            markdown, title = generate_learning_note(url, progress_callback=update_status)

        status_text.success("✅ ノート生成完了！")

        # タブで表示
        tab1, tab2 = st.tabs(["📖 プレビュー", "📄 Markdownコード"])

        with tab1:
            st.markdown(markdown)

        with tab2:
            st.code(markdown, language="markdown")

        # ダウンロードボタン
        st.divider()
        col1, col2, col3 = st.columns([1, 1, 2])

        with col1:
            st.download_button(
                label="⬇️ Markdownをダウンロード",
                data=markdown,
                file_name=f"learning_note_{title[:30]}.md",
                mime="text/markdown"
            )

        with col2:
            if st.button("💾 ファイルに保存"):
                filepath = save_note(markdown, title)
                st.success(f"保存しました: {filepath}")

    except ValueError as e:
        st.error(f"⚠️ 入力エラー: {str(e)}")
    except Exception as e:
        st.error(f"❌ エラーが発生しました: {str(e)}")
        st.info("💡 ヒント: 字幕がない動画は対応していません。字幕付きの動画をお試しください。")

elif generate_btn and not url:
    st.warning("URLを入力してください")

# サイドバー
with st.sidebar:
    st.header("📋 使い方")
    st.markdown("""
    1. YouTube動画のURLをコピー
    2. 上の入力欄に貼り付け
    3. 「ノート生成」ボタンをクリック
    4. 生成されたノートをダウンロード

    **対応形式:**
    - youtube.com/watch?v=...
    - youtu.be/...
    - youtube.com/shorts/...
    """)

    st.divider()
    st.header("⚙️ 設定")
    st.info("Gemini APIキーは`.env`ファイルで設定してください")

    st.divider()
    st.markdown("""
    **💡 Tips:**
    - 字幕付きの動画が必要です
    - 長い動画は処理に時間がかかります
    - 生成されたノートはNotion/Obsidianにそのままコピペできます
    """)
