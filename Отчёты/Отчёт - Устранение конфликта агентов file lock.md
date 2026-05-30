---
task: Устранить конфликт между local-agent.sh и telegram-worker.py v2
date: 2026-05-30
status: completed
duration: 15min
source: local-claude-code
tags: [выполнено, agents, locking, crash-recovery]
---

# Отчёт: Устранение конфликта агентов — file lock

**Дата:** 2026-05-30 | **Приоритет:** высокий

---

## Анализ проблемы

Оба агента уже имели `mkdir`-блокировки (атомарные на POSIX), но **не было recovery от зависших блокировок**:
- Если агент падал/убивался (SIGKILL, sleep Mac), `.lock` директория оставалась навсегда
- Задача застревала в `status: processing` и никогда больше не обрабатывалась

## Что сделано

### local-agent.sh
1. **Stale lock cleanup** — добавлен блок после heartbeat (каждые 5 мин):
   - Сканирует `Задачи/*.md.lock`
   - Проверяет PID из `lock/pid` — жив ли процесс
   - Если PID мёртв **или** блокировка старше 35 мин (TASK_TIMEOUT+300) → удаляет lock
   - Сбрасывает `status: processing → delegated`
2. **PID-файл при создании блокировки** — `echo "$$" > "${LOCK_DIR}/pid"`
3. **Обновление PID после запуска subshell** — `echo "$!" > "${LOCK_DIR}/pid"` (родитель обновляет на PID subshell)

### telegram-worker.py
1. **`cleanup_stale_locks()`** — новая функция с аналогичной логикой:
   - PID-проверка через `os.kill(pid, 0)`
   - Time-based fallback (35 мин)
   - Сброс статуса и удаление lock
2. **PID-файл** — `(lock_dir / "pid").write_text(str(os.getpid()))` при создании блокировки
3. **Вызов каждые ~64 сек** — `if _stale_check_counter % 8 == 0: cleanup_stale_locks()`

## Тест

Создан синтетический стейл: lock директория с PID=99999 (не существует), mtime=-2ч.
Запущен `local-agent.sh` → лог подтвердил:
```
🧹 Зависшая блокировка удалена (7207с, PID=99999): test-stale-lock.md
🔄 Статус сброшен: processing → delegated: test-stale-lock.md
```

## Изменённые файлы

- `~/.claude/agents/local-agent.sh` — stale cleanup + PID-файл
- `~/.claude/agents/telegram-worker.py` — `cleanup_stale_locks()` + PID-файл + вызов в главном цикле
