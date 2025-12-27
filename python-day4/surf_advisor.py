import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import ephem
from typing import Dict, List, Tuple
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API設定
# Streamlit Cloudではst.secretsから、ローカルでは.envから読み込む
try:
    OPENWEATHER_API_KEY = st.secrets.get('OPENWEATHER_API_KEY', '')
except:
    OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', '')
OPENWEATHER_URL = 'https://api.openweathermap.org/data/2.5/forecast'

# Open-Meteo（完全無料、APIキー不要）
OPEN_METEO_URL = 'https://marine-api.open-meteo.com/v1/marine'

def get_moon_phase(date: datetime) -> Dict:
    """月齢と月の満ち欠け状態を計算"""
    observer = ephem.Observer()
    observer.date = date

    moon = ephem.Moon(observer)
    moon_phase = moon.phase

    previous_new = ephem.previous_new_moon(date)
    moon_age = (date - previous_new.datetime()).days

    # 月相の判定
    if moon_phase < 6.25:
        phase_name = "新月"
    elif moon_phase < 43.75:
        phase_name = "上弦の月"
    elif moon_phase < 56.25:
        phase_name = "満月"
    elif moon_phase < 93.75:
        phase_name = "下弦の月"
    else:
        phase_name = "新月"

    # 大潮判定（新月・満月前後3日）
    is_spring_tide = (0 <= moon_age <= 3) or (13 <= moon_age <= 17) or (26 <= moon_age <= 29)

    return {
        'age': moon_age,
        'phase': phase_name,
        'illumination': moon_phase,
        'is_spring_tide': is_spring_tide
    }

