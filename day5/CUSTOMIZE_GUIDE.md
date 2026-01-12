# カスタマイズガイド - AI アシスタント向け

このドキュメントは、将来的にこのゲームをカスタマイズする際に、AIアシスタントがスムーズにサポートできるように作成されています。

---

## 📂 ファイル構成

```
day5/
├── index.html           # HTMLファイル（基本的に編集不要）
├── config.js            # 設定ファイル（素材の見た目を管理）
├── game.js              # ゲームロジック（メインプログラム）
├── CUSTOMIZE_GUIDE.md   # このファイル
├── CODE_STRUCTURE.md    # コード構造の詳細説明
└── EXAMPLES.md          # よくあるカスタマイズ例
```

---

## 🎯 カスタマイズの基本方針

### レベル1：設定変更（初心者向け）
→ **config.js** のみを編集
- 色の変更
- サイズの変更
- ゲーム速度の調整
- ゴール距離の変更

### レベル2：機能追加（中級者向け）
→ **game.js** に新しい関数を追加
- コインの追加
- パワーアップアイテム
- 新しい障害物タイプ
- エフェクト追加

### レベル3：システム拡張（上級者向け）
→ **game.js** の既存関数を修正
- ステージシステム
- セーブ機能
- マルチプレイヤー
- 物理エンジンの変更

---

## 🔧 重要な変数とデータ構造

### グローバル変数
```javascript
// game.js 内
gameState       // "START" | "PLAYING" | "GAMEOVER" | "GOAL"
player          // プレイヤーオブジェクト
obstacles       // 障害物の配列
clouds          // 雲の配列
score           // スコア（数値）
distanceTraveled // 進んだ距離（数値）
groundY         // 地面のY座標（数値）
cameraX         // カメラのX座標（数値）
keys            // キー入力の状態 { left, right, jump }
```

### プレイヤーオブジェクトの構造
```javascript
player = {
    x: 100,              // 画面上のX座標
    y: 500,              // Y座標
    width: 40,           // 幅
    height: 50,          // 高さ
    velocityY: 0,        // Y方向の速度
    velocityX: 0,        // X方向の速度
    jumping: false,      // ジャンプ中か
    worldX: 100          // ワールド座標のX（スクロール対応）
}
```

### 障害物オブジェクトの構造
```javascript
obstacle = {
    x: 800,              // ワールド座標のX
    y: 460,              // Y座標
    width: 30,           // 幅
    height: 40,          // 高さ
    type: 'cactus'       // 'cactus' または 'rock'
}
```

---

## 🎮 主要な関数一覧

### p5.js コアフ��ンクション
```javascript
setup()          // 初期化（1回だけ実行）
draw()           // メインループ（毎フレーム実行）
keyPressed()     // キーが押された時
keyReleased()    // キーが離された時
touchStarted()   // タッチされた時
```

### ゲーム状態管理
```javascript
drawStartScreen()      // スタート画面の描画
drawGameOverScreen()   // ゲームオーバー画面の描画
drawGoalScreen()       // ゴール画面の描画
updateGame()           // ゲームの更新処理
drawGame()             // ゲームの描画処理
resetGame()            // ゲームのリセット
```

### プレイヤー関連
```javascript
updatePlayer()   // プレイヤーの位置・速度更新
drawPlayer()     // プレイヤーの描画
handleJump()     // ジャンプ処理
```

### 障害物関連
```javascript
createObstacle()    // 障害物の生成
updateObstacles()   // 障害物の更新（画面外削除）
drawObstacles()     // 障害物の描画
checkCollision()    // 衝突判定
```

### 背景・UI関連
```javascript
drawClouds()        // 雲の描画
drawGround()        // 地面の描画
drawStartFlag()     // スタート旗の描画
drawGoalFlag()      // ゴール旗の描画
drawUI()            // UI（スコア・距離）の描画
```

### コントロール
```javascript
setupTouchControls()  // タッチボタンのイベント設定
```

---

## 🔄 ゲームループの流れ

```
1. setup() が実行される（初期化）
   ↓
2. draw() が毎フレーム実行される
   ↓
3. gameState によって分岐

   START → drawStartScreen()

   PLAYING → updateGame() → drawGame()
             ├── updatePlayer()
             ├── createObstacle()
             ├── updateObstacles()
             ├── checkCollision()
             └── ゴール判定

   GAMEOVER → drawGame() → drawGameOverScreen()

   GOAL → drawGame() → drawGoalScreen()
```

---

## 🎨 カスタマイズ時の注意点

### 1. 座標系について
- **画面座標**: canvas上の座標（0 〜 canvasWidth）
- **ワールド座標**: ゲーム世界の座標（0 〜 無限）
- プレイヤーは `player.worldX` でワールド座標を持つ
- カメラは `cameraX` でスクロールを管理
- `translate(-cameraX, 0)` で画面をスクロール

