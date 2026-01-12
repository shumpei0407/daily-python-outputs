from typing import Dict, List
from datetime import datetime
from models.journal import Journal, Reflection
from services.ollama_client import OllamaService


class GrowthAnalyzer:
    """成長分析サービス"""

    def __init__(self, ollama_service: OllamaService):
        self.ollama = ollama_service

    def analyze_journal(self, content: str, date: str) -> Journal:
        """日報を分析してJournalオブジェクトを返す"""
        # AIで分析
        summary = self.ollama.generate_summary(content)
        growth_points = self.ollama.extract_growth_points(content)
        skills = self.ollama.extract_skills(content)

        return Journal(
            date=date,
            content=content,
            summary=summary,
            growth_points=growth_points,
            skills=skills
        )

    def should_generate_reflection(self, journal_count: int, trigger_count: int = 5) -> bool:
        """リフレクションを生成すべきかチェック"""
        return journal_count > 0 and journal_count % trigger_count == 0

    def generate_reflection(
        self,
        journals: List[Dict],
        trigger_count: int = 5
    ) -> Reflection:
        """リフレクションを生成"""
        if not journals:
            raise ValueError("日報が空です")

        # 期間を計算
        dates = [j['date'] for j in journals]
        period_start = min(dates)
        period_end = max(dates)

        # AIでリフレクション生成
        reflection_data = self.ollama.generate_reflection(
            journals,
            period_start,
            period_end
        )

        return Reflection(
            period_start=period_start,
            period_end=period_end,
            journal_count=len(journals),
            key_learnings=reflection_data['key_learnings'],
            growth_summary=reflection_data['growth_summary'],
            skill_progress=reflection_data['skill_progress'],
            next_focus=reflection_data['next_focus']
        )
