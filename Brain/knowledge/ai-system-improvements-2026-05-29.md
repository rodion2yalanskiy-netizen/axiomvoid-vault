---
created: 2026-05-29
type: knowledge
tags: [claude-code, telegram-bot, launchd, github-actions, obsidian-sync, ai-agents]
---

# AI-система: конспект улучшений (2026-05-29)

> Исследование по 7 темам: Claude Code, launchd, Telegram бот, Obsidian Sync, AI-агенты, GitHub Actions, Claude API.

---

## 🆕 Новые возможности Claude Code (2026)

### CLI-флаги (актуальные)

```bash
# Неинтерактивный режим — для скриптов и local-agent
claude -p "промпт" --output-format json
claude -p "промпт" --output-format stream-json --verbose

# Авто-режим без подтверждений (безопасный классификатор)
claude --permission-mode auto -p "fix all lint errors"

# Ограничить инструменты при batch-запуске
claude -p "мигрируй $file" --allowedTools "Edit,Bash(git commit *)"

# Продолжить последнюю сессию
claude --continue

# Выбрать сессию из списка
claude --resume
```

### Новые возможности безопасности
- `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` — изоляция PID namespace на Linux
- `CLAUDE_CODE_SCRIPT_CAPS` — лимит вызовов скриптов в сессии
- `--exclude-dynamic-system-prompt-sections` — улучшенное кэширование промптов

### Управление контекстом (критично!)
- Контекст — главный ресурс: деградация качества при заполнении
- `/clear` — между несвязанными задачами (ОБЯЗАТЕЛЬНО)
- `/compact Focus on X` — компакция с фокусом
- `/btw вопрос` — боковой вопрос без загрязнения контекста
- `Esc + Esc` или `/rewind` — откат к чекпоинту

### Правило "3 исправления"
> Если исправлял Claude >2 раз по одному вопросу → `/clear` + переформулировать промпт с нуля. Длинная сессия с накопленными ошибками хуже чистой с лучшим промптом.

### CLAUDE.md — главный рычаг
```markdown
# Что ВКЛЮЧАТЬ:
- Bash-команды, которые Claude не угадает
- Стиль кода, отличающийся от дефолтного
- Тест-команды и раннеры
- Quirks окружения (env vars, пути)
- Архитектурные решения проекта

# Что ИСКЛЮЧАТЬ:
- То что Claude видит в коде сам
- Стандартные практики языка
- Длинные объяснения и туториалы
- Описание каждого файла
```

**Если CLAUDE.md слишком длинный — Claude игнорирует правила!** Регулярно чистить.

Импорт файлов в CLAUDE.md:
```markdown
See @README.md for overview.
- Git workflow: @docs/git-instructions.md
```

### Субагенты для изоляции контекста
```text
Use subagents to investigate how our auth system handles token refresh.
```
→ Субагент читает файлы в своём контексте, в основной приходит только summary.

```text
Use a subagent to review this code for edge cases.
```

### Паттерн Writer/Reviewer (два окна)
| Сессия A (Writer) | Сессия B (Reviewer) |
|---|---|
| `Implement rate limiter` | — |
| — | `Review @src/middleware/rateLimiter.ts. Edge cases, race conditions, existing patterns.` |
| `Адресуй этот feedback: [вывод B]` | — |

### Batch-миграция файлов
```bash
for file in $(cat files.txt); do
  claude -p "Migrate $file from React to Vue. Return OK or FAIL." \
    --allowedTools "Edit,Bash(git commit *)"
done
```

### Цикл Plan → Implement → Commit
1. Plan mode (`Ctrl+G`) — только чтение, без изменений
2. Implement — код + тесты + автозапуск тестов
3. Commit — `commit with descriptive message and open PR`

---

## 🔧 База знаний: частые ошибки и решения

