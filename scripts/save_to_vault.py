#!/usr/bin/env python3
"""
save_to_vault.py — Сохраняет ответ агента в '✅ Выполнено Claude/' vault'а.
Формат файла совпадает с тем, что создавал локальный пайплайн.
"""

import sys
from datetime import datetime, timezone
from pathlib import Path


def main():
    response_file = Path("/tmp/agent_response.txt")
    task_name_file = Path("/tmp/agent_task_name.txt")
    task_path_file = Path("/tmp/agent_task_file.txt")

    if not response_file.exists():
        print("❌ /tmp/agent_response.txt не найден")
        sys.exit(1)

    response = response_file.read_text(encoding="utf-8").strip()
    task_name = task_name_file.read_text(encoding="utf-8").strip() if task_name_file.exists() else "task"
    task_path = task_path_file.read_text(encoding="utf-8").strip() if task_path_file.exists() else ""

    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H%M")

    # Имя файла в формате существующих отчётов
    safe_name = task_name.replace(" ", "_").replace("/", "-")[:40]
    filename = f"Отчёт_{date_str}_ТЗ_{date_str}_{safe_name}_{time_str}.md"

    report_dir = Path("✅ Выполнено Claude")
    report_dir.mkdir(exist_ok=True)
    report_path = report_dir / filename

    content = f"""---
task: {task_name}
source_file: {task_path}
date: {date_str}
time: {time_str} UTC
status: completed
source: github-actions
model: anthropic/claude-sonnet-4.5
tags: [выполнено, ai-pipeline]
---

# ✅ {task_name}

**Дата:** {date_str} {time_str} UTC
**Статус:** ✅ Выполнено
**Источник:** GitHub Actions + OpenRouter

---

{response}
"""

    report_path.write_text(content, encoding="utf-8")
    print(f"📄 Отчёт сохранён: {report_path}")


if __name__ == "__main__":
    main()
