"""
内容处理模块 - 分类、去重、排序新闻
"""

import logging
from typing import List, Dict
from datetime import datetime

logger = logging.getLogger(__name__)


class ContentProcessor:
    """内容处理器"""

    def __init__(self, categories_config: Dict):
        self.categories = categories_config
        self.processed_items = {}

    def process_news(self, news_items: List[Dict]) -> Dict:
        """处理新闻列表"""
        logger.info("开始处理新闻...")

        # 1. 去重
        unique_items = self._deduplicate(news_items)
        logger.info(f"去重后: {len(unique_items)} 条新闻")

        # 2. 分类
        categorized = self._categorize_news(unique_items)

        # 3. 排序
        sorted_items = self._sort_by_category(categorized)

        # 4. 生成摘要
        digest = self._generate_digest(sorted_items)

        return digest

    def _deduplicate(self, news_items: List[Dict]) -> List[Dict]:
        """去除重复新闻"""
        seen_titles = set()
        unique = []

        for item in news_items:
            title = item['title'].lower().strip()
            if title not in seen_titles:
                seen_titles.add(title)
                unique.append(item)

        return unique

    def _categorize_news(self, news_items: List[Dict]) -> Dict:
        """将新闻分类"""
        categorized = {cat['id']: [] for cat in self.categories}

        for item in news_items:
            category_id = self._classify_item(item)
            if category_id in categorized:
                categorized[category_id].append(item)

        return categorized

    def _classify_item(self, item: Dict) -> str:
        """根据关键词分类单个新闻"""
        text = (item['title'] + ' ' + item['summary']).lower()

        # 遍历所有分类，找到最匹配的
        best_match = 'general'
        max_matches = 0

        for category in self.categories:
            cat_id = category['id']
            keywords = category.get('keywords', [])
            matches = sum(1 for kw in keywords if kw.lower() in text)

            if matches > max_matches:
                max_matches = matches
                best_match = cat_id

        return best_match

    def _sort_by_category(self, categorized: Dict) -> Dict:
        """按分类排序"""
        # 按分类顺序重新组织
        sorted_items = {}

        for category in self.categories:
            cat_id = category['id']
            if cat_id in categorized and categorized[cat_id]:
                sorted_items[cat_id] = categorized[cat_id]

        return sorted_items

    def _generate_digest(self, sorted_items: Dict) -> Dict:
        """生成摘要"""
        digest = {
            'timestamp': datetime.now().isoformat(),
            'date': datetime.now().strftime('%Y年%m月%d日'),
            'total_count': sum(len(items) for items in sorted_items.values()),
            'items': {}
        }

        for category in self.categories:
            cat_id = category['id']
            cat_name = category['name']
            cat_emoji = category['emoji']

            if cat_id in sorted_items:
                digest['items'][f"{cat_emoji} {cat_name}"] = sorted_items[cat_id]

        return digest
