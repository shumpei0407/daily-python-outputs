# 🏄 サーフィン情報アドバイザー

日付と場所を入力すると、風・波・月齢などの情報から**サーフィンに最適な時間帯**を提案するWebアプリケーションです。

## 機能

- 📊 **波情報**: 波高、波周期、波向をリアルタイム取得
- 🌪️ **風情報**: 風速・風向（オフショア/オンショア判定）
- 🌙 **月齢情報**: 月の満ち欠け、大潮/小潮判定
- ⭐ **スコアリング**: 総合的なサーフィン適性スコア（0-100点）
- 🏆 **おすすめ時間**: 最適な時間帯を自動提案
- 🎯 **スキルレベル対応**: 初心者/中級者/上級者ごとに最適な波高を判定

## 使用しているAPI（すべて無料）

| API | 用途 | 料金 |
|-----|------|------|
| [OpenWeatherMap](https://openweathermap.org/api) | 風速・風向・天気 | 無料（要登録） |
| [Open-Meteo Marine](https://open-meteo.com/en/docs/marine-weather-api) | 波高・波周期・波向 | 完全無料（登録不要） |
| ephem（ライブラリ） | 月齢計算 | 無料 |

## セットアップ

### 1. リポジトリのクローン

```bash
cd python-day4
```

### 2. 依存パッケージのインストール

```bash
pip3 install -r requirements.txt
```

### 3. 環境変数の設定

`.env.example`をコピーして`.env`ファイルを作成します。

```bash
cp .env.example .env
```

`.env`ファイルを編集してOpenWeatherMap APIキーを設定します。

```
OPENWEATHER_API_KEY=あなたのAPIキー
```

#### OpenWeatherMap APIキーの取得方法

1. [OpenWeatherMap](https://openweathermap.org/api)にアクセス
2. "Sign Up"から無料アカウントを作成
3. ログイン後、"API keys"タブからAPIキーを取得
4. 取得したキーを`.env`ファイルに貼り付け

**⚠️ 重要**: APIキーは発行直後は無効です。**有効化まで2〜3時間**（最大24時間）かかります。
- 有効化されるまでは `401 Unauthorized` エラーが出ます
- その間は波データ（Open-Meteo）のみ取得できます
- 時間を置いてから再度試してください

### 4. アプリの起動

```bash
# 方法1: streamlitコマンドが使える場合
streamlit run surf_advisor.py

# 方法2: streamlitコマンドが見つからない場合
python3 -m streamlit run surf_advisor.py
```

ブラウザが自動的に開き、`http://localhost:8501`でアプリが表示されます。

#### ポート8501が既に使用中の場合

```bash
# 既存のプロセスを終了
lsof -ti:8501 | xargs kill -9

# アプリを再起動
python3 -m streamlit run surf_advisor.py
```

## 使い方

1. **サーフスポット**を選択（日本の主要8箇所から選択可能）
2. **スキルレベル**を選択（初心者/中級者/上級者）
3. **日付**を選択（本日から7日先まで）
4. **「分析開始」**ボタンをクリック

→ 最適な時間帯と詳細なスコア情報が表示されます。

## 対応サーフスポット

| スポット | 特徴 |
|----------|------|
| 湘南（鵠沼） | 首都圏から近い、初心者向け |
| 千葉（九十九里） | 東向きビーチ、安定した波 |
| 千葉（一宮） | サーフィンの聖地 |
| 静岡（御前崎） | 強い風、上級者向け |
| 宮崎（木崎浜） | 温暖、年間通して可能 |
| 高知（生見） | 台風スウェル |
| 新潟（角田浜） | 日本海側、冬がベスト |
| 徳島（小松海岸） | 四国屈指のポイント |

## スコアリングロジック

### 総合スコア = 50（基本点）+ 以下の加算/減算

| 要素 | 配点 | 詳細 |
|------|------|------|
| **波の高さ** | ±20点 | スキルレベルに応じた最適範囲で評価 |
| **波の周期** | ±20点 | 8-12秒が理想的 |
| **風向** | ±15点 | オフショアで最高評価 |
| **風速** | ±10点 | 0-3m/sが理想的 |
| **天気** | ±10点 | 晴れ・曇りで加点 |
| **月齢** | +5点 | 大潮期間にボーナス |

### スキルレベル別 最適波高

- **初心者**: 0.5m - 1.0m（腰〜胸）
- **中級者**: 1.0m - 2.0m（胸〜頭）
- **上級者**: 2.0m - 3.5m（頭オーバー）

### スコアの見方

- **75点以上**: 🏆 最高のコンディション！
- **60-74点**: ✅ 良好、おすすめ
- **45-59点**: ⚠️ 可能だが条件はやや厳しい
- **44点以下**: ❌ おすすめしない

## ファイル構成

```
python-day4/
├── surf_advisor.py      # メインアプリケーション
├── requirements.txt     # 依存パッケージ一覧
├── .env.example        # 環境変数のテンプレート
└── README.md           # このファイル
```

## 技術スタック

- **Python 3.9+**
- **Streamlit**: Webインターフェース
- **Requests**: HTTP通信
- **Pandas**: データ処理
- **ephem**: 天文計算（月齢）
- **python-dotenv**: 環境変数管理

## トラブルシューティング

### `401 Unauthorized` エラーが出る場合

OpenWeatherMap APIキーがまだ有効化されていません。
- APIキー発行後、**2〜3時間待つ**（最大24時間）
- [OpenWeatherMapダッシュボード](https://home.openweathermap.org/api_keys)でキーの状態を確認
- 波データ（Open-Meteo）は問題なく取得できます

### `streamlit: command not found` エラーが出る場合

```bash
# Pythonモジュールとして実行
python3 -m streamlit run surf_advisor.py
```

### ポート8501が使用中の場合

```bash
lsof -ti:8501 | xargs kill -9
python3 -m streamlit run surf_advisor.py
```

### その他のAPIエラー

1. `.env`ファイルが正しく作成されているか確認
2. インターネット接続を確認
3. Open-Meteo APIは登録不要ですが、稀にダウンタイムがあります

### VSCodeを閉じた後、再開する方法

```bash
cd /Users/taguchi/python/python-day4
python3 -m streamlit run surf_advisor.py
```

または、VSCodeで `/Users/taguchi/python/python-day4` フォルダを開く

## ライセンス

MIT License

## 作者

Taguchi

## 今後の改善案

- [ ] 潮汐情報の追加（満潮/干潮時刻）
- [ ] 水温情報の表示
- [ ] 過去のスコア履歴保存
- [ ] グラフによる可視化
- [ ] 複数日の比較表示
- [ ] プッシュ通知機能
