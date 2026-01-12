# 横スクロールゲーム - 中学生向けプログラミング教材

## 🎮 ゲームの説明

スマホで遊べる横スクロールゲームです！
プレイヤーを操作して、障害物を避けながらゴールを目指しましょう。

---

## 📱 遊び方

### スマホの場合
- **◀ボタン**: 左に移動
- **▶ボタン**: 右に移動
- **▲ボタン**: ジャンプ
- **画面タップ**: ジャンプ（ボタン以外の場所）

### パソコンの場合
- **←キー**: 左に移動
- **→キー**: 右に移動
- **スペースキー**: ジャンプ

---

## 🚀 ゲームの起動方法

1. `index.html` をブラウザで開く
2. スタート画面が表示されます
3. タップまたはスペースキーでゲームスタート！

---

## 🎨 ゲームをカスタマイズしよう！

このゲームは **`config.js`** ファイルを編集するだけで、簡単に見た目や動きを変更できます。

### 1. プレイヤーの色を変える

```javascript
// config.js の PLAYER_CONFIG を編集
const PLAYER_CONFIG = {
    bodyColor: { r: 255, g: 100, b: 100 },  // 赤色
    // → { r: 100, g: 100, b: 255 } に変更すると青色になる！
};
```

**色の指定方法**
- `r` (赤): 0〜255
- `g` (緑): 0〜255
- `b` (青): 0〜255

例：
- 赤色: `{ r: 255, g: 0, b: 0 }`
- 緑色: `{ r: 0, g: 255, b: 0 }`
- 青色: `{ r: 0, g: 0, b: 255 }`
- 黄色: `{ r: 255, g: 255, b: 0 }`
- ピンク: `{ r: 255, g: 100, b: 200 }`

---

### 2. ジャンプの高さを変える

```javascript
// config.js の PLAYER_CONFIG を編集
const PLAYER_CONFIG = {
    jumpPower: -16,  // デフォルト値
    // → -20 にすると高く跳べる
    // → -12 にすると低くなる
};
```

**数値が大きいほど（マイナスなので絶対値）高く跳べます**

---

### 3. ゲームの難易度を変える

```javascript
// config.js の GAME_CONFIG を編集
const GAME_CONFIG = {
    scrollSpeed: 5,        // スクロール速度（大きいほど速い）
    goalDistance: 3000,    // ゴールまでの距離（大きいほど長い）
};

// config.js の OBSTACLE_CONFIG を編集
const OBSTACLE_CONFIG = {
    spawnInterval: 90,  // 障害物が出現する間隔
    // → 60 にすると頻繁に出現（難しい）
    // → 120 にすると少なく出現（簡単）
};
```

---

### 4. 背景の色を変える

```javascript
// config.js の BACKGROUND_CONFIG を編集
const BACKGROUND_CONFIG = {
    skyColor: { r: 135, g: 206, b: 235 },      // 空の色（水色）
    groundColor: { r: 101, g: 67, b: 33 },     // 地面の色（茶色）
    grassColor: { r: 34, g: 139, b: 34 },      // 草の色（緑）
};
```

**夜のステージにしたい場合**
```javascript
skyColor: { r: 20, g: 20, b: 50 },     // 暗い青色
groundColor: { r: 50, g: 50, b: 50 },  // グレー
```

---

### 5. BGMを変える

```javascript
// config.js の SOUND_CONFIG を編集
const SOUND_CONFIG = {
    // 好きな音楽のURLに変更できます
    bgmUrl: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",

    // 音量の調整（0.0〜1.0）
    bgmVolume: 0.3,      // BGMの音量
    soundVolume: 0.5,    // 効果音の音量
};
```

**BGMを消したい場合**
```javascript
bgmUrl: "",  // 空文字にする
```

---

## 🎓 プログラミングの学習ポイント

### 初級編：設定ファイルを変更してみよう

1. `config.js` を開く
2. 色や数値を変更する
3. ブラウザでリロード（F5キー）して確認
4. 気に入った設定を見つけよう！

**チャレンジ問題**
- プレイヤーを虹色にしてみよう
- ジャンプ力を2倍にしてみよう
- ゴールまでの距離を10000mにしてみよう

---

