# コード構造詳細ドキュメント

このドキュメントは、game.jsの各関数の詳細な動作を説明します。

---

## 📋 目次

1. [初期化・セットアップ](#初期化セットアップ)
2. [メインループ](#メインループ)
3. [ゲーム状態管理](#ゲーム状態管理)
4. [プレイヤーシステム](#プレイヤーシステム)
5. [障害物システム](#障害物システム)
6. [描画システム](#描画システム)
7. [入力システム](#入力システム)
8. [衝突判定](#衝突判定)

---

## 初期化・セットアップ

### `setup()` - 初期化関数
**呼び出しタイミング**: ゲーム開始時に1回のみ

```javascript
function setup() {
    // キャンバス作成
    createCanvas(GAME_CONFIG.canvasWidth, GAME_CONFIG.canvasHeight);

    // 地面のY座標を設定
    groundY = height - 100;

    // プレイヤーオブジェクトの初期化
    player = {
        x: GAME_CONFIG.playerStartX,        // 画面上のX位置
        y: groundY - PLAYER_CONFIG.height,  // 地面の上に配置
        width: PLAYER_CONFIG.width,
        height: PLAYER_CONFIG.height,
        velocityY: 0,                       // 初期速度はゼロ
        velocityX: 0,
        jumping: false,                     // ジャンプ中フラグ
        worldX: GAME_CONFIG.playerStartX    // ワールド座標
    };

    // 雲を5個ランダムに配置
    for (let i = 0; i < 5; i++) {
        clouds.push({
            x: random(width * 2),           // 画面幅の2倍の範囲に配置
            y: random(50, 150),             // 上部にランダム配置
            size: random(60, 100)           // サイズもランダム
        });
    }

    // スマホ用タッチボタンの設定
    setupTouchControls();
}
```

**編集のポイント**:
- プレイヤーの初期位置を変更: `player.x`, `player.y`
- 雲の数を変更: ループの回数
- 初期設定を追加: この関数内でグローバル変数を初期化

---

### `setupTouchControls()` - タッチコントロール設定
**呼び出しタイミング**: setup() から1回のみ

```javascript
function setupTouchControls() {
    // HTMLボタン要素を取得
    let leftBtn = document.getElementById('leftBtn');
    let rightBtn = document.getElementById('rightBtn');
    let jumpBtn = document.getElementById('jumpBtn');

    // 左ボタン（タッチイベント）
    leftBtn.addEventListener('touchstart', (e) => {
        e.preventDefault();     // デフォルト動作を防止
        keys.left = true;       // 左キーを押された状態に
    });
    leftBtn.addEventListener('touchend', (e) => {
        e.preventDefault();
        keys.left = false;      // 左キーを離された状態に
    });

    // 右ボタン（タッチイベント）
    rightBtn.addEventListener('touchstart', (e) => {
        e.preventDefault();
        keys.right = true;
    });
    rightBtn.addEventListener('touchend', (e) => {
        e.preventDefault();
        keys.right = false;
    });

    // ジャンプボタン
    jumpBtn.addEventListener('touchstart', (e) => {
        e.preventDefault();
        handleJump();           // ジャンプ処理を実行
    });

    // PC用（マウスイベント）
    leftBtn.addEventListener('mousedown', () => keys.left = true);
    leftBtn.addEventListener('mouseup', () => keys.left = false);
    rightBtn.addEventListener('mousedown', () => keys.right = true);
    rightBtn.addEventListener('mouseup', () => keys.right = false);
    jumpBtn.addEventListener('mousedown', () => handleJump());
}
```

**編集のポイント**:
- 新しいボタンを追加する場合、ここに追加
- 長押しで加速などの機能追加も可能

---

## メインループ

### `draw()` - メインループ
**呼び出しタイミング**: 毎フレーム（約60FPS）

```javascript
function draw() {
    // 背景色で画面をクリア
    background(
        BACKGROUND_CONFIG.skyColor.r,
        BACKGROUND_CONFIG.skyColor.g,
        BACKGROUND_CONFIG.skyColor.b
    );

    // ゲーム状態に応じて処理を分岐
    if (gameState === "START") {
        drawStartScreen();              // スタート画面を表示
    } else if (gameState === "PLAYING") {
        updateGame();                   // ゲームを更新
        drawGame();                     // ゲームを描画
    } else if (gameState === "GAMEOVER") {
        drawGame();                     // 背景を描画
        drawGameOverScreen();           // ゲームオーバー画面を重ねて表示
    } else if (gameState === "GOAL") {
        drawGame();                     // 背景を描画
        drawGoalScreen();               // ゴール画面を重ねて表示
    }
}
```

**フロー図**:
```
draw() が毎フレーム実行
    ↓
gameState で分岐
    ↓
START    → drawStartScreen()
PLAYING  → updateGame() → drawGame()
GAMEOVER → drawGame() → drawGameOverScreen()
GOAL     → drawGame() → drawGoalScreen()
```

**編集のポイント**:
- 新しいゲーム状態を追加: `else if (gameState === "PAUSE")`
- グローバルエフェクトを追加: 背景描画の後に追加

---

## ゲーム状態管理

### `updateGame()` - ゲーム更新処理
**呼び出しタイミング**: gameState が "PLAYING" の時、毎フレーム

```javascript
function updateGame() {
    // 1. プレイヤーの位置と速度を更新
    updatePlayer();

    // 2. カメラをプレイヤーに追従させる
    cameraX = player.worldX - width / 4;
    // → プレイヤーが画面の1/4の位置に来るように

    // 3. 一定間隔で障害物を生成
    if (frameCount % OBSTACLE_CONFIG.spawnInterval === 0) {
        createObstacle();
    }

    // 4. 障害物を更新（画面外の削除）
    updateObstacles();

    // 5. 衝突判定
    if (checkCollision()) {
        gameState = "GAMEOVER";         // ゲームオーバーに遷移
    }

    // 6. ゴール判定
    if (player.worldX >= GAME_CONFIG.goalDistance) {
        gameState = "GOAL";             // ゴールに遷移
    }

    // 7. スコアと距離を更新
    score++;
    distanceTraveled = player.worldX - GAME_CONFIG.playerStartX;
}
```

**処理順序が重要**:
1. プレイヤー更新 → カメラ更新 → 障害物生成・更新 → 判定

**編集のポイント**:
- アイテム生成を追加: 障害物生成の後に追加
- 時間制限を追加: 経過時間をカウントして判定
- パワーアップ効果を追加: プレイヤー更新の前に状態チェック

---

### `resetGame()` - ゲームリセット
**呼び出しタイミング**: ゲームオーバー/ゴール後にスペースキーまたはタップ

```javascript
function resetGame() {
    // プレイヤーを初期位置に戻す
    player.worldX = GAME_CONFIG.playerStartX;
    player.x = GAME_CONFIG.playerStartX;
    player.y = groundY - player.height;
    player.velocityY = 0;
    player.velocityX = 0;
    player.jumping = false;

    // 障害物をすべて削除
    obstacles = [];

    // スコアと距離をリセット
    score = 0;
    distanceTraveled = 0;

    // カメラをリセット
    cameraX = 0;

    // スタート画面に戻る
    gameState = "START";
}
```

**編集のポイント**:
- セーブ機能を追加: リセット前にスコアを保存
- 追加した要素のリセット: 新しく追加したアイテムやエフェクトをリセット

---

## プレイヤーシステム

### `updatePlayer()` - プレイヤー更新
**呼び出しタイミング**: updateGame() から毎フレーム

```javascript
function updatePlayer() {
    // 1. 左右移動の処理
    if (keys.left) {
        player.velocityX = -PLAYER_CONFIG.moveSpeed;    // 左に移動
    } else if (keys.right) {
        player.velocityX = PLAYER_CONFIG.moveSpeed;     // 右に移動
    } else {
        player.velocityX = 0;                           // 止まる
    }

    // 2. 重力を適用（毎フレーム下向きの加速度）
    player.velocityY += PLAYER_CONFIG.gravity;

    // 3. 速度を位置に反映
    player.y += player.velocityY;          // Y座標を更新
    player.worldX += player.velocityX;     // ワールドX座標を更新

    // 4. 地面との衝突判定
    if (player.y >= groundY - player.height) {
        player.y = groundY - player.height;     // 地面の上に補正
        player.velocityY = 0;                   // Y速度をリセット
        player.jumping = false;                 // ジャンプ終了
    }

    // 5. 画面左端を越えないように
    if (player.worldX < 0) {
        player.worldX = 0;
    }
}
```

**物理演算の流れ**:
```
重力加速度を速度に加算
    ↓
速度を位置に加算
    ↓
地面判定
    ↓
地面に着いたら速度をリセット
```

**編集のポイント**:
- 空中での横移動速度を変える: `if (!player.jumping)` で分岐
- 最高速度を制限: `player.velocityX` に上限を設定
- 摩擦を追加: `player.velocityX *= 0.9` などで減衰

---

### `handleJump()` - ジャンプ処理
**呼び出しタイミング**: スペースキー、上矢印、タップ時

```javascript
function handleJump() {
    if (gameState === "START") {
        // スタート画面でジャンプ → ゲーム開始
        gameState = "PLAYING";

    } else if (gameState === "PLAYING" && !player.jumping) {
        // ゲーム中かつジャンプ中でない → ジャンプ
        player.velocityY = PLAYER_CONFIG.jumpPower;  // 上向きの速度
        player.jumping = true;                       // ジャンプフラグ

    } else if (gameState === "GAMEOVER" || gameState === "GOAL") {
        // ゲームオーバー/ゴール画面 → リセット
        resetGame();
    }
}
```

**ジャンプの仕組み**:
- `velocityY` に負の値を設定 → 上に移動
- 重力で徐々に速度が減少 → 頂点に達する
- 速度が正になる → 下降
- 地面に着地 → `jumping = false`

**編集のポイント**:
- ダブルジャンプを実装: `jumpCount` 変数を追加
- ジャンプ力を変動させる: パワーアップで `jumpPower` を変更
- ジャンプ中の操作を制限: `if (player.jumping) return;`

---

### `drawPlayer()` - プレイヤー描画
**呼び出しタイミング**: drawGame() から毎フレーム

```javascript
function drawPlayer() {
    push();  // 描画設定を保存

    // 1. 体を描画
    fill(PLAYER_CONFIG.bodyColor.r, PLAYER_CONFIG.bodyColor.g, PLAYER_CONFIG.bodyColor.b);
    rect(player.worldX, player.y, player.width, player.height, 5);

    // 2. 目を描画（白目）
    fill(PLAYER_CONFIG.eyeColor.r, PLAYER_CONFIG.eyeColor.g, PLAYER_CONFIG.eyeColor.b);
    ellipse(player.worldX + 12, player.y + 15, 10, 10);
    ellipse(player.worldX + 28, player.y + 15, 10, 10);

    // 3. 瞳を描画（黒目）
    fill(PLAYER_CONFIG.pupilColor.r, PLAYER_CONFIG.pupilColor.g, PLAYER_CONFIG.pupilColor.b);
    ellipse(player.worldX + 12, player.y + 15, 5, 5);
    ellipse(player.worldX + 28, player.y + 15, 5, 5);

    // 4. 口を描画
    noFill();
    stroke(0);
    strokeWeight(2);
    arc(player.worldX + 20, player.y + 30, 15, 10, 0, PI);
    noStroke();

    pop();  // 描画設定を復元
}
```

**座標の計算**:
- すべて `player.worldX` と `player.y` を基準に相対位置で描画
- `translate(-cameraX, 0)` でスクロールに対応

**編集のポイント**:
- アニメーションを追加: `sin(frameCount)` で上下に揺らす
- 向きを変える: `keys.left` の時に `scale(-1, 1)` で反転
- 装飾を追加: 帽子、髪、服などのパーツを追加

---

## 障害物システム

### `createObstacle()` - 障害物生成
**呼び出しタイミング**: updateGame() から一定間隔で

```javascript
function createObstacle() {
    // ランダムで障害物のタイプを決定
    let obstacleType = random() > 0.5 ? 'cactus' : 'rock';

    // タイプに応じたサイズを取得
    let config = obstacleType === 'cactus'
        ? OBSTACLE_CONFIG.cactusSize
        : OBSTACLE_CONFIG.rockSize;

    // 障害物オブジェクトを配列に追加
    obstacles.push({
        x: cameraX + width + 100,       // 画面右端の外側
        y: groundY - config.height,     // 地面の上
        width: config.width,
        height: config.height,
        type: obstacleType
    });
}
```

**生成位置の計算**:
- `cameraX + width + 100` → カメラ位置 + 画面幅 + 余裕
- これにより画面外から障害物が登場

**編集のポイント**:
- 新しい障害物タイプを追加: `'bird'`, `'hole'` など
- 生成確率を調整: `random() > 0.3` で70%の確率
- 高さをランダムに: `y: random(groundY - 100, groundY - 50)`

---

### `updateObstacles()` - 障害物更新
**呼び出しタイミング**: updateGame() から毎フレーム

```javascript
function updateObstacles() {
    // 配列を後ろから処理（削除しても影響なし）
    for (let i = obstacles.length - 1; i >= 0; i--) {
        // 画面左端より左に行ったら削除
        if (obstacles[i].x < cameraX - 200) {
            obstacles.splice(i, 1);     // 配列から削除
        }
    }
}
```

**配列を後ろから処理する理由**:
- 前から削除すると、インデックスがずれる
- 後ろから削除すれば、まだ処理していない要素に影響なし

**編集のポイント**:
- 障害物を移動させる: `obstacles[i].x -= speed;`
- 障害物にアニメーションを追加: `obstacles[i].rotation += 0.1;`

---

### `drawObstacles()` - 障害物描画
**呼び出しタイミング**: drawGame() から毎フレーム

```javascript
function drawObstacles() {
    for (let obstacle of obstacles) {
        if (obstacle.type === 'cactus') {
            // サボテンの描画
            fill(OBSTACLE_CONFIG.cactusColor.r,
                 OBSTACLE_CONFIG.cactusColor.g,
                 OBSTACLE_CONFIG.cactusColor.b);
            rect(obstacle.x + 10, obstacle.y, 10, obstacle.height, 5);    // 本体
            rect(obstacle.x, obstacle.y + 10, 10, 15, 5);                 // 左腕
            rect(obstacle.x + 20, obstacle.y + 15, 10, 10, 5);            // 右腕

        } else {
            // 岩の描画
            fill(OBSTACLE_CONFIG.rockColor.r,
                 OBSTACLE_CONFIG.rockColor.g,
                 OBSTACLE_CONFIG.rockColor.b);
            triangle(
                obstacle.x + obstacle.width / 2, obstacle.y,              // 上
                obstacle.x, obstacle.y + obstacle.height,                 // 左下
                obstacle.x + obstacle.width, obstacle.y + obstacle.height // 右下
            );
        }
    }
}
```

**編集のポイント**:
- 新しいタイプの描画を追加: `else if (obstacle.type === 'bird')`
- アニメーション効果: `rotate()` で回転させる

---

## 衝突判定

### `checkCollision()` - 衝突判定
**呼び出しタイミング**: updateGame() から毎フレーム

```javascript
function checkCollision() {
    for (let obstacle of obstacles) {
        // AABB（Axis-Aligned Bounding Box）衝突判定
        if (
            player.worldX < obstacle.x + obstacle.width &&      // プレイヤーの左端が障害物の右端より左
            player.worldX + player.width > obstacle.x &&        // プレイヤーの右端が障害物の左端より右
            player.y < obstacle.y + obstacle.height &&          // プレイヤーの上端が障害物の下端より上
            player.y + player.height > obstacle.y               // プレイヤーの下端が障害物の上端より下
        ) {
            return true;    // 衝突している
        }
    }
    return false;           // 衝突していない
}
```

**AABB衝突判定の仕組み**:
```
矩形Aと矩形Bが重なる条件：
- AのLeft < BのRight
- AのRight > BのLeft
- AのTop < BのBottom
- AのBottom > BのTop

すべて満たす → 衝突している
```

**編集のポイント**:
- 当たり判定を小さくする: `player.width - 10` など
- 円形の当たり判定: `dist()` 関数を使用
- 無敵時間を追加: `if (player.invincible) continue;`

---

## 描画システム

### `drawUI()` - UI描画
**呼び出しタイミング**: drawGame() から毎フレーム

```javascript
function drawUI() {
    push();
    textAlign(LEFT);

    // スコア表示
    fill(UI_CONFIG.scoreColor.r, UI_CONFIG.scoreColor.g, UI_CONFIG.scoreColor.b);
    textSize(UI_CONFIG.scoreSize);
    text("スコア: " + score, 20, 40);

    // 距離表示
    fill(UI_CONFIG.distanceColor.r, UI_CONFIG.distanceColor.g, UI_CONFIG.distanceColor.b);
    textSize(UI_CONFIG.distanceSize);
    text("距離: " + floor(distanceTraveled) + " / " + GAME_CONFIG.goalDistance + "m", 20, 70);

    // 進捗バー
    let progress = distanceTraveled / GAME_CONFIG.goalDistance;
    fill(100);
    rect(20, 80, 200, 10);          // 背景
    fill(100, 255, 100);
    rect(20, 80, 200 * progress, 10);  // 進捗

    pop();
}
```

**編集のポイント**:
- 新しいUIを追加: コイン数、残りライフなど
- UIの配置を変更: 座標を調整
- アイコンを追加: `image()` で画像表示

---

## 入力システム

### `keyPressed()` / `keyReleased()`
**呼び出しタイミング**: キーが押された/離された時

```javascript
function keyPressed() {
    if (key === ' ' || keyCode === UP_ARROW) {
        handleJump();
    }
    if (keyCode === LEFT_ARROW) keys.left = true;
    if (keyCode === RIGHT_ARROW) keys.right = true;
}

function keyReleased() {
    if (keyCode === LEFT_ARROW) keys.left = false;
    if (keyCode === RIGHT_ARROW) keys.right = false;
}
```

**編集のポイント**:
- 新しいキーを追加: `key === 'd'` など
- ポーズ機能: `key === 'p'` で `gameState = "PAUSE"`

---

**最終更新**: 2026-01-07
