import os
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# === Загрузка переменных окружения ===
print("🔄 Загружаем переменные окружения...")
API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")
SESSION_STRING = os.getenv("TELETHON_SESSION")

if not SESSION_STRING:
    print("❌ Ошибка: переменная TELETHON_SESSION пуста!")
    exit(1)
else:
    print("✅ Переменные окружения успешно загружены.")

# === Конфигурация ===
CHANNEL_USERNAME = '@POVITRYANAZZH'  # канал, куда будут отправляться сообщения
MEDIA_FOLDER = '/app/Telethon_Media'
os.makedirs(MEDIA_FOLDER, exist_ok=True)

MONITORED_CHANNELS = [
    '@INSIDERUKR', '@BLYSKAVKA_UA', '@VANEK_NIKOLAEV',
    '@MON1TOR_UA', '@ZHYTO_BEST', '@KUDY_LETYT',
    '@ALARMUKRAINE', '@RAKETA_TREVOGA'
]

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

# === Обработчик новых сообщений ===
def setup_handler(client):
    @client.on(events.NewMessage(chats=MONITORED_CHANNELS))
    async def handler(event):
        print("🔥 Обнаружено новое сообщение")
        msg_text = event.message.text or ""
        lower_msg = msg_text.lower()
        print(f"📩 Текст сообщения: {msg_text[:100]}...")

        for neg in NEGATIVE_KEYWORDS:
            if neg in lower_msg:
                print(f"⛔ Содержит минус-слово: {neg}")
                return

        for key in KEYWORDS:
            if key.lower() in lower_msg:
                print(f"✅ Ключевое слово: {key}")

                file_path = None
                if event.message.media:
                    try:
                        file_path = await client.download_media(event.message.media, MEDIA_FOLDER)
                        print(f"📁 Медиа скачано: {file_path}")
                    except Exception as e:
                        print(f"⚠️ Ошибка скачивания медиа: {e}")

                try:
                    if file_path:
                        await client.send_file(CHANNEL_USERNAME, file_path, caption=f"🚨 Новини:\n{msg_text}")
                    else:
                        await client.send_message(CHANNEL_USERNAME, f"🚨 Новини:\n{msg_text}")
                    print("📤 Отправлено в канал.")
                except Exception as e:
                    print(f"❌ Ошибка отправки: {e}")
                break

# === Главная функция ===
async def main():
    print("🚀 main() запущена")
    try:
        client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
        await client.start()
        print("🤖 Клиент Telegram запущен")

        print("📋 Получаем список каналов...")
        dialogs = await client.get_dialogs()
        for d in dialogs:
            if d.is_channel:
                print(f"• Канал: {d.name} | @{getattr(d.entity, 'username', 'без username')}")

        # Устанавливаем обработчик
        setup_handler(client)
        print("🎧 Бот слушает каналы...")

        # Тестовое сообщение
        try:
            await client.send_message(CHANNEL_USERNAME, "✅ Бот запущен и готов к работе.")
            print("📨 Тестовое сообщение отправлено.")
        except Exception as e:
            print(f"❌ Не удалось отправить тест: {e}")

        await client.run_until_disconnected()

    except Exception as e:
        print(f"❌ Ошибка в main(): {e}")

# === Точка входа ===
if __name__ == "__main__":
    asyncio.run(main())
