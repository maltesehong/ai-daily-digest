#!/usr/bin/env python3
"""
AI Daily Digest - Main Entry Point
采集、处理、发送AI行业日报
"""

import os
import sys
import json
import logging
from datetime import datetime
from pathlib import Path

# 添加src目录到Python路径
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from collector import NewsCollector
from processor import ContentProcessor
from sender import EmailSender

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_config():
    """加载配置文件"""
    config_dir = Path(__file__).parent / 'config'

    with open(config_dir / 'sources.json', 'r', encoding='utf-8') as f:
        sources = json.load(f)

    with open(config_dir / 'categories.json', 'r', encoding='utf-8') as f:
        categories = json.load(f)

    return {
        'sources': sources,
        'categories': categories
    }


def main():
    """主程序流程"""
    logger.info("=" * 60)
    logger.info("🤖 AI Daily Digest 启动")
    logger.info(f"⏰ 执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)

    try:
        # 1. 加载配置
        logger.info("📋 加载配置文件...")
        config = load_config()

        # 2. 采集新闻
        logger.info("🔍 开始采集新闻...")
        collector = NewsCollector(config['sources'])
        news_items = collector.collect_news()
        logger.info(f"✅ 采集完成，共获得 {len(news_items)} 条新闻")

        if not news_items:
            logger.warning("⚠️ 未采集到任何新闻，程序退出")
            return

        # 3. 处理内容
        logger.info("🔄 处理和分类内容...")
        processor = ContentProcessor(config['categories'])
        digest = processor.process_news(news_items)

        # 4. 生成摘要统计
        total_count = sum(len(items) for items in digest['items'].values())
        logger.info(f"📊 分类完成，共 {total_count} 条新闻")

        # 5. 发送邮件
        logger.info("📧 准备发送邮件...")
        sender = EmailSender()
        success = sender.send_digest(digest)

        if success:
            logger.info("✅ 日报发送成功！")
        else:
            logger.error("❌ 日报发送失败")
            sys.exit(1)

        logger.info("=" * 60)
        logger.info("🎉 任务完成！")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"❌ 发生错误: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
