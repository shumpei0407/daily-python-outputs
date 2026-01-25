# YouTube 文字起こし・要約サービス

YouTube URLを入力するだけで、文字起こしと要約を自動生成してダウンロードできるWebサービスです。

**完全無料** - すべてローカルで処理するため、APIキー不要です。

## 機能

- YouTube動画の文字起こし取得
  - YouTube字幕API（優先）
  - faster-whisper音声認識（字幕がない場合に自動フォールバック）
- AIによる要約生成（Ollama）
- 文字起こし・要約のダウンロード（.txt / .md形式）

## 必要な準備

### 1. Ollamaのインストール

```bash
# macOS
brew install ollama

# または公式サイトからダウンロード
# https://ollama.ai
```

### 2. LLMモデルのダウンロード

```bash
# Ollamaを起動
ollama serve

# モデルをダウンロード（いずれか1つ以上）
ollama pull llama3.2    # 推奨（2GB）
ollama pull gemma2      # 高品質（5GB）
```

### 3. Pythonライブラリのインストール

```bash
cd python-day10
pip3 install -r requirements.txt
```

### 4. FFmpegのインストール（Whisper使用時に必要）

```bash
# macOS
brew install ffmpeg

# Ubuntu
sudo apt-get install ffmpeg
```

## 起動方法

```bash
# Ollamaが起動していることを確認
ollama serve

# アプリを起動
python3 -m streamlit run app.py
```

ブラウザで http://localhost:8501 を開きます。

## 使い方

1. YouTube URLを入力欄に貼り付け
2. 「処理開始」ボタンをクリック
3. 文字起こしと要約が生成されます
4. ダウンロードボタンで保存

## サイドバー設定

- **要約モデル**: Ollamaで使用するLLMを選択
  - llama3.2（推奨）、gemma2、qwen2.5、mistral
- **Whisperモデル**: 字幕がない場合の音声認識精度
  - tiny: 最速
  - base: バランス（推奨）
  - small: 高精度
  - medium: 最高精度

## ファイル構成

```
python-day10/
├── app.py                 # Streamlit メインアプリ
├── requirements.txt       # 依存ライブラリ
├── README.md
├── .gitignore
├── services/
│   ├── __init__.py
│   ├── youtube.py         # URL解析・動画情報取得
│   ├── transcriber.py     # 文字起こし（字幕API + Whisper）
│   └── summarizer.py      # Ollama要約生成
└── temp/                  # 音声一時ファイル用
    └── .gitkeep
```

## 技術スタック

| 機能 | 技術 | 費用 |
|------|------|------|
| 文字起こし（優先） | youtube-transcript-api | 無料 |
| 文字起こし（フォールバック） | faster-whisper | 無料 |
| 要約生成 | Ollama (llama3.2等) | 無料 |
| 音声ダウンロード | yt-dlp | 無料 |
| UI | Streamlit | 無料 |

## トラブルシューティング

### Ollamaに接続できない
```bash
# Ollamaが起動しているか確認
ollama list

# 起動していない場合
ollama serve
```

### Whisperが遅い
- サイドバーでWhisperモデルを「tiny」に変更
- または「base」を使用（バランス型）

### 字幕が取得できない
- 一部の動画は字幕が無効化されています
- その場合、自動的にWhisperで音声認識を行います
