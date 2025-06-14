from linebot import LineBotApi
from linebot.models import (TemplateSendMessage, ButtonsTemplate, PostbackAction, URIAction)
import os


Channel_access_token = os.environ.get("channel_access_token")

def action_template_message(user):
    line_bot_api = LineBotApi(Channel_access_token)
    line_bot_api.push_message(user, TemplateSendMessage(
        alt_text='ButtonsTemplate',
        template=ButtonsTemplate(
            thumbnail_image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRNLpH2P2cSoh97-1UV7azRL2m-y_mcMftY2A&s',
            title='是否有填過心理諮商前導問卷?',
            text='填寫問卷有助於機器人更好地了解您的狀況',
            actions=[
                URIAction(
                    label='>沒有，我要填寫問卷<',
                    uri='https://forms.gle/D7nVGuiJAAcrsNV4A'
                ),
                PostbackAction(
                    label='>我已填寫問卷，開始諮商<',
                    text='啟動諮商機器人',
                    data='我需要幫助'
                ),
            ]
        )
    ))
