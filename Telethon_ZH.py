from telethon import TelegramClient, events
from config import API_ID, API_HASH, PHONE
import os
import base64
from io import BytesIO

# Переменные окружения  новго
session_data = os.getenv("TELETHON_SESSION")  # Получаем сессию из переменных окружения
session_path = "/app/sessions/new_session_name.session"

# Создаём папку для сессии


# Декодируем и восстанавливаем файл сессии, если он есть
if session_data:
    os.makedirs("/app/sessions", exist_ok=True)
    with open(session_path, "wb") as f:
        f.write(base64.b64decode(session_data))
    print("Сессия успешно загружена из переменной окружения.")
else:
    print("Ошибка: Переменная TELETHON_SESSION пуста!")
    exit(1)

# Инициализируем клиент Telethon
client = TelegramClient(session_path, API_ID, API_HASH)

# Настройки бота
CHANNEL_USERNAME = '@ZHZAGROZA'
KEYWORDS = ['ракетная атака', 'повітряна тривога', 'воздушная тревога', 'Житомир', 'БпЛА', 
    'Житомирі та області повітряна тривога', 'Озерне', 'Житомира', 'Житомирщина', 
    'Житомщину', 'Житомщини', 'Житомську', 'Житомської', 'Житомирська область', 
    'Житомська', 'Балістика', 'Загроза балістики', 'Мопеди', 'Шахеди', 'Шахеды', 
    'Мопеды', 'Шахедов', 'Мопедов', 'мопедов', 'шахедов', 'шахедів', 'мопеди', 
    'шахеди', 'шахеды', 'мопеды', 'мопед', 'шахед', 'мопеда', 'шахеда', 'Шахед', 
    'Мопед', 'ракета', 'ракети', 'ракеты', 'ракет', 'балістики', 'Швидкісна ціль', 
    'Балістики', 'балістикою', 'балістичного', 'КАБ', 'ракетою', 'ракетой', 
    'ракетна небезпека', 'балистикой', 'балистики', 'балістичних', 'подлетает к', 
    'підлітає до', 'ту-95мс', 'ту-95м3', 'Ту-22М3', 'Взлет', 'Взліт', 'Ціль на', 
    'Цель на', 'Втрати військ росії станом', 'тактичної авіації', 'носії калібрів', 
    'Актуальна карта повітряних тривог', 'Відбій тривоги', 'Втрати військ росії']
MONITORED_CHANNELS = ['@INSIDERUKR', '@BLYSKAVKA_UA', '@VANEK_NIKOLAEV', '@MON1TOR_UA', '@ZHYTO_BEST', 
    '@KUDY_LETYT', '@ALARMUKRAINE', '@RAKETA_TREVOGA']
NEGATIVE_KEYWORDS = [
    'юмор', 'мем', 'анекдот', 'реклама', 'котик', 'котики', 'підписуйся', 'підпишись', 
    'розіграш', 'конкурс', 'прогноз погоди', 'афіша', 'цитата', 'гороскоп', 'погода',
    'гороскопи', 'знижка', 'акція', 'розпродаж', 'на щиті'
]
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

    # Пропускаем, если содержит минус-слова
    for neg_word in NEGATIVE_KEYWORDS:
        if neg_word in message:
            print(f"Сообщение содержит минус-слово '{neg_word}', пропускаем.")
            return  # Выходим из обработчика, не обрабатываем сообщение

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

async def main():
    await client.connect()
    print("Бот подключен!")

    # Запуск основного цикла обработки сообщений
    print("Бот слушает сообщения...")
    
    # Ждём, пока бот будет работать (обработчики уже активны)
    await client.run_until_disconnected()

    # Это сообщение отправится **только после завершения работы бота**, что не совсем корректно.
    # Перенеси `await client.send_message(...)` внутрь `handler`, если хочешь тестировать отправку сразу.

with client:
    client.loop.run_until_complete(main())