def get_weather_data(lat: float, lon: float) -> List[Dict]:
    """OpenWeatherMapから天気・風データを取得"""
    if not OPENWEATHER_API_KEY:
        st.warning("OpenWeatherMap APIキーが未設定です。デモデータを使用します。")
        return []

    params = {
        'lat': lat,
        'lon': lon,
        'appid': OPENWEATHER_API_KEY,
        'units': 'metric',
        'lang': 'ja'
    }

    try:
        response = requests.get(OPENWEATHER_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        weather_data = []
        for item in data['list']:
            weather_data.append({
                'datetime': datetime.fromtimestamp(item['dt']),
                'temp': item['main']['temp'],
                'weather': item['weather'][0]['description'],
                'wind_speed': item['wind']['speed'],
                'wind_deg': item['wind'].get('deg', 0),
                'rain': item.get('rain', {}).get('3h', 0)
            })

        return weather_data

    except Exception as e:
        st.error(f"天気データ取得エラー: {e}")
        return []

def get_wave_data(lat: float, lon: float, start_date: str, end_date: str) -> List[Dict]:
    """Open-Meteoから波情報を取得（完全無料）"""
    params = {
        'latitude': lat,
        'longitude': lon,
        'start_date': start_date,
        'end_date': end_date,
        'hourly': 'wave_height,wave_period,wave_direction',
        'timezone': 'Asia/Tokyo'
    }

    try:
        response = requests.get(OPEN_METEO_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if 'hourly' not in data:
            return []

        hourly = data['hourly']
        wave_data = []

        for i in range(len(hourly['time'])):
            wave_data.append({
                'datetime': datetime.fromisoformat(hourly['time'][i]),
                'wave_height': hourly['wave_height'][i] if hourly['wave_height'][i] else 0,
                'wave_period': hourly['wave_period'][i] if hourly['wave_period'][i] else 0,
                'wave_direction': hourly['wave_direction'][i] if hourly['wave_direction'][i] else 0
            })

        return wave_data

    except Exception as e:
        st.error(f"波データ取得エラー: {e}")
        return []

def get_wind_direction_name(deg: float) -> str:
    """風向を8方位で返す"""
    directions = ['北', '北東', '東', '南東', '南', '南西', '西', '北西']
    idx = int((deg + 22.5) / 45) % 8
    return directions[idx]

def classify_wind_offshore(wind_deg: float, beach_facing: float) -> Tuple[str, int]:
    """
    風向がオフショアかオンショアかを判定

    beach_facing: ビーチが向いている方角（度）
    - 湘南: 180（南向き）
    - 九十九里: 90（東向き）
    """
    # ビーチに対する風の相対角度
    relative_angle = (wind_deg - beach_facing + 180) % 360

    if 45 <= relative_angle <= 135:
        return "オフショア", 15
    elif 135 < relative_angle <= 180 or 0 <= relative_angle < 45:
        return "サイドオフショア", 10
    elif 225 <= relative_angle <= 315:
        return "オンショア", -15
    else:
        return "サイドオンショア", -5

def calculate_surf_score(weather: Dict, wave: Dict, moon: Dict,
                         skill_level: str, beach_facing: float) -> Tuple[int, List[str]]:
    """サーフィン適性スコアを計算（0-100点）"""
    score = 50
    reasons = []

    # スキルレベルに応じた最適波高
    skill_ranges = {
        '初心者': (0.5, 1.0),
        '中級者': (1.0, 2.0),
        '上級者': (2.0, 3.5)
    }

    # 【波の高さ】（±20点）
    wave_height = wave['wave_height']
    min_h, max_h = skill_ranges.get(skill_level, (1.0, 2.0))

    if min_h <= wave_height <= max_h:
        score += 20
        reasons.append(f"✓ 最適な波高 ({wave_height:.1f}m - {skill_level}向け)")
    elif wave_height < min_h:
        if wave_height < min_h * 0.5:
            score -= 10
            reasons.append(f"✗ 波が小さすぎる ({wave_height:.1f}m)")
        else:
            score += 5
            reasons.append(f"△ やや小さい波 ({wave_height:.1f}m)")
    else:
        if wave_height > 3.5:
            score -= 20
            reasons.append(f"⚠️ 危険な波高 ({wave_height:.1f}m)")
        elif wave_height > max_h:
            score -= 10
            reasons.append(f"△ 波が高め ({wave_height:.1f}m)")
        else:
            score += 10
            reasons.append(f"○ 良好な波高 ({wave_height:.1f}m)")

    # 【波の周期】（±20点）
    wave_period = wave['wave_period']
    if 8 <= wave_period <= 12:
        score += 20
        reasons.append(f"✓ 理想的な周期 ({wave_period:.0f}秒)")
    elif 6 <= wave_period < 8 or 12 < wave_period <= 14:
        score += 10
        reasons.append(f"○ 良好な周期 ({wave_period:.0f}秒)")
    elif 14 < wave_period <= 16:
        score += 5
        reasons.append(f"△ 長周期 ({wave_period:.0f}秒 - 上級者向け)")
    else:
        score -= 10
        reasons.append(f"✗ 不適切な周期 ({wave_period:.0f}秒)")

    # 【風向】（±15点）
    wind_type, wind_score = classify_wind_offshore(weather['wind_deg'], beach_facing)
    score += wind_score
    wind_dir_name = get_wind_direction_name(weather['wind_deg'])

    if wind_score > 0:
        reasons.append(f"✓ {wind_type}（{wind_dir_name}風）")
    else:
        reasons.append(f"✗ {wind_type}（{wind_dir_name}風）")

    # 【風速】（±10点）
    wind_speed = weather['wind_speed']
    if wind_speed <= 3:
        score += 10
        reasons.append(f"✓ 穏やかな風 ({wind_speed:.1f}m/s)")
    elif wind_speed <= 5:
        score += 8
        reasons.append(f"✓ 軽い風 ({wind_speed:.1f}m/s)")
    elif wind_speed <= 8:
        score += 3
        reasons.append(f"○ やや風あり ({wind_speed:.1f}m/s)")
    elif wind_speed <= 10:
        score -= 5
        reasons.append(f"△ 強めの風 ({wind_speed:.1f}m/s)")
    else:
        score -= 10
        reasons.append(f"✗ 強風 ({wind_speed:.1f}m/s)")

    # 【天気】（±10点）
    if weather['rain'] == 0:
        score += 5
        reasons.append("✓ 雨なし")
    elif weather['rain'] < 2:
        reasons.append(f"△ 小雨 ({weather['rain']:.1f}mm)")
    else:
        score -= 5
        reasons.append(f"✗ 雨 ({weather['rain']:.1f}mm)")

    # 【月齢ボーナス】（±5点）
    if moon['is_spring_tide']:
        score += 5
        reasons.append(f"✓ 大潮期間（{moon['phase']}）- うねり入りやすい")
    else:
        reasons.append(f"○ 小潮期間（{moon['phase']}）")

    # スコアを0-100に制限
    score = max(0, min(100, score))

    return score, reasons

def get_beach_info() -> Dict[str, Tuple[float, float, float]]:
    """
    サーフスポット情報
    (緯度, 経度, ビーチの向き（度）)
    """
    return {
        '湘南（鵠沼）': (35.3333, 139.4833, 180),  # 南向き
        '千葉（九十九里）': (35.5500, 140.4000, 90),  # 東向き
        '千葉（一宮）': (35.3667, 140.4000, 90),  # 東向き
        '静岡（御前崎）': (34.6000, 138.2167, 180),  # 南向き
        '宮崎（木崎浜）': (31.9833, 131.4667, 135),  # 南東向き
        '高知（生見）': (33.5667, 134.2833, 135),  # 南東向き
        '新潟（角田浜）': (37.7667, 138.8667, 270),  # 西向き
        '徳島（小松海岸）': (33.9667, 134.5833, 135)  # 南東向き
    }

# ========== Streamlit UI ==========
st.set_page_config(page_title="サーフィン情報アドバイザー", page_icon="🏄", layout="wide")

st.title('🏄 サーフィン情報アドバイザー')
st.markdown('**日付と場所を入力すると、風・波・月齢から最適なサーフィン時間を提案します**')

# サイドバー
st.sidebar.header('📋 条件を入力')

beaches = get_beach_info()
location = st.sidebar.selectbox('📍 サーフスポット', list(beaches.keys()))

skill_level = st.sidebar.selectbox('🏄 スキルレベル', ['初心者', '中級者', '上級者'])

target_date = st.sidebar.date_input(
    '📅 日付',
    datetime.now(),
    min_value=datetime.now(),
    max_value=datetime.now() + timedelta(days=7)
)

if st.sidebar.button('🔍 分析開始', type='primary'):
    lat, lon, beach_facing = beaches[location]

    st.header(f'📊 {location}の予報 ({target_date.strftime("%Y年%m月%d日")})')

    # 月齢情報
    target_datetime = datetime.combine(target_date, datetime.min.time())
    moon_info = get_moon_phase(target_datetime)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric('🌙 月齢', f'{moon_info["age"]}日')
    with col2:
        st.metric('🌕 月相', moon_info['phase'])
    with col3:
        tide_type = '大潮' if moon_info['is_spring_tide'] else '小潮'
        st.metric('🌊 潮汐', tide_type)

    # データ取得
    with st.spinner('データを取得中...'):
        # 天気データ
        weather_data = get_weather_data(lat, lon)

        # 波データ
        start_date = target_date.strftime('%Y-%m-%d')
        end_date = (target_date + timedelta(days=1)).strftime('%Y-%m-%d')
        wave_data = get_wave_data(lat, lon, start_date, end_date)

    if weather_data and wave_data:
        # データをマージ
        results = []

        for weather in weather_data:
            if weather['datetime'].date() != target_date:
                continue

            # 最も近い時刻の波データを探す
            closest_wave = min(wave_data,
                             key=lambda w: abs((w['datetime'] - weather['datetime']).total_seconds()))

            score, reasons = calculate_surf_score(weather, closest_wave, moon_info,
                                                 skill_level, beach_facing)

            results.append({
                '時刻': weather['datetime'].strftime('%H:%M'),
                'datetime': weather['datetime'],
                'スコア': score,
                '波高': f"{closest_wave['wave_height']:.1f}m",
                '周期': f"{closest_wave['wave_period']:.0f}秒",
                '風速': f"{weather['wind_speed']:.1f}m/s",
                '風向': get_wind_direction_name(weather['wind_deg']),
                '天気': weather['weather'],
                '気温': f"{weather['temp']:.1f}°C",
                '評価理由': reasons
            })

        if results:
            # スコアでソート
            results_sorted = sorted(results, key=lambda x: x['スコア'], reverse=True)

            # ベストタイム
            best = results_sorted[0]

            st.success(f"🏆 **おすすめ時間: {best['時刻']}**")

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric('適性スコア', f"{best['スコア']}/100")
            with col2:
                if best['スコア'] >= 75:
                    st.metric('評価', '最高！', delta='excellent')
                elif best['スコア'] >= 60:
                    st.metric('評価', '良好', delta='good')
                elif best['スコア'] >= 45:
                    st.metric('評価', '普通', delta='fair')
                else:
                    st.metric('評価', '要注意', delta='poor')
            with col3:
                st.metric('波高', best['波高'])
            with col4:
                st.metric('周期', best['周期'])

            st.markdown("**📝 評価理由:**")
            for reason in best['評価理由']:
                st.markdown(f"- {reason}")

            st.divider()

            # 全時間帯の詳細
            st.subheader('⏰ 全時間帯の詳細')

            df = pd.DataFrame([{k: v for k, v in r.items() if k != '評価理由' and k != 'datetime'}
                              for r in results_sorted])

            # スコア別に色付け
            def highlight_score(row):
                score = row['スコア']
                if score >= 75:
                    color = 'background-color: #d4edda'
                elif score >= 60:
                    color = 'background-color: #fff3cd'
                elif score >= 45:
                    color = 'background-color: #f8d7da'
                else:
                    color = 'background-color: #f5c6cb'
                return [color] * len(row)

            st.dataframe(df.style.apply(highlight_score, axis=1),
                        use_container_width=True, height=400)

            # 詳細を展開表示
            with st.expander('📋 各時間帯の詳細な評価理由'):
                for result in results_sorted:
                    st.markdown(f"### {result['時刻']} (スコア: {result['スコア']}/100)")
                    for reason in result['評価理由']:
                        st.markdown(f"- {reason}")
                    st.divider()
        else:
            st.warning('選択した日付のデータがありません')
    else:
        st.error('データを取得できませんでした')

# サイドバーにヘルプ
with st.sidebar.expander('ℹ️ 使い方'):
    st.markdown("""
    ### APIキーの設定（OpenWeatherMapのみ）

    1. [OpenWeatherMap](https://openweathermap.org/api)で無料登録
    2. APIキーを取得
    3. `.env`ファイルを作成:
    ```
    OPENWEATHER_API_KEY=your_key
    ```

    ### スコアの見方
    - **75点以上**: 最高のコンディション
    - **60-74点**: 良好、おすすめ
    - **45-59点**: 可能だが条件はやや厳しい
    - **44点以下**: おすすめしない

    ### 波データについて
    Open-Meteo APIを使用（完全無料、登録不要）
    """)

with st.sidebar.expander('🔧 スコアリング基準'):
    st.markdown("""
    **波の高さ** (±20点)
    - 初心者: 0.5-1.0m
    - 中級者: 1.0-2.0m
    - 上級者: 2.0-3.5m

    **波の周期** (±20点)
    - 理想: 8-12秒
    - 良好: 6-8秒, 12-14秒

    **風向** (±15点)
    - オフショア: +15
    - オンショア: -15

    **風速** (±10点)
    - 0-3m/s: +10
    - 10m/s以上: -10

    **月齢** (+5点)
    - 大潮時にボーナス
    """)
