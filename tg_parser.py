"""
tg_parser.py — Универсальный скачиватель файлов из Telegram-каналов.

Использование:
    python tg_parser.py

Настройка:
    Заполни файл .env (см. .env.example).

Авторизация:
    При первом запуске Telegram попросит номер телефона и код.
    Сессия сохраняется в файл {SESSION_NAME}.session —
    повторная авторизация не нужна.
"""

import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.tl.types import DocumentAttributeFilename

# -------------------------------------------------
# Настройки
# -------------------------------------------------

load_dotenv()

API_ID           = int(os.getenv("API_ID", "0"))
API_HASH         = os.getenv("API_HASH", "")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "")
SESSION_NAME     = os.getenv("SESSION_NAME", "my_session")

# Папка для скачанных файлов
DOWNLOAD_DIR = Path("downloads")

# Фильтр по расширениям. Пустой список = скачивать всё.
# Пример: ['.pdf', '.docx', '.jpg']
FILTER_EXTENSIONS = ['.pdf']

# Лимит сообщений. None = без лимита (все сообщения канала).
LIMIT = None

# -------------------------------------------------
# Вспомогательные функции
# -------------------------------------------------

def get_filename(message) -> str | None:
    """Извлекает имя файла из сообщения Telegram."""
    if not message.document:
        return None

    # Ищем атрибут с именем файла
    for attr in message.document.attributes:
        if isinstance(attr, DocumentAttributeFilename):
            return attr.file_name

    # Если имя не задано — генерируем из ID и mime-типа
    mime = message.document.mime_type or "application/octet-stream"
    ext = mime.split("/")[-1]
    return f"document_{message.id}.{ext}"


def should_download(filename: str) -> bool:
    """Проверяет, нужно ли скачивать файл по его расширению."""
    if not FILTER_EXTENSIONS:
        return True
    suffix = Path(filename).suffix.lower()
    return suffix in FILTER_EXTENSIONS


def check_env():
    """Проверяет, что конфиг заполнен."""
    errors = []
    if not API_ID:
        errors.append("API_ID не задан")
    if not API_HASH:
        errors.append("API_HASH не задан")
    if not CHANNEL_USERNAME:
        errors.append("CHANNEL_USERNAME не задан")
    if errors:
        print("Ошибка конфига:")
        for e in errors:
            print(f"   - {e}")
        print("\nЗаполни файл .env (см. .env.example)")
        return False
    return True


# -------------------------------------------------
# Основная логика
# -------------------------------------------------

async def download_files():
    DOWNLOAD_DIR.mkdir(exist_ok=True)

    async with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        me = await client.get_me()
        print(f"Подключено к Telegram как {me.first_name}")
        print(f"Канал: {CHANNEL_USERNAME}")

        if FILTER_EXTENSIONS:
            print(f"Фильтр: {', '.join(FILTER_EXTENSIONS)}")
        else:
            print("Фильтр: все файлы")

        print("-" * 50)

        downloaded = 0
        skipped = 0
        total_checked = 0

        async for message in client.iter_messages(CHANNEL_USERNAME, limit=LIMIT):
            total_checked += 1

            filename = get_filename(message)
            if not filename:
                continue

            if not should_download(filename):
                continue

            dest = DOWNLOAD_DIR / filename

            if dest.exists():
                skipped += 1
                continue

            print(f"Скачиваю: {filename}")
            await client.download_media(message, str(dest))
            print(f"  Сохранено: {dest}")
            downloaded += 1

        print("-" * 50)
        print(f"Проверено сообщений:   {total_checked}")
        print(f"Скачано файлов:        {downloaded}")
        print(f"Пропущено (уже есть):  {skipped}")
        print(f"Папка:                 {DOWNLOAD_DIR.resolve()}")


def main():
    if not check_env():
        return
    asyncio.run(download_files())


if __name__ == "__main__":
    main()
