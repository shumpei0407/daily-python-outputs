// ==========================================
// ゲーム設定ファイル - 素材の置き換えはここで！
// ==========================================

const PLAYER_CONFIG = {
    bodyColor: { r: 255, g: 100, b: 100 },
    width: 40,
    height: 50,
    eyeColor: { r: 255, g: 255, b: 255 },
    pupilColor: { r: 0, g: 0, b: 0 },
    jumpPower: -16,
    moveSpeed: 5,
    gravity: 0.8
};

const OBSTACLE_CONFIG = {
    cactusColor: { r: 34, g: 139, b: 34 },
    cactusSize: { width: 30, height: 40 },
    rockColor: { r: 128, g: 128, b: 128 },
    rockSize: { width: 40, height: 30 },
    spawnInterval: 90
};

const BACKGROUND_CONFIG = {
    skyColor: { r: 135, g: 206, b: 235 },
    cloudColor: { r: 255, g: 255, b: 255, a: 200 },
    cloudSpeed: 0.5,
    groundColor: { r: 101, g: 67, b: 33 },
    grassColor: { r: 34, g: 139, b: 34 }
};

const GAME_CONFIG = {
    canvasWidth: 800,
    canvasHeight: 600,
    scrollSpeed: 5,
    goalDistance: 3000,
    playerStartX: 100
};

const START_GOAL_CONFIG = {
    startFlag: {
        poleColor: { r: 100, g: 50, b: 0 },
        flagColor: { r: 100, g: 200, b: 100 },
        text: "スタート"
    },
    goalFlag: {
        poleColor: { r: 100, g: 50, b: 0 },
        flagColor: { r: 255, g: 200, b: 50 },
        text: "ゴール！"
    }
};

const UI_CONFIG = {
    scoreColor: { r: 255, g: 255, b: 255 },
    scoreSize: 32,
    distanceColor: { r: 255, g: 255, b: 255 },
    distanceSize: 24,
    titleColor: { r: 255, g: 255, b: 255 },
    titleSize: 48,
    messageColor: { r: 255, g: 255, b: 255 },
    messageSize: 24
};
