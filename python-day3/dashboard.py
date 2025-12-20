import streamlit as st
import os
from dotenv import load_dotenv
import requests
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go

# 環境変数の読み込み
load_dotenv()

# APIキーの取得
ESTAT_API_KEY = os.getenv("ESTAT_API_KEY")

# ページの設定
st.set_page_config(
    page_title="国内の経済指標",
    page_icon="📊",
    layout="wide"
)

# タイトル
st.title("国内の経済指標")

# 景気動向指数データ取得関数
@st.cache_data
def get_keiki_data():
    """e-StatのAPIから景気動向指数を取得"""

    print("=" * 60)
    print("景気動向指数データの取得を開始します")
    print("=" * 60)

    if not ESTAT_API_KEY:
        error_msg = "エラー: APIキーが設定されていません。.envファイルを確認してください。"
        print(error_msg)
        return None, error_msg

    print(f"APIキー: {ESTAT_API_KEY[:10]}...")

    # e-Stat APIのエンドポイント
    url = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"

    # 景気動向指数の統計表ID（長期系列）
    stats_data_id = "0003446461"  # 景気動向指数 長期系列

    params = {
        "appId": ESTAT_API_KEY,
        "statsDataId": stats_data_id,
        "cdCat01": "100",  # CI一致指数
        "limit": 1000,  # できるだけ多くのデータを取得（全期間）
        "metaGetFlg": "Y",  # メタ情報も取得
    }

    print(f"\nリクエストURL: {url}")
    print(f"統計表ID: {stats_data_id}")
    print(f"パラメータ: {json.dumps(params, indent=2, ensure_ascii=False)}")

    try:
        print("\nAPIリクエストを送信中...")
        response = requests.get(url, params=params, timeout=30)

        print(f"ステータスコード: {response.status_code}")
        print(f"レスポンスヘッダー: {dict(response.headers)}")

        # ステータスコードの確認
        if response.status_code != 200:
            error_msg = f"APIリクエストエラー: ステータスコード {response.status_code}"
            print(f"\n{error_msg}")
            print(f"レスポンス本文:\n{response.text[:500]}")
            return None, error_msg

        # JSONデータの解析
        print("\nJSONデータを解析中...")
        data = response.json()

        # レスポンスの構造を確認
        print(f"\nレスポンスのキー: {list(data.keys())}")

        # エラーチェック
        if "GET_STATS_DATA" not in data:
            error_msg = f"予期しないレスポンス形式: {json.dumps(data, indent=2, ensure_ascii=False)[:500]}"
            print(f"\n{error_msg}")
            return None, error_msg

        result = data["GET_STATS_DATA"]["STATISTICAL_DATA"]

        # データが存在するか確認
        if "DATA_INF" not in result or "VALUE" not in result["DATA_INF"]:
            error_msg = "データが見つかりませんでした"
            print(f"\n{error_msg}")
            print(f"利用可能なキー: {list(result.keys())}")
            return None, error_msg

        values = result["DATA_INF"]["VALUE"]

        print(f"\n取得したデータ件数: {len(values)}件")
        print(f"サンプルデータ（最初の3件）:")
        for i, val in enumerate(values[:3]):
            print(f"  {i+1}. {json.dumps(val, indent=4, ensure_ascii=False)}")

        # データフレームに変換
        df = pd.DataFrame(values)

        print(f"\nデータフレームの形状: {df.shape}")
        print(f"カラム: {list(df.columns)}")
        print(f"\nデータフレームのサンプル:")
        print(df.head())

        # 列名を日本語に変換
        column_mapping = {
            '@tab': '表番号',
            '@cat01': '指標分類',
            '@time': '時間軸',
            '@unit': '単位',
            '$': 'CI一致指数'
        }

        df = df.rename(columns=column_mapping)

        # 時間軸を読みやすい形式に変換（例: 1985000101 -> 1985年1月）
        if '時間軸' in df.columns:
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

            df['年月'] = df['時間軸'].apply(format_time)

        # CI一致指数を数値型に変換
        if 'CI一致指数' in df.columns:
            df['CI一致指数'] = pd.to_numeric(df['CI一致指数'], errors='coerce')

        # 時間軸で降順ソートして重複を削除（最新のデータを優先）
        if '時間軸' in df.columns:
            df = df.sort_values('時間軸', ascending=False)
            df = df.drop_duplicates(subset=['時間軸'], keep='first')
            print(f"\n重複削除後のデータ件数: {len(df)}件")

        print(f"\n列名を日本語に変換しました")
        print(f"変換後のカラム: {list(df.columns)}")
        print(f"\n変換後のデータフレームのサンプル（最新順）:")
        print(df.head(15))

        print("\n" + "=" * 60)
        print("データ取得成功")
        print("=" * 60)

        return df, None

    except requests.exceptions.Timeout:
        error_msg = "エラー: APIリクエストがタイムアウトしました"
        print(f"\n{error_msg}")
        return None, error_msg

    except requests.exceptions.RequestException as e:
        error_msg = f"エラー: リクエスト中に問題が発生しました - {str(e)}"
        print(f"\n{error_msg}")
        return None, error_msg

    except json.JSONDecodeError as e:
        error_msg = f"エラー: JSONの解析に失敗しました - {str(e)}"
        print(f"\n{error_msg}")
        print(f"レスポンステキスト: {response.text[:500]}")
        return None, error_msg

    except Exception as e:
        error_msg = f"エラー: 予期しないエラーが発生しました - {type(e).__name__}: {str(e)}"
        print(f"\n{error_msg}")
        import traceback
        print(f"トレースバック:\n{traceback.format_exc()}")
        return None, error_msg


