---
date: 2026-05-21
tags: [qsnera, отчет, svg, дизайн, github]
status: завершено
---

# Отчёт по интеграции графики QSNera

## Что было сделано

В рамках задачи по улучшению визуальной идентичности сайта **QSNera Studio** были созданы два оригинальных SVG-элемента и интегрированы в `index.html`.

---

## Созданные файлы

### `assets/qsnera-mark.svg` — Монограмный герб (400×400)

Концепция — **diamond seal с bookmatched мраморными прожилками**: прямая визуальная метафора главной услуги студии (укладка крупноформатного зеркального мрамора).

Состав элемента:
- Внешняя алмазная рамка с угловыми акцент-точками и «крыльями» (stroke 1.6px)
- Внутренняя алмазная кольцо (глубина, ощущение архитектурного чертежа)
- **6 пар мраморных прожилок** — каждая нарисована в левой половине и зеркально отражена вправо; все сходятся на центральном шве `x=200` (ось bookmatching)
- Центральная вертикальная ось-шов (визуальный символ технологии bookmatching)
- Горизонтальные правила с алмазным акцентом-ювелиром в центре
- Монограмма **QS** (Georgia serif, font-size 60, letter-spacing 10)
- Подпись **STUDIO** (Helvetica Neue, uppercase, letter-spacing 5.5)
- Золотые градиенты: `#e5cda8 → #c5a880 → #8c7352` по диагонали
- Фон: полностью прозрачный — работает на любом тёмном фоне

### `assets/qsnera-divider.svg` — Секционный разделитель (800×44)

Минималистичный люксовый горизонтальный разделитель между секциями страницы.

Состав:
- Горизонтальная золотая линия, затухающая к краям (gradient opacity: 0 → 0.85 → 0)
- Центральный ромб с внутренним кольцом и точкой-пульсом
- Радиальное мягкое свечение за центром
- 4 уровня симметричных тиков убывающего размера (80 / 160 / 240 / 320px от центра)

---

## Как изменился дизайн сайта

### Шапка (Header) и футер (Footer)
| Было | Стало |
|---|---|
| Простой inline SVG (ромб + 2 линии + точка) | Полный детализированный герб `qsnera-mark.svg` |
| CSS hover через `.logo-mark path { stroke }` | CSS `filter: brightness(1.3) drop-shadow(...)` — золотое свечение |
| Размер: 34px header / 30px footer | 38px header / 32px footer |

### Секции страницы
Разделитель `qsnera-divider.svg` добавлен в конец **6 секций**:

| Секция | Фон секции |
|---|---|
| `#philosophy` | `--color-charcoal-dark` |
| `#marble-showcase` | `--color-charcoal-mid` |
| `#services` | `--color-charcoal-mid` |
| `#portfolio` | `--color-charcoal-dark` |
| `#precision` | `--color-charcoal-mid` |
| `#contact` | `--color-charcoal-mid` |

CSS класс `.section-divider`: flex-центрирование, `padding-top: 4.5rem`, ширина `min(860px, 88%)`, opacity 0.82.

---

## Коммиты на GitHub

### Коммит 1 — Создание SVG-ассетов
```
commit edfac21
feat(assets): add premium SVG emblem and decorative divider
```
Добавлены файлы:
- `assets/qsnera-mark.svg` (создан с нуля)
- `assets/qsnera-divider.svg` (создан с нуля)

### Коммит 2 — Интеграция в сайт
```
commit 00b57db
feat(ui): integrate SVG emblem and dividers into site layout
```
Изменён файл:
- `index.html` (+41 строка / -16 строк)

---

## Репозиторий

**GitHub:** [rodion2yalanskiy-netizen/premium-tiling-website](https://github.com/rodion2yalanskiy-netizen/premium-tiling-website)  
**Ветка:** `main`  
**Дата:** 2026-05-21
