import requests
import json
import os
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()
ESTAT_API_KEY = os.getenv("ESTAT_API_KEY")

print("=" * 80)
print("e-Stat API テスト: 消費者物価指数の統計表を検索")
print("=" * 80)

# 統計表情報を検索
url = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsList"
params = {
    "appId": ESTAT_API_KEY,
    "searchWord": "消費者物価指数 2020年基準",
    "limit": 10
}

print(f"\n検索ワード: 消費者物価指数")
print(f"リクエストURL: {url}")
print(f"\nAPIリクエストを送信中...\n")

try:
    response = requests.get(url, params=params, timeout=30)
    print(f"ステータスコード: {response.status_code}\n")

    if response.status_code == 200:
        data = response.json()

        print("レスポンスの構造:")
        print(json.dumps(data, indent=2, ensure_ascii=False)[:1000])
        print("\n" + "=" * 80)

        if "GET_STATS_LIST" in data:
            datalist_inf = data["GET_STATS_LIST"]["DATALIST_INF"]

            # TABLE_INFを取得
            if "TABLE_INF" in datalist_inf:
                table_inf = datalist_inf["TABLE_INF"]
                # リストでない場合はリストに変換
                stats_list = table_inf if isinstance(table_inf, list) else [table_inf]
            else:
                print("TABLE_INFが見つかりません")
                print(f"DATALIST_INFのキー: {list(datalist_inf.keys())}")
                stats_list = []

            print(f"\n検索結果: {len(stats_list)}件\n")
            print("=" * 80)

            for i, stat in enumerate(stats_list, 1):
                print(f"\n【統計 {i}】")
                print(f"統計表ID: {stat.get('@id', 'N/A')}")
                print(f"統計名: {stat.get('STAT_NAME', {}).get('$', 'N/A')}")
                print(f"政府組織: {stat.get('GOV_ORG', {}).get('$', 'N/A')}")
                print(f"タイトル: {stat.get('TITLE', {}).get('$', stat.get('TITLE', 'N/A'))}")
                print(f"統計名称: {stat.get('STATISTICS_NAME', 'N/A')}")

                # この統計表IDでデータを取得してみる
                stats_id = stat.get('@id', '')
                if stats_id:
                    print(f"\n  → この統計表IDでデータ取得を試行: {stats_id}")

                    data_url = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"
                    data_params = {
                        "appId": ESTAT_API_KEY,
                        "statsDataId": stats_id,
                        "limit": 3
                    }

                    data_response = requests.get(data_url, params=data_params, timeout=30)
                    if data_response.status_code == 200:
                        result = data_response.json()
                        if "GET_STATS_DATA" in result:
                            stat_data = result["GET_STATS_DATA"]["STATISTICAL_DATA"]
                            if "DATA_INF" in stat_data and "VALUE" in stat_data["DATA_INF"]:
                                values = stat_data["DATA_INF"]["VALUE"]
                                print(f"  ✓ データ取得成功! ({len(values)}件)")
                                print(f"  サンプル: {json.dumps(values[0], ensure_ascii=False)[:200]}...")
                            else:
                                print(f"  ✗ データが見つかりません")
                                print(f"  利用可能なキー: {list(stat_data.keys())}")
                    else:
                        print(f"  ✗ データ取得失敗 (ステータス: {data_response.status_code})")

                print("-" * 80)
        else:
            print("検索結果が見つかりませんでした")
            print(f"レスポンス: {json.dumps(data, indent=2, ensure_ascii=False)[:500]}")
    else:
        print(f"エラー: ステータスコード {response.status_code}")
        print(f"レスポンス: {response.text[:500]}")

except Exception as e:
    print(f"エラーが発生しました: {type(e).__name__}: {str(e)}")
    import traceback
    print(traceback.format_exc())

print("\n" + "=" * 80)
