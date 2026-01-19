"""
ナマケモノの8ビット風ドット絵データ（SVGベース）
Game Boy風の4色制限を再現した可愛い各進化段階のスプライト
"""

# ============================================================
# Game Boy 4色パレット
# ============================================================
GAMEBOY_PALETTE = {
    "darkest": "#0f380f",   # 最も暗い緑
    "dark": "#306230",      # 暗い緑
    "light": "#8bac0f",     # 明るい緑
    "lightest": "#9bbc0f",  # 最も明るい緑
}

def create_sloth_svg(stage_id):
    """進化段階に応じた8ビット風ナマケモノSVGを生成"""

    D = GAMEBOY_PALETTE["darkest"]   # 最暗 - 輪郭、目
    K = GAMEBOY_PALETTE["dark"]      # 暗 - 体の影
    L = GAMEBOY_PALETTE["light"]     # 明 - 体
    W = GAMEBOY_PALETTE["lightest"]  # 最明 - ハイライト

    svg_sprites = {
        # ============================================================
        # 0: たまご - ヒビ入りの可愛い卵
        # ============================================================
        0: f'''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
            <!-- 卵本体 -->
            <rect x="20" y="12" width="24" height="4" fill="{W}"/>
            <rect x="16" y="16" width="32" height="4" fill="{W}"/>
            <rect x="12" y="20" width="40" height="4" fill="{W}"/>
            <rect x="12" y="24" width="40" height="4" fill="{L}"/>
            <rect x="12" y="28" width="40" height="4" fill="{L}"/>
            <rect x="12" y="32" width="40" height="4" fill="{L}"/>
            <rect x="12" y="36" width="40" height="4" fill="{L}"/>
            <rect x="16" y="40" width="32" height="4" fill="{K}"/>
            <rect x="20" y="44" width="24" height="4" fill="{K}"/>
            <rect x="24" y="48" width="16" height="4" fill="{D}"/>
            <!-- ヒビ -->
            <rect x="28" y="16" width="4" height="4" fill="{K}"/>
            <rect x="32" y="20" width="4" height="4" fill="{K}"/>
            <rect x="28" y="24" width="4" height="4" fill="{K}"/>
            <rect x="24" y="28" width="4" height="4" fill="{K}"/>
            <!-- ハイライト -->
            <rect x="20" y="20" width="4" height="4" fill="{W}"/>
            <rect x="24" y="20" width="4" height="4" fill="{W}"/>
        </svg>''',

        # ============================================================
        # 1: あかちゃん - 小さくて目がキラキラ
        # ============================================================
        1: f'''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
            <!-- 耳 -->
            <rect x="12" y="8" width="8" height="4" fill="{K}"/>
            <rect x="44" y="8" width="8" height="4" fill="{K}"/>
            <!-- 頭 -->
            <rect x="16" y="8" width="32" height="4" fill="{L}"/>
            <rect x="12" y="12" width="40" height="4" fill="{L}"/>
            <rect x="8" y="16" width="48" height="4" fill="{L}"/>
            <!-- 目のマスク -->
            <rect x="8" y="20" width="48" height="4" fill="{K}"/>
            <rect x="8" y="24" width="48" height="4" fill="{K}"/>
            <!-- 目 -->
            <rect x="16" y="20" width="8" height="8" fill="{D}"/>
            <rect x="40" y="20" width="8" height="8" fill="{D}"/>
            <!-- 目のハイライト -->
            <rect x="16" y="20" width="4" height="4" fill="{W}"/>
            <rect x="40" y="20" width="4" height="4" fill="{W}"/>
            <!-- 顔下部 -->
            <rect x="8" y="28" width="48" height="4" fill="{L}"/>
            <!-- 鼻 -->
            <rect x="28" y="28" width="8" height="4" fill="{D}"/>
            <!-- 口（笑顔）-->
            <rect x="24" y="32" width="4" height="4" fill="{D}"/>
            <rect x="36" y="32" width="4" height="4" fill="{D}"/>
            <!-- 体 -->
            <rect x="12" y="32" width="40" height="4" fill="{L}"/>
            <rect x="16" y="36" width="32" height="4" fill="{L}"/>
            <rect x="16" y="40" width="32" height="4" fill="{K}"/>
            <!-- 手 -->
            <rect x="8" y="36" width="8" height="8" fill="{K}"/>
            <rect x="48" y="36" width="8" height="8" fill="{K}"/>
            <!-- 足 -->
            <rect x="16" y="44" width="12" height="4" fill="{K}"/>
            <rect x="36" y="44" width="12" height="4" fill="{K}"/>
        </svg>''',

        # ============================================================
        # 2: こども - 成長して笑顔
        # ============================================================
        2: f'''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
            <!-- 耳 -->
            <rect x="8" y="4" width="8" height="4" fill="{K}"/>
            <rect x="48" y="4" width="8" height="4" fill="{K}"/>
            <!-- 頭 -->
            <rect x="16" y="4" width="32" height="4" fill="{L}"/>
            <rect x="12" y="8" width="40" height="4" fill="{L}"/>
            <rect x="8" y="12" width="48" height="4" fill="{L}"/>
            <!-- 目のマスク -->
            <rect x="8" y="16" width="48" height="4" fill="{K}"/>
            <rect x="8" y="20" width="48" height="4" fill="{K}"/>
            <!-- 目 -->
            <rect x="12" y="16" width="12" height="8" fill="{D}"/>
            <rect x="40" y="16" width="12" height="8" fill="{D}"/>
            <!-- 目のハイライト -->
            <rect x="12" y="16" width="4" height="4" fill="{W}"/>
            <rect x="16" y="20" width="4" height="4" fill="{W}"/>
            <rect x="40" y="16" width="4" height="4" fill="{W}"/>
            <rect x="44" y="20" width="4" height="4" fill="{W}"/>
            <!-- 顔下部 -->
            <rect x="8" y="24" width="48" height="4" fill="{L}"/>
            <!-- 鼻 -->
            <rect x="28" y="24" width="8" height="4" fill="{D}"/>
            <!-- 笑顔 -->
            <rect x="20" y="28" width="4" height="4" fill="{D}"/>
            <rect x="24" y="32" width="16" height="4" fill="{D}"/>
            <rect x="40" y="28" width="4" height="4" fill="{D}"/>
            <!-- 体 -->
            <rect x="8" y="28" width="12" height="4" fill="{L}"/>
            <rect x="44" y="28" width="12" height="4" fill="{L}"/>
            <rect x="12" y="32" width="40" height="4" fill="{L}"/>
            <rect x="16" y="36" width="32" height="4" fill="{L}"/>
            <rect x="16" y="40" width="32" height="4" fill="{K}"/>
            <!-- 手 -->
            <rect x="4" y="32" width="8" height="12" fill="{K}"/>
            <rect x="52" y="32" width="8" height="12" fill="{K}"/>
            <!-- 足 -->
            <rect x="16" y="44" width="12" height="4" fill="{K}"/>
            <rect x="36" y="44" width="12" height="4" fill="{K}"/>
        </svg>''',

        # ============================================================
        # 3: わかもの - 爪が生えてワイルド
        # ============================================================
        3: f'''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
            <!-- 耳 -->
            <rect x="8" y="4" width="8" height="4" fill="{K}"/>
            <rect x="48" y="4" width="8" height="4" fill="{K}"/>
            <!-- 頭 -->
            <rect x="16" y="4" width="32" height="4" fill="{L}"/>
            <rect x="12" y="8" width="40" height="4" fill="{L}"/>
            <rect x="8" y="12" width="48" height="4" fill="{L}"/>
            <!-- 目のマスク -->
            <rect x="8" y="16" width="48" height="4" fill="{K}"/>
            <rect x="8" y="20" width="48" height="4" fill="{K}"/>
            <!-- 目（キリッ）-->
            <rect x="12" y="18" width="12" height="6" fill="{D}"/>
            <rect x="40" y="18" width="12" height="6" fill="{D}"/>
            <rect x="12" y="16" width="4" height="4" fill="{W}"/>
            <rect x="44" y="16" width="4" height="4" fill="{W}"/>
            <!-- 顔 -->
            <rect x="8" y="24" width="48" height="4" fill="{L}"/>
            <rect x="28" y="24" width="8" height="4" fill="{D}"/>
            <!-- 口 -->
            <rect x="24" y="28" width="4" height="4" fill="{D}"/>
            <rect x="36" y="28" width="4" height="4" fill="{D}"/>
            <!-- 体 -->
            <rect x="8" y="28" width="16" height="4" fill="{L}"/>
            <rect x="40" y="28" width="16" height="4" fill="{L}"/>
            <rect x="12" y="32" width="40" height="4" fill="{L}"/>
            <rect x="16" y="36" width="32" height="4" fill="{L}"/>
            <rect x="16" y="40" width="32" height="4" fill="{K}"/>
            <!-- 手 -->
            <rect x="4" y="28" width="4" height="16" fill="{K}"/>
            <rect x="56" y="28" width="4" height="16" fill="{K}"/>
            <!-- 爪！ -->
            <rect x="0" y="28" width="4" height="4" fill="{D}"/>
            <rect x="0" y="32" width="4" height="4" fill="{D}"/>
            <rect x="0" y="36" width="4" height="4" fill="{D}"/>
            <rect x="60" y="28" width="4" height="4" fill="{D}"/>
            <rect x="60" y="32" width="4" height="4" fill="{D}"/>
            <rect x="60" y="36" width="4" height="4" fill="{D}"/>
            <!-- 足 -->
            <rect x="16" y="44" width="12" height="4" fill="{K}"/>
            <rect x="36" y="44" width="12" height="4" fill="{K}"/>
        </svg>''',

        # ============================================================
        # 4: おとな - 落ち着いた優しい顔
        # ============================================================
        4: f'''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
            <!-- 耳 -->
            <rect x="8" y="4" width="8" height="4" fill="{K}"/>
            <rect x="48" y="4" width="8" height="4" fill="{K}"/>
            <!-- 頭 -->
            <rect x="16" y="4" width="32" height="4" fill="{L}"/>
            <rect x="12" y="8" width="40" height="4" fill="{L}"/>
            <rect x="8" y="12" width="48" height="4" fill="{L}"/>
            <!-- 目のマスク -->
            <rect x="8" y="16" width="48" height="4" fill="{K}"/>
            <rect x="8" y="20" width="48" height="4" fill="{K}"/>
            <!-- 目（半目で穏やか）-->
            <rect x="12" y="18" width="12" height="4" fill="{D}"/>
            <rect x="40" y="18" width="12" height="4" fill="{D}"/>
            <rect x="12" y="18" width="4" height="4" fill="{W}"/>
            <rect x="48" y="18" width="4" height="4" fill="{W}"/>
            <!-- 顔 -->
            <rect x="8" y="24" width="48" height="4" fill="{L}"/>
            <rect x="28" y="24" width="8" height="4" fill="{D}"/>
            <!-- にっこり -->
            <rect x="20" y="28" width="4" height="4" fill="{D}"/>
            <rect x="24" y="28" width="4" height="4" fill="{L}"/>
            <rect x="28" y="28" width="8" height="4" fill="{L}"/>
            <rect x="36" y="28" width="4" height="4" fill="{L}"/>
            <rect x="40" y="28" width="4" height="4" fill="{D}"/>
            <!-- 体 -->
            <rect x="8" y="28" width="12" height="4" fill="{L}"/>
            <rect x="44" y="28" width="12" height="4" fill="{L}"/>
            <rect x="12" y="32" width="40" height="4" fill="{L}"/>
            <rect x="16" y="36" width="32" height="4" fill="{L}"/>
            <rect x="16" y="40" width="32" height="4" fill="{K}"/>
            <!-- 手と爪 -->
            <rect x="4" y="28" width="4" height="16" fill="{K}"/>
            <rect x="56" y="28" width="4" height="16" fill="{K}"/>
            <rect x="0" y="28" width="4" height="4" fill="{D}"/>
            <rect x="0" y="32" width="4" height="4" fill="{D}"/>
            <rect x="0" y="36" width="4" height="4" fill="{D}"/>
            <rect x="60" y="28" width="4" height="4" fill="{D}"/>
            <rect x="60" y="32" width="4" height="4" fill="{D}"/>
            <rect x="60" y="36" width="4" height="4" fill="{D}"/>
            <!-- 足 -->
            <rect x="16" y="44" width="12" height="4" fill="{K}"/>
            <rect x="36" y="44" width="12" height="4" fill="{K}"/>
        </svg>''',

        # ============================================================
        # 5: ベテラン - ヒゲと星バッジ
        # ============================================================
        5: f'''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
            <!-- 耳 -->
            <rect x="8" y="4" width="8" height="4" fill="{K}"/>
            <rect x="48" y="4" width="8" height="4" fill="{K}"/>
            <!-- 頭 -->
            <rect x="16" y="4" width="32" height="4" fill="{L}"/>
            <rect x="12" y="8" width="40" height="4" fill="{L}"/>
            <rect x="8" y="12" width="48" height="4" fill="{L}"/>
            <!-- 目のマスク -->
            <rect x="8" y="16" width="48" height="4" fill="{K}"/>
            <rect x="8" y="20" width="48" height="4" fill="{K}"/>
            <!-- 目 -->
            <rect x="12" y="18" width="12" height="4" fill="{D}"/>
            <rect x="40" y="18" width="12" height="4" fill="{D}"/>
            <rect x="12" y="18" width="4" height="4" fill="{W}"/>
            <rect x="48" y="18" width="4" height="4" fill="{W}"/>
            <!-- 顔 -->
            <rect x="8" y="24" width="48" height="4" fill="{L}"/>
            <rect x="28" y="24" width="8" height="4" fill="{D}"/>
            <!-- ヒゲ -->
            <rect x="4" y="24" width="4" height="4" fill="{W}"/>
            <rect x="0" y="28" width="4" height="4" fill="{W}"/>
            <rect x="56" y="24" width="4" height="4" fill="{W}"/>
            <rect x="60" y="28" width="4" height="4" fill="{W}"/>
            <!-- 口 -->
            <rect x="24" y="28" width="4" height="4" fill="{D}"/>
            <rect x="36" y="28" width="4" height="4" fill="{D}"/>
            <!-- 体 -->
            <rect x="8" y="28" width="16" height="4" fill="{L}"/>
            <rect x="40" y="28" width="16" height="4" fill="{L}"/>
            <rect x="12" y="32" width="40" height="4" fill="{L}"/>
            <rect x="16" y="36" width="32" height="4" fill="{L}"/>
            <rect x="16" y="40" width="32" height="4" fill="{K}"/>
            <!-- 手と爪 -->
            <rect x="4" y="32" width="4" height="12" fill="{K}"/>
            <rect x="56" y="32" width="4" height="12" fill="{K}"/>
            <rect x="0" y="32" width="4" height="4" fill="{D}"/>
            <rect x="0" y="36" width="4" height="4" fill="{D}"/>
            <rect x="0" y="40" width="4" height="4" fill="{D}"/>
            <rect x="60" y="32" width="4" height="4" fill="{D}"/>
            <rect x="60" y="36" width="4" height="4" fill="{D}"/>
            <rect x="60" y="40" width="4" height="4" fill="{D}"/>
            <!-- 足 -->
            <rect x="16" y="44" width="12" height="4" fill="{K}"/>
            <rect x="36" y="44" width="12" height="4" fill="{K}"/>
            <!-- 星バッジ -->
            <rect x="48" y="40" width="4" height="4" fill="{W}"/>
            <rect x="44" y="44" width="4" height="4" fill="{W}"/>
            <rect x="48" y="44" width="4" height="4" fill="{W}"/>
            <rect x="52" y="44" width="4" height="4" fill="{W}"/>
            <rect x="48" y="48" width="4" height="4" fill="{W}"/>
        </svg>''',

        # ============================================================
        # 6: マスター - 帽子付き
        # ============================================================
        6: f'''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
            <!-- 帽子 -->
            <rect x="24" y="0" width="16" height="4" fill="{D}"/>
            <rect x="20" y="4" width="24" height="4" fill="{D}"/>
            <rect x="16" y="8" width="32" height="4" fill="{K}"/>
            <!-- 耳 -->
            <rect x="8" y="8" width="8" height="4" fill="{K}"/>
            <rect x="48" y="8" width="8" height="4" fill="{K}"/>
            <!-- 頭 -->
            <rect x="16" y="8" width="32" height="4" fill="{L}"/>
            <rect x="12" y="12" width="40" height="4" fill="{L}"/>
            <!-- 目のマスク -->
            <rect x="8" y="16" width="48" height="4" fill="{K}"/>
            <rect x="8" y="20" width="48" height="4" fill="{K}"/>
            <!-- 眉毛 -->
            <rect x="12" y="16" width="8" height="4" fill="{D}"/>
            <rect x="44" y="16" width="8" height="4" fill="{D}"/>
            <!-- 目 -->
            <rect x="12" y="20" width="8" height="4" fill="{D}"/>
            <rect x="44" y="20" width="8" height="4" fill="{D}"/>
            <rect x="12" y="20" width="4" height="4" fill="{W}"/>
            <rect x="48" y="20" width="4" height="4" fill="{W}"/>
            <!-- 顔 -->
            <rect x="8" y="24" width="48" height="4" fill="{L}"/>
            <rect x="28" y="24" width="8" height="4" fill="{D}"/>
            <!-- 口 -->
            <rect x="24" y="28" width="4" height="4" fill="{D}"/>
            <rect x="36" y="28" width="4" height="4" fill="{D}"/>
            <!-- 体 -->
            <rect x="8" y="28" width="16" height="4" fill="{L}"/>
            <rect x="40" y="28" width="16" height="4" fill="{L}"/>
            <rect x="12" y="32" width="40" height="4" fill="{L}"/>
            <rect x="16" y="36" width="32" height="4" fill="{L}"/>
            <rect x="16" y="40" width="32" height="4" fill="{K}"/>
            <!-- 手と爪 -->
            <rect x="4" y="28" width="4" height="16" fill="{K}"/>
            <rect x="56" y="28" width="4" height="16" fill="{K}"/>
            <rect x="0" y="28" width="4" height="4" fill="{D}"/>
            <rect x="0" y="32" width="4" height="4" fill="{D}"/>
            <rect x="0" y="36" width="4" height="4" fill="{D}"/>
            <rect x="60" y="28" width="4" height="4" fill="{D}"/>
            <rect x="60" y="32" width="4" height="4" fill="{D}"/>
            <rect x="60" y="36" width="4" height="4" fill="{D}"/>
            <!-- 足 -->
            <rect x="16" y="44" width="12" height="4" fill="{K}"/>
            <rect x="36" y="44" width="12" height="4" fill="{K}"/>
            <!-- オーラ -->
            <rect x="0" y="12" width="4" height="4" fill="{W}"/>
            <rect x="60" y="12" width="4" height="4" fill="{W}"/>
        </svg>''',

        # ============================================================
        # 7: レジェンド - 王冠！
        # ============================================================
        7: f'''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
            <!-- 王冠 -->
            <rect x="16" y="0" width="4" height="8" fill="{W}"/>
            <rect x="28" y="0" width="8" height="4" fill="{W}"/>
            <rect x="44" y="0" width="4" height="8" fill="{W}"/>
            <rect x="20" y="4" width="24" height="4" fill="{W}"/>
            <rect x="16" y="8" width="32" height="4" fill="{W}"/>
            <!-- 宝石 -->
            <rect x="28" y="8" width="8" height="4" fill="{D}"/>
            <!-- 耳 -->
            <rect x="8" y="8" width="8" height="4" fill="{K}"/>
            <rect x="48" y="8" width="8" height="4" fill="{K}"/>
            <!-- 頭 -->
            <rect x="12" y="12" width="40" height="4" fill="{L}"/>
            <!-- 目のマスク -->
            <rect x="8" y="16" width="48" height="4" fill="{K}"/>
            <rect x="8" y="20" width="48" height="4" fill="{K}"/>
            <!-- 輝く目 -->
            <rect x="12" y="16" width="12" height="8" fill="{W}"/>
            <rect x="40" y="16" width="12" height="8" fill="{W}"/>
            <rect x="16" y="20" width="4" height="4" fill="{D}"/>
            <rect x="44" y="20" width="4" height="4" fill="{D}"/>
            <!-- 顔 -->
            <rect x="8" y="24" width="48" height="4" fill="{L}"/>
            <rect x="28" y="24" width="8" height="4" fill="{D}"/>
            <!-- 口 -->
            <rect x="24" y="28" width="4" height="4" fill="{D}"/>
            <rect x="36" y="28" width="4" height="4" fill="{D}"/>
            <!-- 体 -->
            <rect x="8" y="28" width="16" height="4" fill="{L}"/>
            <rect x="40" y="28" width="16" height="4" fill="{L}"/>
            <rect x="12" y="32" width="40" height="4" fill="{L}"/>
            <rect x="16" y="36" width="32" height="4" fill="{L}"/>
            <rect x="16" y="40" width="32" height="4" fill="{K}"/>
            <!-- 手と金の爪 -->
            <rect x="4" y="28" width="4" height="16" fill="{K}"/>
            <rect x="56" y="28" width="4" height="16" fill="{K}"/>
            <rect x="0" y="28" width="4" height="4" fill="{W}"/>
            <rect x="0" y="32" width="4" height="4" fill="{W}"/>
            <rect x="0" y="36" width="4" height="4" fill="{W}"/>
            <rect x="60" y="28" width="4" height="4" fill="{W}"/>
            <rect x="60" y="32" width="4" height="4" fill="{W}"/>
            <rect x="60" y="36" width="4" height="4" fill="{W}"/>
            <!-- 足 -->
            <rect x="16" y="44" width="12" height="4" fill="{K}"/>
            <rect x="36" y="44" width="12" height="4" fill="{K}"/>
            <!-- オーラ -->
            <rect x="0" y="8" width="4" height="4" fill="{W}"/>
            <rect x="60" y="8" width="4" height="4" fill="{W}"/>
            <rect x="0" y="48" width="4" height="4" fill="{W}"/>
            <rect x="60" y="48" width="4" height="4" fill="{W}"/>
        </svg>''',

        # ============================================================
        # 8: しんわ - 神秘的な銀色、光輪
        # ============================================================
        8: f'''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
            <!-- 光輪 -->
            <rect x="20" y="0" width="24" height="4" fill="{W}"/>
            <rect x="16" y="4" width="4" height="4" fill="{W}"/>
            <rect x="44" y="4" width="4" height="4" fill="{W}"/>
            <rect x="20" y="8" width="24" height="4" fill="{W}"/>
            <!-- 星々 -->
            <rect x="4" y="4" width="4" height="4" fill="{W}"/>
            <rect x="56" y="8" width="4" height="4" fill="{W}"/>
            <rect x="0" y="24" width="4" height="4" fill="{W}"/>
            <rect x="60" y="20" width="4" height="4" fill="{W}"/>
            <!-- 耳 -->
            <rect x="8" y="12" width="8" height="4" fill="{L}"/>
            <rect x="48" y="12" width="8" height="4" fill="{L}"/>
            <!-- 頭（銀色=明るい）-->
            <rect x="16" y="12" width="32" height="4" fill="{W}"/>
            <rect x="12" y="16" width="40" height="4" fill="{W}"/>
            <!-- 目のマスク -->
            <rect x="8" y="20" width="48" height="4" fill="{L}"/>
            <rect x="8" y="24" width="48" height="4" fill="{L}"/>
            <!-- 星の目 -->
            <rect x="16" y="20" width="4" height="4" fill="{W}"/>
            <rect x="12" y="24" width="4" height="4" fill="{W}"/>
            <rect x="20" y="24" width="4" height="4" fill="{W}"/>
            <rect x="44" y="20" width="4" height="4" fill="{W}"/>
            <rect x="40" y="24" width="4" height="4" fill="{W}"/>
            <rect x="48" y="24" width="4" height="4" fill="{W}"/>
            <!-- 顔 -->
            <rect x="8" y="28" width="48" height="4" fill="{W}"/>
            <rect x="28" y="28" width="8" height="4" fill="{L}"/>
            <!-- 口 -->
            <rect x="24" y="32" width="4" height="4" fill="{L}"/>
            <rect x="36" y="32" width="4" height="4" fill="{L}"/>
            <!-- 体 -->
            <rect x="8" y="32" width="16" height="4" fill="{W}"/>
            <rect x="40" y="32" width="16" height="4" fill="{W}"/>
            <rect x="12" y="36" width="40" height="4" fill="{W}"/>
            <rect x="16" y="40" width="32" height="4" fill="{W}"/>
            <rect x="16" y="44" width="32" height="4" fill="{L}"/>
            <!-- 手と銀の爪 -->
            <rect x="4" y="32" width="4" height="16" fill="{L}"/>
            <rect x="56" y="32" width="4" height="16" fill="{L}"/>
            <rect x="0" y="32" width="4" height="4" fill="{W}"/>
            <rect x="0" y="36" width="4" height="4" fill="{W}"/>
            <rect x="0" y="40" width="4" height="4" fill="{W}"/>
            <rect x="60" y="32" width="4" height="4" fill="{W}"/>
            <rect x="60" y="36" width="4" height="4" fill="{W}"/>
            <rect x="60" y="40" width="4" height="4" fill="{W}"/>
            <!-- 足 -->
            <rect x="16" y="48" width="12" height="4" fill="{L}"/>
            <rect x="36" y="48" width="12" height="4" fill="{L}"/>
        </svg>''',

        # ============================================================
        # 9: かみ - 究極形態！羽と二重光輪
        # ============================================================
        9: f'''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
            <!-- 二重光輪 -->
            <rect x="16" y="0" width="32" height="4" fill="{W}"/>
            <rect x="12" y="4" width="4" height="4" fill="{W}"/>
            <rect x="48" y="4" width="4" height="4" fill="{W}"/>
            <rect x="16" y="8" width="32" height="4" fill="{W}"/>
            <!-- 輝く粒子 -->
            <rect x="0" y="0" width="4" height="4" fill="{W}"/>
            <rect x="60" y="4" width="4" height="4" fill="{W}"/>
            <rect x="4" y="20" width="4" height="4" fill="{W}"/>
            <rect x="56" y="16" width="4" height="4" fill="{W}"/>
            <rect x="0" y="40" width="4" height="4" fill="{W}"/>
            <rect x="60" y="44" width="4" height="4" fill="{W}"/>
            <!-- 羽（左）-->
            <rect x="0" y="24" width="4" height="4" fill="{W}"/>
            <rect x="0" y="28" width="8" height="4" fill="{W}"/>
            <rect x="0" y="32" width="4" height="4" fill="{L}"/>
            <rect x="4" y="24" width="4" height="4" fill="{L}"/>
            <!-- 羽（右）-->
            <rect x="60" y="24" width="4" height="4" fill="{W}"/>
            <rect x="56" y="28" width="8" height="4" fill="{W}"/>
            <rect x="60" y="32" width="4" height="4" fill="{L}"/>
            <rect x="56" y="24" width="4" height="4" fill="{L}"/>
            <!-- 耳 -->
            <rect x="8" y="12" width="8" height="4" fill="{L}"/>
            <rect x="48" y="12" width="8" height="4" fill="{L}"/>
            <!-- 頭（輝く）-->
            <rect x="16" y="12" width="32" height="4" fill="{W}"/>
            <rect x="12" y="16" width="40" height="4" fill="{W}"/>
            <!-- 目のマスク -->
            <rect x="12" y="20" width="40" height="4" fill="{L}"/>
            <rect x="12" y="24" width="40" height="4" fill="{L}"/>
            <!-- 宇宙の目 -->
            <rect x="16" y="20" width="8" height="8" fill="{D}"/>
            <rect x="40" y="20" width="8" height="8" fill="{D}"/>
            <rect x="16" y="20" width="4" height="4" fill="{K}"/>
            <rect x="20" y="24" width="4" height="4" fill="{L}"/>
            <rect x="44" y="20" width="4" height="4" fill="{K}"/>
            <rect x="40" y="24" width="4" height="4" fill="{L}"/>
            <!-- 顔 -->
            <rect x="12" y="28" width="40" height="4" fill="{W}"/>
            <rect x="28" y="28" width="8" height="4" fill="{L}"/>
            <!-- 穏やかな微笑み -->
            <rect x="20" y="32" width="4" height="4" fill="{L}"/>
            <rect x="24" y="32" width="16" height="4" fill="{W}"/>
            <rect x="40" y="32" width="4" height="4" fill="{L}"/>
            <!-- 体 -->
            <rect x="16" y="36" width="32" height="4" fill="{W}"/>
            <rect x="16" y="40" width="32" height="4" fill="{W}"/>
            <rect x="20" y="44" width="24" height="4" fill="{L}"/>
            <!-- 足 -->
            <rect x="20" y="48" width="8" height="4" fill="{W}"/>
            <rect x="36" y="48" width="8" height="4" fill="{W}"/>
        </svg>''',

        # ============================================================
        # 死亡時 - 悲しいバツ目と天使の輪
        # ============================================================
        "dead": f'''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
            <!-- 天使の輪 -->
            <rect x="20" y="0" width="24" height="4" fill="{L}"/>
            <rect x="16" y="4" width="4" height="4" fill="{L}"/>
            <rect x="44" y="4" width="4" height="4" fill="{L}"/>
            <rect x="20" y="8" width="24" height="4" fill="{L}"/>
            <!-- 耳 -->
            <rect x="8" y="8" width="8" height="4" fill="{D}"/>
            <rect x="48" y="8" width="8" height="4" fill="{D}"/>
            <!-- 頭 -->
            <rect x="16" y="8" width="32" height="4" fill="{K}"/>
            <rect x="12" y="12" width="40" height="4" fill="{K}"/>
            <rect x="8" y="16" width="48" height="4" fill="{K}"/>
            <!-- 目のマスク -->
            <rect x="8" y="20" width="48" height="4" fill="{D}"/>
            <rect x="8" y="24" width="48" height="4" fill="{D}"/>
            <!-- バツ目 -->
            <rect x="12" y="20" width="4" height="4" fill="{L}"/>
            <rect x="20" y="20" width="4" height="4" fill="{L}"/>
            <rect x="16" y="24" width="4" height="4" fill="{L}"/>
            <rect x="12" y="28" width="4" height="4" fill="{L}"/>
            <rect x="20" y="28" width="4" height="4" fill="{L}"/>
            <rect x="40" y="20" width="4" height="4" fill="{L}"/>
            <rect x="48" y="20" width="4" height="4" fill="{L}"/>
            <rect x="44" y="24" width="4" height="4" fill="{L}"/>
            <rect x="40" y="28" width="4" height="4" fill="{L}"/>
            <rect x="48" y="28" width="4" height="4" fill="{L}"/>
            <!-- 顔 -->
            <rect x="8" y="28" width="48" height="4" fill="{K}"/>
            <rect x="28" y="28" width="8" height="4" fill="{D}"/>
            <!-- 悲しい口 -->
            <rect x="24" y="32" width="16" height="4" fill="{D}"/>
            <rect x="20" y="36" width="4" height="4" fill="{D}"/>
            <rect x="40" y="36" width="4" height="4" fill="{D}"/>
            <!-- 体 -->
            <rect x="8" y="32" width="16" height="4" fill="{K}"/>
            <rect x="40" y="32" width="16" height="4" fill="{K}"/>
            <rect x="12" y="36" width="40" height="4" fill="{K}"/>
            <rect x="16" y="40" width="32" height="4" fill="{K}"/>
            <rect x="16" y="44" width="32" height="4" fill="{D}"/>
            <!-- だらんとした手 -->
            <rect x="4" y="40" width="4" height="8" fill="{D}"/>
            <rect x="0" y="44" width="4" height="4" fill="{D}"/>
            <rect x="56" y="40" width="4" height="8" fill="{D}"/>
            <rect x="60" y="44" width="4" height="4" fill="{D}"/>
            <!-- 足 -->
            <rect x="16" y="48" width="12" height="4" fill="{D}"/>
            <rect x="36" y="48" width="12" height="4" fill="{D}"/>
        </svg>'''
    }

    return svg_sprites.get(stage_id, svg_sprites[0])


def get_all_sprites():
    """全スプライトを取得"""
    return {i: create_sloth_svg(i) for i in range(10)}


# テスト用
if __name__ == "__main__":
    print("Game Boy Style Sloth Sprites")
    print("=" * 40)
    for i in range(10):
        svg = create_sloth_svg(i)
        print(f"Stage {i}: {len(svg)} characters")
    print(f"Dead: {len(create_sloth_svg('dead'))} characters")