# 消費者物価指数データ取得関数
@st.cache_data
def get_cpi_data():
    """e-StatのAPIから消費者物価指数（CPI）を取得"""

    print("=" * 60)
    print("消費者物価指数データの取得を開始します")
    print("=" * 60)

    if not ESTAT_API_KEY:
        error_msg = "エラー: APIキーが設定されていません。.envファイルを確認してください。"
        print(error_msg)
        return None, error_msg

    print(f"APIキー: {ESTAT_API_KEY[:10]}...")

    # e-Stat APIのエンドポイント
    url = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"

    # 消費者物価指数の統計表ID
    # 総務省統計局の消費者物価指数（2020年基準）
    stats_data_id = "0003427113"  # 2020年基準消費者物価指数

    params = {
        "appId": ESTAT_API_KEY,
        "statsDataId": stats_data_id,
        "cdCat01": "0001",  # 総合指数
        "cdArea": "13A01",  # 全国
        "limit": 50,  # より多くのデータを取得
        "metaGetFlg": "Y",  # メタ情報も取得
    }

    print(f"\nリクエストURL: {url}")
    print(f"統計表ID: {stats_data_id}")
    print(f"パラメータ: {json.dumps(params, indent=2, ensure_ascii=False)}")

    try:
        print("\nAPIリクエストを送信中...")
        response = requests.get(url, params=params, timeout=30)

        print(f"ステータスコード: {response.status_code}")
        print(f"レスポンスヘッダー: {dict(response.headers)}")

        # ステータスコードの確認
        if response.status_code != 200:
            error_msg = f"APIリクエストエラー: ステータスコード {response.status_code}"
            print(f"\n{error_msg}")
            print(f"レスポンス本文:\n{response.text[:500]}")
            return None, error_msg

        # JSONデータの解析
        print("\nJSONデータを解析中...")
        data = response.json()

        # レスポンスの構造を確認
        print(f"\nレスポンスのキー: {list(data.keys())}")

        # エラーチェック
        if "GET_STATS_DATA" not in data:
            error_msg = f"予期しないレスポンス形式: {json.dumps(data, indent=2, ensure_ascii=False)[:500]}"
            print(f"\n{error_msg}")
            return None, error_msg

        result = data["GET_STATS_DATA"]["STATISTICAL_DATA"]

        # データが存在するか確認
        if "DATA_INF" not in result or "VALUE" not in result["DATA_INF"]:
            error_msg = "データが見つかりませんでした"
            print(f"\n{error_msg}")
            print(f"利用可能なキー: {list(result.keys())}")
            return None, error_msg

        values = result["DATA_INF"]["VALUE"]

        print(f"\n取得したデータ件数: {len(values)}件")
        print(f"サンプルデータ（最初の3件）:")
        for i, val in enumerate(values[:3]):
            print(f"  {i+1}. {json.dumps(val, indent=4, ensure_ascii=False)}")

        # データフレームに変換
        df = pd.DataFrame(values)

        print(f"\nデータフレームの形状: {df.shape}")
        print(f"カラム: {list(df.columns)}")
        print(f"\nデータフレームのサンプル:")
        print(df.head())

        # 列名を日本語に変換
        column_mapping = {
            '@tab': '表番号',
            '@cat01': '品目分類',
            '@area': '地域コード',
            '@time': '時間軸',
            '@unit': '単位',
            '$': '指数値'
        }

        df = df.rename(columns=column_mapping)

        # 時間軸を読みやすい形式に変換（例: 2025001111 -> 2025年11月）
        if '時間軸' in df.columns:
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

            df['年月'] = df['時間軸'].apply(format_time)

        # 指数値を数値型に変換
        if '指数値' in df.columns:
            df['指数値'] = pd.to_numeric(df['指数値'], errors='coerce')

        print(f"\n列名を日本語に変換しました")
        print(f"変換後のカラム: {list(df.columns)}")
        print(f"\n変換後のデータフレームのサンプル:")
        print(df.head())

        print("\n" + "=" * 60)
        print("データ取得成功")
        print("=" * 60)

        return df, None

    except requests.exceptions.Timeout:
        error_msg = "エラー: APIリクエストがタイムアウトしました"
        print(f"\n{error_msg}")
        return None, error_msg

    except requests.exceptions.RequestException as e:
        error_msg = f"エラー: リクエスト中に問題が発生しました - {str(e)}"
        print(f"\n{error_msg}")
        return None, error_msg

    except json.JSONDecodeError as e:
        error_msg = f"エラー: JSONの解析に失敗しました - {str(e)}"
        print(f"\n{error_msg}")
        print(f"レスポンステキスト: {response.text[:500]}")
        return None, error_msg

    except Exception as e:
        error_msg = f"エラー: 予期しないエラーが発生しました - {type(e).__name__}: {str(e)}"
        print(f"\n{error_msg}")
        import traceback
        print(f"トレースバック:\n{traceback.format_exc()}")
        return None, error_msg