### Ошибка: launchd "Operation not Allowed"
**Симптомы:** Скрипт работает из терминала, но падает через launchd  
**Причина:** macOS TCC (Transparency Consent and Control) — launchd-процесс не имеет прав доступа к защищённым папкам  
**Решение:**
```bash
# 1. Переместить скрипт и лог-файлы из Desktop/Documents в home dir
mv ~/Desktop/myscript.sh ~/scripts/myscript.sh
# Лог должен быть в ~/Library/Logs/ или ~/logs/

# 2. В plist использовать полные пути
<key>StandardOutPath</key>
<string>/Users/username/logs/agent.log</string>

# 3. Убедиться что plist лежит в правильном месте
~/Library/LaunchAgents/com.myagent.plist
```

### Ошибка: launchd PATH не находит команды
**Симптомы:** `python3: command not found`, `git: command not found` в логах launchd  
**Причина:** launchd запускает с минимальным PATH (/usr/bin:/bin:/usr/sbin:/sbin)  
**Решение:**
```xml
<!-- В plist файле добавить EnvironmentVariables -->
<key>EnvironmentVariables</key>
<dict>
  <key>PATH</key>
  <string>/usr/local/bin:/usr/bin:/bin:/opt/homebrew/bin</string>
  <key>HOME</key>
  <string>/Users/username</string>
</dict>
```
Или в bash-скрипте:
```bash
#!/bin/bash
export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
source "$HOME/.claude/.env"
```

### Ошибка: launchd скрипт не запускается (permissions)
**Симптомы:** Тихий failure, нет логов  
**Причина:** Нет execute permission или неверный shebang  
**Решение:**
```bash
chmod 755 ~/scripts/myscript.sh
# Проверить shebang (первая строка):
#!/bin/bash   # правильно
#! /bin/bash  # неправильно (пробел)

# Проверить plist синтаксис:
plutil -lint ~/Library/LaunchAgents/com.myagent.plist

# Перезагрузить агент:
launchctl unload ~/Library/LaunchAgents/com.myagent.plist
launchctl load ~/Library/LaunchAgents/com.myagent.plist

# Проверить статус:
launchctl list | grep myagent
```

### Ошибка: Telegram бот падает без перезапуска
**Симптомы:** Бот перестаёт отвечать, Railway показывает crash  
**Причина:** Необработанное исключение в handler  
**Решение — глобальный error handler:**
```python
import traceback
import html
from telegram import Update
from telegram.ext import Application, ContextTypes

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Глобальный обработчик — бот не падает никогда."""
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)
    
    # Логировать всегда
    logger.error("Exception while handling update:", exc_info=context.error)
    
    # Уведомить разработчика
    message = (
        f"Исключение:\n"
        f"<pre>{html.escape(tb_string[:3000])}</pre>"
    )
    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=message,
        parse_mode="HTML"
    )

# Регистрация:
application.add_error_handler(error_handler)
```

### Ошибка: Telegram Flood / Rate Limit (RetryAfter)
**Симптомы:** `telegram.error.RetryAfter: Flood control exceeded. Retry in X seconds`  
**Причина:** >30 сообщений/сек разным пользователям или >1 сообщение/сек одному чату  
**Решение:**
```python
from telegram.error import RetryAfter
import asyncio

async def send_with_retry(bot, chat_id, text, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await bot.send_message(chat_id=chat_id, text=text)
        except RetryAfter as e:
            if attempt < max_retries - 1:
                await asyncio.sleep(e.retry_after + 1)
            else:
                raise
```

### Ошибка: Obsidian Sync iOS "stuck" / файлы не появляются
**Симптомы:** На iPhone файлы не обновляются, иконка облака не исчезает  
**Решение (по порядку):**
```
1. В iOS Obsidian → Settings → Sync → Force full re-sync
2. Папки с иконкой ↓ → долгое нажатие → Download Now
3. Выключить iCloud для Obsidian → подождать 30 сек → включить
4. killall bird  (на Mac — перезапуск iCloud daemon)
5. Если ничего не помогло — переместить vault в новую папку iCloud
```

