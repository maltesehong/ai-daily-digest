#!/usr/bin/env python3
import os, sys, json, logging, smtplib
from datetime import datetime
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import feedparser

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_config():
    config_dir = Path(__file__).parent / 'config'
    with open(config_dir / 'sources.json', 'r', encoding='utf-8') as f:
        sources = json.load(f)
    with open(config_dir / 'categories.json', 'r', encoding='utf-8') as f:
        categories_data = json.load(f)
        categories = categories_data.get('categories', [])
    return sources, categories

def collect_news(sources):
    news_items = []
    logger.info("🔍 开始采集新闻...")
    for source in sources:
        try:
            logger.info(f"📡 采集: {source['name']}")
            feed = feedparser.parse(source['url'])
            count = 0
            for entry in feed.entries[:10]:
                if count >= 10:
                    break
                title = entry.get('title', 'No title')
                link = entry.get('link', '')
                summary = entry.get('summary', '')[:200]
                news_items.append({'title': title, 'link': link, 'source': source['name'], 'summary': summary})
                count += 1
            logger.info(f"  ✅ 获得 {count} 条")
        except Exception as e:
            logger.warning(f"  ❌ 失败: {str(e)}")
    logger.info(f"✅ 采集完成，共 {len(news_items)} 条")
    return news_items

def categorize_news(news_items, categories):
    logger.info("🔄 开始分类...")
    categorized = {cat['id']: [] for cat in categories}
    for item in news_items:
        text = (item['title'] + ' ' + item['summary']).lower()
        best_cat = None
        for cat in categories:
            keywords = cat.get('keywords', [])
            if any(kw.lower() in text for kw in keywords):
                best_cat = cat['id']
                break
        if best_cat and best_cat in categorized:
            categorized[best_cat].append(item)
    return categorized

def send_email(categorized, categories):
    logger.info("📧 生成邮件...")
    sender_email = os.getenv('GMAIL_SENDER', '')
    sender_password = os.getenv('GMAIL_PASSWORD', '')
    recipient_email = os.getenv('RECIPIENT_EMAIL', '')
    if not all([sender_email, sender_password, recipient_email]):
        logger.error("❌ 邮件配置不完整")
        return False
    try:
        total = sum(len(items) for items in categorized.values())
        date_str = datetime.now().strftime('%Y年%m月%d日')
        html = f'<div style="font-family:Arial;max-width:800px;margin:0 auto;background:#f9fafb;padding:20px;"><div style="background:white;padding:30px;border-radius:8px;box-shadow:0 1px 3px rgba(0,0,0,0.1);"><h1 style="color:#4F46E5;margin:0;text-align:center;">🤖 AI 行业日报</h1><p style="color:#666;text-align:center;margin:10px 0 30px 0;">{date_str}</p><div style="background:#F0F4FF;padding:15px;border-radius:6px;text-align:center;color:#4F46E5;font-weight:bold;margin-bottom:30px;">📊 今日共收集 {total} 条相关新闻</div>'
        for cat in categories:
            cat_id = cat['id']
            items = categorized.get(cat_id, [])
            if items:
                html += f'<div style="margin:20px 0;border-left:4px solid #4F46E5;padding-left:15px;"><h3 style="color:#4F46E5;margin-top:0;">{cat["emoji"]} {cat["name"]}</h3>'
                for idx, item in enumerate(items[:10], 1):
                    html += f'<div style="margin-bottom:12px;padding-bottom:12px;border-bottom:1px solid #E5E7EB;"><p style="margin:0 0 5px 0;"><strong>{idx}. {item["title"]}</strong></p><p style="margin:0 0 5px 0;color:#666;font-size:13px;">{item["summary"]}</p><p style="margin:0;font-size:12px;color:#999;">来源: {item["source"]} | <a href="{item["link"]}" style="color:#4F46E5;">查看</a></p></div>'
                html += '</div>'
        html += '<div style="text-align:center;margin-top:30px;padding-top:20px;border-top:1px solid #E5E7EB;color:#999;font-size:12px;"><p>来自 AI Daily Digest</p></div></div></div>'
        logger.info("📨 发送邮件...")
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"🤖 AI 行业日报 - {date_str}"
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg.attach(MIMEText(html, 'html', 'utf-8'))
        with smtplib.SMTP(smtp_server='smtp.gmail.com', port=587, timeout=10) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        logger.info("✅ 邮件发送成功！")
        return True
    except Exception as e:
        logger.error(f"❌ 邮件发送失败: {str(e)}")
        return False

def main():
    logger.info("="*60)
    logger.info("🤖 AI Daily Digest 启动")
    logger.info(f"⏰ 执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("="*60)
    try:
        logger.info("📋 加载配置文件...")
        sources, categories = load_config()
        news_items = collect_news(sources)
        if not news_items:
            logger.warning("⚠️ 未采集到新闻")
            return
        categorized = categorize_news(news_items, categories)
        success = send_email(categorized, categories)
        if success:
            logger.info("="*60)
            logger.info("🎉 任务完成！")
            logger.info("="*60)
        else:
            logger.error("❌ 任务失败")
            sys.exit(1)
    except Exception as e:
        logger.error(f"❌ 发生错误: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