# データ取得
st.header("消費者物価指数（CPI）")

with st.spinner("データを取得中..."):
    df, error = get_cpi_data()

if error:
    st.error(f"エラーが発生しました: {error}")
    st.info("コンソールで詳細なエラーメッセージを確認してください。")
elif df is not None:
    st.success(f"データを取得しました（{len(df)}件）")

    # 表示用に必要な列だけを選択
    display_columns = []
    if '年月' in df.columns:
        display_columns.append('年月')
    if '指数値' in df.columns:
        display_columns.append('指数値')
    if '品目分類' in df.columns:
        display_columns.append('品目分類')
    if '地域コード' in df.columns:
        display_columns.append('地域コード')

    if display_columns:
        df_display = df[display_columns].copy()
    else:
        df_display = df

    # データを古い順に並べ替え（グラフ用）
    if '年月' in df_display.columns:
        df_chart = df_display.sort_values('年月', ascending=True).copy()
    else:
        df_chart = df_display.copy()

    # 折れ線グラフの作成
    if '年月' in df_chart.columns and '指数値' in df_chart.columns:
        st.subheader("📈 消費者物価指数の推移")

        # Plotlyで折れ線グラフを作成
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df_chart['年月'],
            y=df_chart['指数値'],
            mode='lines+markers',
            name='消費者物価指数',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=6),
            hovertemplate='<b>%{x}</b><br>指数値: %{y}<extra></extra>'
        ))

        fig.update_layout(
            title={
                'text': '消費者物価指数（2020年基準）の推移',
                'x': 0.5,
                'xanchor': 'center'
            },
            xaxis=dict(
                title='年月',
                showgrid=True,
                gridwidth=1,
                gridcolor='lightgray'
            ),
            yaxis=dict(
                title='指数値',
                showgrid=True,
                gridwidth=1,
                gridcolor='lightgray'
            ),
            hovermode='x unified',
            height=500,
            template='plotly_white',
            font=dict(size=12),
            showlegend=True
        )

        st.plotly_chart(fig, use_container_width=True)

    # データを新しい順に並べ替え（テーブル表示用）
    if '年月' in df_display.columns:
        df_display = df_display.sort_values('年月', ascending=False)

    # 直近12ヶ月のデータに絞る
    df_recent = df_display.head(12)

    st.subheader("📊 直近12ヶ月のデータ")
    st.dataframe(df_recent, use_container_width=True)

    # 全データも表示
    with st.expander("全データを表示"):
        st.dataframe(df_display, use_container_width=True)

