"""
邮件发送模块 - 通过Gmail发送日报
"""

import os
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict
from datetime import datetime

logger = logging.getLogger(__name__)


class EmailSender:
    """邮件发送器"""

    def __init__(self):
        self.sender_email = os.getenv('GMAIL_SENDER', '')
        self.sender_password = os.getenv('GMAIL_PASSWORD', '')
        self.recipient_email = os.getenv('RECIPIENT_EMAIL', '')
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587

        if not all([self.sender_email, self.sender_password, self.recipient_email]):
            logger.warning("⚠️ 邮件配置不完整，请检查环境变量")

    def send_digest(self, digest: Dict) -> bool:
        """发送日报邮件"""
        try:
            subject = f"🤖 AI 行业日报 - {digest['date']}"
            html_content = self._generate_html(digest)

            # 创建邮件
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = self.sender_email
            message['To'] = self.recipient_email

            # 添加HTML内容
            message.attach(MIMEText(html_content, 'html', 'utf-8'))

            # 发送邮件
            logger.info(f"正在发送邮件到: {self.recipient_email}")
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)

            logger.info("✅ 邮件发送成功")
            return True

        except Exception as e:
            logger.error(f"❌ 邮件发送失败: {str(e)}")
            return False

    def _generate_html(self, digest: Dict) -> str:
        """生成HTML格式的日报"""
        items_html = ""

        for category_name, items in digest['items'].items():
            items_html += f"""
            <div style="margin: 20px 0; border-left: 4px solid #4F46E5; padding-left: 15px;">
                <h3 style="color: #4F46E5; margin-top: 0;">{category_name}</h3>
            """

            for idx, item in enumerate(items[:10], 1):  # 每个分类最多显示5条
                items_html += f"""
                <div style="margin-bottom: 12px; padding-bottom: 12px; border-bottom: 1px solid #E5E7EB;">
                    <p style="margin: 0 0 5px 0;">
                        <strong>{idx}. {item['title']}</strong>
                    </p>
                    <p style="margin: 0 0 5px 0; color: #666; font-size: 13px;">
                        {item.get('summary', 'No summary')}
                    </p>
                    <p style="margin: 0; font-size: 12px; color: #999;">
                        来源: {item['source']} |
                        <a href="{item['link']}" style="color: #4F46E5; text-decoration: none;">查看原文</a>
                    </p>
                </div>
                """

            items_html += "</div>"

        html_content = f"""
        <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body {{
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                        line-height: 1.6;
                        color: #333;
                        max-width: 800px;
                        margin: 0 auto;
                        padding: 20px;
                        background-color: #F9FAFB;
                    }}
                    .container {{
                        background-color: #FFFFFF;
                        border-radius: 8px;
                        padding: 30px;
                        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                    }}
                    .header {{
                        text-align: center;
                        border-bottom: 2px solid #4F46E5;
                        padding-bottom: 20px;
                        margin-bottom: 30px;
                    }}
                    .header h1 {{
                        color: #4F46E5;
                        margin: 0;
                        font-size: 28px;
                    }}
                    .date {{
                        color: #666;
                        font-size: 14px;
                        margin-top: 5px;
                    }}
                    .stats {{
                        background-color: #F0F4FF;
                        border-radius: 6px;
                        padding: 15px;
                        margin-bottom: 30px;
                        text-align: center;
                        color: #4F46E5;
                        font-weight: bold;
                    }}
                    .footer {{
                        text-align: center;
                        margin-top: 30px;
                        padding-top: 20px;
                        border-top: 1px solid #E5E7EB;
                        color: #999;
                        font-size: 12px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🤖 AI 行业日报</h1>
                        <div class="date">{digest['date']}</div>
                    </div>

                    <div class="stats">
                        📊 今日共收集 {digest['total_count']} 条相关新闻
                    </div>

                    {items_html}

                    <div class="footer">
                        <p>来自 AI Daily Digest | 自动生成 | 订阅地址: <a href="https://github.com/yourusername/ai-daily-digest" style="color: #4F46E5;">GitHub</a></p>
                    </div>
                </div>
            </body>
        </html>
        """

        return html_content
