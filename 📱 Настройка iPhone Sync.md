---
tags: [настройка, github, sync, iphone]
created: 2026-05-24
---

# 📱 Настройка синхронизации iPhone → GitHub

> Выполни эти шаги ОДИН РАЗ — потом всё работает автоматически.

---

## Шаг 1 — Создай GitHub токен (2 мин)

1. Открой на телефоне браузер → перейди на:
   **https://github.com/settings/tokens/new**

2. Заполни:
   - **Note:** `Obsidian iPhone`
   - **Expiration:** `No expiration` (или 1 год)
   - **Scopes:** поставь галочку на `repo` (первый пункт)

3. Нажми **Generate token**

4. **СКОПИРУЙ токен** — он выглядит как `ghp_xxxxxxxxxxxx`
   ⚠️ Токен показывается ОДИН РАЗ — сохрани его!

---

## Шаг 2 — Установи Obsidian Git на iPhone

1. Obsidian → `Settings` → `Community plugins`
2. Нажми **Turn on community plugins** (если не включено)
3. **Browse** → поиск: `Obsidian Git`
4. Install → Enable

**Или:** плагин уже установлен — проверь в списке активных плагинов.

---

## Шаг 3 — Подключи к GitHub репо

В Obsidian на iPhone:
1. `Settings` → `Obsidian Git`

2. Прокрути вниз до **Authentication / Commit Author**:
   - **Username:** `rodion2yalanskiy-netizen`
   - **Password:** вставь токен из Шага 1 (`ghp_xxx...`)
   - **Author name:** `Rodion`
   - **Author email:** `rodion2yalanskiy@gmail.com`

3. В самом верху настроек:
   - **Remote:** `origin`
   - **Remote branch:** `main`

4. **Auto pull interval:** `10` (минут)
5. **Pull on startup:** ✅ включи

---

## Шаг 4 — Первая синхронизация

1. Нажми на иконку `</>` в левой панели Obsidian (Source Control)
2. Нажми кнопку **Pull** (стрелка вниз)
3. Подожди 30-60 секунд
4. Все файлы загрузятся!

---

## Результат

После настройки:
```
Ты создаёшь задачу в Obsidian на iPhone
         ↓ (push при сохранении)
GitHub → Actions → выполняет → создаёт отчёт
         ↓ (vault-sync.sh 5 мин)
GitHub обновлён
         ↓ (Obsidian Git auto-pull 10 мин)
Отчёт появляется на iPhone
```

**Итого задержка: ~15 минут**

---

## Если что-то не работает

- Убедись что включены Community plugins: `Settings → Community plugins → OFF → ON`
- Проверь токен — он должен начинаться с `ghp_`
- Попробуй Pull вручную через Source Control