else:
    st.warning("データが取得できませんでした")

# 景気動向指数セクション
st.header("景気動向指数（CI一致指数）")

with st.spinner("データを取得中..."):
    df_keiki, error_keiki = get_keiki_data()

if error_keiki:
    st.error(f"エラーが発生しました: {error_keiki}")
    st.info("コンソールで詳細なエラーメッセージを確認してください。")
elif df_keiki is not None:
    st.success(f"データを取得しました（{len(df_keiki)}件）")

    # 表示用に必要な列だけを選択
    display_columns_keiki = []
    if '年月' in df_keiki.columns:
        display_columns_keiki.append('年月')
    if 'CI一致指数' in df_keiki.columns:
        display_columns_keiki.append('CI一致指数')
    if '指標分類' in df_keiki.columns:
        display_columns_keiki.append('指標分類')

    if display_columns_keiki:
        df_keiki_display = df_keiki[display_columns_keiki].copy()
    else:
        df_keiki_display = df_keiki

    # データを古い順に並べ替え（グラフ用）
    if '年月' in df_keiki_display.columns:
        df_keiki_chart = df_keiki_display.sort_values('年月', ascending=True).copy()
    else:
        df_keiki_chart = df_keiki_display.copy()

    # 折れ線グラフの作成
    if '年月' in df_keiki_chart.columns and 'CI一致指数' in df_keiki_chart.columns:
        st.subheader("📈 景気動向指数の推移")

        # Plotlyで折れ線グラフを作成
        fig_keiki = go.Figure()

        fig_keiki.add_trace(go.Scatter(
            x=df_keiki_chart['年月'],
            y=df_keiki_chart['CI一致指数'],
            mode='lines+markers',
            name='CI一致指数',
            line=dict(color='#ff7f0e', width=3),
            marker=dict(size=6),
            hovertemplate='<b>%{x}</b><br>CI一致指数: %{y}<extra></extra>'
        ))

        fig_keiki.update_layout(
            title={
                'text': '景気動向指数（CI一致指数）の推移',
                'x': 0.5,
                'xanchor': 'center'
            },
            xaxis=dict(
                title='年月',
                showgrid=True,
                gridwidth=1,
                gridcolor='lightgray'
            ),
            yaxis=dict(
                title='CI一致指数',
                showgrid=True,
                gridwidth=1,
                gridcolor='lightgray'
            ),
            hovermode='x unified',
            height=500,
            template='plotly_white',
            font=dict(size=12),
            showlegend=True
        )

        st.plotly_chart(fig_keiki, use_container_width=True)

    # データを新しい順に並べ替え（テーブル表示用）
    if '年月' in df_keiki_display.columns:
        df_keiki_display = df_keiki_display.sort_values('年月', ascending=False)

    # 直近12ヶ月のデータに絞る
    df_keiki_recent = df_keiki_display.head(12)

    st.subheader("📊 直近12ヶ月のデータ")
    st.dataframe(df_keiki_recent, use_container_width=True)

    # 全データも表示
    with st.expander("全データを表示"):
        st.dataframe(df_keiki_display, use_container_width=True)

else:
    st.warning("データが取得できませんでした")
