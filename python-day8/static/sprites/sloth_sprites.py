"""
ナマケモノのドット絵データ（SVGベース）
各進化段階のスプライトを定義
"""

# 色の定義
COLORS = {
    "body": "#8B7355",      # 茶色（体）
    "face": "#D4B896",     # ベージュ（顔）
    "eye": "#333333",      # 黒（目）
    "nose": "#5C4033",     # 濃い茶色（鼻）
    "claw": "#4A4A4A",     # グレー（爪）
    "egg": "#F5F5DC",      # ベージュ（卵）
    "egg_spot": "#DDD8C4", # 卵の模様
    "baby_body": "#A0896C",
    "gold": "#FFD700",     # 金色
    "silver": "#C0C0C0",   # 銀色
    "rainbow": ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7", "#DDA0DD"],
}

def create_pixel_rect(x, y, color, size=8):
    """ピクセル四角を生成"""
    return f'<rect x="{x}" y="{y}" width="{size}" height="{size}" fill="{color}"/>'

def create_sloth_svg(stage_id):
    """進化段階に応じたナマケモノSVGを生成"""

    svg_sprites = {
        # 0: たまご
        0: '''<svg viewBox="0 0 128 128" xmlns="http://www.w3.org/2000/svg">
            <ellipse cx="64" cy="70" rx="35" ry="45" fill="#F5F5DC"/>
            <ellipse cx="50" cy="55" rx="8" ry="10" fill="#DDD8C4"/>
            <ellipse cx="75" cy="80" rx="6" ry="8" fill="#DDD8C4"/>
            <ellipse cx="55" cy="90" rx="5" ry="6" fill="#DDD8C4"/>
            <!-- 揺れるアニメーション用のクラック -->
            <path d="M64 35 L60 45 L68 50 L62 58" stroke="#AAA" stroke-width="2" fill="none"/>
        </svg>''',

        # 1: あかちゃん
        1: '''<svg viewBox="0 0 128 128" xmlns="http://www.w3.org/2000/svg">
            <!-- 体 -->
            <ellipse cx="64" cy="80" rx="30" ry="25" fill="#A0896C"/>
            <!-- 顔 -->
            <circle cx="64" cy="55" r="25" fill="#D4B896"/>
            <!-- 目のマスク -->
            <ellipse cx="64" cy="52" rx="20" ry="12" fill="#5C4033"/>
            <!-- 目 -->
            <circle cx="55" cy="52" r="5" fill="#333"/>
            <circle cx="73" cy="52" r="5" fill="#333"/>
            <circle cx="56" cy="51" r="2" fill="#FFF"/>
            <circle cx="74" cy="51" r="2" fill="#FFF"/>
            <!-- 鼻 -->
            <ellipse cx="64" cy="62" rx="4" ry="3" fill="#5C4033"/>
            <!-- 小さな手 -->
            <ellipse cx="40" cy="75" rx="8" ry="6" fill="#A0896C"/>
            <ellipse cx="88" cy="75" rx="8" ry="6" fill="#A0896C"/>
        </svg>''',

        # 2: こども
        2: '''<svg viewBox="0 0 128 128" xmlns="http://www.w3.org/2000/svg">
            <!-- 体 -->
            <ellipse cx="64" cy="85" rx="32" ry="28" fill="#8B7355"/>
            <!-- 顔 -->
            <circle cx="64" cy="50" r="28" fill="#D4B896"/>
            <!-- 目のマスク -->
            <ellipse cx="64" cy="47" rx="22" ry="14" fill="#5C4033"/>
            <!-- 目（少し大きめ）-->
            <circle cx="52" cy="47" r="6" fill="#333"/>
            <circle cx="76" cy="47" r="6" fill="#333"/>
            <circle cx="53" cy="45" r="2.5" fill="#FFF"/>
            <circle cx="77" cy="45" r="2.5" fill="#FFF"/>
            <!-- 鼻 -->
            <ellipse cx="64" cy="58" rx="5" ry="4" fill="#5C4033"/>
            <!-- 笑顔 -->
            <path d="M58 64 Q64 70 70 64" stroke="#5C4033" stroke-width="2" fill="none"/>
            <!-- 手 -->
            <ellipse cx="35" cy="80" rx="10" ry="8" fill="#8B7355"/>
            <ellipse cx="93" cy="80" rx="10" ry="8" fill="#8B7355"/>
            <!-- 足 -->
            <ellipse cx="50" cy="105" rx="8" ry="6" fill="#8B7355"/>
            <ellipse cx="78" cy="105" rx="8" ry="6" fill="#8B7355"/>
        </svg>''',

        # 3: わかもの
        3: '''<svg viewBox="0 0 128 128" xmlns="http://www.w3.org/2000/svg">
            <!-- 体 -->
            <ellipse cx="64" cy="88" rx="35" ry="30" fill="#8B7355"/>
            <!-- 顔 -->
            <circle cx="64" cy="48" r="30" fill="#D4B896"/>
            <!-- 目のマスク -->
            <ellipse cx="64" cy="45" rx="24" ry="15" fill="#5C4033"/>
            <!-- 目 -->
            <circle cx="50" cy="45" r="7" fill="#333"/>
            <circle cx="78" cy="45" r="7" fill="#333"/>
            <circle cx="52" cy="43" r="3" fill="#FFF"/>
            <circle cx="80" cy="43" r="3" fill="#FFF"/>
            <!-- 鼻 -->
            <ellipse cx="64" cy="58" rx="5" ry="4" fill="#5C4033"/>
            <!-- 口 -->
            <path d="M56 65 Q64 72 72 65" stroke="#5C4033" stroke-width="2" fill="none"/>
            <!-- 腕（伸ばしている）-->
            <ellipse cx="28" cy="75" rx="12" ry="10" fill="#8B7355"/>
            <ellipse cx="100" cy="75" rx="12" ry="10" fill="#8B7355"/>
            <!-- 爪 -->
            <line x1="20" y1="70" x2="15" y2="65" stroke="#4A4A4A" stroke-width="3"/>
            <line x1="20" y1="75" x2="12" y2="75" stroke="#4A4A4A" stroke-width="3"/>
            <line x1="20" y1="80" x2="15" y2="85" stroke="#4A4A4A" stroke-width="3"/>
            <!-- 足 -->
            <ellipse cx="48" cy="110" rx="10" ry="7" fill="#8B7355"/>
            <ellipse cx="80" cy="110" rx="10" ry="7" fill="#8B7355"/>
        </svg>''',

        # 4: おとな
        4: '''<svg viewBox="0 0 128 128" xmlns="http://www.w3.org/2000/svg">
            <!-- 体 -->
            <ellipse cx="64" cy="90" rx="38" ry="32" fill="#8B7355"/>
            <!-- 顔 -->
            <circle cx="64" cy="45" r="32" fill="#D4B896"/>
            <!-- 目のマスク -->
            <ellipse cx="64" cy="42" rx="26" ry="16" fill="#5C4033"/>
            <!-- 目（落ち着いた表情）-->
            <ellipse cx="48" cy="42" rx="7" ry="6" fill="#333"/>
            <ellipse cx="80" cy="42" rx="7" ry="6" fill="#333"/>
            <circle cx="50" cy="40" r="3" fill="#FFF"/>
            <circle cx="82" cy="40" r="3" fill="#FFF"/>
            <!-- 鼻 -->
            <ellipse cx="64" cy="56" rx="6" ry="5" fill="#5C4033"/>
            <!-- 穏やかな笑み -->
            <path d="M54 64 Q64 70 74 64" stroke="#5C4033" stroke-width="2" fill="none"/>
            <!-- 腕 -->
            <ellipse cx="25" cy="78" rx="14" ry="11" fill="#8B7355"/>
            <ellipse cx="103" cy="78" rx="14" ry="11" fill="#8B7355"/>
            <!-- 爪 -->
            <line x1="15" y1="72" x2="8" y2="66" stroke="#4A4A4A" stroke-width="3"/>
            <line x1="14" y1="78" x2="5" y2="78" stroke="#4A4A4A" stroke-width="3"/>
            <line x1="15" y1="84" x2="8" y2="90" stroke="#4A4A4A" stroke-width="3"/>
            <!-- 足 -->
            <ellipse cx="46" cy="115" rx="12" ry="8" fill="#8B7355"/>
            <ellipse cx="82" cy="115" rx="12" ry="8" fill="#8B7355"/>
        </svg>''',

        # 5: ベテラン
        5: '''<svg viewBox="0 0 128 128" xmlns="http://www.w3.org/2000/svg">
            <!-- 体 -->
            <ellipse cx="64" cy="90" rx="38" ry="32" fill="#7A6548"/>
            <!-- 顔 -->
            <circle cx="64" cy="45" r="32" fill="#D4B896"/>
            <!-- 目のマスク -->
            <ellipse cx="64" cy="42" rx="26" ry="16" fill="#5C4033"/>
            <!-- 賢そうな目 -->
            <ellipse cx="48" cy="42" rx="7" ry="5" fill="#333"/>
            <ellipse cx="80" cy="42" rx="7" ry="5" fill="#333"/>
            <circle cx="50" cy="40" r="2.5" fill="#FFF"/>
            <circle cx="82" cy="40" r="2.5" fill="#FFF"/>
            <!-- 鼻 -->
            <ellipse cx="64" cy="56" rx="6" ry="5" fill="#5C4033"/>
            <!-- 笑顔 -->
            <path d="M54 64 Q64 72 74 64" stroke="#5C4033" stroke-width="2" fill="none"/>
            <!-- ヒゲ（ベテラン感）-->
            <line x1="50" y1="70" x2="40" y2="75" stroke="#AAA" stroke-width="1.5"/>
            <line x1="78" y1="70" x2="88" y2="75" stroke="#AAA" stroke-width="1.5"/>
            <!-- 腕 -->
            <ellipse cx="25" cy="78" rx="14" ry="11" fill="#7A6548"/>
            <ellipse cx="103" cy="78" rx="14" ry="11" fill="#7A6548"/>
            <!-- 爪 -->
            <line x1="15" y1="72" x2="8" y2="66" stroke="#4A4A4A" stroke-width="3"/>
            <line x1="14" y1="78" x2="5" y2="78" stroke="#4A4A4A" stroke-width="3"/>
            <line x1="15" y1="84" x2="8" y2="90" stroke="#4A4A4A" stroke-width="3"/>
            <!-- 足 -->
            <ellipse cx="46" cy="115" rx="12" ry="8" fill="#7A6548"/>
            <ellipse cx="82" cy="115" rx="12" ry="8" fill="#7A6548"/>
            <!-- バッジ -->
            <circle cx="95" cy="95" r="10" fill="#FFD700"/>
            <text x="95" y="99" text-anchor="middle" font-size="12" fill="#333">★</text>
        </svg>''',

        # 6: マスター
        6: '''<svg viewBox="0 0 128 128" xmlns="http://www.w3.org/2000/svg">
            <!-- オーラ -->
            <ellipse cx="64" cy="70" rx="55" ry="50" fill="none" stroke="#FFD700" stroke-width="2" opacity="0.3"/>
            <!-- 体 -->
            <ellipse cx="64" cy="90" rx="38" ry="32" fill="#6B5344"/>
            <!-- 顔 -->
            <circle cx="64" cy="45" r="32" fill="#D4B896"/>
            <!-- 目のマスク -->
            <ellipse cx="64" cy="42" rx="26" ry="16" fill="#5C4033"/>
            <!-- マスターの目（知恵を感じる）-->
            <ellipse cx="48" cy="42" rx="6" ry="5" fill="#333"/>
            <ellipse cx="80" cy="42" rx="6" ry="5" fill="#333"/>
            <circle cx="49" cy="40" r="2" fill="#FFF"/>
            <circle cx="81" cy="40" r="2" fill="#FFF"/>
            <!-- 眉毛 -->
            <line x1="42" y1="32" x2="54" y2="34" stroke="#5C4033" stroke-width="2"/>
            <line x1="86" y1="32" x2="74" y2="34" stroke="#5C4033" stroke-width="2"/>
            <!-- 鼻 -->
            <ellipse cx="64" cy="56" rx="6" ry="5" fill="#5C4033"/>
            <!-- 笑顔 -->
            <path d="M54 64 Q64 72 74 64" stroke="#5C4033" stroke-width="2" fill="none"/>
            <!-- 腕 -->
            <ellipse cx="25" cy="78" rx="14" ry="11" fill="#6B5344"/>
            <ellipse cx="103" cy="78" rx="14" ry="11" fill="#6B5344"/>
            <!-- 爪 -->
            <line x1="15" y1="72" x2="8" y2="66" stroke="#4A4A4A" stroke-width="3"/>
            <line x1="14" y1="78" x2="5" y2="78" stroke="#4A4A4A" stroke-width="3"/>
            <line x1="15" y1="84" x2="8" y2="90" stroke="#4A4A4A" stroke-width="3"/>
            <!-- 足 -->
            <ellipse cx="46" cy="115" rx="12" ry="8" fill="#6B5344"/>
            <ellipse cx="82" cy="115" rx="12" ry="8" fill="#6B5344"/>
            <!-- マスターの帽子 -->
            <ellipse cx="64" cy="18" rx="20" ry="8" fill="#4A4A4A"/>
            <rect x="50" y="8" width="28" height="12" fill="#4A4A4A"/>
        </svg>''',

        # 7: レジェンド
        7: '''<svg viewBox="0 0 128 128" xmlns="http://www.w3.org/2000/svg">
            <!-- 輝くオーラ -->
            <ellipse cx="64" cy="70" rx="58" ry="53" fill="none" stroke="#FFD700" stroke-width="3" opacity="0.5"/>
            <ellipse cx="64" cy="70" rx="52" ry="47" fill="none" stroke="#FFA500" stroke-width="2" opacity="0.3"/>
            <!-- 体（金色がかった毛並み）-->
            <ellipse cx="64" cy="90" rx="38" ry="32" fill="#8B7355"/>
            <ellipse cx="64" cy="90" rx="36" ry="30" fill="url(#legendGrad)" opacity="0.3"/>
            <!-- 顔 -->
            <circle cx="64" cy="45" r="32" fill="#D4B896"/>
            <!-- 目のマスク -->
            <ellipse cx="64" cy="42" rx="26" ry="16" fill="#5C4033"/>
            <!-- レジェンドの目（輝いている）-->
            <ellipse cx="48" cy="42" rx="6" ry="5" fill="#333"/>
            <ellipse cx="80" cy="42" rx="6" ry="5" fill="#333"/>
            <circle cx="49" cy="40" r="3" fill="#FFD700"/>
            <circle cx="81" cy="40" r="3" fill="#FFD700"/>
            <!-- 鼻 -->
            <ellipse cx="64" cy="56" rx="6" ry="5" fill="#5C4033"/>
            <!-- 笑顔 -->
            <path d="M54 64 Q64 72 74 64" stroke="#5C4033" stroke-width="2" fill="none"/>
            <!-- 腕 -->
            <ellipse cx="25" cy="78" rx="14" ry="11" fill="#8B7355"/>
            <ellipse cx="103" cy="78" rx="14" ry="11" fill="#8B7355"/>
            <!-- 金の爪 -->
            <line x1="15" y1="72" x2="8" y2="66" stroke="#FFD700" stroke-width="3"/>
            <line x1="14" y1="78" x2="5" y2="78" stroke="#FFD700" stroke-width="3"/>
            <line x1="15" y1="84" x2="8" y2="90" stroke="#FFD700" stroke-width="3"/>
            <!-- 足 -->
            <ellipse cx="46" cy="115" rx="12" ry="8" fill="#8B7355"/>
            <ellipse cx="82" cy="115" rx="12" ry="8" fill="#8B7355"/>
            <!-- 王冠 -->
            <polygon points="64,5 54,20 50,12 45,22 40,15 40,25 88,25 88,15 83,22 78,12 74,20" fill="#FFD700"/>
            <circle cx="64" cy="18" r="4" fill="#E94560"/>
            <defs>
                <linearGradient id="legendGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#FFD700;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#FFA500;stop-opacity:1" />
                </linearGradient>
            </defs>
        </svg>''',

        # 8: しんわ
        8: '''<svg viewBox="0 0 128 128" xmlns="http://www.w3.org/2000/svg">
            <!-- 神秘的なオーラ -->
            <ellipse cx="64" cy="70" rx="60" ry="55" fill="none" stroke="url(#mythGrad)" stroke-width="4" opacity="0.6"/>
            <!-- 星々 -->
            <circle cx="20" cy="20" r="2" fill="#FFF"/>
            <circle cx="108" cy="25" r="2" fill="#FFF"/>
            <circle cx="15" cy="100" r="1.5" fill="#FFF"/>
            <circle cx="113" cy="95" r="1.5" fill="#FFF"/>
            <!-- 体（銀色の毛並み）-->
            <ellipse cx="64" cy="90" rx="38" ry="32" fill="#C0C0C0"/>
            <!-- 顔 -->
            <circle cx="64" cy="45" r="32" fill="#E8E8E8"/>
            <!-- 目のマスク（神秘的な紫）-->
            <ellipse cx="64" cy="42" rx="26" ry="16" fill="#6B5B95"/>
            <!-- 神話の目（星が輝く）-->
            <ellipse cx="48" cy="42" rx="6" ry="5" fill="#1a1a2e"/>
            <ellipse cx="80" cy="42" rx="6" ry="5" fill="#1a1a2e"/>
            <polygon points="49,40 50,38 51,40 53,41 51,42 50,44 49,42 47,41" fill="#FFF"/>
            <polygon points="81,40 82,38 83,40 85,41 83,42 82,44 81,42 79,41" fill="#FFF"/>
            <!-- 鼻 -->
            <ellipse cx="64" cy="56" rx="6" ry="5" fill="#6B5B95"/>
            <!-- 笑顔 -->
            <path d="M54 64 Q64 72 74 64" stroke="#6B5B95" stroke-width="2" fill="none"/>
            <!-- 腕 -->
            <ellipse cx="25" cy="78" rx="14" ry="11" fill="#C0C0C0"/>
            <ellipse cx="103" cy="78" rx="14" ry="11" fill="#C0C0C0"/>
            <!-- 銀の爪 -->
            <line x1="15" y1="72" x2="8" y2="66" stroke="#E8E8E8" stroke-width="3"/>
            <line x1="14" y1="78" x2="5" y2="78" stroke="#E8E8E8" stroke-width="3"/>
            <line x1="15" y1="84" x2="8" y2="90" stroke="#E8E8E8" stroke-width="3"/>
            <!-- 足 -->
            <ellipse cx="46" cy="115" rx="12" ry="8" fill="#C0C0C0"/>
            <ellipse cx="82" cy="115" rx="12" ry="8" fill="#C0C0C0"/>
            <!-- 神話の輪 -->
            <ellipse cx="64" cy="15" rx="25" ry="8" fill="none" stroke="#FFD700" stroke-width="3"/>
            <defs>
                <linearGradient id="mythGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#DDA0DD;stop-opacity:1" />
                    <stop offset="50%" style="stop-color:#87CEEB;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#DDA0DD;stop-opacity:1" />
                </linearGradient>
            </defs>
        </svg>''',

        # 9: かみ
        9: '''<svg viewBox="0 0 128 128" xmlns="http://www.w3.org/2000/svg">
            <!-- 虹色のオーラ -->
            <ellipse cx="64" cy="70" rx="62" ry="58" fill="none" stroke="url(#godGrad1)" stroke-width="5" opacity="0.7"/>
            <ellipse cx="64" cy="70" rx="56" ry="52" fill="none" stroke="url(#godGrad2)" stroke-width="3" opacity="0.5"/>
            <!-- 輝く粒子 -->
            <circle cx="25" cy="30" r="3" fill="#FFD700" opacity="0.8"/>
            <circle cx="103" cy="35" r="2" fill="#FF6B6B" opacity="0.8"/>
            <circle cx="20" cy="90" r="2" fill="#4ECDC4" opacity="0.8"/>
            <circle cx="108" cy="100" r="3" fill="#96CEB4" opacity="0.8"/>
            <circle cx="30" cy="60" r="1.5" fill="#FFF"/>
            <circle cx="98" cy="65" r="1.5" fill="#FFF"/>
            <!-- 体（虹色に輝く）-->
            <ellipse cx="64" cy="90" rx="38" ry="32" fill="url(#godBody)"/>
            <!-- 顔 -->
            <circle cx="64" cy="45" r="32" fill="#FFF8E7"/>
            <!-- 目のマスク（虹色）-->
            <ellipse cx="64" cy="42" rx="26" ry="16" fill="url(#godMask)"/>
            <!-- 神の目（宇宙を映す）-->
            <ellipse cx="48" cy="42" rx="7" ry="6" fill="#0a0a1a"/>
            <ellipse cx="80" cy="42" rx="7" ry="6" fill="#0a0a1a"/>
            <!-- 目の中の星雲 -->
            <circle cx="46" cy="41" r="2" fill="#FF6B6B" opacity="0.7"/>
            <circle cx="50" cy="43" r="1.5" fill="#4ECDC4" opacity="0.7"/>
            <circle cx="78" cy="41" r="2" fill="#4ECDC4" opacity="0.7"/>
            <circle cx="82" cy="43" r="1.5" fill="#FFEAA7" opacity="0.7"/>
            <!-- 鼻 -->
            <ellipse cx="64" cy="56" rx="6" ry="5" fill="#D4A574"/>
            <!-- 穏やかな微笑み -->
            <path d="M52 64 Q64 74 76 64" stroke="#D4A574" stroke-width="2" fill="none"/>
            <!-- 腕 -->
            <ellipse cx="25" cy="78" rx="14" ry="11" fill="url(#godBody)"/>
            <ellipse cx="103" cy="78" rx="14" ry="11" fill="url(#godBody)"/>
            <!-- 虹の爪 -->
            <line x1="15" y1="72" x2="8" y2="66" stroke="url(#clawGrad)" stroke-width="4"/>
            <line x1="14" y1="78" x2="5" y2="78" stroke="url(#clawGrad)" stroke-width="4"/>
            <line x1="15" y1="84" x2="8" y2="90" stroke="url(#clawGrad)" stroke-width="4"/>
            <!-- 足 -->
            <ellipse cx="46" cy="115" rx="12" ry="8" fill="url(#godBody)"/>
            <ellipse cx="82" cy="115" rx="12" ry="8" fill="url(#godBody)"/>
            <!-- 神の光輪 -->
            <ellipse cx="64" cy="12" rx="28" ry="10" fill="none" stroke="url(#haloGrad)" stroke-width="4"/>
            <!-- 天使の羽（小さめ）-->
            <path d="M20 70 Q5 55 15 45 Q25 50 30 65" fill="#FFF" opacity="0.6"/>
            <path d="M108 70 Q123 55 113 45 Q103 50 98 65" fill="#FFF" opacity="0.6"/>
            <defs>
                <linearGradient id="godGrad1" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#FF6B6B"/>
                    <stop offset="25%" style="stop-color:#FFEAA7"/>
                    <stop offset="50%" style="stop-color:#96CEB4"/>
                    <stop offset="75%" style="stop-color:#45B7D1"/>
                    <stop offset="100%" style="stop-color:#DDA0DD"/>
                </linearGradient>
                <linearGradient id="godGrad2" x1="100%" y1="0%" x2="0%" y2="100%">
                    <stop offset="0%" style="stop-color:#DDA0DD"/>
                    <stop offset="50%" style="stop-color:#FFD700"/>
                    <stop offset="100%" style="stop-color:#FF6B6B"/>
                </linearGradient>
                <linearGradient id="godBody" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#FFE4B5"/>
                    <stop offset="50%" style="stop-color:#FFD700"/>
                    <stop offset="100%" style="stop-color:#FFF8DC"/>
                </linearGradient>
                <linearGradient id="godMask" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" style="stop-color:#6B5B95"/>
                    <stop offset="50%" style="stop-color:#45B7D1"/>
                    <stop offset="100%" style="stop-color:#6B5B95"/>
                </linearGradient>
                <linearGradient id="clawGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#FFD700"/>
                    <stop offset="50%" style="stop-color:#FFF"/>
                    <stop offset="100%" style="stop-color:#FFD700"/>
                </linearGradient>
                <linearGradient id="haloGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" style="stop-color:#FFD700"/>
                    <stop offset="50%" style="stop-color:#FFF"/>
                    <stop offset="100%" style="stop-color:#FFD700"/>
                </linearGradient>
            </defs>
        </svg>''',

        # 死亡時
        "dead": '''<svg viewBox="0 0 128 128" xmlns="http://www.w3.org/2000/svg">
            <!-- 体 -->
            <ellipse cx="64" cy="90" rx="38" ry="32" fill="#666"/>
            <!-- 顔 -->
            <circle cx="64" cy="50" r="30" fill="#999"/>
            <!-- 目のマスク -->
            <ellipse cx="64" cy="47" rx="24" ry="15" fill="#555"/>
            <!-- X目 -->
            <line x1="44" y1="40" x2="54" y2="50" stroke="#333" stroke-width="3"/>
            <line x1="54" y1="40" x2="44" y2="50" stroke="#333" stroke-width="3"/>
            <line x1="74" y1="40" x2="84" y2="50" stroke="#333" stroke-width="3"/>
            <line x1="84" y1="40" x2="74" y2="50" stroke="#333" stroke-width="3"/>
            <!-- 鼻 -->
            <ellipse cx="64" cy="60" rx="5" ry="4" fill="#555"/>
            <!-- 悲しい口 -->
            <path d="M54 72 Q64 65 74 72" stroke="#555" stroke-width="2" fill="none"/>
            <!-- 腕（だらん）-->
            <ellipse cx="28" cy="95" rx="12" ry="10" fill="#666"/>
            <ellipse cx="100" cy="95" rx="12" ry="10" fill="#666"/>
            <!-- 天使の輪 -->
            <ellipse cx="64" cy="15" rx="15" ry="5" fill="none" stroke="#FFD700" stroke-width="2" opacity="0.5"/>
        </svg>'''
    }

    return svg_sprites.get(stage_id, svg_sprites[0])


def get_all_sprites():
    """全スプライトを取得"""
    return {i: create_sloth_svg(i) for i in range(10)}
