from datetime import datetime
from typing import Dict, List, Optional


class Journal:
    """日報データモデル"""

    def __init__(
        self,
        date: str,
        content: str,
        summary: Optional[str] = None,
        growth_points: Optional[List[str]] = None,
        skills: Optional[List[str]] = None,
        challenges: Optional[List[str]] = None
    ):
        self.date = date
        self.content = content
        self.summary = summary
        self.growth_points = growth_points or []
        self.skills = skills or []
        self.challenges = challenges or []

    def to_dict(self) -> Dict:
        """辞書形式に変換"""
        return {
            'date': self.date,
            'content': self.content,
            'summary': self.summary,
            'growth_points': self.growth_points,
            'skills': self.skills,
            'challenges': self.challenges,
            'created_at': datetime.now().isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Journal':
        """辞書から日報オブジェクトを生成"""
        return cls(
            date=data.get('date', ''),
            content=data.get('content', ''),
            summary=data.get('summary'),
            growth_points=data.get('growth_points', []),
            skills=data.get('skills', []),
            challenges=data.get('challenges', [])
        )


class Reflection:
    """リフレクション（振り返り）データモデル"""

    def __init__(
        self,
        period_start: str,
        period_end: str,
        journal_count: int,
        key_learnings: List[str],
        growth_summary: str,
        skill_progress: Dict[str, int],
        next_focus: List[str]
    ):
        self.period_start = period_start
        self.period_end = period_end
        self.journal_count = journal_count
        self.key_learnings = key_learnings
        self.growth_summary = growth_summary
        self.skill_progress = skill_progress
        self.next_focus = next_focus

    def to_dict(self) -> Dict:
        """辞書形式に変換"""
        return {
            'period_start': self.period_start,
            'period_end': self.period_end,
            'journal_count': self.journal_count,
            'key_learnings': self.key_learnings,
            'growth_summary': self.growth_summary,
            'skill_progress': self.skill_progress,
            'next_focus': self.next_focus,
            'created_at': datetime.now().isoformat()
        }
