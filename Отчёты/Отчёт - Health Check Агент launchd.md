---
date: 2026-05-30
status: completed
type: report
---

# Отчёт: Health Check Агент для launchd

## Что сделано

Создан единый скрипт мониторинга всех 14 com.axiomvoid.* launchd агентов.

### Новые файлы
- `~/.claude/agents/health-check.sh` — скрипт проверки
- `~/Library/LaunchAgents/com.axiomvoid.health-check.plist` — launchd задание (каждые 30 мин)

### Логика проверки

**KeepAlive агенты** (telegram-worker) — проверяется наличие PID:
- Нет в launchctl list → уведомление
- KeepAlive=true, но нет PID → уведомление

**Периодические агенты** (остальные 13) — проверяется код выхода:
- Не загружен в launchd → уведомление
- Последний запуск завершился с ошибкой (exit ≠ 0) → уведомление

При обнаружении проблем шлёт в Telegram HTML-сообщение с именами упавших агентов.

### Параметры plist
- `StartInterval: 1800` (30 минут)
- `ProcessType: Standard` (средний приоритет, не Background)
- `Nice: 5`
- `RunAtLoad: true`

## Результат первого запуска

```
[2026-05-30 16:45:20] OK [com.axiomvoid.telegram-worker]: PID=1957
[2026-05-30 16:45:20] OK [com.axiomvoid.bug-hunter]: loaded, last exit=0
... (все 14 агентов)
[2026-05-30 16:45:20] PASS: все 14 агентов работают нормально
```

Все 14 агентов — зелёные, Telegram уведомление не отправлено (штатная работа).

## ✅ Что сработало
- `launchctl list | awk "$3 == label"` — точное совпадение без ложных срабатываний
- `source ~/.claude/.env` для получения TELEGRAM_TOKEN/ADMIN_CHAT_ID
- `curl --data-urlencode` для безопасной передачи HTML с переносами строк
- launchd plist загружен и отработал при первом RunAtLoad

## ❌ Что НЕ сработало
- (проблем не было)

## 🔄 Что осталось / улучшения
- Добавить self в список мониторинга (health-check мониторит сам себя?)
- Опционально: "зелёный отчёт" раз в день даже если всё OK
