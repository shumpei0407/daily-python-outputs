from notion_client import Client
from typing import Dict, List, Optional
import os


class NotionService:
    """Notion API連携サービス"""

    def __init__(self, api_key: str, database_id: str):
        self.client = Client(auth=api_key)
        self.database_id = database_id

    def create_journal_page(self, journal_data: Dict) -> Dict:
        """日報ページをNotionに作成"""
        try:
            page = self.client.pages.create(
                parent={"database_id": self.database_id},
                properties={
                    "タイトル": {
                        "title": [
                            {
                                "text": {
                                    "content": f"日報 - {journal_data['date']}"
                                }
                            }
                        ]
                    },
                    "日付": {
                        "date": {
                            "start": journal_data['date']
                        }
                    },
                    "サマリー": {
                        "rich_text": [
                            {
                                "text": {
                                    "content": journal_data.get('summary', '')[:2000]
                                }
                            }
                        ]
                    },
                    "スキル": {
                        "multi_select": [
                            {"name": skill} for skill in journal_data.get('skills', [])
                        ]
                    }
                },
                children=[
                    {
                        "object": "block",
                        "type": "heading_2",
                        "heading_2": {
                            "rich_text": [{"type": "text", "text": {"content": "本文"}}]
                        }
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {"content": journal_data['content'][:2000]}
                                }
                            ]
                        }
                    },
                    {
                        "object": "block",
                        "type": "heading_3",
                        "heading_3": {
                            "rich_text": [{"type": "text", "text": {"content": "成長ポイント"}}]
                        }
                    },
                    {
                        "object": "block",
                        "type": "bulleted_list_item",
                        "bulleted_list_item": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {"content": point}
                                }
                            ]
                        }
                    } for point in journal_data.get('growth_points', [])
                ]
            )
            return {"success": True, "page_id": page["id"]}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def create_reflection_page(self, reflection_data: Dict) -> Dict:
        """リフレクションページをNotionに作成"""
        try:
            page = self.client.pages.create(
                parent={"database_id": self.database_id},
                properties={
                    "タイトル": {
                        "title": [
                            {
                                "text": {
                                    "content": f"リフレクション - {reflection_data['period_start']} 〜 {reflection_data['period_end']}"
                                }
                            }
                        ]
                    },
                    "日付": {
                        "date": {
                            "start": reflection_data['period_start'],
                            "end": reflection_data['period_end']
                        }
                    },
                    "タイプ": {
                        "select": {
                            "name": "リフレクション"
                        }
                    }
                },
                children=self._build_reflection_blocks(reflection_data)
            )
            return {"success": True, "page_id": page["id"]}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _build_reflection_blocks(self, data: Dict) -> List[Dict]:
        """リフレクション用のNotionブロックを構築"""
        blocks = [
            {
                "object": "block",
                "type": "callout",
                "callout": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": f"📊 {data['journal_count']}日分の日報から振り返りました"
                            }
                        }
                    ],
                    "icon": {"emoji": "🎯"}
                }
            },
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "🌟 成長サマリー"}}]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": data['growth_summary']}
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "📚 主な学び"}}]
                }
            }
        ]

        # 学びリスト
        for learning in data['key_learnings']:
            blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": learning}}]
                }
            })

        # スキル進捗
        blocks.extend([
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "📈 スキル進捗"}}]
                }
            }
        ])

        for skill, count in data['skill_progress'].items():
            blocks.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": f"{skill}: {count}回言及"}
                        }
                    ]
                }
            })

        # 次のフォーカス
        blocks.extend([
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "🎯 次に意識すること"}}]
                }
            }
        ])

        for focus in data['next_focus']:
            blocks.append({
                "object": "block",
                "type": "to_do",
                "to_do": {
                    "rich_text": [{"type": "text", "text": {"content": focus}}],
                    "checked": False
                }
            })

        return blocks

    def get_recent_journals(self, limit: int = 5) -> List[Dict]:
        """最近の日報を取得"""
        try:
            results = self.client.databases.query(
                database_id=self.database_id,
                sorts=[{"property": "日付", "direction": "descending"}],
                page_size=limit
            )
            return results.get("results", [])
        except Exception as e:
            print(f"Error fetching journals: {e}")
            return []
