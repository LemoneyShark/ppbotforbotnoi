from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
#from jwt import InvalidSignatureError
from linebot import LineBotApi, WebhookHandler
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, 
    TemplateSendMessage, ButtonsTemplate, 
    QuickReply, QuickReplyButton, CarouselTemplate, 
    CarouselColumn, URITemplateAction
)
from linebot.models import MessageAction

app = FastAPI()

LINE_CHANNEL_ACCESS_TOKEN = "pdRdO+rCJ9iaAxxYpHSTPicSGchi2zzoTGJ1fNY56zL3ELj66NUJ3dCpr1PXLJIuuNcYKQcLvqGONReHsayIOjT6v8+dgnx/vzg3I6erJUsulbhWyUken4RIFctoww0EtU6QiGG0NnTiK0zVC2WZEQdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "94d9d3da2b59a6f79aea93944cd404a5"

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.post("/callback")
async def callback(request: Request):
    body = await request.body()
    signature = request.headers["X-Line-Signature"]

    try:
        handler.handle(body.decode('utf-8'), signature)
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    return JSONResponse(content={"status": "ok"})

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event: MessageEvent):
    if event.message.text.lower() == "buttons":
        buttons_template = ButtonsTemplate(
            title='Profile Facebook',
            text='Description',
            actions=[
                URITemplateAction(label='Link', uri='https://www.facebook.com/phiraphat.thiangtit'),
                QuickReplyButton(action=TextSendMessage(label='Quick Reply', text='Quick Reply Selected')),
            ]
        )
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(alt_text='Buttons Template', template=buttons_template)
        )


    elif event.message.text.lower() == "quick reply":
        quick_reply = QuickReply(items=[
            QuickReplyButton(action=MessageAction(label='buttons', text='buttons')),
            QuickReplyButton(action=MessageAction(label='carousel', text='carousel'))
        ])
        
        message = TextSendMessage(
            text='Choose an option:', 
            quick_reply=quick_reply
        )
        
        line_bot_api.reply_message(event.reply_token, message)

    elif event.message.text.lower() == "carousel":
        carousel_template = CarouselTemplate(columns=[
            CarouselColumn(
                thumbnail_image_url='https://th.portal-pokemon.com/play/resources/pokedex/img/pm/0783062d0d860b8ae7d8e859241a700359c4d981.png',
                title='โคดัก',
                text='หงุดหงิดกับอาการปวดหัวอยู่เสมอ พออาการปวดหัวรุนแรงขึ้นจะเริ่มใช้พลังลึกลับ',
                actions=[
                    URITemplateAction(label='Go to Pokedex', uri='https://th.portal-pokemon.com/play/pokedex/0054')
                ]
            ),
            CarouselColumn(
                thumbnail_image_url='https://th.portal-pokemon.com/play/resources/pokedex/img/pm/5794f0251b1180998d72d1f8568239620ff5279c.png',
                title='เซนิกาเมะ',
                text='หลังจากเกิดมาแล้วหลังจะพองจนกลายเป็นกระดองแข็งๆ',
                actions=[
                    URITemplateAction(label='Go to Pokedex', uri='https://th.portal-pokemon.com/play/pokedex/0007')
                ]
            )
        ])
        line_bot_api.reply_message(
            event.reply_token,
            TemplateSendMessage(alt_text='Carousel Template', template=carousel_template)
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Send 'buttons', 'quick reply', or 'carousel'")
        )
        
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
