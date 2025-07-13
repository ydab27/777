import os
import base64
import asyncio
from telethon import TelegramClient, events
from config import API_ID, API_HASH, PHONE

# Инициализация путей и папок
session_data = os.getenv("TELETHON_SESSION")
session_path = "/app/sessions/new_session_name.session"
media_folder = '/app/Telethon_Media'
os.makedirs("/app/sessions", exist_ok=True)
os.makedirs(media_folder, exist_ok=True)

# Загружаем session
if session_data:
    with open(session_path, "wb") as f:
        f.write(base64.b64decode(session_data))
    print("✅ Сессия успешно загружена.")
else:
    print("❌ Ошибка: переменная TELETHON_SESSION пуста!")
    exit(1)

# Настройки
client = TelegramClient(session_path, API_ID, API_HASH)
CHANNEL_USERNAME = '@ZHZAGROZA'

# Каналы для мониторинга
MONITORED_CHANNELS = [
    '@INSIDERUKR', '@BLYSKAVKA_UA', '@VANEK_NIKOLAEV',
    '@MON1TOR_UA', '@ZHYTO_BEST', '@KUDY_LETYT',
    '@ALARMUKRAINE', '@RAKETA_TREVOGA'
]

# Ключевые и минус-слова
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
    'юмор', 'мем', 'анекдот', 'реклама', 'котик', 'котики', 'підписуйся',
    'підпишись', 'розіграш', 'конкурс', 'погода', 'афіша', 'гороскоп',
    'цитата', 'знижка', 'акція', 'на щиті', 'коляски'
]

# Обработчик новых сообщений
@client.on(events.NewMessage(chats=MONITORED_CHANNELS))
async def handler(event):
    print("🔥 Сработал обработчик")
    msg_text = event.message.text or ""
    lower_msg = msg_text.lower()
    print(f"📨 Получено сообщение: {msg_text}")

    # Проверка на минус-слова
    for bad in NEGATIVE_KEYWORDS:
        if bad in lower_msg:
            print(f"⛔ Минус-слово '{bad}' — сообщение игнорируется.")
            return

    # Поиск ключевых слов
    for key in KEYWORDS:
        if key.lower() in lower_msg:
            print(f"✅ Найдено ключевое слово: {key}")

            # Попытка скачать медиа
            file_path = None
            if event.message.media:
                try:
                    file_path = await client.download_media(event.message.media, media_folder)
                    print(f"📁 Медиа сохранено: {file_path}")
                except Exception as e:
                    print(f"⚠️ Ошибка при скачивании медиа: {e}")

            # Отправка в Telegram канал
            try:
                if file_path:
                    await client.send_file(CHANNEL_USERNAME, file_path, caption=f"🚨 Новини:\n{msg_text}")
                else:
                    await client.send_message(CHANNEL_USERNAME, f"🚨 Новини:\n{msg_text}")
                print("📤 Сообщение отправлено в канал.")
            except Exception as e:
                print(f"❌ Ошибка при отправке: {e}")
            break

# Основная функция
async def main():
    await client.start()
    print("🤖 Бот запущен и слушает...")

    # Проверка подписки — вывод всех доступных каналов
    dialogs = await client.get_dialogs()
    print("📋 Аккаунт видит каналы:")
    for d in dialogs:
        if d.is_channel:
            print(f" - {d.name} | @{getattr(d.entity, 'username', 'нет username')}")

    # Тестовое сообщение (можно закомментировать)
    try:
        await client.send_message(CHANNEL_USERNAME, "✅ Тест: бот успешно запущен и работает.")
    except Exception as e:
        print(f"❌ Ошибка отправки теста: {e}")

    await client.run_until_disconnected()

# Запуск
if __name__ == "__main__":
    asyncio.run(main())
