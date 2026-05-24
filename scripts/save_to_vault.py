#!/usr/bin/env python3
"""
save_to_vault.py — Сохраняет ответ агента в '✅ Выполнено Claude/' vault'а.

ПРАВИЛО ИМЕНОВАНИЯ (постоянное):
  Имя файла = "Отчёт: {название заметки из 🤖 AI Задачи}.md"
  Пример:    "Отчёт: Что ты умеешь.md"
  Пример:    "Отчёт: Пост для Instagram.md"
"""

import sys
from datetime import datetime, timezone
from pathlib import Path


def main():
    response_file   = Path("/tmp/agent_response.txt")
    task_name_file  = Path("/tmp/agent_task_name.txt")
    task_path_file  = Path("/tmp/agent_task_file.txt")

    if not response_file.exists():
        print("❌ /tmp/agent_response.txt не найден")
        sys.exit(1)

    response  = response_file.read_text(encoding="utf-8").strip()
    task_name = task_name_file.read_text(encoding="utf-8").strip() if task_name_file.exists() else "Задача"
    task_path = task_path_file.read_text(encoding="utf-8").strip() if task_path_file.exists() else ""

    now      = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M UTC")

    # ─────────────────────────────────────────────────────────
    # ПРАВИЛО: имя отчёта = "Отчёт: {название заметки}.md"
    # Название берётся из имени файла задачи (без расширения)
    # Недопустимые символы для файловой системы убираются
    # ─────────────────────────────────────────────────────────
    safe_name = task_name.replace("/", "-").replace("\\", "-").replace(":", " —")
    filename  = f"Отчёт: {safe_name}.md"

    report_dir  = Path("✅ Выполнено Claude")
    report_dir.mkdir(exist_ok=True)
    report_path = report_dir / filename

    # Если отчёт с таким именем уже есть — добавляем дату чтобы не перезаписать
    if report_path.exists():
        filename  = f"Отчёт: {safe_name} ({date_str}).md"
        report_path = report_dir / filename

    content = f"""---
task: {task_name}
source_file: {task_path}
date: {date_str}
time: {time_str}
status: completed
source: github-actions
tags: [выполнено, ai-pipeline]
---

# ✅ Отчёт: {task_name}

**Дата:** {date_str} {time_str}
**Задача:** [[{task_name}]]

---

{response}
"""

    report_path.write_text(content, encoding="utf-8")
    print(f"📄 Отчёт сохранён: {report_path}")


if __name__ == "__main__":
    main()
