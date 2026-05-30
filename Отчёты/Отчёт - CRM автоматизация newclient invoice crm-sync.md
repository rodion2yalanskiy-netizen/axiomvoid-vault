---
date: 2026-05-30
status: done
tags: [отчёт, crm, telegram, stripe]
---

# Отчёт: CRM автоматизация — /newclient, /invoice, crm-sync

## Что сделано

### ЗАДАЧА 1 — /newclient
- Добавлен обработчик `/newclient` в `~/Desktop/axiomvoid-bot/bot.py`
- Пошаговый диалог: имя → email → тип проекта (кнопки) → бюджет
- После шага 4 создаёт файл клиента в `axiomvoid-vault/Клиенты/` через GitHub API
- Обновляет `CRM-Обзор.md` — добавляет строку в таблицу и раздел «Все клиенты»
- Состояния сессии: `nc_name → nc_email → nc_type → nc_budget`

### ЗАДАЧА 2 — /invoice
- Добавлен обработчик `/invoice` в `bot.py`
- Пошаговый диалог: имя клиента → сумма USD → описание услуги
- Создаёт Stripe Checkout Session (POST `/v1/checkout/sessions`)
- Отправляет ссылку на оплату
- Записывает инвойс в файл клиента в Obsidian
- Состояния: `inv_client → inv_amount → inv_desc`

### ЗАДАЧА 3 — crm-sync.sh
- Создан `~/.claude/agents/crm-sync.sh`
- Каждый час сканирует `~/vaults/AxiomVoid/Клиенты/*.md`
- Парсит frontmatter (status, budget, deadline)
- Перестраивает CRM-Обзор.md полностью (Pipeline + Активные + Все клиенты)
- Git commit + push в axiomvoid-vault
- launchd: `com.axiomvoid.crm-sync` (интервал 3600 сек)

## Технические детали
- `AXIOMVOID_REPO = "rodion2yalanskiy-netizen/axiomvoid-vault"`
- `STRIPE_SECRET_KEY` добавлен в Railway Variables
- `GITHUB_TOKEN` на Railway обновлён с `gho_` → `ghp_` (PAT с доступом к axiomvoid-vault)
- Railway не auto-деплоит (webhook сломан) → деплой через `serviceInstanceDeployV2`

## Проверки
| Пункт | Статус | Детали |
|-------|--------|--------|
| /newclient → файл в Клиенты/ | ✅ Код готов, деплой SUCCESS | Live-тест провести на телефоне |
| /invoice → Stripe ссылка | ✅ Stripe API проверен (HTTP 200) | Live-тест провести на телефоне |
| crm-sync.sh вручную | ✅ | 2 клиента, git push выполнен |
| launchctl crm-sync | ✅ | `-	0	com.axiomvoid.crm-sync` |
| git push axiomvoid-bot | ✅ | commit 171c619 |
| git push axiomvoid-vault | ✅ | commit bec9307 |

## Важно для тестирования
- Отправлять сообщения БОТУ (не от бота) — открыть @Improvement_for_mi_bot в Telegram
- /newclient → 4 шага → проверить файл в Клиенты/ в Obsidian
- /invoice → 3 шага → проверить Stripe Dashboard + файл клиента

## Коммиты
- `axiomvoid-bot main`: 171c619 (CRM автоматизация)
- `axiomvoid-vault main`: bec9307 (crm-sync обновление)
