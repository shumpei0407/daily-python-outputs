"""
ナマケモノ育成タスク管理システム - データモデル
"""
import json
import os
from datetime import datetime, date
from pathlib import Path

DATA_FILE = Path(__file__).parent / "data" / "sloth_data.json"

# ナマケモノの進化段階（10種類）
EVOLUTION_STAGES = [
    {"id": 0, "name": "たまご", "required_days": 0, "description": "生まれたばかりのたまご"},
    {"id": 1, "name": "あかちゃん", "required_days": 1, "description": "かわいい赤ちゃんナマケモノ"},
    {"id": 2, "name": "こども", "required_days": 3, "description": "元気な子供ナマケモノ"},
    {"id": 3, "name": "わかもの", "required_days": 7, "description": "好奇心旺盛な若者"},
    {"id": 4, "name": "おとな", "required_days": 14, "description": "立派な大人ナマケモノ"},
    {"id": 5, "name": "ベテラン", "required_days": 21, "description": "経験豊富なベテラン"},
    {"id": 6, "name": "マスター", "required_days": 30, "description": "タスクの達人"},
    {"id": 7, "name": "レジェンド", "required_days": 50, "description": "伝説のナマケモノ"},
    {"id": 8, "name": "しんわ", "required_days": 75, "description": "神話級の存在"},
    {"id": 9, "name": "かみ", "required_days": 100, "description": "神となったナマケモノ"},
]


def get_default_data():
    """デフォルトのデータ構造を返す"""
    return {
        "sloth": {
            "name": "なまけもの",
            "evolution_stage": 0,
            "consecutive_days": 0,
            "total_tasks_completed": 0,
            "created_at": datetime.now().isoformat(),
            "is_alive": True,
        },
        "task": {
            "content": None,
            "created_at": None,
            "completed": False,
            "completed_at": None,
        },
        "history": [],
        "last_task_date": None,
        "last_check_date": None,
    }


def ensure_data_dir():
    """データディレクトリを作成"""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)


def load_data():
    """データをJSONファイルから読み込む"""
    ensure_data_dir()
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return get_default_data()


def save_data(data):
    """データをJSONファイルに保存"""
    ensure_data_dir()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_evolution_stage(consecutive_days):
    """継続日数から進化段階を取得"""
    stage = 0
    for i, evolution in enumerate(EVOLUTION_STAGES):
        if consecutive_days >= evolution["required_days"]:
            stage = i
    return EVOLUTION_STAGES[stage]


def check_sloth_status(data):
    """
    ナマケモノの状態をチェック
    - 3日間タスク未完了で死亡
    - 0時でタスクリセット
    """
    today = date.today().isoformat()

    # 既に死んでいる場合
    if not data["sloth"]["is_alive"]:
        return data, "dead"

    last_task_date = data.get("last_task_date")

    if last_task_date:
        last_date = date.fromisoformat(last_task_date)
        days_since_last = (date.today() - last_date).days

        # 3日以上放置で死亡
        if days_since_last >= 3:
            data["sloth"]["is_alive"] = False
            save_data(data)
            return data, "died"

    # 日付が変わったらタスクをリセット
    last_check = data.get("last_check_date")
    if last_check != today:
        # 前日のタスクが完了していなかった場合、連続記録リセット
        if data["task"]["content"] and not data["task"]["completed"]:
            # 連続記録をリセットしない（3日猶予があるため）
            pass

        # タスクをリセット（内容は保持、完了状態のみリセット）
        if data["task"]["completed"]:
            # 完了していた場合は新しい日のためにリセット
            data["task"]["completed"] = False
            data["task"]["completed_at"] = None

        data["last_check_date"] = today
        save_data(data)

    return data, "alive"


def set_task(content):
    """タスクを設定"""
    data = load_data()
    data, status = check_sloth_status(data)

    if status == "dead" or status == "died":
        return False, "ナマケモノは死んでしまいました...リセットしてください"

    data["task"] = {
        "content": content,
        "created_at": datetime.now().isoformat(),
        "completed": False,
        "completed_at": None,
    }
    save_data(data)
    return True, "タスクを設定しました"


def complete_task():
    """タスクを完了"""
    data = load_data()
    data, status = check_sloth_status(data)

    if status == "dead" or status == "died":
        return False, "ナマケモノは死んでしまいました...リセットしてください", None

    if not data["task"]["content"]:
        return False, "タスクが設定されていません", None

    if data["task"]["completed"]:
        return False, "今日のタスクは既に完了しています", None

    today = date.today().isoformat()
    last_task_date = data.get("last_task_date")

    # 連続日数の計算
    if last_task_date:
        last_date = date.fromisoformat(last_task_date)
        days_diff = (date.today() - last_date).days
        if days_diff == 1:
            # 連続
            data["sloth"]["consecutive_days"] += 1
        elif days_diff > 1:
            # 連続が途切れた（でも3日以内なので生きている）
            data["sloth"]["consecutive_days"] = 1
        # days_diff == 0 の場合は同じ日なので何もしない
    else:
        # 初めてのタスク完了
        data["sloth"]["consecutive_days"] = 1

    # タスク完了処理
    data["task"]["completed"] = True
    data["task"]["completed_at"] = datetime.now().isoformat()
    data["sloth"]["total_tasks_completed"] += 1
    data["last_task_date"] = today

    # 進化チェック
    old_stage = data["sloth"]["evolution_stage"]
    new_stage_info = get_evolution_stage(data["sloth"]["consecutive_days"])
    data["sloth"]["evolution_stage"] = new_stage_info["id"]

    # 履歴に追加
    data["history"].append({
        "task": data["task"]["content"],
        "completed_at": data["task"]["completed_at"],
        "consecutive_days": data["sloth"]["consecutive_days"],
    })

    evolved = old_stage < new_stage_info["id"]
    save_data(data)

    if evolved:
        return True, f"タスク完了！ナマケモノが「{new_stage_info['name']}」に進化しました！", new_stage_info
    return True, "タスク完了！ナマケモノが喜んでいます！", None


def reset_game():
    """ゲームをリセット"""
    data = get_default_data()
    save_data(data)
    return data


def get_status():
    """現在の状態を取得"""
    data = load_data()
    data, status = check_sloth_status(data)

    stage_info = get_evolution_stage(data["sloth"]["consecutive_days"])

    # 次の進化までの日数を計算
    next_stage = None
    days_to_next = None
    if stage_info["id"] < len(EVOLUTION_STAGES) - 1:
        next_stage = EVOLUTION_STAGES[stage_info["id"] + 1]
        days_to_next = next_stage["required_days"] - data["sloth"]["consecutive_days"]

    # 残り猶予日数
    days_until_death = 3
    if data.get("last_task_date"):
        last_date = date.fromisoformat(data["last_task_date"])
        days_since = (date.today() - last_date).days
        days_until_death = max(0, 3 - days_since)

    return {
        "sloth": data["sloth"],
        "task": data["task"],
        "stage_info": stage_info,
        "next_stage": next_stage,
        "days_to_next": days_to_next,
        "days_until_death": days_until_death,
        "status": status,
    }
