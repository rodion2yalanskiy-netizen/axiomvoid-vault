---
tags: [antigravity, claude-code, mcp, интеграция, отчет]
date: 2026-05-22
status: completed
---

# 🤖 Отчёт: Настройка Antigravity ↔ Claude Code
**Дата:** 2026-05-22

---

## ✅ Что настроено автоматически

### 1. AgentAPI мост — Claude Code → Antigravity
Antigravity предоставляет `agentapi` — gRPC интерфейс для программного взаимодействия.

**Созданы скрипты:**
| Скрипт | Что делает |
|--------|-----------|
| `~/.claude/hooks/antigravity-send.sh "задача"` | Отправить задачу агенту Antigravity |
| `~/.claude/hooks/antigravity-get.sh <id>` | Проверить статус разговора |
| `~/.claude/hooks/workflow-pipeline.sh "" "задача"` | Полный цикл: задача → Antigravity → лог в Obsidian |

**Команда для Claude Code:**
```
/antigravity [описание задачи]
```

### 2. Env переменные в `~/.claude/settings.json`
```json
"env": {
  "ANTIGRAVITY_LS_ADDRESS": "127.0.0.1:53840",
  "ANTIGRAVITY_CSRF_TOKEN": "...",
  "ANTIGRAVITY_PROJECT_ID": "fe98a51a-..."
}
```
Теперь Antigravity доступен из любого Claude Code контекста.

### 3. Глобальный `~/CLAUDE.md`
Памятка по экосистеме загружается в каждой сессии Claude Code — пути, команды, стиль кода QSNera.

### 4. Тест интеграции — ✅ ПРОЙДЕН
```
~/.claude/hooks/antigravity-send.sh "тест"
→ ✅ Conversation ID: cb52819c-...
→ 📋 Залогировано в Obsidian
```

---

## ⚠️ Требует ручной настройки (только через UI Antigravity)

### MCP серверы в Antigravity
Antigravity хранит конфиг MCP серверов во внутренней БД — нет публичного config файла.  
Нужно добавить через интерфейс:

**Как добавить MCP сервер в Antigravity:**
1. Открой **Antigravity** → нажми иконку ⚙️ **Settings** (левая панель)
2. Перейди в раздел **MCP Servers** или **Tools**
3. Нажми **Add MCP Server** / **+ New**
4. Добавь следующие серверы:

**Obsidian MCP:**
```
Name: obsidian
Command: obsidian-mcp-server
Env:
  OBSIDIAN_API_KEY=9f4a98117886a89acb8d09e0e640989de2cf462f518cff2409bc0709f21860da
  OBSIDIAN_BASE_URL=https://127.0.0.1:27124
  OBSIDIAN_VERIFY_SSL=false
```

**Context7 (документация):**
```
Name: context7
Command: npx
Args: -y @upstash/context7-mcp
```

**Filesystem (vault'ы):**
```
Name: filesystem
Command: npx
Args: -y @modelcontextprotocol/server-filesystem /Users/rodionyalanskiy/Desktop/Бизнес\ QSNera /Users/rodionyalanskiy/Desktop/Цифровой\ мозг
```

---

## 🔄 Схема работы (как использовать)

```
ТЫ пишешь задачу в Obsidian
         ↓
Говоришь Claude Code: /antigravity [задача]
         ↓
Claude Code → отправляет задачу в Antigravity через agentapi
         ↓
Antigravity (Gemini) → планирует, использует Computer Use, генерирует изображения
         ↓
Результат → Claude Code выполняет код / git commit / GitHub
         ↓
Отчёт → автоматически в Obsidian
```

---

## 📊 Статус дорожной карты Неделя 4

| Задача | Статус |
|--------|--------|
| Настроить Antigravity API | ✅ Выполнено |
| Создать bridge скрипты | ✅ Выполнено |
| Протестировать связь | ✅ Выполнено |
| MCP серверы в Antigravity UI | ⚠️ Вручную (5 мин) |
| Создать субагентов | 🔜 Следующий шаг |

---

## ✅ Обновление: MCP серверы добавлены автоматически — 2026-05-22

Найден публичный config файл: `~/.gemini/config/mcp_config.json`  
Дублирован в: `~/.gemini/antigravity/mcp_config.json`

**Добавлены серверы:**
- ✅ `github-mcp-server` — уже был
- ✅ `obsidian` — добавлен
- ✅ `filesystem` — добавлен (все vault'ы + QSNera)
- ✅ `context7` — добавлен

**Подтверждение из WAL файла разговора:**
> "Listing Connected Servers... obsidian, filesystem, github, context7"

**Текущий статус Antigravity:**
⚠️ `QUOTA_EXHAUSTED` на Gemini API — сброс через ~113ч (2026-05-27). Конфигурация полностью готова.

---

## ✅ Обновление 2: QUOTA_EXHAUSTED — решено — 2026-05-22

**Проблема:** Gemini `flash` модель исчерпала квоту (сброс через 113ч).  
**Решение:** Переключён на `flash_lite` — отдельная квота, работает без ограничений.

**Тест пройден:**
- Antigravity (flash_lite) прочитал `Бизнес QSNera/Dashboard.md` через filesystem MCP ✅
- Все 7 шагов завершились со статусом 3 (COMPLETED) ✅
- QUOTA_EXHAUSTED = 0 раз ✅

**Обновления:**
- `antigravity-env.sh` — автоматически определяет порт и CSRF при каждом запуске
- `antigravity-send.sh` — теперь использует `flash_lite` по умолчанию + автопорт
- Порт больше не нужно обновлять вручную после перезапуска Antigravity
