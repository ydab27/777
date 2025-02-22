from telethon import TelegramClient, events
from config import API_ID, API_HASH, PHONE  # Импортируем api_id и api_hash из config.py
import os

# Переменные настройки
CHANNEL_USERNAME = '@ZHZAGROZA'  # Укажите ваш канал, куда бот будет отправлять сообщения
KEYWORDS = [
    'ракетная атака', 'повітряна тривога', 'воздушная тревога', 'Житомир', 'БпЛА', 
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
    'Актуальна карта повітряних тривог', 'Відбій тривоги', 'Втрати військ росії'
]
MONITORED_CHANNELS = [
    '@INSIDERUKR', '@BLYSKAVKA_UA', '@VANEK_NIKOLAEV', '@MON1TOR_UA', '@ZHYTO_BEST', 
    '@KUDY_LETYT', '@ALARMUKRAINE', '@RAKETA_TREVOGA'
]  # Каналы для мониторинга

# Папка для сохранения изображений
MEDIA_FOLDER = '/app/Telethon_Media'
os.makedirs(MEDIA_FOLDER, exist_ok=True)

SESSION_DIR = '/app/sessions'
session_file = os.path.join(SESSION_DIR, 'session_name.session')
#if os.path.exists(session_file):
#   os.remove(session_file)
#   print("Сессионный файл удален.")

# Создаем клиент Telethon
client = TelegramClient('new_session_name', API_ID, API_HASH)

# Обработчик новых сообщений
@client.on(events.NewMessage(chats=MONITORED_CHANNELS))
async def handler(event):
    try:
        # Проверка, есть ли текст в сообщении
        if not event.message.text:
            print("Сообщение не содержит текста, пропускаем.")
            return
        
        message = event.message.text.lower()  # Преобразуем текст в нижний регистр
        print(f"Получено сообщение: {event.message.text}")
        
        # Проверяем, есть ли ключевые слова в сообщении
        for keyword in KEYWORDS:
            print(f"Проверка на ключевое слово: {keyword}")
            if keyword.lower() in message:
                # Проверяем наличие медиа в сообщении
                file_path = None
                if event.message.media:
                    try:
                        file_path = await client.download_media(event.message.media, MEDIA_FOLDER)
                        print(f"Медиа сохранено: {file_path}")
                    except Exception as e:
                        print(f"Ошибка при скачивании медиа: {e}")

                # Отправляем сообщение в канал через Telethon
                try:
                    if file_path:
                        # Отправляем текст и изображение
                        await client.send_file(CHANNEL_USERNAME, file_path, caption=f"Новина на тему '{keyword}':\n{event.message.text}")
                    else:
                        # Отправляем только текст
                        await client.send_message(CHANNEL_USERNAME, f"Новина на тему '{keyword}':\n{event.message.text}")
                    print(f"Сообщение отправлено: {event.message.text}")
                except Exception as e:
                    print(f"Ошибка при отправке сообщения в канал: {e}")
                break  # Останавливаем проверку, если нашли ключевое слово
    except Exception as e:
        print(f"Ошибка при обработке события: {e}")

# Запуск клиента
print("Бот запущен и мониторит каналы...")
client.start(phone=PHONE)  # Здесь передаем телефон
client.run_until_disconnected()
