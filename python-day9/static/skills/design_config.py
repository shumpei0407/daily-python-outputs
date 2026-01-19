"""
デザインスキル設定ファイル
テーマやカラーパレットを一元管理し、簡単に変更できるようにする
"""

# ============================================================
# テーマ設定 - ここを変更するだけでデザインを切り替えられます
# ============================================================
CURRENT_THEME = "gameboy"  # "gameboy", "gameboy_pocket", "gameboy_color"

# ============================================================
# Game Boy オリジナル (クラシックな緑モノクロ)
# ============================================================
THEME_GAMEBOY = {
    "name": "Game Boy Classic",
    "description": "クラシックなゲームボーイ風緑モノクロ",

    # 基本4色パレット (Game Boyの制限を再現)
    "palette": {
        "darkest": "#0f380f",    # 最も暗い緑
        "dark": "#306230",       # 暗い緑
        "light": "#8bac0f",      # 明るい緑
        "lightest": "#9bbc0f",   # 最も明るい緑
    },

    # UI要素用カラー
    "colors": {
        "background": "#9bbc0f",     # 背景 (最も明るい)
        "container_bg": "#8bac0f",   # コンテナ背景
        "panel_bg": "#306230",       # パネル背景
        "border": "#0f380f",         # ボーダー
        "text_primary": "#0f380f",   # メインテキスト
        "text_secondary": "#306230", # サブテキスト
        "accent": "#0f380f",         # アクセント
        "danger": "#0f380f",         # 危険表示
        "success": "#0f380f",        # 成功表示
    },

    # スプライト用カラー
    "sprite_colors": {
        "body": "#306230",
        "face": "#8bac0f",
        "eye": "#0f380f",
        "nose": "#0f380f",
        "claw": "#0f380f",
        "egg": "#9bbc0f",
        "egg_spot": "#8bac0f",
        "highlight": "#9bbc0f",
        "shadow": "#0f380f",
    },

    # フォント設定
    "fonts": {
        "primary": "'Press Start 2P', 'DotGothic16', monospace",
        "size_title": "12px",
        "size_normal": "8px",
        "size_small": "6px",
    },

    # UI設定
    "ui": {
        "border_width": "4px",
        "border_radius": "0px",  # Game Boyはピクセルパーフェクト
        "pixel_scale": "2",
    }
}

# ============================================================
# Game Boy Pocket (よりクリアな緑)
# ============================================================
THEME_GAMEBOY_POCKET = {
    "name": "Game Boy Pocket",
    "description": "ゲームボーイポケット風のクリアな表示",

    "palette": {
        "darkest": "#1a1a1a",
        "dark": "#4a4a4a",
        "light": "#8a8a8a",
        "lightest": "#c5c5c5",
    },

    "colors": {
        "background": "#c5c5c5",
        "container_bg": "#8a8a8a",
        "panel_bg": "#4a4a4a",
        "border": "#1a1a1a",
        "text_primary": "#1a1a1a",
        "text_secondary": "#4a4a4a",
        "accent": "#1a1a1a",
        "danger": "#1a1a1a",
        "success": "#1a1a1a",
    },

    "sprite_colors": {
        "body": "#4a4a4a",
        "face": "#8a8a8a",
        "eye": "#1a1a1a",
        "nose": "#1a1a1a",
        "claw": "#1a1a1a",
        "egg": "#c5c5c5",
        "egg_spot": "#8a8a8a",
        "highlight": "#c5c5c5",
        "shadow": "#1a1a1a",
    },

    "fonts": {
        "primary": "'Press Start 2P', 'DotGothic16', monospace",
        "size_title": "12px",
        "size_normal": "8px",
        "size_small": "6px",
    },

    "ui": {
        "border_width": "4px",
        "border_radius": "0px",
        "pixel_scale": "2",
    }
}

# ============================================================
# Game Boy Color (カラフルだがレトロ)
# ============================================================
THEME_GAMEBOY_COLOR = {
    "name": "Game Boy Color",
    "description": "ゲームボーイカラー風の限定カラー",

    "palette": {
        "darkest": "#1f1f3d",
        "dark": "#3d3d7a",
        "light": "#7a7ab8",
        "lightest": "#b8b8f5",
    },

    "colors": {
        "background": "#1f1f3d",
        "container_bg": "#3d3d7a",
        "panel_bg": "#1f1f3d",
        "border": "#b8b8f5",
        "text_primary": "#b8b8f5",
        "text_secondary": "#7a7ab8",
        "accent": "#f5d033",
        "danger": "#f55033",
        "success": "#33f550",
    },

    "sprite_colors": {
        "body": "#7a5233",
        "face": "#d4a574",
        "eye": "#1f1f3d",
        "nose": "#5c3d1f",
        "claw": "#3d3d3d",
        "egg": "#f5f5dc",
        "egg_spot": "#d4d4a5",
        "highlight": "#f5d033",
        "shadow": "#1f1f3d",
    },

    "fonts": {
        "primary": "'Press Start 2P', 'DotGothic16', monospace",
        "size_title": "12px",
        "size_normal": "8px",
        "size_small": "6px",
    },

    "ui": {
        "border_width": "4px",
        "border_radius": "0px",
        "pixel_scale": "2",
    }
}

# ============================================================
# テーマ取得関数
# ============================================================
THEMES = {
    "gameboy": THEME_GAMEBOY,
    "gameboy_pocket": THEME_GAMEBOY_POCKET,
    "gameboy_color": THEME_GAMEBOY_COLOR,
}

def get_current_theme():
    """現在のテーマを取得"""
    return THEMES.get(CURRENT_THEME, THEME_GAMEBOY)

def get_theme(theme_name):
    """指定したテーマを取得"""
    return THEMES.get(theme_name, THEME_GAMEBOY)

def get_all_themes():
    """全テーマのリストを取得"""
    return {name: theme["name"] for name, theme in THEMES.items()}

def get_css_variables(theme=None):
    """テーマからCSS変数を生成"""
    if theme is None:
        theme = get_current_theme()

    css_vars = []

    # カラー変数
    for key, value in theme["colors"].items():
        css_vars.append(f"--color-{key.replace('_', '-')}: {value};")

    # パレット変数
    for key, value in theme["palette"].items():
        css_vars.append(f"--palette-{key}: {value};")

    # フォント変数
    for key, value in theme["fonts"].items():
        css_vars.append(f"--font-{key.replace('_', '-')}: {value};")

    # UI変数
    for key, value in theme["ui"].items():
        css_vars.append(f"--ui-{key.replace('_', '-')}: {value};")

    return "\n    ".join(css_vars)
