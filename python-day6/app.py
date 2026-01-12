from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime
import yaml
import os
import json

from services.notion_client import NotionService
from services.ollama_client import OllamaService
from services.analyzer import GrowthAnalyzer

app = Flask(__name__)

# 設定読み込み
def load_config():
    config_path = 'config.yaml'
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    return None

config = load_config()

# サービス初期化
notion_service = None
ollama_service = None
analyzer = None

if config:
    notion_service = NotionService(
        api_key=config['notion']['api_key'],
        database_id=config['notion']['database_id']
    )
    ollama_service = OllamaService(
        model=config['ollama']['model']
    )
    analyzer = GrowthAnalyzer(ollama_service)

# ローカルストレージ（簡易的な日報カウント保存）
JOURNAL_COUNT_FILE = 'journal_count.json'

def get_journal_count():
    """日報カウントを取得"""
    if os.path.exists(JOURNAL_COUNT_FILE):
        with open(JOURNAL_COUNT_FILE, 'r') as f:
            data = json.load(f)
            return data.get('count', 0)
    return 0

def increment_journal_count():
    """日報カウントをインクリメント"""
    count = get_journal_count() + 1
    with open(JOURNAL_COUNT_FILE, 'w') as f:
        json.dump({'count': count}, f)
    return count

def reset_journal_count():
    """日報カウントをリセット"""
    with open(JOURNAL_COUNT_FILE, 'w') as f:
        json.dump({'count': 0}, f)

@app.route('/')
def index():
    """トップページ - 日報入力フォーム"""
    if not config:
        return render_template('error.html', message='config.yamlが見つかりません')

    journal_count = get_journal_count()
    trigger_count = config.get('reflection', {}).get('trigger_count', 5)

    return render_template(
        'index.html',
        journal_count=journal_count,
        trigger_count=trigger_count,
        today=datetime.now().strftime('%Y-%m-%d')
    )

@app.route('/submit', methods=['POST'])
def submit_journal():
    """日報を送信"""
    try:
        content = request.form.get('content')
        date = request.form.get('date', datetime.now().strftime('%Y-%m-%d'))

        if not content:
            return jsonify({'success': False, 'error': '日報内容が空です'})

        # 日報を分析
        journal = analyzer.analyze_journal(content, date)

        # Notionに保存
        result = notion_service.create_journal_page(journal.to_dict())

        if not result['success']:
            return jsonify({'success': False, 'error': result['error']})

        # カウントをインクリメント
        count = increment_journal_count()
        trigger_count = config.get('reflection', {}).get('trigger_count', 5)

        # リフレクション生成チェック
        should_reflect = analyzer.should_generate_reflection(count, trigger_count)

        response_data = {
            'success': True,
            'page_id': result['page_id'],
            'journal_count': count,
            'summary': journal.summary,
            'growth_points': journal.growth_points,
            'skills': journal.skills,
            'should_reflect': should_reflect
        }

        if should_reflect:
            response_data['reflection_url'] = url_for('generate_reflection', _external=True)

        return jsonify(response_data)

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/reflection')
def generate_reflection():
    """リフレクションを生成"""
    try:
        trigger_count = config.get('reflection', {}).get('trigger_count', 5)

        # Notionから最近の日報を取得
        recent_journals = notion_service.get_recent_journals(limit=trigger_count)

        if not recent_journals:
            return render_template('error.html', message='日報が見つかりません')

        # Notionのデータを変換
        journals_data = []
        for page in recent_journals:
            props = page.get('properties', {})

            # 日付取得
            date_prop = props.get('日付', {})
            date = date_prop.get('date', {}).get('start', '')

            # サマリー取得
            summary_prop = props.get('サマリー', {})
            summary_texts = summary_prop.get('rich_text', [])
            summary = summary_texts[0].get('text', {}).get('content', '') if summary_texts else ''

            # スキル取得
            skills_prop = props.get('スキル', {})
            skills = [s['name'] for s in skills_prop.get('multi_select', [])]

            journals_data.append({
                'date': date,
                'content': summary,  # 簡易的にサマリーを使用
                'skills': skills
            })

        # リフレクション生成
        reflection = analyzer.generate_reflection(journals_data, trigger_count)

        # Notionに保存
        notion_service.create_reflection_page(reflection.to_dict())

        # カウントをリセット
        reset_journal_count()

        return render_template('reflection.html', reflection=reflection)

    except Exception as e:
        return render_template('error.html', message=f'エラー: {str(e)}')

@app.route('/health')
def health():
    """ヘルスチェック"""
    return jsonify({
        'status': 'ok',
        'config_loaded': config is not None,
        'journal_count': get_journal_count()
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
