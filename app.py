# -*- coding: utf-8 -*-

import re
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, LocationSendMessage
app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('cOV7xFlKlK9pMjcjLyCGVbrfVKjRtsrkpb3puKiOQJjX0x500jd409hJG2LI9DUsAxElAqdnl367/ckwVwU3szWQc20hzmwiOXdCaFFDVfT3SAO1ShRKSzGpe5it83MA5Z3Zw4UXkwiK2FSo54bXqQdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('66d3e9a98d9fda9a1a2759b900723497')

line_bot_api.push_message('Ub7fe430067da033fed91a0467d46a2d4', TextSendMessage(text='你可以開始了'))

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    if message == '告訴我秘密':  # 更高效的匹配方式
        location_message = LocationSendMessage(
            title='台中市政府',
            address='台中',
            latitude=24.162243302373087,
            longitude=120.64688666952166
        )
        line_bot_api.reply_message(event.reply_token, location_message)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))

if __name__ == "__main__":
    app.run()