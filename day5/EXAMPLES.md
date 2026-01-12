# カスタマイズ実例集

よくあるカスタマイズのコード例をまとめています。コピー＆ペーストですぐに使えます。

---

## 📋 目次

1. [プレイヤーのカスタマイズ](#プレイヤーのカスタマイズ)
2. [新しいアイテムの追加](#新しいアイテムの追加)
3. [新しい障害物の追加](#新しい障害物の追加)
4. [ゲームシステムの拡張](#ゲームシステムの拡張)
5. [エフェクトの追加](#エフェクトの追加)
6. [難易度調整](#難易度調整)

---

## プレイヤーのカスタマイズ

### 例1: ダブルジャンプの実装

**手順**:
1. プレイヤーに `jumpCount` プロパティを追加
2. `handleJump()` を修正
3. `updatePlayer()` で地面に着いたらリセット

**コード**:

```javascript
// ===== setup() 内のプレイヤー初期化に追加 =====
player = {
    // ... 既存のプロパティ ...
    jumpCount: 0,          // 追加: ジャンプ回数
    maxJumps: 2            // 追加: 最大ジャンプ回数
};

// ===== handleJump() を以下に置き換え =====
function handleJump() {
    if (gameState === "START") {
        gameState = "PLAYING";
    } else if (gameState === "PLAYING" && player.jumpCount < player.maxJumps) {
        player.velocityY = PLAYER_CONFIG.jumpPower;
        player.jumping = true;
        player.jumpCount++;    // ジャンプ回数を増やす
    } else if (gameState === "GAMEOVER" || gameState === "GOAL") {
        resetGame();
    }
}

// ===== updatePlayer() の地面判定部分を修正 =====
if (player.y >= groundY - player.height) {
    player.y = groundY - player.height;
    player.velocityY = 0;
    player.jumping = false;
    player.jumpCount = 0;      // 追加: 地面に着いたらリセット
}
```

---

### 例2: プレイヤーの向きを変える

**左右移動に応じてプレイヤーが向きを変える**

```javascript
// ===== setup() 内のプレイヤー初期化に追加 =====
player = {
    // ... 既存のプロパティ ...
    direction: 1           // 1: 右向き, -1: 左向き
};

// ===== updatePlayer() の左右移動部分に追加 =====
if (keys.left) {
    player.velocityX = -PLAYER_CONFIG.moveSpeed;
    player.direction = -1;     // 追加: 左向き
} else if (keys.right) {
    player.velocityX = PLAYER_CONFIG.moveSpeed;
    player.direction = 1;      // 追加: 右向き
} else {
    player.velocityX = 0;
}

// ===== drawPlayer() を以下のように修正 =====
function drawPlayer() {
    push();

    // プレイヤーの中心を基準に反転
    translate(player.worldX + player.width / 2, player.y + player.height / 2);
    scale(player.direction, 1);    // 左向きの時は反転
    translate(-player.width / 2, -player.height / 2);

    // 体を描画（座標は (0, 0) 基準に）
    fill(PLAYER_CONFIG.bodyColor.r, PLAYER_CONFIG.bodyColor.g, PLAYER_CONFIG.bodyColor.b);
    rect(0, 0, player.width, player.height, 5);

    // 目を描画
    fill(PLAYER_CONFIG.eyeColor.r, PLAYER_CONFIG.eyeColor.g, PLAYER_CONFIG.eyeColor.b);
    ellipse(12, 15, 10, 10);
    ellipse(28, 15, 10, 10);

    // 瞳を描画
    fill(PLAYER_CONFIG.pupilColor.r, PLAYER_CONFIG.pupilColor.g, PLAYER_CONFIG.pupilColor.b);
    ellipse(12, 15, 5, 5);
    ellipse(28, 15, 5, 5);

    // 口を描画
    noFill();
    stroke(0);
    strokeWeight(2);
    arc(20, 30, 15, 10, 0, PI);
    noStroke();

    pop();
}
```

---

### 例3: プレイヤーにアニメーションを追加

**上下に揺れる動き**

```javascript
// ===== drawPlayer() に追加 =====
function drawPlayer() {
    push();

    // ジャンプ中は回転、地上では上下に揺れる
    let offsetY = 0;
    let rotation = 0;

    if (player.jumping) {
        rotation = player.velocityY * 0.05;  // 速度に応じて回転
    } else {
        offsetY = sin(frameCount * 0.2) * 3;  // 上下に揺れる
    }

    // プレイヤーの中心で回転
    translate(player.worldX + player.width / 2, player.y + player.height / 2 + offsetY);
    rotate(rotation);
    translate(-player.width / 2, -player.height / 2);

    // ... 以下は既存の描画コード ...
}
```

---

## 新しいアイテムの追加

### 例4: コインの実装

**手順**:
1. グローバル変数にコイン配列を追加
2. コイン生成関数を作成
3. コイン更新・描画関数を作成
4. 取得判定を追加

**コード**:

```javascript
// ===== ファイル冒頭のグローバル変数に追加 =====
let coins = [];
let coinScore = 0;

// ===== setup() の後に追加 =====
function createCoin() {
    coins.push({
        x: cameraX + width + random(100, 300),
        y: random(groundY - 150, groundY - 50),
        size: 20,
        collected: false,
        rotation: 0
    });
}

function updateCoins() {
    for (let i = coins.length - 1; i >= 0; i--) {
        let coin = coins[i];

        // 回転アニメーション
        coin.rotation += 0.1;

        // プレイヤーとの距離を計算
        let distance = dist(
            player.worldX + player.width / 2,
            player.y + player.height / 2,
            coin.x,
            coin.y
        );

        // 取得判定（距離30以内）
        if (distance < 30 && !coin.collected) {
            coin.collected = true;
            coinScore += 10;
            score += 100;  // スコアも加算
        }

        // 画面外に出たら削除
        if (coin.x < cameraX - 100) {
            coins.splice(i, 1);
        }
    }
}

function drawCoins() {
    for (let coin of coins) {
        if (!coin.collected) {
            push();
            translate(coin.x, coin.y);
            rotate(coin.rotation);

            // コインの描画
            fill(255, 215, 0);        // 金色
            stroke(200, 150, 0);
            strokeWeight(2);
            ellipse(0, 0, coin.size, coin.size);

            // 中心に模様
            fill(255, 235, 100);
            ellipse(0, 0, coin.size * 0.6, coin.size * 0.6);

            pop();
        }
    }
}

// ===== updateGame() に追加 =====
function updateGame() {
    updatePlayer();
    cameraX = player.worldX - width / 4;

    // 障害物生成
    if (frameCount % OBSTACLE_CONFIG.spawnInterval === 0) {
        createObstacle();
    }

    // コイン生成を追加
    if (frameCount % 60 === 0) {      // 1秒に1個
        createCoin();
    }

    updateObstacles();
    updateCoins();                     // 追加

    if (checkCollision()) {
        gameState = "GAMEOVER";
    }

    if (player.worldX >= GAME_CONFIG.goalDistance) {
        gameState = "GOAL";
    }

    score++;
    distanceTraveled = player.worldX - GAME_CONFIG.playerStartX;
}

// ===== drawGame() に追加 =====
function drawGame() {
    push();
    translate(-cameraX, 0);
    drawClouds();
    drawGround();
    drawStartFlag(GAME_CONFIG.playerStartX, groundY);
    drawGoalFlag(GAME_CONFIG.goalDistance, groundY);
    drawCoins();          // 追加（障害物の前に描画）
    drawObstacles();
    drawPlayer();
    pop();
    drawUI();
}

// ===== drawUI() にコイン数表示を追加 =====
function drawUI() {
    push();
    textAlign(LEFT);

    fill(UI_CONFIG.scoreColor.r, UI_CONFIG.scoreColor.g, UI_CONFIG.scoreColor.b);
    textSize(UI_CONFIG.scoreSize);
    text("スコア: " + score, 20, 40);

    // コイン数表示を追加
    fill(255, 215, 0);
    text("コイン: " + coinScore, 20, 80);

    fill(UI_CONFIG.distanceColor.r, UI_CONFIG.distanceColor.g, UI_CONFIG.distanceColor.b);
    textSize(UI_CONFIG.distanceSize);
    text("距離: " + floor(distanceTraveled) + " / " + GAME_CONFIG.goalDistance + "m", 20, 110);

    let progress = distanceTraveled / GAME_CONFIG.goalDistance;
    fill(100);
    rect(20, 120, 200, 10);
    fill(100, 255, 100);
    rect(20, 120, 200 * progress, 10);

    pop();
}

// ===== resetGame() にコイン関連のリセットを追加 =====
function resetGame() {
    player.worldX = GAME_CONFIG.playerStartX;
    player.x = GAME_CONFIG.playerStartX;
    player.y = groundY - player.height;
    player.velocityY = 0;
    player.velocityX = 0;
    player.jumping = false;

    obstacles = [];
    coins = [];           // 追加
    score = 0;
    coinScore = 0;        // 追加
    distanceTraveled = 0;
    cameraX = 0;

    gameState = "START";
}
```

---

## 新しい障害物の追加

### 例5: 空飛ぶ鳥の追加

**上空を飛ぶ鳥型の障害物**

```javascript
// ===== config.js に追加 =====
const OBSTACLE_CONFIG = {
    // ... 既存の設定 ...
    birdColor: { r: 80, g: 80, b: 120 },
    birdSize: { width: 30, height: 20 },
    birdHeight: 200  // 地面からの高さ
};

// ===== createObstacle() を修正 =====
function createObstacle() {
    // 鳥を追加（33%の確率）
    let rand = random();
    let obstacleType;
    if (rand < 0.33) {
        obstacleType = 'cactus';
    } else if (rand < 0.66) {
        obstacleType = 'rock';
    } else {
        obstacleType = 'bird';
    }

    let config;
    let yPos;

    if (obstacleType === 'bird') {
        config = OBSTACLE_CONFIG.birdSize;
        yPos = groundY - OBSTACLE_CONFIG.birdHeight;
    } else {
        config = obstacleType === 'cactus'
            ? OBSTACLE_CONFIG.cactusSize
            : OBSTACLE_CONFIG.rockSize;
        yPos = groundY - config.height;
    }

    obstacles.push({
        x: cameraX + width + 100,
        y: yPos,
        width: config.width,
        height: config.height,
        type: obstacleType,
        wingAngle: 0  // 羽の角度（アニメーション用）
    });
}

// ===== updateObstacles() を修正（アニメーション追加） =====
function updateObstacles() {
    for (let i = obstacles.length - 1; i >= 0; i--) {
        let obstacle = obstacles[i];

        // 鳥の羽ばたきアニメーション
        if (obstacle.type === 'bird') {
            obstacle.wingAngle += 0.2;
        }

        if (obstacle.x < cameraX - 200) {
            obstacles.splice(i, 1);
        }
    }
}

// ===== drawObstacles() に鳥の描画を追加 =====
function drawObstacles() {
    for (let obstacle of obstacles) {
        if (obstacle.type === 'cactus') {
            // ... 既存のサボテン描画 ...
        } else if (obstacle.type === 'rock') {
            // ... 既存の岩描画 ...
        } else if (obstacle.type === 'bird') {
            // 鳥の描画
            push();
            fill(OBSTACLE_CONFIG.birdColor.r,
                 OBSTACLE_CONFIG.birdColor.g,
                 OBSTACLE_CONFIG.birdColor.b);

            // 体
            ellipse(obstacle.x + 15, obstacle.y + 10, 25, 15);

            // 頭
            ellipse(obstacle.x + 25, obstacle.y + 7, 12, 12);

            // くちばし
            fill(255, 150, 0);
            triangle(
                obstacle.x + 30, obstacle.y + 7,
                obstacle.x + 35, obstacle.y + 5,
                obstacle.x + 35, obstacle.y + 9
            );

            // 羽（羽ばたきアニメーション）
            fill(OBSTACLE_CONFIG.birdColor.r,
                 OBSTACLE_CONFIG.birdColor.g,
                 OBSTACLE_CONFIG.birdColor.b);
            let wingOffset = sin(obstacle.wingAngle) * 5;
            triangle(
                obstacle.x + 10, obstacle.y + 10,
                obstacle.x + 5, obstacle.y + 10 + wingOffset,
                obstacle.x + 15, obstacle.y + 15
            );

            pop();
        }
    }
}
```

---

## ゲームシステムの拡張

### 例6: ライフシステムの追加

**3回当たったらゲームオーバー**

```javascript
// ===== グローバル変数に追加 =====
let playerLives = 3;
let invincibleTimer = 0;

// ===== setup() 内のプレイヤー初期化に追加 =====
player = {
    // ... 既存のプロパティ ...
    invincible: false
};

// ===== updateGame() の衝突判定部分を修正 =====
function updateGame() {
    updatePlayer();
    cameraX = player.worldX - width / 4;

    // 無敵時間のカウントダウン
    if (invincibleTimer > 0) {
        invincibleTimer--;
        if (invincibleTimer === 0) {
            player.invincible = false;
        }
    }

    if (frameCount % OBSTACLE_CONFIG.spawnInterval === 0) {
        createObstacle();
    }

    updateObstacles();

    // 衝突判定を修正
    if (checkCollision() && !player.invincible) {
        playerLives--;              // ライフを減らす
        invincibleTimer = 120;      // 2秒間無敵
        player.invincible = true;

        if (playerLives <= 0) {
            gameState = "GAMEOVER";
        }
    }

    if (player.worldX >= GAME_CONFIG.goalDistance) {
        gameState = "GOAL";
    }

    score++;
    distanceTraveled = player.worldX - GAME_CONFIG.playerStartX;
}

// ===== drawPlayer() を修正（無敵時は点滅） =====
function drawPlayer() {
    // 無敵時は点滅させる
    if (player.invincible && frameCount % 10 < 5) {
        return;  // 5フレームごとに非表示
    }

    push();
    // ... 既存の描画コード ...
    pop();
}

// ===== drawUI() にライフ表示を追加 =====
function drawUI() {
    push();
    textAlign(LEFT);

    fill(UI_CONFIG.scoreColor.r, UI_CONFIG.scoreColor.g, UI_CONFIG.scoreColor.b);
    textSize(UI_CONFIG.scoreSize);
    text("スコア: " + score, 20, 40);

    // ライフ表示を追加
    fill(255, 100, 100);
    text("❤ × " + playerLives, 20, 80);

    fill(UI_CONFIG.distanceColor.r, UI_CONFIG.distanceColor.g, UI_CONFIG.distanceColor.b);
    textSize(UI_CONFIG.distanceSize);
    text("距離: " + floor(distanceTraveled) + " / " + GAME_CONFIG.goalDistance + "m", 20, 110);

    let progress = distanceTraveled / GAME_CONFIG.goalDistance;
    fill(100);
    rect(20, 120, 200, 10);
    fill(100, 255, 100);
    rect(20, 120, 200 * progress, 10);

    pop();
}

// ===== resetGame() にライフのリセットを追加 =====
function resetGame() {
    // ... 既存のリセットコード ...
    playerLives = 3;        // 追加
    invincibleTimer = 0;    // 追加
}
```

---

### 例7: ステージシステム

**距離に応じて背景色が変わる**

```javascript
// ===== config.js に追加 =====
const STAGE_CONFIG = {
    stage1: {  // 0 - 1000m
        skyColor: { r: 135, g: 206, b: 235 },
        groundColor: { r: 101, g: 67, b: 33 }
    },
    stage2: {  // 1000 - 2000m
        skyColor: { r: 255, g: 180, b: 100 },
        groundColor: { r: 150, g: 100, b: 50 }
    },
    stage3: {  // 2000 - 3000m
        skyColor: { r: 50, g: 50, b: 100 },
        groundColor: { r: 80, g: 80, b: 80 }
    }
};

// ===== draw() の背景描画を修正 =====
function draw() {
    // ステージに応じた背景色
    let stage;
    if (distanceTraveled < 1000) {
        stage = STAGE_CONFIG.stage1;
    } else if (distanceTraveled < 2000) {
        stage = STAGE_CONFIG.stage2;
    } else {
        stage = STAGE_CONFIG.stage3;
    }

    background(stage.skyColor.r, stage.skyColor.g, stage.skyColor.b);

    // ... 既存のコード ...
}

// ===== drawGround() も同様に修正 =====
function drawGround() {
    let stage;
    if (distanceTraveled < 1000) {
        stage = STAGE_CONFIG.stage1;
    } else if (distanceTraveled < 2000) {
        stage = STAGE_CONFIG.stage2;
    } else {
        stage = STAGE_CONFIG.stage3;
    }

    fill(stage.groundColor.r, stage.groundColor.g, stage.groundColor.b);
    rect(cameraX - 100, groundY, width + 200, height - groundY);

    fill(BACKGROUND_CONFIG.grassColor.r, BACKGROUND_CONFIG.grassColor.g, BACKGROUND_CONFIG.grassColor.b);
    rect(cameraX - 100, groundY - 10, width + 200, 10);
}
```

---

## エフェクトの追加

### 例8: パーティクルエフェクト

**ジャンプ時に粒子が飛び散る**

```javascript
// ===== グローバル変数に追加 =====
let particles = [];

// ===== パーティクルクラス =====
class Particle {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.velocityX = random(-3, 3);
        this.velocityY = random(-5, -1);
        this.life = 30;  // 30フレーム生存
        this.size = random(3, 8);
    }

    update() {
        this.x += this.velocityX;
        this.y += this.velocityY;
        this.velocityY += 0.2;  // 重力
        this.life--;
    }

    draw() {
        let alpha = map(this.life, 0, 30, 0, 255);
        fill(255, 200, 100, alpha);
        noStroke();
        ellipse(this.x, this.y, this.size);
    }

    isDead() {
        return this.life <= 0;
    }
}

// ===== handleJump() にパーティクル生成を追加 =====
function handleJump() {
    if (gameState === "START") {
        gameState = "PLAYING";
    } else if (gameState === "PLAYING" && !player.jumping) {
        player.velocityY = PLAYER_CONFIG.jumpPower;
        player.jumping = true;

        // パーティクルを生成
        for (let i = 0; i < 10; i++) {
            particles.push(new Particle(
                player.worldX + player.width / 2,
                player.y + player.height
            ));
        }
    } else if (gameState === "GAMEOVER" || gameState === "GOAL") {
        resetGame();
    }
}

// ===== updateGame() にパーティクル更新を追加 =====
function updateGame() {
    // ... 既存のコード ...

    // パーティクルを更新
    for (let i = particles.length - 1; i >= 0; i--) {
        particles[i].update();
        if (particles[i].isDead()) {
            particles.splice(i, 1);
        }
    }

    // ... 既存のコード ...
}

// ===== drawGame() にパーティクル描画を追加 =====
function drawGame() {
    push();
    translate(-cameraX, 0);
    drawClouds();
    drawGround();
    drawStartFlag(GAME_CONFIG.playerStartX, groundY);
    drawGoalFlag(GAME_CONFIG.goalDistance, groundY);
    drawObstacles();
    drawPlayer();

    // パーティクルを描画
    for (let particle of particles) {
        particle.draw();
    }

    pop();
    drawUI();
}

// ===== resetGame() にパーティクルリセットを追加 =====
function resetGame() {
    // ... 既存のコード ...
    particles = [];  // 追加
}
```

---

## 難易度調整

### 例9: 徐々に難しくなるシステム

**進むほど障害物の出現頻度が上がる**

```javascript
// ===== updateGame() の障害物生成を修正 =====
function updateGame() {
    updatePlayer();
    cameraX = player.worldX - width / 4;

    // 距離に応じて出現頻度を変える
    let difficulty = 1 + floor(distanceTraveled / 500) * 0.1;  // 500mごとに10%速く
    let spawnInterval = floor(OBSTACLE_CONFIG.spawnInterval / difficulty);

    if (frameCount % spawnInterval === 0) {
        createObstacle();
    }

    updateObstacles();

    if (checkCollision()) {
        gameState = "GAMEOVER";
    }

    if (player.worldX >= GAME_CONFIG.goalDistance) {
        gameState = "GOAL";
    }

    score++;
    distanceTraveled = player.worldX - GAME_CONFIG.playerStartX;
}
```

---

## 🎓 まとめ

これらの例を組み合わせることで、より複雑で面白いゲームを作ることができます。

**次のステップ**:
1. まずは1つの例を実装してみる
2. 動作を確認する
3. 他の例と組み合わせる
4. 自分だけのアイデアを追加する

**困ったら**:
- コンソール（F12）でエラーを確認
- CUSTOMIZE_GUIDE.md を読み返す
- AIアシスタントに具体的に質問する

---

**最終更新**: 2026-01-07
