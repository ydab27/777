from telethon import TelegramClient, events
from config import API_ID, API_HASH, PHONE
import os
import base64
from io import BytesIO

# Переменные окружения  новго
session_data = os.getenv("TELETHON_SESSION")  # Получаем сессию из переменных окружения
session_path = "/app/sessions/new_session_name.session"

# Создаём папку для сессии
os.makedirs("/app/sessions", exist_ok=True)

# Декодируем и восстанавливаем файл сессии, если он есть
if session_data:
    session_stream = BytesIO(base64.b64decode(session_data))
    print("Сессия успешно загружена из переменной окружения.")
else:
    print("Ошибка: Переменная TELETHON_SESSION пуста!")
    exit(1)

# Инициализируем клиент Telethon
client = TelegramClient(session_path, API_ID, API_HASH)

# Настройки бота
CHANNEL_USERNAME = '@ZHZAGROZA'
KEYWORDS = ['ракетная атака', 'повітряна тривога', 'воздушная тревога', 'Житомир']
MONITORED_CHANNELS = ['@INSIDERUKR', '@BLYSKAVKA_UA', '@VANEK_NIKOLAEV']

# Папка для сохранения медиа
MEDIA_FOLDER = '/app/Telethon_Media'
os.makedirs(MEDIA_FOLDER, exist_ok=True)

print("Бот подписан на каналы и слушает сообщения...")
# Обработчик новых сообщений
@client.on(events.NewMessage(chats=MONITORED_CHANNELS))
async def handler(event):
    message = event.message.text.lower() if event.message.text else ""
    print("Новое сообщение в отслеживаемом канале!")
    print(f"Получено сообщение: {message}")

    for keyword in KEYWORDS:
        if keyword.lower() in message:
            file_path = None
            if event.message.media:
                try:
                    file_path = await client.download_media(event.message.media, MEDIA_FOLDER)
                    print(f"Медиа сохранено: {file_path}")
                except Exception as e:
                    print(f"Ошибка скачивания медиа: {e}")

            try:
                if file_path:
                    await client.send_file(CHANNEL_USERNAME, file_path, caption=f"Новость: {event.message.text}")
                else:
                    await client.send_message(CHANNEL_USERNAME, f"Новость: {event.message.text}")
                print("Сообщение отправлено")
            except Exception as e:
                print(f"Ошибка отправки сообщения: {e}")
            break  # Останавливаем проверку, если нашли ключевое слово

# Запуск бота
print("Бот запущен...")
client.start(phone=PHONE)
async def test_send():
    await client.send_message(CHANNEL_USERNAME, "Тестовое сообщение от бота на Railway!")

with client:
    client.loop.run_until_complete(test_send())

client.run_until_disconnected()

