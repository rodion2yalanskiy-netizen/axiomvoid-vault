---
task: Миграция QSNera → Axiom:Void
date: 2026-05-28
time: 01:15 local
status: partially_completed
duration: ~75 мин
source: cron-auto (ef2a3569)
tool: claude-code
tags: [миграция, axiom-void, qsnera, ребрендинг]
---

# ✅ Отчёт: Миграция QSNera → Axiom:Void

**Дата:** 2026-05-28 | **Автозапуск:** cron `ef2a3569` (запланирован в 00:54)
**Бэкап-тег:** `backup-before-axiomvoid-20260527`

---

## 📊 Статус по шагам

| Шаг | Описание | Статус | Коммит |
|-----|----------|--------|--------|
| 1 | Агент-файлы `~/.claude/agents/*.md` | ✅ Выполнено | — |
| 2 | `~/CLAUDE.md` (глобальный) | ✅ Выполнено | — |
| 3 | `Brain/Memories.md` | ✅ Выполнено | `063f379` |
| 4 | `index.html` — полный rebuild | ❌ Заблокирован TCC | — |
| 5 | Telegram бот `bot.py` + `analyzer.py` | ❌ Заблокирован TCC | — |
| 6 | Переименование гайда + CLAUDE.md vault | ✅ Выполнено | `c4e0b2a` |
| 7 | Dashboard'ы обоих vault'ов | ✅ Выполнено | `f9bde54`, `ba18fc9` |

**Итог: 5/7 шагов выполнено. 2 шага заблокированы TCC.**

---

## ✅ Выполнено успешно

### Шаг 1 — Агент-файлы (~/.claude/agents/)

Обновлены 6 из 9 файлов (3 не содержали QSNera-специфики):

**dispatcher.md:**
- `мультиагентной AI-команды QSNera` → `мультиагентной AI-команды Axiom:Void`

**frontend-dev.md:**
- Цвета: `#1a1a1a / #d4a843 / #fff` → `#000000 / #00D4FF / #E8E8E8`, JetBrains Mono / Inter

**marketer.md:**
- Контекст: плитка/мрамор → веб-разработка, цифровые продукты
- SEO-ядро: 5 ключевиков для веб-студии
- Целевая аудитория: стартапы, digital-трансформация

**designer.md:**
- Дизайн-система: все 8 CSS-переменных Axiom:Void, JetBrains Mono, glow-тени

**devops.md:**
- `Railway (основная платформа QSNera)` → `Railway (основная платформа Axiom:Void)`

**marketer.md (style):**
- `Luxury сегмент: статус` → `Tech-продукт: точность, надёжность`

---

### Шаг 2 — ~/CLAUDE.md (глобальный)

- Заголовок: `QSNera` → `Axiom:Void`
- Секция стиля полностью заменена:
  - Цвета: `#1a1a1a/#d4a843` → `#000000/#00D4FF`
  - Шрифты: `Playfair Display / Inter` → `JetBrains Mono / Inter`
  - Тон: `премиум, мрамор` → `архитектор, строгий минимализм`

---

### Шаг 3 — Brain/Memories.md

Diff с бэкапом подтверждает:
- `основатель студии QSNera` → `основатель студии Axiom:Void`
- Строка про плитку → веб-разработка + список 4 услуг
- Структура vault-папок без emoji (убраны все 📝✅💡🏗)
- Сортировка: `проекты/QSNera` → `проекты/Axiom:Void`
- Footline обновлена датой и тегом миграции

**Push:** `063f379` → digital-brain-vault/main ✅

---

### Шаг 6 — Гайд переименован

- `Инструкция_QSNera_Guide.md` → `Инструкция_AxiomVoid_Guide.md`
- frontmatter: title + version 1.0 → 2.0 + updated
- Описание бизнеса: плитка → Axiom:Void + список услуг
- CLAUDE.md vault: ссылка обновлена
- **Push:** `c4e0b2a` → digital-brain-vault/main ✅

---

### Шаг 7 — Dashboard'ы

**Бизнес QSNera/Dashboard.md:**
- title: `QSNera — Дашборд` → `Axiom:Void — Дашборд бизнеса`
- H1: `QSNera — Бизнес` → `Axiom:Void — Бизнес`
- Tagline: `Премиум укладка плитки` → `Веб-разработка | axiom-void.dev`
- **Push:** `f9bde54` → qsnera-vault/main ✅

