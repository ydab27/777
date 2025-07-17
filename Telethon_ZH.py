import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# 🔐 Получаем переменные окружения
API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")
SESSION_STRING = os.getenv("TELETHON_SESSION")

# 🚨 Проверка переменных окружения
if not API_ID or not API_HASH or not SESSION_STRING:
    print("❌ Ошибка: отсутствует одна из переменных окружения TELEGRAM_API_ID / TELEGRAM_API_HASH / TELETHON_SESSION")
    exit(1)

try:
    API_ID = int(API_ID)
except ValueError:
    print("❌ Ошибка: TELEGRAM_API_ID должен быть числом.")
    exit(1)

print("✅ Переменные окружения успешно загружены.")

# 📲 Инициализация клиента
client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# 📨 Канал для отправки
CHANNEL_USERNAME = '@POVITRYANAZZH'

# 📡 Мониторим эти каналы
MONITORED_CHANNELS = [
    '@INSIDERUKR', '@BLYSKAVKA_UA', '@VANEK_NIKOLAEV',
    '@MON1TOR_UA', '@ZHYTO_BEST', '@KUDY_LETYT',
    '@ALARMUKRAINE', '@RAKETA_TREVOGA'
]

# 🎯 Ключевые и 🚫 Минус-слова
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

# 📁 Папка для медиа
MEDIA_FOLDER = '/app/Telethon_Media'
os.makedirs(MEDIA_FOLDER, exist_ok=True)

# 📥 Обработчик сообщений
@client.on(events.NewMessage(chats=MONITORED_CHANNELS))
async def handler(event):
    msg_text = event.message.text or ""
    lower_msg = msg_text.lower()
    print(f"📨 Новое сообщение из {event.chat.username or 'неизвестно'}: {msg_text[:100]}...")

    if any(bad in lower_msg for bad in NEGATIVE_KEYWORDS):
        print("⛔ Сообщение содержит минус-слово, игнорируется.")
        return

    if any(key.lower() in lower_msg for key in KEYWORDS):
        print("✅ Найдено ключевое слово. Подготовка к отправке.")
        file_path = None

        if event.message.media:
            try:
                file_path = await client.download_media(event.message.media, MEDIA_FOLDER)
                print(f"📁 Медиа сохранено: {file_path}")
            except Exception as e:
                print(f"⚠️ Ошибка загрузки медиа: {e}")

        try:
            if file_path:
                await client.send_file(CHANNEL_USERNAME, file_path, caption=f"🚨 Новини:\n{msg_text}")
            else:
                await client.send_message(CHANNEL_USERNAME, f"🚨 Новини:\n{msg_text}")
            print("📤 Сообщение успешно отправлено в канал.")
        except Exception as e:
            print(f"❌ Ошибка при отправке в канал: {e}")

# 🧠 Главная функция
async def main():
    print("🚀 main() запущена")
    await client.start()
    print("🤖 Бот запущен и слушает...")

    try:
        dialogs = await client.get_dialogs()
        print("📋 Аккаунт видит каналы:")
        for d in dialogs:
            if d.is_channel:
                print(f" - {d.name} | @{getattr(d.entity, 'username', 'нет username')}")
    except Exception as e:
        print(f"⚠️ Не удалось получить список каналов: {e}")

    try:
        await client.send_message(CHANNEL_USERNAME, "✅ Тест: бот успешно запущен и работает.")
    except Exception as e:
        print(f"⚠️ Ошибка отправки тестового сообщения: {e}")

    await client.run_until_disconnected()

# ▶️ Запуск
if __name__ == "__main__":
    asyncio.run(main())
