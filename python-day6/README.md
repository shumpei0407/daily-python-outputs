# 📝 Growth Journal - 成長を可視化する日報システム

日報を書くだけで、AIが自動的に成長を分析してNotionに記録するシステムです。

## ✨ 特徴

- 🌐 **Webフォームで簡単入力**：ブラウザから日報を書くだけ
- 🤖 **AI自動サマリー生成**：ローカルLLM（Ollama）で要約
- 📊 **Notion連携**：データベースに自動保存
- 🎯 **5日報ごとのリフレクション**：成長ポイント・学び・次の課題を自動抽出
- 📈 **成長指標の可視化**：スキル・経験を自動分類

## 🚀 セットアップ

### 1. 必要なもの

- Python 3.8以上
- Ollama（ローカルLLM）
- Notion APIキー

### 2. インストール

```bash
# パッケージインストール
pip install -r requirements.txt

# Ollamaのインストール（macOS）
brew install ollama

# Ollamaモデルのダウンロード
ollama pull llama2
```

### 3. 設定

`config.yaml`を作成して以下を設定：

```yaml
notion:
  api_key: "your_notion_api_key"
  database_id: "your_database_id"

ollama:
  model: "llama2"
  base_url: "http://localhost:11434"

reflection:
  trigger_count: 5  # 5日報ごとにリフレクション生成
```

### 4. 起動

```bash
# Ollamaを起動
ollama serve

# アプリケーション起動
python app.py
```

ブラウザで `http://localhost:5000` を開く

## 📁 プロジェクト構造

```
python-day6/
├── app.py                 # Flaskアプリケーション
├── requirements.txt       # 依存パッケージ
├── config.yaml           # 設定ファイル
├── models/
│   └── journal.py        # 日報データモデル
├── services/
│   ├── notion_client.py  # Notion API連携
│   ├── ollama_client.py  # Ollama連携
│   ├── analyzer.py       # 成長指標分析
│   └── reflection.py     # リフレクション生成
├── templates/
│   ├── index.html        # 日報入力フォーム
│   └── reflection.html   # リフレクション表示
└── static/
    └── style.css         # スタイル

```

## 🎯 使い方

1. **日報を書く**：Webフォームに今日の活動を入力
2. **自動処理**：AIがサマリーを生成してNotionに保存
3. **5日後**：自動的にリフレクションが生成され、成長を振り返り

## 💡 リフレクション内容

- 📚 学んだこと・できるようになったこと
- 🎯 乗り越えた課題
- 📈 スキル成長グラフ
- 💭 次に意識すべきポイント

## 🔧 開発予定

- [ ] スキルツリー可視化
- [ ] 月次レポート自動生成
- [ ] Slack/Discord通知機能
