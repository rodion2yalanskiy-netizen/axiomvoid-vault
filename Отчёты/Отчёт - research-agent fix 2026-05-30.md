---
date: 2026-05-30
type: report
status: completed
tags: [отчёт, research-agent, исправление, агенты]
---

# Отчёт — Исправление research-agent 2026-05-30

## Связи
- [[Dashboard]]

---

## Задача
Расследовать и починить `research-agent` — 2026-05-29 в 23:34 зафиксирована ошибка получения данных.

## Анализ ошибки

**Лог:** `research-agent.log` строка 29–30:
```
ERROR: 
2026-05-29 23:34 — ERROR: claude не вернул контент (exit 1)
```

**Причина:** Claude CLI вернул exit code 1 с пустым stderr. Точная причина неизвестна (скорее всего: transient API error или rate limit). Старый код логировал `result.stderr[:200]` — если stderr пустой, в лог писалась пустая строка.

**Сопутствующие проблемы:**
1. Нет retry-логики — одна неудача = 2 часа простоя
2. Нет Telegram-уведомления при ошибке — пользователь не знал
3. Захват ошибки неполный (только stderr, не stdout)

## Что исправлено

**Файл:** `~/.claude/agents/research-agent.sh`

### 1. Retry-логика (до 3 попыток)
```bash
MAX_ATTEMPTS=3
while [ $ATTEMPT -lt $MAX_ATTEMPTS ] && [ -z "$CONTENT" ]; do
    ...
    [ $ATTEMPT -lt $MAX_ATTEMPTS ] && sleep 30
done
```

### 2. Улучшенный захват ошибки
```python
err = (result.stderr or result.stdout or 'пустой ответ от claude')[:500]
```

### 3. Telegram-уведомление при ошибке
```bash
curl ... --data-urlencode "text=⚠️ research-agent: ошибка мониторинга ($DATE $TIME)
Попыток: $MAX_ATTEMPTS — все неудачны
Причина: $ERR_SHORT"
```

## Статус

Все последующие запуски (00:37, 01:34, 03:36, 05:37, 07:38, 09:39) прошли успешно — ошибка была единоразовой. Новый код обеспечит устойчивость при следующем подобном случае.

---
*Выполнено: Claude Code 2026-05-30*
