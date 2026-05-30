---
tags: [claude-code, automation, web-testing, design, tokens, prompt, reference]
date: 2026-05-23
status: 🟢 Активный
source: obsidian-pipeline
---

# 🤖 Claude Code — Web Automation & Optimization Master Prompt

> **Теги:** #claude-code #automation #web-testing #design #tokens #prompt
> **Дата:** 2026-05-23
> **Статус:** 🟢 Активный

---

## 📋 Контекст задачи

Этот промт настраивает Claude Code на три задачи:

1. **Автоматическое тестирование сайта** (клики, проверка элементов, E2E)
2. **Экономия токенов** при длительной работе
3. **Экспертиза по дизайну** (UI/UX, анимации, frontend)

---

## 🧩 Скиллы и инструменты (встроенные в Claude)

| Скилл | Назначение |
|---|---|
| `frontend-design` | Дизайн UI, компоненты, анимации, CSS |
| `file-reading` | Чтение загруженных файлов (HTML, JSON, CSV) |
| `pdf` / `pdf-reading` | Работа с документацией в PDF |
| `docx` | Чтение/создание Word-документов |
| `xlsx` | Таблицы с тест-кейсами, баг-репортами |
| `product-self-knowledge` | Актуальные данные по API Anthropic и лимитам |

---

## 🔌 MCP-плагины для браузерной автоматизации

### 1. Playwright MCP
```
npm: @playwright/mcp
Возможности: клики, навигация, скриншоты, формы, ожидание элементов, E2E-тесты
```

### 2. Puppeteer MCP
```
npm: puppeteer-mcp-server
Возможности: headless Chrome, скриншоты, PDF-экспорт, клики, eval JS
```

### 3. Browserbase MCP (облачный)
```
Возможности: удалённый браузер, запись сессий, параллельные тесты
```

### 4. Filesystem MCP
```
npm: @modelcontextprotocol/server-filesystem
Чтение/запись файлов проекта напрямую
```

### 5. GitHub MCP
```
npm: @modelcontextprotocol/server-github
Коммиты, PR, Issues прямо из диалога с Claude
```

### 6. Lighthouse / Axe MCP
```
Performance, Accessibility, SEO аудит страниц + WCAG-проверка
```

---

## 🔧 Установка MCP (конфиг Claude Code)

```json
// ~/.claude/claude_desktop_config.json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/project"]
    }
  }
}
```

---

## 💰 Стратегии экономии токенов

### В CLAUDE.md проекта

```markdown
## Token Efficiency Rules
- Отвечай кратко, без объяснений если не просят
- Не повторяй код целиком — используй diff-формат
- Для больших файлов показывай только изменённые функции
- Используй псевдокод перед написанием полного кода
- Сначала спроси уточняющие вопросы, потом генерируй
```

### Техники в промтах

```
✅ "Покажи только изменённую часть функции"
✅ "Ответь в формате diff"
✅ "Сначала план (bullet points), потом код"
✅ "Не объясняй очевидное"
✅ Используй /compact в Claude Code для сжатия контекста
✅ Разбивай большие задачи на мелкие сессии
✅ Храни состояние в файлах, а не в контексте
```

---

## 🎨 Принципы дизайна (frontend-design скилл)

### Типографика
- **Не использовать:** Inter, Roboto, Arial, system-ui
- **Использовать:** характерные Display-шрифты + рафинированный body-шрифт
- **Источники:** Google Fonts (Playfair, DM Serif, Syne, Cabinet Grotesk)

### Цвет
- CSS-переменные для консистентности
- Доминирующий цвет + острый акцент (не равномерное распределение)
- Избегать: purple-gradient на белом (это "AI-клише")

### Анимации
- CSS-only для HTML-страниц (GSAP/Motion для React)
- Приоритет: staggered reveals при загрузке > микро-анимации
- Scroll-trigger + hover states обязательны

### Композиция
- Асимметрия, overlapping, диагональный поток
- Grid-breaking элементы
- Щедрое negative space ИЛИ контролируемая плотность

---

## 🚀 Мастер-промт для Claude Code сессии

```
Ты — senior fullstack-разработчик и QA-инженер.

## Задачи на сессии:
1. ТЕСТИРОВАНИЕ: Playwright MCP — кликай кнопки, проверяй элементы, тексты,
   навигацию, формы. Краткий отчёт об ошибках.
2. ЭКОНОМИЯ ТОКЕНОВ: кратко, diff-формат, план → код, не повторяй код.
3. ДИЗАЙН-РЕВЬЮ: нестандартные шрифты, критика generic-эстетики,
   конкретные анимации, улучшения композиции.

## Проект: /Users/rodionyalanskiy/Desktop/premium-tiling-website
## Стек: Vanilla HTML5 + CSS3 + JS (no frameworks)
## Начни с: [проверь главную / ревью дизайна header / и т.д.]
```

---

## 📐 Чеклист тестирования Axiom:Void

### Функциональность
- [ ] Все кнопки кликабельны и реагируют
- [ ] Формы валидируются и отправляются
- [ ] Навигация — все ссылки ведут куда надо
- [ ] FAQ аккордеон открывается/закрывается
- [ ] Мобильное меню работает

### Визуальное
- [ ] Нет сломанных изображений
- [ ] Нет переполнения текста (overflow)
- [ ] Консистентные отступы и шрифты
- [ ] Корректно на мобильном (375px)
- [ ] Корректно на десктопе (1440px)

### Производительность
- [ ] Lighthouse > 80 по всем метрикам
- [ ] Нет ошибок в консоли браузера
- [ ] Изображения оптимизированы

### Доступность
- [ ] Alt-тексты у всех изображений
- [ ] Keyboard navigation работает
- [ ] WCAG AA контрастность соблюдена

---

## 📚 Полезные ресурсы

- [Claude Code Docs](https://docs.claude.ai/claude-code)
- [MCP Servers Registry](https://github.com/modelcontextprotocol/servers)
- [Playwright MCP](https://github.com/microsoft/playwright-mcp)
- [Prompt Engineering Guide](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview)
- [Motion Library](https://motion.dev)
- [Google Fonts](https://fonts.google.com)

---

*Создано автоматически Claude Sonnet 4.6 • 2026-05-23 через obsidian-pipeline*

## Связи
- [[Dashboard]]
- [[Маркетинг]]
- [[ARCHITECTURE_RULES]]
