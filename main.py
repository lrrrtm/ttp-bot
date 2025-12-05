import asyncio
import logging
from loader import dp, bot
from database.db import init_db
import handlers.commands
import handlers.admin
import handlers.callbacks
import handlers.group
import handlers.private
from config import GROUP_CHAT_ID, TOPIC_NEW_ID

async def main():
    logging.basicConfig(level=logging.INFO)
    print("Инициализация базы данных...")
    await init_db()
    
    try:
        await bot.send_message(chat_id=GROUP_CHAT_ID, message_thread_id=TOPIC_NEW_ID, text="🔄 Бот был перезапущен")
    except Exception as e:
        logging.error(f"Не удалось отправить сообщение о перезапуске: {e}")

    print("Бот запущен. Нажми Ctrl+C для остановки.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
