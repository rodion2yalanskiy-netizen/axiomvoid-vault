---
date: 2026-05-30
status: done
task: Расследовать и починить research-agent (ошибка 23:34)
tags: [отчёт, агент, research-agent, отладка]
---

# Отчёт: Починка research-agent

## Проблема

2026-05-29 в 23:34 зафиксировано:
```
2026-05-29 23:34 — research-agent START
2026-05-29 23:34 — файл уже есть, дополняем
ERROR: 
2026-05-29 23:34 — ERROR: claude не вернул контент (exit 1)
```

## Диагноз

- Ошибка от **старой версии** скрипта (до добавления retry)
- Claude CLI вернул `exit 1` с пустым stderr — скорее всего transient API error
- Старый скрипт: 1 попытка → провал → 2 часа простоя без уведомления
- `Terminated: 15` шум в err.log — `kill $KILLPID` без `wait`

## Что сделано

### 1. Классификация ошибок (`check_network()`)
При каждом провале теперь выполняется `curl https://api.anthropic.com` для определения типа:
- `нет сети/Anthropic недоступен`
- `таймаут (>200s)`
- `rate limit API` (stderr содержит 429)
- `API ошибка (exit N)`
- `пустой ответ`

### 2. Экспоненциальный backoff
Задержка между попытками: 30s → 60s → 120s (было: всегда 30s)

### 3. Очистка "Terminated: 15" шума
```bash
# Было:
kill $KILLPID 2>/dev/null
# Стало:
{ kill $KILLPID 2>/dev/null; wait $KILLPID 2>/dev/null; } 2>/dev/null
```

### 4. Улучшенный Telegram при ошибке
```
⚠️ research-agent: ошибка мониторинга (2026-05-29 23:34)
Попыток: 3 — все неудачны
Тип: нет сети/Anthropic недоступен
Детали: ERROR[exit=1]: ...
```

## Файл

`~/.claude/agents/research-agent.sh`

## Статус

Синтаксис проверен (`bash -n`). Следующий запуск покажет работу новой логики.
