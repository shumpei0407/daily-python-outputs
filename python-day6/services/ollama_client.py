import ollama
from typing import Dict, List


class OllamaService:
    """Ollama（ローカルLLM）連携サービス"""

    def __init__(self, model: str = "llama2"):
        self.model = model

    def generate_summary(self, content: str) -> str:
        """日報から要約を生成"""
        prompt = f"""
以下の日報から、重要なポイントを3-5文で要約してください。
要約には以下を含めてください：
- 主な活動内容
- 達成したこと
- 学んだこと

日報:
{content}

要約:
"""
        try:
            response = ollama.generate(model=self.model, prompt=prompt)
            return response['response'].strip()
        except Exception as e:
            print(f"Error generating summary: {e}")
            return "要約の生成に失敗しました"

    def extract_growth_points(self, content: str) -> List[str]:
        """成長ポイントを抽出"""
        prompt = f"""
以下の日報から、成長につながる行動や学びを箇条書きで抽出してください。
各項目は1文で簡潔に記述してください。

日報:
{content}

成長ポイント（箇条書き）:
"""
        try:
            response = ollama.generate(model=self.model, prompt=prompt)
            # レスポンスを行ごとに分割して箇条書きに変換
            lines = response['response'].strip().split('\n')
            growth_points = [
                line.strip('- •*').strip()
                for line in lines
                if line.strip() and line.strip('- •*').strip()
            ]
            return growth_points[:5]  # 最大5つ
        except Exception as e:
            print(f"Error extracting growth points: {e}")
            return []

    def extract_skills(self, content: str) -> List[str]:
        """スキル・技術キーワードを抽出"""
        prompt = f"""
以下の日報から、学んだ技術やスキルのキーワードを抽出してください。
プログラミング言語、フレームワーク、ツール、概念などを含めてください。
各キーワードは1-3単語で、カンマ区切りで出力してください。

日報:
{content}

スキルキーワード:
"""
        try:
            response = ollama.generate(model=self.model, prompt=prompt)
            # カンマ区切りで分割
            skills_text = response['response'].strip()
            skills = [
                skill.strip()
                for skill in skills_text.split(',')
                if skill.strip()
            ]
            return skills[:10]  # 最大10個
        except Exception as e:
            print(f"Error extracting skills: {e}")
            return []

    def generate_reflection(
        self,
        journals: List[Dict],
        period_start: str,
        period_end: str
    ) -> Dict:
        """複数の日報からリフレクションを生成"""
        # 日報を結合
        combined_content = "\n\n---\n\n".join([
            f"【{j['date']}】\n{j['content']}"
            for j in journals
        ])

        # 全体の成長サマリー
        summary_prompt = f"""
以下は{len(journals)}日分の日報です。
この期間の成長を2-3文で要約してください。
特に、スキルの向上や新しい気づきに焦点を当ててください。

{combined_content}

成長サマリー:
"""

        # 主な学び
        learnings_prompt = f"""
以下の日報から、特に重要な学びを3-5個、箇条書きで抽出してください。

{combined_content}

主な学び:
"""

        # 次に意識すること
        next_focus_prompt = f"""
以下の日報を分析して、次に意識すべきポイントや改善点を3個、箇条書きで提案してください。

{combined_content}

次に意識すること:
"""

        try:
            # サマリー生成
            summary_response = ollama.generate(model=self.model, prompt=summary_prompt)
            growth_summary = summary_response['response'].strip()

            # 学び抽出
            learnings_response = ollama.generate(model=self.model, prompt=learnings_prompt)
            learnings_lines = learnings_response['response'].strip().split('\n')
            key_learnings = [
                line.strip('- •*').strip()
                for line in learnings_lines
                if line.strip() and line.strip('- •*').strip()
            ][:5]

            # 次のフォーカス抽出
            focus_response = ollama.generate(model=self.model, prompt=next_focus_prompt)
            focus_lines = focus_response['response'].strip().split('\n')
            next_focus = [
                line.strip('- •*').strip()
                for line in focus_lines
                if line.strip() and line.strip('- •*').strip()
            ][:3]

            # スキル集計
            skill_progress = {}
            for journal in journals:
                for skill in journal.get('skills', []):
                    skill_progress[skill] = skill_progress.get(skill, 0) + 1

            return {
                'growth_summary': growth_summary,
                'key_learnings': key_learnings,
                'next_focus': next_focus,
                'skill_progress': skill_progress
            }

        except Exception as e:
            print(f"Error generating reflection: {e}")
            return {
                'growth_summary': 'リフレクションの生成に失敗しました',
                'key_learnings': [],
                'next_focus': [],
                'skill_progress': {}
            }