### 2. 衝突判定の計算
```javascript
// 矩形同士の衝突判定（AABB）
if (
    player.worldX < obstacle.x + obstacle.width &&
    player.worldX + player.width > obstacle.x &&
    player.y < obstacle.y + obstacle.height &&
    player.y + player.height > obstacle.y
) {
    // 衝突している
}
```

### 3. 障害物の生成タイミング
- `frameCount % OBSTACLE_CONFIG.spawnInterval === 0` で生成
- 画面右端（`cameraX + width + 100`）に生成される
- 画面左端を過ぎたら削除される

### 4. 重力と物理演算
```javascript
// 毎フレーム
player.velocityY += PLAYER_CONFIG.gravity;  // 重力を加える
player.y += player.velocityY;               // 速度を位置に反映

// 地面に着いたら
if (player.y >= groundY - player.height) {
    player.y = groundY - player.height;
    player.velocityY = 0;
    player.jumping = false;
}
```

---

## 🛠️ よくあるカスタマイズ要望

### 1. 新しいアイテムを追加したい
→ `EXAMPLES.md` の「コイン追加」を参照

### 2. 敵キャラクターを動かしたい
→ 障害物に `velocityX` プロパティを追加して `updateObstacles()` で移動

### 3. ダブルジャンプを実装したい
→ プレイヤーに `jumpCount` プロパティを追加

### 4. ステージを変えたい
→ config.js に `STAGE_CONFIG` を追加して背景色を切り替え

### 5. BGM/効果音を追加したい
→ p5.sound.min.js を index.html に追加してから実装

### 6. セーブ機能が欲しい
→ `localStorage.setItem()` でスコアを保存

---

## 📋 カスタマイズ前のチェックリスト

カスタマイズを始める前に確認してください：

- [ ] 現在のゲームが正常に動作している
- [ ] どのファイルを編集するか明確になっている
- [ ] 編集前にバックアップを取っている
- [ ] ブラウザのコンソール（F12）を開いてエラーを確認できる
- [ ] 変更内容が既存の機能と競合しないか確認している

---

## 🐛 デバッグのヒント

### エラーが出たら
1. ブラウザのコンソール（F12キー）を開く
2. エラーメッセージの行番号を確認
3. その行の前後を確認
4. console.log() でデバッグ出力を追加

### ゲームが動かなくなったら
1. `console.log("ここまで実行された")` を要所に追加
2. どの時点で止まっているか確認
3. 変数の値を console.log() で出力

### よくあるミス
- セミコロン `;` の付け忘れ
- カッコ `{}` や `[]` の閉じ忘れ
- 変数名のタイポ（スペルミス）
- config.js で定義していない値を使っている

---

## 💬 AI アシスタントへの指示例

カスタマイズを依頼する際は、以下のように具体的に伝えてください：

### 良い例
```
「プレイヤーの色を青色（RGB: 100, 100, 255）に変更して、
ジャンプ力を現在の1.5倍にしてください」

「障害物にコインを追加したい。コインは黄色の円で、
取ると+10点、画面上に常に2〜3個表示されるようにしてください」
```

### 悪い例（情報不足）
```
「もっと面白くして」
「色を変えて」
「難しくして」
```

---

## 📌 重要なコーディング規約

このプロジェクトでは以下の規約を守ってください：

1. **設定値は config.js に書く**
   - マジックナンバー（直接書かれた数値）を避ける

2. **関数は1つの役割に集中**
   - 関数が長くなりすぎたら分割を検討

3. **日本語コメントを付ける**
   - 中学生が読んでも理解できるように

4. **変数名は分かりやすく**
   - `x`, `y` より `playerX`, `playerY`

5. **グローバル変数は最小限に**
   - 必要なものだけをグローバルに

---

## 🔗 関連ファイル

詳細な情報は以下のファイルを参照してください：

- [CODE_STRUCTURE.md](CODE_STRUCTURE.md) - コードの詳細構造
- [EXAMPLES.md](EXAMPLES.md) - 具体的なカスタマイズ例とコード
- [README.md](README.md) - 基本的な使い方

---

## 📞 サポートが必要な場合

AIアシスタントに質問する際は：

1. **何を実現したいか**を明確に伝える
2. **どのファイルのどの部分**を変更するか分かっていれば伝える
3. **エラーメッセージ**があれば全文をコピーして伝える
4. **期待する動作**と**実際の動作**を説明する

---

**最終更新**: 2026-01-07
**バージョン**: 1.0
**対象ファイル**: day5/ 内の全ファイル