### 中級編：ゲームロジックを理解しよう

`game.js` を開いて、以下の部分を読んでみましょう：

#### プレイヤーの動き（重力の実装）
```javascript
// updatePlayer() 関数
player.velocityY += PLAYER_CONFIG.gravity;  // 重力を適用
player.y += player.velocityY;               // Y座標を更新
```

#### 衝突判定
```javascript
// checkCollision() 関数
if (
    player.worldX < obstacle.x + obstacle.width &&
    player.worldX + player.width > obstacle.x &&
    player.y < obstacle.y + obstacle.height &&
    player.y + player.height > obstacle.y
) {
    return true;  // 当たった！
}
```

---

### 上級編：新しい機能を追加してみよう

#### 1. コインを集める機能を追加

`game.js` に以下のコードを追加：

```javascript
// コインのリスト
let coins = [];

// コインの生成（createObstacle関数の近くに追加）
function createCoin() {
    coins.push({
        x: cameraX + width + 100,
        y: random(groundY - 150, groundY - 50),
        size: 20,
        collected: false
    });
}

// コインの描画（drawObstacles関数の近くに追加）
function drawCoins() {
    fill(255, 215, 0);  // 金色
    for (let coin of coins) {
        if (!coin.collected) {
            ellipse(coin.x, coin.y, coin.size, coin.size);
        }
    }
}
```

#### 2. ダブルジャンプ機能

```javascript
// プレイヤーに jumpCount を追加
player.jumpCount = 0;

// handleJump() 関数を修正
function handleJump() {
    if (gameState === "PLAYING" && player.jumpCount < 2) {
        player.velocityY = PLAYER_CONFIG.jumpPower;
        player.jumping = true;
        player.jumpCount++;
    }
    // 地面に着いたら jumpCount をリセット
}
```

#### 3. スコアボーナスシステム

```javascript
// ジャンプでポイント追加
if (player.jumping) {
    score += 2;  // ジャンプ中は2倍
}
```

---

## 📚 学習リソース

### p5.jsについて学ぶ
- [p5.js公式サイト（日本語）](https://p5js.org/ja/)
- [p5.jsリファレンス](https://p5js.org/reference/)

### 色について学ぶ
- [RGB カラーピッカー](https://www.google.com/search?q=color+picker)
- 好きな色のRGB値を調べられます

### ゲーム開発について学ぶ
- 当たり判定（衝突検出）
- スクロールの仕組み
- ゲームループ（setup と draw）

---

## 🛠️ ファイル構成

```
day5/
├── index.html    # メインのHTMLファイル
├── config.js     # 設定ファイル（ここを編集！）
├── game.js       # ゲームロジック
└── README.md     # このファイル
```

---

## 💡 よくある質問

### Q1. ゲームが動かない
**A.** ブラウザのコンソールを確認してください（F12キーを押す）。エラーメッセージが表示されます。

### Q2. BGMが流れない
**A.** ブラウザによっては自動再生がブロックされることがあります。画面をタップすると再生されます。

### Q3. スマホで動かない
**A.** 最新のブラウザ（Chrome、Safari）を使用してください。

### Q4. 色を変更したのに反映されない
**A.** ブラウザをリロード（更新）してください。キャッシュが残っている場合は、Ctrl+Shift+R（強制リロード）を試してください。

---

## 🎯 発展課題

1. **新しい障害物を追加しよう**
   - 鳥、穴、壁など

2. **パワーアップアイテムを作ろう**
   - 無敵時間、スピードアップなど

3. **ステージセレクト機能**
   - 複数のステージを作って選べるように

4. **ランキング機能**
   - ハイスコアを保存する（localStorage使用）

5. **マルチプレイヤー**
   - 2人で競争できるモードを追加

---

## 📝 作者より

このゲームは中学生の皆さんがプログラミングの楽しさを学べるように作りました。

**大切なこと：**
- 失敗を恐れずに色々試してみよう！
- 分からないことがあったら調べてみよう
- 自分だけのオリジナルゲームを作ってみよう

**プログラミングは創造力を形にする魔法です！**

楽しんでください！

---

## 📄 ライセンス

このプロジェクトは教育目的で自由に使用・改変できます。
