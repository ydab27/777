import asyncio
import os
import base64
from io import BytesIO
from telethon import TelegramClient, events
from config import API_ID, API_HASH, PHONE

# Загрузка сессии
session_data = os.getenv("TELETHON_SESSION")
session_path = "/app/sessions/new_session_name.session"

if session_data:
    os.makedirs("/app/sessions", exist_ok=True)
    with open(session_path, "wb") as f:
        f.write(base64.b64decode(session_data))
    print("✅ Сессия успешно загружена из переменной окружения.")
else:
    print("❌ Ошибка: Переменная TELETHON_SESSION пуста!")
    exit(1)

# Инициализация клиента
client = TelegramClient(session_path, API_ID, API_HASH)

# Настройки
CHANNEL_USERNAME = '@ZHZAGROZA'
MEDIA_FOLDER = '/app/Telethon_Media'
os.makedirs(MEDIA_FOLDER, exist_ok=True)

KEYWORDS = [
    'ракетная атака', 'повітряна тривога', 'воздушная тревога', 'Житомир', 'БпЛА',
    'Озерне', 'Житомира', 'Житомирщина', 'Житомщину', 'Житомщини', 'Житомську',
    'Житомської', 'Житомирська область', 'Балістика', 'Загроза балістики', 'Мопеди',
    'Шахеди', 'Шахеды', 'мопеды', 'шахедов', 'шахедів', 'мопедов', 'мопеди',
    'мопед', 'шахед', 'ракета', 'ракеты', 'балістики', 'КАБ', 'ракетой',
    'ракетна небезпека', 'балистикой', 'ту-95', 'Ту-22М3', 'Ціль на', 'Цель на',
    'Втрати військ росії', 'Актуальна карта повітряних тривог', 'Відбій тривоги'
]

NEGATIVE_KEYWORDS = [
    'юмор', 'мем', 'анекдот', 'реклама', 'котик', 'котики', 'розіграш', 'конкурс', 'погода', 'афіша', 'гороскоп',
    'цитата', 'знижка', 'акція', 'на щиті', 'коляски'
]

# Список каналов (можешь потом снова подключить фильтр по ним)
MONITORED_CHANNELS = [
    '@INSIDERUKR', '@BLYSKAVKA_UA', '@VANEK_NIKOLAEV', '@MON1TOR_UA',
    '@ZHYTO_BEST', '@KUDY_LETYT', '@ALARMUKRAINE', '@RAKETA_TREVOGA'
]

print("📡 Бот подписан и слушает сообщения...")

@client.on(events.NewMessage)  # для теста: без filters по chat
async def handler(event):
    print("🔥 Сработал обработчик события!")
    message = event.message.text or ""
    print(f"📨 Получено сообщение: {message}")

    lower_message = message.lower()

    # Фильтр по минус-словам
    for neg in NEGATIVE_KEYWORDS:
        if neg in lower_message:
            print(f"🚫 Минус-слово '{neg}' — сообщение пропущено.")
            return

    # Поиск ключевых слов
    for keyword in KEYWORDS:
        if keyword.lower() in lower_message:
            file_path = None
            if event.message.media:
                try:
                    file_path = await client.download_media(event.message.media, MEDIA_FOLDER)
                    print(f"📁 Медиа сохранено: {file_path}")
                except Exception as e:
                    print(f"⚠️ Ошибка при загрузке медиа: {e}")

            try:
                if file_path:
                    await client.send_file(CHANNEL_USERNAME, file_path, caption=f"🚨 Новини: {message}")
                else:
                    await client.send_message(CHANNEL_USERNAME, f"🚨 Новини: {message}")
                print("✅ Сообщение отправлено в канал.")
            except Exception as e:
                print(f"❌ Ошибка при отправке: {e}")
            break  # чтобы не дублировать, если сработало одно ключевое слово

async def main():
    await client.start()
    print("🤖 Бот подключён.")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())

