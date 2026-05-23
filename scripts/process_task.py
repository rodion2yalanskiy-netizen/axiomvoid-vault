#!/usr/bin/env python3
"""
process_task.py — Читает задачу из vault, отправляет в OpenRouter.
Сохраняет ответ в /tmp/agent_response.txt для save_to_vault.py
"""

import os, sys, json, requests
from pathlib import Path

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
TASK_FILE = os.environ.get("TASK_FILE", "")
MODEL = "anthropic/claude-sonnet-4.5"
MAX_TOKENS = 2000


def find_task() -> Path:
    if TASK_FILE:
        p = Path(TASK_FILE)
        if p.exists():
            return p
        print(f"⚠️  Файл не найден: {TASK_FILE}")

    tasks_dir = Path("🤖 AI Задачи")
    files = sorted(
        [f for f in tasks_dir.glob("*.md") if f.name != "README.md"],
        key=lambda f: f.stat().st_mtime, reverse=True
    )
    if not files:
        print("❌ Нет задач в '🤖 AI Задачи/'")
        sys.exit(1)
    return files[0]


def read_task(path: Path) -> str:
    text = path.read_text(encoding="utf-8").strip()
    # Убираем YAML frontmatter
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            text = text[end + 3:].strip()
    return text


def call_openrouter(task_text: str, task_name: str) -> str:
    if not OPENROUTER_API_KEY:
        print("❌ OPENROUTER_API_KEY не задан")
        sys.exit(1)

    prompt = (
        f"Ты — AI-агент для выполнения задач бизнеса QSNera (студия укладки премиум-плитки).\n\n"
        f"Задача: {task_name}\n\n"
        f"Содержание:\n{task_text}\n\n"
        f"Выполни задачу. Ответ в Markdown с разделами:\n"
        f"## ✅ Выполнено\n## 📋 Детали\n## 💡 Рекомендации (если есть)"
    )

    resp = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/rodion2yalanskiy-netizen/qsnera-vault",
            "X-Title": "QSNera AI Agent",
        },
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": MAX_TOKENS,
            "stream": False,
        },
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()
    usage = data.get("usage", {})
    print(f"✅ Токены: {usage.get('prompt_tokens','?')} in / {usage.get('completion_tokens','?')} out")
    return data["choices"][0]["message"]["content"]


def main():
    task_path = find_task()
    task_name = task_path.stem
    print(f"📄 Задача: {task_path}")

    task_text = read_task(task_path)
    if not task_text:
        print("❌ Файл пустой")
        sys.exit(1)

    print(f"📤 Отправляю в OpenRouter ({MODEL})...")
    response = call_openrouter(task_text, task_name)

    Path("/tmp/agent_response.txt").write_text(response, encoding="utf-8")
    Path("/tmp/agent_task_name.txt").write_text(task_name, encoding="utf-8")
    Path("/tmp/agent_task_file.txt").write_text(str(task_path), encoding="utf-8")
    print("💾 Ответ сохранён во временные файлы")


if __name__ == "__main__":
    main()
