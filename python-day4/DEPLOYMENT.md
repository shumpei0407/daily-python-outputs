# 🚀 Web公開手順（Streamlit Cloud）

このアプリを無料でWeb公開する方法を説明します。

## 準備

### 1. GitHubアカウント作成
- [GitHub](https://github.com/)でアカウントを作成（無料）

### 2. OpenWeatherMap APIキーを取得
1. [OpenWeatherMap](https://openweathermap.org/api)にアクセス
2. "Sign Up"から無料アカウント作成
3. ログイン後、"API keys"タブからAPIキーをコピー

## デプロイ手順

### ステップ1: GitHubリポジトリ作成

1. GitHubにログイン
2. 右上の「+」→「New repository」をクリック
3. リポジトリ名を入力（例: `surf-advisor`）
4. 「Public」を選択（無料プラン）
5. 「Create repository」をクリック

### ステップ2: コードをGitHubにプッシュ

ターミナルで以下を実行:

```bash
cd /Users/taguchi/python/python-day4

# Gitリポジトリを初期化
git init

# ファイルを追加
git add .

# コミット
git commit -m "Initial commit: Surf Advisor App"

# GitHubリポジトリと連携（YOUR_USERNAMEを自分のユーザー名に変更）
git remote add origin https://github.com/YOUR_USERNAME/surf-advisor.git

# プッシュ
git branch -M main
git push -u origin main
```

### ステップ3: Streamlit Cloudでデプロイ

1. [Streamlit Cloud](https://streamlit.io/cloud)にアクセス
2. 「Sign up」→「Continue with GitHub」でGitHubアカウントでログイン
3. 「New app」をクリック
4. 設定を入力:
   - **Repository**: `YOUR_USERNAME/surf-advisor`
   - **Branch**: `main`
   - **Main file path**: `surf_advisor.py`
5. 「Advanced settings」をクリック
6. 「Secrets」セクションに以下を貼り付け:
   ```toml
   OPENWEATHER_API_KEY = "あなたのAPIキー"
   ```
7. 「Deploy!」をクリック

### ステップ4: 完成！

数分待つと、以下のようなURLでアプリが公開されます:
```
https://YOUR_USERNAME-surf-advisor-surf-advisor-xxxxxx.streamlit.app
```

このURLを友達にシェアすれば、誰でもアクセスできます！

## アプリの更新方法

コードを修正したら:

```bash
git add .
git commit -m "Update: 修正内容"
git push
```

自動的にStreamlit Cloudに反映されます。

## トラブルシューティング

### エラー: "No module named 'ephem'"
→ `requirements.txt`が正しくコミットされているか確認

### エラー: "API Key not found"
→ Streamlit Cloudの「Settings」→「Secrets」でAPIキーを確認

### アプリが表示されない
→ Streamlit Cloudのログを確認（右下の「Manage app」→「Logs」）

## 無料プランの制限

- **Streamlit Cloud無料プラン**:
  - 1ユーザーあたり1アプリまで公開可能
  - リソース: 1GB RAM
  - パブリックリポジトリのみ

制限を超える場合は有料プラン（$20/月〜）が必要です。

## 代替デプロイ方法

### Heroku（無料プランは廃止）
現在は有料プランのみ

### Render（無料プラン有り）
1. [Render](https://render.com/)でアカウント作成
2. 「New Web Service」を選択
3. GitHubリポジトリを選択
4. 設定:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run surf_advisor.py --server.port=$PORT --server.address=0.0.0.0`
5. 環境変数に`OPENWEATHER_API_KEY`を設定

### Railway（無料クレジット$5/月）
1. [Railway](https://railway.app/)でアカウント作成
2. 「New Project」→「Deploy from GitHub repo」
3. リポジトリを選択
4. 環境変数を設定

## カスタムドメイン設定（オプション）

Streamlit Cloud Pro（有料）でカスタムドメインが使えます:
- 例: `https://surfadvisor.com`

## セキュリティ注意事項

⚠️ **絶対にAPIキーをコードに直接書かないでください**

- `.env`ファイルは`.gitignore`で除外
- Streamlit Cloudの「Secrets」機能を使用
- GitHubに誤ってプッシュした場合は、APIキーを再発行

## サポート

問題が発生した場合:
1. [Streamlit Community Forum](https://discuss.streamlit.io/)
2. [Streamlit Documentation](https://docs.streamlit.io/)
