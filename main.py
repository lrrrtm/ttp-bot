import asyncio
import logging
import uvicorn
from loader import dp, bot
from database.db import init_db
import handlers.commands
import handlers.admin
import handlers.callbacks
import handlers.group
import handlers.private
from config import GROUP_CHAT_ID, TOPIC_SERVICE_MESSAGES_ID
from api import app

async def start_api():
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    logging.basicConfig(level=logging.INFO)
    print("Инициализация базы данных...")
    await init_db()
    
    try:
        await bot.send_message(
            chat_id=GROUP_CHAT_ID, 
            message_thread_id=TOPIC_SERVICE_MESSAGES_ID, 
            text="🔄 Бот был перезапущен",
            disable_notification=True
        )
    except Exception as e:
        logging.error(f"Не удалось отправить сообщение о перезапуске: {e}")

    print("Бот запущен. Нажми Ctrl+C для остановки.")
    
    # Запускаем бота и API параллельно
    await asyncio.gather(
        dp.start_polling(bot),
        start_api()
    )

if __name__ == "__main__":
    asyncio.run(main())