**Критическое правило:** Папки БЕЗ emoji!  
```
❌ 📝 Задачи/   →   ✅ Задачи/
❌ ✅ Выполнено/  →   ✅ Архив/
```
iOS Obsidian Sync ломается на Unicode-символах в именах папок.

### Ошибка: GitHub Actions — зависимости устанавливаются при каждом запуске
**Симптомы:** Workflow занимает 5+ минут, npm install каждый раз  
**Причина:** Нет кэширования зависимостей  
**Решение:**
```yaml
- name: Cache node_modules
  uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-

- name: Install dependencies
  run: npm ci  # не npm install!
```

---

## 💡 Лучшие практики для нашей системы

### local-agent.sh улучшения

**1. Давать Claude проверочные команды:**
```bash
# Вместо просто запуска задачи — добавлять в промпт:
PROMPT="$TASK_CONTENT

After completing, run: python3 -c 'import sys; print(sys.version)' to verify environment.
Return a summary with: ✅ Done / ❌ Failed + reason."
```

**2. Использовать --output-format для парсинга:**
```bash
RESULT=$(claude -p "$PROMPT" --output-format json 2>/dev/null)
STATUS=$(echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('result','')[:500])")
```

**3. Авто-режим для unattended задач:**
```bash
claude --permission-mode auto -p "$PROMPT"
```

### Telegram бот — паттерны надёжности

**Conversation state через context.user_data:**
```python
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Сохранять состояние между сообщениями
    if 'step' not in context.user_data:
        context.user_data['step'] = 'initial'
    
    step = context.user_data['step']
    # ...логика...
    context.user_data['step'] = 'next_step'
```

**Webhook vs Polling — для Railway:**
```python
# Polling надёжнее на Railway (не нужен публичный URL)
application.run_polling(
    allowed_updates=Update.ALL_TYPES,
    drop_pending_updates=True  # игнорировать накопленные при downtime
)
```

### GitHub Actions — наша оптимизация

**Разбить ai-agent.yml на параллельные jobs:**
```yaml
jobs:
  classify:
    runs-on: ubuntu-latest
    outputs:
      vault: ${{ steps.classify.outputs.vault }}
    steps:
      - id: classify
        run: echo "vault=AxiomVoid" >> $GITHUB_OUTPUT
  
  process:
    needs: classify
    runs-on: ubuntu-latest
    steps:
      - run: echo "Processing for vault ${{ needs.classify.outputs.vault }}"
```

**Path filtering — не запускать лишнее:**
```yaml
on:
  push:
    paths:
      - 'Задачи/**.md'  # только при изменении задач
```

**Явный timeout:**
```yaml
jobs:
  my-job:
    timeout-minutes: 10  # не дефолтные 6 часов!
```

**Pin actions по SHA:**
```yaml
# Безопасно:
- uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2
# Небезопасно:
- uses: actions/checkout@v4  # tag может быть перемещён
```

---

## 🚀 Идеи для улучшения системы (по приоритету)

### 1. ВЫСОКИЙ — Верификация задач в local-agent.sh
**Проблема:** Агент не знает, реально ли выполнена задача  
**Решение:** Добавить в промпт требование самопроверки
```bash
VERIFY_PROMPT="$TASK_CONTENT

IMPORTANT: After completing the task:
1. Run relevant tests or verification commands
2. Output exactly: STATUS:OK or STATUS:FAIL:reason
3. Never claim success without running a check"
```

### 2. ВЫСОКИЙ — Глобальный error handler в боте
Текущий бот, скорее всего, падает при NetworkError.  
Добавить `application.add_error_handler(error_handler)` — см. код выше.

### 3. СРЕДНИЙ — Кэширование зависимостей в GitHub Actions
Добавить `actions/cache` для pip/npm — сократит время workflow на 60%.

