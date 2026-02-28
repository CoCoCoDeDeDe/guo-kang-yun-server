# app/services/email.py
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr
from typing import List

from app.core.config import settings

# 初始化邮件连接配置
conf = ConnectionConfig(
  MAIL_USERNAME=settings.MAIL_USERNAME,
  MAIL_PASSWORD=settings.MAIL_PASSWORD,
  MAIL_FROM=settings.MAIL_FROM,
  MAIL_PORT=settings.MAIL_PORT,
  MAIL_SERVER=settings.MAIL_SERVER,
  MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
  MAIL_STARTTLS=settings.MAIL_STARTTLS,
  MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
  USE_CREDENTIALS=settings.USE_CREDENTIALS,
  VALIDATE_CERTS=settings.VALIDATE_CERTS
)

async def send_warning_email(emails: List[EmailStr], warning_title: str, content: str):
  """
  异步发送 HTML 格式的预警邮件给全体用户
  """
  if not emails:
    print("没有可发送的用户邮箱。")
    return

  # 简单的 HTML 邮件模板，看起来更正式
  html_content = f"""
  <div style="padding: 20px; background-color: #fce4e4; border-radius: 8px; font-family: 'Microsoft YaHei', sans-serif;">
    <h2 style="color: #d9534f;">🚨 病虫害紧急预警</h2>
    <p style="font-size: 16px; color: #333;"><strong>影响范围/标题：</strong> {warning_title}</p>
    <p style="font-size: 16px; color: #333;"><strong>防治建议：</strong></p>
    <p style="font-size: 15px; color: #555; line-height: 1.6; background-color: #fff; padding: 15px; border-radius: 4px;">
      {content}
    </p>
    <hr style="border: 1px solid #ecc8c8; margin: 20px 0;" />
    <p style="font-size: 12px; color: #999;">此邮件由果康云系统自动广播，请勿直接回复。做好病虫害防治，祝您丰收！</p>
  </div>
  """

  # 组装邮件内容
  message = MessageSchema(
    subject=f"【果康云】病虫害预警：{warning_title}",
    recipients=emails,       # fastapi-mail 支持批量发送，直接传入列表即可
    body=html_content,
    subtype=MessageType.html   # 指定邮件格式为 HTML
  )

  fm = FastMail(conf)
  try:
    await fm.send_message(message)
    print(f"✅ 成功向 {len(emails)} 名果农发送真实预警邮件！")
  except Exception as e:
    print(f"❌ 邮件发送失败: {e}")