from fastapi import FastAPI, Request
import logging
from loader import bot
from database import crud
from keyboards import inline
from config import GROUP_CHAT_ID, TOPIC_NEW_ID
from utils import format_application_text

app = FastAPI()

@app.post("/webhook")
async def receive_webhook(request: Request):
    try:
        data = await request.json()
        logging.info(f"Received webhook data: {data}")

        # Получаем сырые данные
        nickname = data.get("nickname", "")
        server = data.get("server", "")
        realname = data.get("realname", "")
        age = data.get("age", "")
        contact = data.get("contact", "")
        row_link = data.get("row_link", "")

        # 1. Создаем заявку в БД (сохраняем только сырые данные, text пустой)
        app_id = await crud.create_application(
            text="", 
            chat_id=GROUP_CHAT_ID,
            topic_id=TOPIC_NEW_ID,
            message_id=0,  # Будет обновлено после отправки сообщения
            nickname=nickname,
            server=server,
            realname=realname,
            age=age,
            contact=contact,
            spreadsheet_link=row_link
        )

        # 2. Формируем текст для отправки в Telegram
        formatted_body = format_application_text(nickname, server, realname, age, contact)
        new_text = f"⚡ НОВАЯ ЗАЯВКА #{app_id} ⚡\n\n{formatted_body}"
        
        if row_link:
            new_text += f"\n\n<a href='{row_link}'>📑 Открыть в таблице</a>"
        
        sent_message = await bot.send_message(
            chat_id=GROUP_CHAT_ID,
            text=new_text,
            message_thread_id=TOPIC_NEW_ID,
            reply_markup=inline.get_new_app_keyboard(app_id),
            parse_mode="HTML",
            disable_web_page_preview=True
        )

        # 3. Обновляем message_id в БД
        await crud.update_application(
            app_id,
            chat_id=sent_message.chat.id,
            topic_id=sent_message.message_thread_id,
            message_id=sent_message.message_id
        )

        return {"status": "ok", "app_id": app_id}
    except Exception as e:
        logging.error(f"Error processing webhook: {e}")
        return {"status": "error", "message": str(e)}
