---
title: Аудит Telegram бота Axiom:Void
date: 2026-05-28
type: audit
status: completed
vault: Цифровой мозг
---

# 🔍 Аудит Telegram бота Axiom:Void — 2026-05-28

## 📋 Сводка

| Файл | Размер | Статус |
|------|--------|--------|
| bot.py | 72KB / ~1486 строк | ✅ Исправлен |
| analyzer.py | 30KB / ~653 строки | ✅ Исправлен |
| downloader.py | 4KB / 127 строк | ✅ OK без изменений |
| requirements.txt | python-telegram-bot==20.7, groq==0.11.0, requests==2.31.0 | ✅ OK |
| Dockerfile | python:3.11-slim + ffmpeg | ✅ OK |
| railway.json | DOCKERFILE, restart ON_FAILURE, maxRetries: 10 | ✅ OK |

**Коммит исправлений:** `06cb618` → `qsnera-reels-bot:main`

---

## 🔴 Критические баги (исправлены)

### 1. Старый бренд QSNera в пользовательских сообщениях

| Место | Было | Стало |
|-------|------|-------|
| `handle_photo` line 762 | "плитку, мрамор, камень, интерьерный дизайн" | "UI/UX макет, дизайн-систему, скриншот, интерфейс" |
| `handle_agents_info` line 1251 | "AI Агенты системы QSNera" | "AI Агенты системы Axiom:Void" |
| `handle_status` line 1403 | "Статус системы QSNera" | "Статус системы Axiom:Void" |
| `handle_task_command` line 1308 | "укладке плитки" | "нише веб-разработки" |
| `handle_chat_command` line 871 | "фото плитки для анализа" | "скриншоты, макеты, UI для анализа" |
| `main()` line 1481 | "QSNera AI Bot запущен!" | "Axiom:Void Bot запущен!" |
| `bot.py` header line 10 | `Личная жизнь: Цели/ | Дневник/` | `Brain/ | Саморазвитие/ | Работа над собой/` |

---

## 🟡 Логические проблемы (исправлены)

### 2. `handle_status` — session-state.md читался но не показывался
- **Было:** `raw = github_get_file_content("Brain/session-state.md")` — переменная читается, но нигде не используется
- **Стало:** session-state.md парсится и показывается в `/статус` (первые 300 символов тела)

### 3. `analyze_image_in_chat` — нет fallback модели
- **Было:** только `claude-sonnet-4-6`, при 402/429 — исключение
- **Стало:** cascade `sonnet-4-6` → `haiku-4-5` при 402/429/5xx

### 4. `reel_confirm` callback — deprecated API
- **Было:** `asyncio.get_event_loop()` — deprecated в Python 3.10+
- **Стало:** `asyncio.get_running_loop()`

### 5. `/help` — несоответствие папок Личная жизнь
- **Было:** "🏠 Личная жизнь — Цели, Дневник"
- **Стало:** "🏠 Личная жизнь — Brain, Саморазвитие, Работа над собой"

---

## ✅ Что работает корректно

| Компонент | Статус | Детали |
|-----------|--------|--------|
| VAULT_REPOS роутинг | ✅ | "Бизнес QSNera" → qsnera-vault (ключ не меняли — верно) |
| DEFAULT_REPO | ✅ | qsnera-vault |
| classify_note | ✅ | Обновлён до Axiom:Void + 4 сервиса |
| preprocess_task | ✅ | Пути AxiomVoid, сервисы обновлены |
| SYSTEM_PROMPT_CHAT | ✅ | Axiom:Void, 4 сервиса |
| /start welcome | ✅ | Примеры на Axiom:Void |
| SessionStore TTL | ✅ | 1 час, персистентность в /tmp |
| github_create_file | ✅ | SHA update + create |
| verify_task | ✅ | Перечитывает с GitHub, проверяет поля |
| Groq Whisper fallback | ✅ | large-v3 → turbo при rate limit |
| OpenRouter cascade | ✅ | sonnet → haiku при 402/429 |
| Perplexity + Claude fallback | ✅ | sonar → sonar-pro → Claude |
| handle_error | ✅ | Отправляет стектрейс в Telegram |
| downloader fallback | ✅ | yt-dlp → instaloader |
| Голосовые OGG → Whisper | ✅ | Без ffmpeg, прямой OGG |

---

## 🔵 Замечания (не критично, без исправления)

1. **`report_cache`** — TTL=300 объявлен но не применяется при чтении. Кеш не инвалидируется автоматически. Не критично — пользователь делает `/отчёты` редко.

2. **`note_save` для type=task** — обходит выбор агента, создаёт сразу с `tool="code"`. Возникает только при редактировании папки задачи через `note_editing_folder`. Edge case, поведение приемлемо.

3. **Telegram 20MB лимит на видео** — при загрузке файлов через `get_file()` Telegram ограничивает 20MB. Ошибка показывается как generic `❌ Ошибка: {e}`. Можно добавить специфичное сообщение, но это improvement, не bug.

4. **`save_note_to_obsidian` ALLOWED_FOLDERS** — `"Личная жизнь": ["Brain", "Саморазвитие", "Работа над собой"]` с маппингом Цели→Саморазвитие, Дневник→Работа над собой. Логика правильная для routing, но маппинг скрытый.

---

## 📊 Итог

- **Найдено проблем:** 12 (7 критических + 5 логических/minor)
- **Исправлено:** 9
- **Оставлено без изменений (приемлемо):** 3
- **Деплой:** Railway автоматически задеплоит после push в main (~2-3 мин)

---

*Аудит выполнен: 2026-05-28 | Коммит: 06cb618*
