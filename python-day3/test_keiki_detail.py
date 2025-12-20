import requests
import json
import os
from dotenv import load_dotenv
import pandas as pd

# 環境変数の読み込み
load_dotenv()
ESTAT_API_KEY = os.getenv("ESTAT_API_KEY")

print("=" * 80)
print("景気動向指数の詳細データ取得テスト")
print("=" * 80)

url = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"
stats_data_id = "0003446461"  # 景気動向指数 長期系列

params = {
    "appId": ESTAT_API_KEY,
    "statsDataId": stats_data_id,
    "cdCat01": "100",  # CI一致指数
    "limit": 1000,  # できるだけ多くのデータを取得
    "metaGetFlg": "Y",
}

print(f"統計表ID: {stats_data_id}")
print(f"パラメータ: {json.dumps(params, indent=2, ensure_ascii=False)}\n")

try:
    response = requests.get(url, params=params, timeout=30)
    print(f"ステータスコード: {response.status_code}\n")

    if response.status_code == 200:
        data = response.json()
        result = data["GET_STATS_DATA"]["STATISTICAL_DATA"]
        values = result["DATA_INF"]["VALUE"]

        print(f"取得したデータ件数: {len(values)}件\n")

        # データフレームに変換
        df = pd.DataFrame(values)

        print("最初の10件のデータ:")
        print(df.head(10))

        print("\n最後の10件のデータ:")
        print(df.tail(10))

        print(f"\n時間軸(@time)のユニークな値の数: {df['@time'].nunique()}件")
        print(f"時間軸の最小値: {df['@time'].min()}")
        print(f"時間軸の最大値: {df['@time'].max()}")

        # 時間軸を年月に変換
        def format_time(time_str):
            try:
                time_str = str(time_str)
                if len(time_str) >= 10:
                    year = time_str[0:4]
                    month = time_str[6:8]
                    return f"{year}年{month}月"
                return time_str
            except:
                return time_str

        df['年月'] = df['@time'].apply(format_time)

        print("\n年月でソートした最新10件:")
        df_sorted = df.sort_values('@time', ascending=False)
        print(df_sorted[['@time', '年月', '$']].head(10))

except Exception as e:
    print(f"エラー: {type(e).__name__}: {str(e)}")
    import traceback
    print(traceback.format_exc())

print("\n" + "=" * 80)
