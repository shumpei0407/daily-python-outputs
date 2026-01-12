// ゲーム状態
let gameState = "START";
let player;
let obstacles = [];
let clouds = [];
let score = 0;
let distanceTraveled = 0;
let groundY;
let cameraX = 0;
let keys = { left: false, right: false, jump: false };

function setup() {
    createCanvas(GAME_CONFIG.canvasWidth, GAME_CONFIG.canvasHeight);
    groundY = height - 100;

    player = {
        x: GAME_CONFIG.playerStartX,
        y: groundY - PLAYER_CONFIG.height,
        width: PLAYER_CONFIG.width,
        height: PLAYER_CONFIG.height,
        velocityY: 0,
        velocityX: 0,
        jumping: false,
        worldX: GAME_CONFIG.playerStartX
    };

    for (let i = 0; i < 5; i++) {
        clouds.push({
            x: random(width * 2),
            y: random(50, 150),
            size: random(60, 100)
        });
    }

    setupTouchControls();
    console.log("ゲーム起動完了！");
}

function draw() {
    background(BACKGROUND_CONFIG.skyColor.r, BACKGROUND_CONFIG.skyColor.g, BACKGROUND_CONFIG.skyColor.b);

    if (gameState === "START") {
        drawStartScreen();
    } else if (gameState === "PLAYING") {
        updateGame();
        drawGame();
    } else if (gameState === "GAMEOVER") {
        drawGame();
        drawGameOverScreen();
    } else if (gameState === "GOAL") {
        drawGame();
        drawGoalScreen();
    }
}

function drawStartScreen() {
    push();
    fill(UI_CONFIG.titleColor.r, UI_CONFIG.titleColor.g, UI_CONFIG.titleColor.b);
    textAlign(CENTER, CENTER);
    textSize(UI_CONFIG.titleSize);
    text("横スクロールゲーム", width / 2, height / 2 - 100);
    textSize(UI_CONFIG.messageSize);
    text("ゴールを目指そう！", width / 2, height / 2 - 40);
    text("障害物に当たらないように注意！", width / 2, height / 2);
    text("タップ、またはスペースキーでスタート", width / 2, height / 2 + 80);
    pop();
}

function drawGameOverScreen() {
    push();
    fill(0, 0, 0, 150);
    rect(0, 0, width, height);
    fill(255, 100, 100);
    textAlign(CENTER, CENTER);
    textSize(UI_CONFIG.titleSize);
    text("ゲームオーバー", width / 2, height / 2 - 60);
    fill(UI_CONFIG.messageColor.r, UI_CONFIG.messageColor.g, UI_CONFIG.messageColor.b);
    textSize(UI_CONFIG.messageSize);
    text("進んだ距離: " + floor(distanceTraveled) + "m", width / 2, height / 2);
    text("スコア: " + score, width / 2, height / 2 + 40);
    text("タップ、またはスペースキーでリスタート", width / 2, height / 2 + 100);
    pop();
}

function drawGoalScreen() {
    push();
    fill(255, 200, 50, 200);
    rect(0, 0, width, height);
    fill(255, 100, 0);
    textAlign(CENTER, CENTER);
    textSize(UI_CONFIG.titleSize + 10);
    text("🎉 ゴール！ 🎉", width / 2, height / 2 - 80);
    fill(UI_CONFIG.messageColor.r, UI_CONFIG.messageColor.g, UI_CONFIG.messageColor.b);
    textSize(UI_CONFIG.messageSize + 8);
    text("おめでとうございます！", width / 2, height / 2 - 20);
    text("スコア: " + score, width / 2, height / 2 + 20);
    text("タップ、またはスペースキーでリスタート", width / 2, height / 2 + 80);
    pop();
}

