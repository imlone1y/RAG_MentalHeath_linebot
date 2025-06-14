from flask import Flask, request, abort
import json
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    PushMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    PostbackEvent
)
from llamaindex_merged import assistant_reply, assistant_create
from template_message import action_template_message
from chat_manager import manage_chat
import os

app = Flask(__name__)

# 設定您的 Channel Access Token 和 Channel Secret
channel_access_token = os.environ.get("channel_access_token")
channel_secret = os.environ.get("channel_secret")


# 初始化 WebhookHandler
handler = WebhookHandler(channel_secret)

# **改用字典來儲存每位使用者的 active 狀態**
active_users = {}

@app.route("/", methods=['POST'])
def callback():
    """處理 LINE Webhook 請求"""
    signature = request.headers.get('X-Line-Signature')
    body = request.get_data(as_text=True)

    if not signature:
        abort(400)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

def get_user_name(user_id):
    """從 LINE API 獲取用戶名稱"""
    config = Configuration(access_token=channel_access_token)
    with ApiClient(config) as api_client:
        messaging_api = MessagingApi(api_client)

        try:
            profile = messaging_api.get_profile(user_id)
            user_name = profile.display_name
            print(f"✅ 獲取用戶: {user_name} 的訊息")
            return user_name
        except Exception as e:
            print(f"無法獲取用戶名稱: {e}")
            return "未知使用者"  # 預設值，避免 `NoneType` 錯誤

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    """處理使用者發送的訊息"""
    user_id = event.source.user_id
    user_name = get_user_name(user_id)  # 取得使用者名稱
    message_text = event.message.text

    # 正確初始化 MessagingApi
    config = Configuration(access_token=channel_access_token)
    with ApiClient(config) as api_client:
        messaging_api = MessagingApi(api_client)

        if message_text == '!help':
            action_template_message(user_id)
        elif message_text == '!exit':
            if user_id in active_users and active_users[user_id]:  # **只關閉該使用者的 active**
                active_users[user_id] = False
                # 對話紀錄整理
                reply_message(messaging_api, event.reply_token, "離開心理諮商模式，正在儲存對話紀錄")
                manage_chat(user_id,user_name)
                push_message(messaging_api, user_id, '✅ 對話紀錄儲存成功')
            else:
                reply_message(messaging_api, event.reply_token, "您目前未在心理諮商模式。")
        elif user_id in active_users and active_users[user_id]:  # **確保只有啟動的使用者能對話**
            response_text = assistant_reply(user_id, user_name, message_text)  # **使用 user_id 獲取對應的 chat_engine**
            reply_message(messaging_api, event.reply_token, response_text)
        else:
            push_message(messaging_api, user_id, '輸入 "!help" 顯示選單')

@handler.add(PostbackEvent)
def handle_postback(event):
    """處理 Postback 事件（例如點擊選單）"""
    user_id = event.source.user_id
    user_name = get_user_name(user_id)
    postback_data = event.postback.data

    config = Configuration(access_token=channel_access_token)
    with ApiClient(config) as api_client:
        messaging_api = MessagingApi(api_client)

        if postback_data == '我需要幫助':
            active_users[user_id] = True  # **讓該使用者進入 active 模式**
            reply_message(messaging_api, event.reply_token, f"{user_name}，您的心理諮商機器人正在準備中，請稍後...")
            assistant_create(user_id, user_name)  # **創建屬於該使用者的 chat_engine**
            push_message(messaging_api, user_id, "創建完成！可以開始聊天了！(輸入 '!exit' 來結束諮商模式)")


def reply_message(messaging_api, reply_token, message_text):
    """回覆使用者訊息"""
    message = TextMessage(text=message_text)
    reply_request = ReplyMessageRequest(
        reply_token=reply_token,
        messages=[message]
    )
    messaging_api.reply_message(reply_request)

def push_message(messaging_api, user_id, message_text):
    """主動推送訊息給使用者"""
    message = TextMessage(text=message_text)
    push_request = PushMessageRequest(
        to=user_id,
        messages=[message]
    )
    messaging_api.push_message(push_request)

if __name__ == "__main__":
    app.run()