**Цифровой мозг/Dashboard.md:**
- Ссылка `[[Инструкция_QSNera_Guide]]` → `[[Инструкция_AxiomVoid_Guide]]`
- **Push:** `ba18fc9` → digital-brain-vault/main ✅

---

## ❌ Не выполнено — требует действий

### Причина: macOS TCC (Full Disk Access)

Desktop папка (`~/Desktop/`) заблокирована для текущего Claude Code процесса.
Затронуты шаги 4 и 5.

### Шаг 4 — index.html (ТРЕБУЕТСЯ ВРУЧНУЮ)

Нужно выполнить на Mac в Terminal:

```bash
# Проверь доступ:
ls ~/Desktop/premium-tiling-website/

# Или разреши Full Disk Access:
# System Settings → Privacy & Security → Full Disk Access → добавь Terminal
```

После восстановления доступа — запусти задачу через бот:
> "задача: полный rebuild index.html сайта под Axiom:Void: цвета #000000/#00D4FF, JetBrains Mono, 10 секций: hero/trust-bar/services/portfolio/why-us/process/testimonials/faq/cta/contact"

### Шаг 5 — Telegram бот (ТРЕБУЕТСЯ ВРУЧНУЮ)

```bash
# В bot.py:
# "QSNera AI Bot" → "Axiom:Void Bot"
# SYSTEM_PROMPT_CHAT: плитка/мрамор → веб-студия

# В analyzer.py:
# classify_note: "QSNera (укладка)" → "Axiom:Void (веб-студия)"
# preprocess_task SYSTEM: аналогично

# Vault-имена ("Бизнес QSNera") — НЕ менять!

cd ~/Desktop/qsnera-reels-bot
git add -A && git commit -m "feat: update bot context to Axiom:Void" && git push
```

---

## 🔍 Diff-верификация с бэкапом

### Brain/Memories.md ✅
```diff
-основатель студии **QSNera**
+основатель студии **Axiom:Void**
-Студия: укладка **премиум-плитки**
+Студия: **веб-разработка и цифровые продукты**
```

### Dashboard.md (Бизнес) ✅
```diff
-title: QSNera — Дашборд
+title: Axiom:Void — Дашборд бизнеса
-Премиум укладка плитки и натурального камня
+Веб-разработка и цифровые продукты | axiom-void.dev
```

### CLAUDE.md (vault) ✅
```diff
-Родион Яланский / QSNera
+Родион Яланский / Axiom:Void
-укладка премиум-плитки (мрамор, натуральный камень, Zellige)
+веб-разработка и цифровые продукты
```

### index.html ⚠️
Desktop заблокирован — diff недоступен. Файл не изменён.

---

## 📁 Изменённые файлы

| Файл | Изменение |
|------|-----------|
| `~/.claude/agents/dispatcher.md` | QSNera → Axiom:Void |
| `~/.claude/agents/frontend-dev.md` | Цвета + шрифты |
| `~/.claude/agents/marketer.md` | Полный ребрендинг контекста |
| `~/.claude/agents/designer.md` | Дизайн-система |
| `~/.claude/agents/devops.md` | Название платформы |
| `~/CLAUDE.md` | Заголовок + стиль |
| `~/vaults/Цифровой мозг/Brain/Memories.md` | Полный ребрендинг |
| `~/vaults/Цифровой мозг/CLAUDE.md` | Заголовок + бизнес + ссылка гайда |
| `~/vaults/Цифровой мозг/Dashboard.md` | Ссылка на гайд |
| `~/vaults/Цифровой мозг/Инструкция_AxiomVoid_Guide.md` | Новый файл (из QSNera) |
| `~/vaults/Бизнес QSNera/Dashboard.md` | Полный ребрендинг |

---

## ⚠️ Что НЕ изменено (как запрошено)

- `~/vaults/Бизнес QSNera/` — не переименован ✅
- `~/Library/LaunchAgents/com.qsnera.*.plist` — не тронуты ✅
- `~/.claude/.env` — не тронут ✅
- GitHub repo names — не изменены ✅
- Vault-имена в коде бота — не изменены ✅
- Railway project ID `62add92f` — не изменён ✅

---

*Отчёт создан автоматически: 2026-05-28 | Cron ef2a3569 | Claude Sonnet 4.6*
