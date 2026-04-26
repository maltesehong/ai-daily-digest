"""
新闻采集模块 - 从多个来源采集AI相关新闻
"""

import feedparser
import requests
import logging
from datetime import datetime, timedelta
from typing import List, Dict
import json

logger = logging.getLogger(__name__)


class NewsCollector:
    """新闻采集器"""

    def __init__(self, sources_config: Dict):
        self.sources = sources_config
        self.timeout = 10
        self.news_items = []

    def collect_news(self) -> List[Dict]:
        """采集所有来源的新闻"""
        logger.info("开始采集新闻...")

        # 采集RSS源
        for source in self.sources.get('rss_feeds', []):
            logger.info(f"📡 采集RSS: {source['name']}")
            self._collect_from_rss(source)

        # 采集API来源
        for source in self.sources.get('api_sources', []):
            logger.info(f"🌐 采集API: {source['name']}")
            self._collect_from_api(source)

        # 采集爬虫来源
        for source in self.sources.get('web_sources', []):
            logger.info(f"🕷️ 采集网站: {source['name']}")
            self._collect_from_web(source)

        return self.news_items

    def _collect_from_rss(self, source: Dict):
        """从RSS源采集新闻"""
        try:
            feed = feedparser.parse(source['url'])
            count = 0

            for entry in feed.entries[:10]:  # 每个源最多10条
                # 检查是否包含关键词
                if self._has_keywords(entry, source.get('keywords', [])):
                    item = {
                        'title': entry.get('title', 'No title'),
                        'link': entry.get('link', ''),
                        'source': source['name'],
                        'source_type': 'RSS',
                        'published': entry.get('published', str(datetime.now())),
                        'summary': entry.get('summary', '')[:200],
                        'timestamp': datetime.now().isoformat()
                    }
                    self.news_items.append(item)
                    count += 1

            logger.info(f"  ✅ 获得 {count} 条新闻")
        except Exception as e:
            logger.warning(f"  ❌ RSS采集失败: {str(e)}")

    def _collect_from_api(self, source: Dict):
        """从API采集新闻"""
        try:
            headers = {
                'User-Agent': 'AI-Daily-Digest/1.0'
            }

            if source['name'] == 'NewsAPI':
                self._collect_newsapi(source, headers)
            else:
                logger.warning(f"  ⚠️ 暂不支持此API源")

        except Exception as e:
            logger.warning(f"  ❌ API采集失败: {str(e)}")

    def _collect_newsapi(self, source: Dict, headers: Dict):
        """采集NewsAPI"""
        try:
            url = source['url']
            api_key = source.get('api_key', '')

            if not api_key:
                logger.warning("  ⚠️ NewsAPI密钥未配置，跳过")
                return

            params = {
                'q': 'AI OR "artificial intelligence" OR GPT OR LLM',
                'language': 'en',
                'sortBy': 'publishedAt',
                'apiKey': api_key,
                'pageSize': 20
            }

            response = requests.get(url, params=params, headers=headers, timeout=self.timeout)
            data = response.json()
            count = 0

            if data.get('status') == 'ok':
                for article in data.get('articles', [])[:20]:
                    item = {
                        'title': article.get('title', 'No title'),
                        'link': article.get('url', ''),
                        'source': article.get('source', {}).get('name', 'Unknown'),
                        'source_type': 'NewsAPI',
                        'published': article.get('publishedAt', str(datetime.now())),
                        'summary': article.get('description', '')[:200],
                        'timestamp': datetime.now().isoformat()
                    }
                    self.news_items.append(item)
                    count += 1

            logger.info(f"  ✅ 获得 {count} 条新闻")
        except Exception as e:
            logger.warning(f"  ❌ NewsAPI采集失败: {str(e)}")

    def _collect_from_web(self, source: Dict):
        """从网页采集新闻（简单实现）"""
        logger.info(f"  ℹ️ 网页采集需要自定义爬虫逻辑")

    def _has_keywords(self, entry: Dict, keywords: List[str]) -> bool:
        """检查条目是否包含关键词"""
        if not keywords:
            return True

        text = (entry.get('title', '') + ' ' + entry.get('summary', '')).lower()
        return any(kw.lower() in text for kw in keywords)
