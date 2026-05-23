---
tags: [инструменты, claude-code, openrouter, настройка]
date: 2026-05-22
status: ready
---

# OpenRouter — пошаговая настройка для Claude Code

> OpenRouter — посредник между Claude Code и моделями ИИ. Ты платишь только OpenRouter, Anthropic не знает о тебе как клиенте.

---

## Шаг 1 — Получить API-ключ

1. Зайди на [openrouter.ai/keys](https://openrouter.ai/keys)
2. Нажми **Create Key**
3. Скопируй ключ — он выглядит как `sk-or-v1-xxxxxxxxxxxx`
4. Пополни баланс на [openrouter.ai/credits](https://openrouter.ai/credits) (минимум $5)

---

## Шаг 2 — Прописать ключ в конфиге терминала

Файл `~/.bash_profile` **уже создан** и готов к заполнению.

Открой терминал и выполни:

```bash
nano ~/.bash_profile
```

Найди эти строки (они закомментированы `#`) и раскомментируй, вставив свой ключ:

```bash
export ANTHROPIC_BASE_URL="https://openrouter.ai/api/v1"
export ANTHROPIC_API_KEY="sk-or-v1-ВАШ_КЛЮЧ_ЗДЕСЬ"
```

Замени `sk-or-v1-ВАШ_КЛЮЧ_ЗДЕСЬ` на реальный ключ из Шага 1.

Сохрани: `Ctrl+O` → `Enter` → `Ctrl+X`

---

## Шаг 3 — Применить настройки

```bash
source ~/.bash_profile
```

---

## Шаг 4 — Проверить что всё работает

```bash
echo $ANTHROPIC_BASE_URL   # должно вывести: https://openrouter.ai/api/v1
claude --version            # должно запуститься без ошибок
```

---

## Шаг 5 — Проверить баланс и расходы

- Баланс: [openrouter.ai/credits](https://openrouter.ai/credits)
- Расходы по запросам: [openrouter.ai/activity](https://openrouter.ai/activity)

---

## ⚠️ Важно

- Pipeline (claude -p из launchd) использует **другое окружение** — переменные из ~/.bash_profile там не работают автоматически
- Для pipeline нужно добавить ключ в plist-файл: `~/Library/LaunchAgents/com.qsnera.obsidian-task-watcher.plist`
- Claude Code Code запросит помочь с этим когда у тебя будет ключ — просто напиши задачу в 🤖 AI Задачи

---

## Статус

- [x] ~/.bash_profile создан (2026-05-22)
- [ ] API-ключ получен на openrouter.ai
- [ ] Ключ вписан в ~/.bash_profile
- [ ] source ~/.bash_profile выполнен
- [ ] Работа в терминале через OpenRouter проверена
