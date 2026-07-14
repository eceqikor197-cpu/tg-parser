# tg_parser — Автономный Telegram-парсер

Универсальный скрипт для скачивания файлов (PDF и других) из Telegram-каналов через официальный Telegram API (Telethon).

## Структура

```
tg_parser/
├── .env              # Твои API-ключи (не коммитить!)
├── .env.example      # Шаблон конфига
├── requirements.txt  # Зависимости
├── tg_parser.py      # Основной скрипт
└── downloads/        # Папка для скачанных файлов (создаётся автоматически)
```

## Быстрый старт

### 1. Установи зависимости
```bash
pip install -r requirements.txt
```

### 2. Получи API-ключи
1. Зайди на https://my.telegram.org
2. Войди через свой номер телефона
3. Перейди в "API development tools"
4. Создай приложение → получи `api_id` и `api_hash`

### 3. Заполни `.env`
```env
API_ID=123456
API_HASH=abcdef1234567890abcdef1234567890
CHANNEL_USERNAME=@channel_name
```

### 4. Запусти
```bash
python tg_parser.py
```

При первом запуске Telegram попросит номер телефона и код подтверждения.  
Сессия сохранится в файл `.session` — повторно авторизовываться не нужно.

## Настройки в скрипте

| Параметр | Описание |
|---|---|
| `DOWNLOAD_DIR` | Папка для файлов (по умолчанию `downloads/`) |
| `FILTER_EXTENSIONS` | Расширения файлов, например `['.pdf', '.docx']` или `[]` для всего |
| `LIMIT` | Кол-во сообщений для обхода (по умолчанию без лимита) |
| `SESSION_NAME` | Имя файла сессии |

## .gitignore (рекомендуется)

```
.env
*.session
downloads/
```