### 4. СРЕДНИЙ — Паттерн субагентов для сложных задач
Вместо одного большого промпта в local-agent:
```bash
# Исследовать → планировать → реализовать в отдельных вызовах
claude -p "Explore codebase and output analysis JSON" --output-format json > /tmp/analysis.json
claude -p "Given analysis: $(cat /tmp/analysis.json). Create implementation plan." > /tmp/plan.md
claude -p "Execute plan: $(cat /tmp/plan.md)" --permission-mode auto
```

### 5. СРЕДНИЙ — Self-improving: логировать метрики задач
```bash
# В local-agent.sh добавить:
echo "$(date)|$TASK_NAME|$EXIT_CODE|${DURATION}s" >> ~/.claude/agents/metrics.log
```
→ Раз в неделю daily-self-dev.sh анализирует: какие задачи падают, сколько времени занимают.

### 6. НИЗКИЙ — Obsidian Sync мониторинг
Добавить в daily-self-dev.sh проверку: сколько файлов в vault vs GitHub → расхождение = алерт.

### 7. НИЗКИЙ — `/clear` в CLAUDE.md как явное правило
Добавить в CLAUDE.md: "After completing each task, suggest /clear if context > 50% full."

---

## 📚 Ключевые инсайты по Claude API

### Claude 4.x меняет поведение!
- Старые версии: инферировал намерение, расширял запросы
- Claude 4.x: делает буквально то что написано, не больше
- **Правило:** Явно писать что "comprehensive" значит для конкретной задачи

### Промпт-инжиниринг для агентов
```
Плохо: "Улучши код"
Хорошо: "Рефактори функцию process_task() в local-agent.sh:
  - Убери дублирование между строками 45-60 и 80-95
  - Добавь retry для git push (max 3 попытки)
  - Сохрани текущее поведение логирования
  После рефакторинга запусти: bash local-agent.sh --dry-run"
```

### Цепочка промптов для сложных задач
```
Шаг 1: "Проанализируй auth flow в src/auth/"
Шаг 2: "Основываясь на анализе, спроектируй OAuth2 интеграцию"  
Шаг 3: "Реализуй дизайн из шага 2, запусти тесты"
```

### CLAUDE.md = самый высокий ROI
Одна хорошо написанная инструкция в CLAUDE.md > 100 повторных объяснений.  
Но: если файл слишком длинный — Claude игнорирует его части.

---

## 📚 Источники

- [Claude Code Best Practices (официально)](https://code.claude.com/docs/en/best-practices) — полная документация, всё о субагентах, hooks, CLAUDE.md
- [50 Claude Code Tips — Builder.io](https://www.builder.io/blog/claude-code-tips-best-practices) — практические советы
- [Claude Code Advanced 2026 — SmartScope](https://smartscope.blog/en/generative-ai/claude/claude-code-best-practices-advanced-2026/) — hooks, subagents, context management
- [PTB Exceptions & Logging — GitHub Wiki](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Exceptions,-Warnings-and-Logging) — официальная документация
- [PTB Error Handler Example](https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/errorhandlerbot.py) — готовый код
- [Obsidian Sync Troubleshoot](https://help.obsidian.md/sync/troubleshoot) — официальный гайд
- [GitHub Actions Optimization — Marcus Felling](https://marcusfelling.com/blog/2025/optimizing-github-actions-workflows-for-speed) — конкретные техники
- [AI Agent Self-Improvement — Medium](https://medium.com/@abhilasha.sinha/smart-ai-evolution-strategies-for-building-self-improving-autonomous-agents-a9978648ef9f) — паттерны
- [Agentic AI Design Patterns 2025 — Shakudo](https://www.shakudo.io/blog/5-agentic-ai-design-patterns-transforming-enterprise-operations-in-2025) — enterprise паттерны
- [Claude Prompting Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) — официальная документация

## Связи
- [[Dashboard]]
