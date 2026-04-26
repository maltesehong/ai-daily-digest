import os,sys,json,logging,smtplib,feedparser
from datetime import datetime
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(message)s')
logger=logging.getLogger()
def main():
 logger.info("🤖 启动")
 config_dir=Path(__file__).parent/'config'
 with open(config_dir/'sources.json')as f:sources=json.load(f)
 with open(config_dir/'categories.json')as f:categories=json.load(f).get('categories',[])
 news=[item for source in sources for item in [{**{'title':e.get('title',''),'link':e.get('link',''),'source':source['name'],'summary':e.get('summary','')[:200]}} for e in feedparser.parse(source['url']).entries[:10]]]
 logger.info(f"采集{len(news)}条")
 cat={c['id']:[] for c in categories}
 for item in news:
  text=(item['title']+item['summary']).lower()
  for c in categories:
   if any(kw.lower()in text for kw in c.get('keywords',[])):cat[c['id']].append(item);break
 logger.info("发送邮件")
 total=sum(len(v)for v in cat.values())
 html=f'<html><body><h1>🤖 AI日报 {datetime.now().strftime("%Y年%m月%d日")}</h1><p>共{total}条</p>'
 for c in categories:
  if cat[c['id']]:html+=f"<h2>{c['emoji']} {c['name']}</h2>"
  for i,item in enumerate(cat[c['id']][:10],1):html+=f"<p>{i}. {item['title']}</p>"
 html+='</body></html>'
 msg=MIMEMultipart('alternative')
 msg['Subject']=f"🤖 AI日报 {datetime.now().strftime('%Y年%m月%d日')}"
 msg['From']=os.getenv('GMAIL_SENDER')
 msg['To']=os.getenv('RECIPIENT_EMAIL')
 msg.attach(MIMEText(html,'html','utf-8'))
 with smtplib.SMTP('smtp.gmail.com',587,timeout=10)as server:
  server.starttls()
  server.login(os.getenv('GMAIL_SENDER'),os.getenv('GMAIL_PASSWORD'))
  server.send_message(msg)
 logger.info("✅完成")
if __name__=='__main__':main()