function updateGame() {
    updatePlayer();
    cameraX = player.worldX - width / 4;

    if (frameCount % OBSTACLE_CONFIG.spawnInterval === 0) {
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

function drawGame() {
    push();
    translate(-cameraX, 0);
    drawClouds();
    drawGround();
    drawStartFlag(GAME_CONFIG.playerStartX, groundY);
    drawGoalFlag(GAME_CONFIG.goalDistance, groundY);
    drawObstacles();
    drawPlayer();
    pop();
    drawUI();
}

function updatePlayer() {
    if (keys.left) {
        player.velocityX = -PLAYER_CONFIG.moveSpeed;
    } else if (keys.right) {
        player.velocityX = PLAYER_CONFIG.moveSpeed;
    } else {
        player.velocityX = 0;
    }

    player.velocityY += PLAYER_CONFIG.gravity;
    player.y += player.velocityY;
    player.worldX += player.velocityX;

    if (player.y >= groundY - player.height) {
        player.y = groundY - player.height;
        player.velocityY = 0;
        player.jumping = false;
    }

    if (player.worldX < 0) {
        player.worldX = 0;
    }
}

function drawPlayer() {
    push();
    fill(PLAYER_CONFIG.bodyColor.r, PLAYER_CONFIG.bodyColor.g, PLAYER_CONFIG.bodyColor.b);
    rect(player.worldX, player.y, player.width, player.height, 5);
    fill(PLAYER_CONFIG.eyeColor.r, PLAYER_CONFIG.eyeColor.g, PLAYER_CONFIG.eyeColor.b);
    ellipse(player.worldX + 12, player.y + 15, 10, 10);
    ellipse(player.worldX + 28, player.y + 15, 10, 10);
    fill(PLAYER_CONFIG.pupilColor.r, PLAYER_CONFIG.pupilColor.g, PLAYER_CONFIG.pupilColor.b);
    ellipse(player.worldX + 12, player.y + 15, 5, 5);
    ellipse(player.worldX + 28, player.y + 15, 5, 5);
    noFill();
    stroke(0);
    strokeWeight(2);
    arc(player.worldX + 20, player.y + 30, 15, 10, 0, PI);
    noStroke();
    pop();
}

function createObstacle() {
    let obstacleType = random() > 0.5 ? 'cactus' : 'rock';
    let config = obstacleType === 'cactus' ? OBSTACLE_CONFIG.cactusSize : OBSTACLE_CONFIG.rockSize;
    obstacles.push({
        x: cameraX + width + 100,
        y: groundY - config.height,
        width: config.width,
        height: config.height,
        type: obstacleType
    });
}

function updateObstacles() {
    for (let i = obstacles.length - 1; i >= 0; i--) {
        if (obstacles[i].x < cameraX - 200) {
            obstacles.splice(i, 1);
        }
    }
}

function drawObstacles() {
    for (let obstacle of obstacles) {
        if (obstacle.type === 'cactus') {
            fill(OBSTACLE_CONFIG.cactusColor.r, OBSTACLE_CONFIG.cactusColor.g, OBSTACLE_CONFIG.cactusColor.b);
            rect(obstacle.x + 10, obstacle.y, 10, obstacle.height, 5);
            rect(obstacle.x, obstacle.y + 10, 10, 15, 5);
            rect(obstacle.x + 20, obstacle.y + 15, 10, 10, 5);
        } else {
            fill(OBSTACLE_CONFIG.rockColor.r, OBSTACLE_CONFIG.rockColor.g, OBSTACLE_CONFIG.rockColor.b);
            triangle(
                obstacle.x + obstacle.width / 2, obstacle.y,
                obstacle.x, obstacle.y + obstacle.height,
                obstacle.x + obstacle.width, obstacle.y + obstacle.height
            );
        }
    }
}

function checkCollision() {
    for (let obstacle of obstacles) {
        if (player.worldX < obstacle.x + obstacle.width &&
            player.worldX + player.width > obstacle.x &&
            player.y < obstacle.y + obstacle.height &&
            player.y + player.height > obstacle.y) {
            return true;
        }
    }
    return false;
}

function drawClouds() {
    fill(BACKGROUND_CONFIG.cloudColor.r, BACKGROUND_CONFIG.cloudColor.g, BACKGROUND_CONFIG.cloudColor.b, BACKGROUND_CONFIG.cloudColor.a);
    noStroke();
    for (let cloud of clouds) {
        ellipse(cloud.x, cloud.y, cloud.size, cloud.size * 0.6);
        ellipse(cloud.x - cloud.size * 0.3, cloud.y + cloud.size * 0.1, cloud.size * 0.7, cloud.size * 0.5);
        ellipse(cloud.x + cloud.size * 0.3, cloud.y + cloud.size * 0.1, cloud.size * 0.7, cloud.size * 0.5);
    }
}

function drawGround() {
    fill(BACKGROUND_CONFIG.groundColor.r, BACKGROUND_CONFIG.groundColor.g, BACKGROUND_CONFIG.groundColor.b);
    rect(cameraX - 100, groundY, width + 200, height - groundY);
    fill(BACKGROUND_CONFIG.grassColor.r, BACKGROUND_CONFIG.grassColor.g, BACKGROUND_CONFIG.grassColor.b);
    rect(cameraX - 100, groundY - 10, width + 200, 10);
}

function drawStartFlag(x, y) {
    push();
    fill(START_GOAL_CONFIG.startFlag.poleColor.r, START_GOAL_CONFIG.startFlag.poleColor.g, START_GOAL_CONFIG.startFlag.poleColor.b);
    rect(x - 5, y - 100, 5, 100);
    fill(START_GOAL_CONFIG.startFlag.flagColor.r, START_GOAL_CONFIG.startFlag.flagColor.g, START_GOAL_CONFIG.startFlag.flagColor.b);
    triangle(x, y - 100, x, y - 60, x + 50, y - 80);
    fill(0);
    textAlign(CENTER);
    textSize(12);
    text(START_GOAL_CONFIG.startFlag.text, x + 25, y - 75);
    pop();
}

function drawGoalFlag(x, y) {
    push();
    fill(START_GOAL_CONFIG.goalFlag.poleColor.r, START_GOAL_CONFIG.goalFlag.poleColor.g, START_GOAL_CONFIG.goalFlag.poleColor.b);
    rect(x - 5, y - 100, 5, 100);
    fill(START_GOAL_CONFIG.goalFlag.flagColor.r, START_GOAL_CONFIG.goalFlag.flagColor.g, START_GOAL_CONFIG.goalFlag.flagColor.b);
    triangle(x, y - 100, x, y - 60, x + 50, y - 80);
    fill(0);
    textAlign(CENTER);
    textSize(12);
    text(START_GOAL_CONFIG.goalFlag.text, x + 25, y - 75);
    pop();
}

function drawUI() {
    push();
    textAlign(LEFT);
    fill(UI_CONFIG.scoreColor.r, UI_CONFIG.scoreColor.g, UI_CONFIG.scoreColor.b);
    textSize(UI_CONFIG.scoreSize);
    text("スコア: " + score, 20, 40);
    fill(UI_CONFIG.distanceColor.r, UI_CONFIG.distanceColor.g, UI_CONFIG.distanceColor.b);
    textSize(UI_CONFIG.distanceSize);
    text("距離: " + floor(distanceTraveled) + " / " + GAME_CONFIG.goalDistance + "m", 20, 70);
    let progress = distanceTraveled / GAME_CONFIG.goalDistance;
    fill(100);
    rect(20, 80, 200, 10);
    fill(100, 255, 100);
    rect(20, 80, 200 * progress, 10);
    pop();
}

function setupTouchControls() {
    let leftBtn = document.getElementById('leftBtn');
    let rightBtn = document.getElementById('rightBtn');
    let jumpBtn = document.getElementById('jumpBtn');

    leftBtn.addEventListener('touchstart', (e) => { e.preventDefault(); keys.left = true; });
    leftBtn.addEventListener('touchend', (e) => { e.preventDefault(); keys.left = false; });
    rightBtn.addEventListener('touchstart', (e) => { e.preventDefault(); keys.right = true; });
    rightBtn.addEventListener('touchend', (e) => { e.preventDefault(); keys.right = false; });
    jumpBtn.addEventListener('touchstart', (e) => { e.preventDefault(); handleJump(); });

    leftBtn.addEventListener('mousedown', () => keys.left = true);
    leftBtn.addEventListener('mouseup', () => keys.left = false);
    rightBtn.addEventListener('mousedown', () => keys.right = true);
    rightBtn.addEventListener('mouseup', () => keys.right = false);
    jumpBtn.addEventListener('mousedown', () => handleJump());
}

function handleJump() {
    if (gameState === "START") {
        gameState = "PLAYING";
    } else if (gameState === "PLAYING" && !player.jumping) {
        player.velocityY = PLAYER_CONFIG.jumpPower;
        player.jumping = true;
    } else if (gameState === "GAMEOVER" || gameState === "GOAL") {
        resetGame();
    }
}

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

function touchStarted() {
    if (touches.length > 0) {
        let touch = touches[0];
        if (touch.y < height - 120) {
            handleJump();
        }
    }
    return false;
}

function resetGame() {
    player.worldX = GAME_CONFIG.playerStartX;
    player.x = GAME_CONFIG.playerStartX;
    player.y = groundY - player.height;
    player.velocityY = 0;
    player.velocityX = 0;
    player.jumping = false;
    obstacles = [];
    score = 0;
    distanceTraveled = 0;
    cameraX = 0;
    gameState = "START";
}
