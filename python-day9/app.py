"""
ナマケモノ育成タスク管理システム - Flaskアプリケーション
"""
from flask import Flask, render_template, request, jsonify
from models import (
    get_status,
    set_task,
    complete_task,
    reset_game,
    load_data,
    EVOLUTION_STAGES,
)
from static.sprites.sloth_sprites import create_sloth_svg

app = Flask(__name__)


@app.route("/")
def index():
    """メインページ"""
    status = get_status()
    # 初期スプライトをサーバーサイドで生成
    if status.get("status") == "dead" or status.get("status") == "died":
        initial_sprite = create_sloth_svg("dead")
    else:
        initial_sprite = create_sloth_svg(status["sloth"]["evolution_stage"])
    return render_template("index.html", status=status, initial_sprite=initial_sprite)


@app.route("/api/status")
def api_status():
    """ステータスAPIエンドポイント"""
    status = get_status()
    return jsonify(status)


@app.route("/api/sprite/<int:stage_id>")
def api_sprite(stage_id):
    """スプライト取得API"""
    if stage_id < 0 or stage_id > 9:
        stage_id = 0
    svg = create_sloth_svg(stage_id)
    return svg, 200, {"Content-Type": "image/svg+xml"}


@app.route("/api/sprite/dead")
def api_sprite_dead():
    """死亡スプライト取得API"""
    svg = create_sloth_svg("dead")
    return svg, 200, {"Content-Type": "image/svg+xml"}


@app.route("/api/task", methods=["POST"])
def api_set_task():
    """タスク設定API"""
    data = request.get_json()
    content = data.get("content", "").strip()

    if not content:
        return jsonify({"success": False, "message": "タスクを入力してください"})

    success, message = set_task(content)
    status = get_status()
    return jsonify({"success": success, "message": message, "status": status})


@app.route("/api/task/complete", methods=["POST"])
def api_complete_task():
    """タスク完了API"""
    success, message, evolved = complete_task()
    status = get_status()
    return jsonify({
        "success": success,
        "message": message,
        "evolved": evolved,
        "status": status
    })


@app.route("/api/reset", methods=["POST"])
def api_reset():
    """ゲームリセットAPI"""
    reset_game()
    status = get_status()
    return jsonify({"success": True, "message": "ゲームをリセットしました", "status": status})


@app.route("/api/evolutions")
def api_evolutions():
    """進化一覧API"""
    return jsonify(EVOLUTION_STAGES)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
