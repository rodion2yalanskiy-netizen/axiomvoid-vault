#!/usr/bin/env python3
"""
router_agent.py — Классифицирует заметки из inbox/ и перемещает в нужные папки.
Категории: business → AI Задачи, tech/personal → AI Делегат, task → tasks/
"""
import os
import re
import sys
import requests
from pathlib import Path

OPENROUTER_KEY = os.environ.get("OPENROUTER_API_KEY", "")
INPUT_FILE = os.environ.get("INPUT_FILE", "")


def call_openrouter(prompt: str) -> str:
    resp = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_KEY}",
            "HTTP-Referer": "https://github.com/rodion2yalanskiy-netizen/qsnera-vault",
            "X-Title": "QSNera Router",
            "Content-Type": "application/json",
        },
        json={
            "model": "anthropic/claude-sonnet-4.5",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 20,
        },
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"].strip().lower()


def strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4:].strip()
    return text.strip()


def add_or_update_frontmatter(text: str, updates: dict) -> str:
    """Add or update frontmatter fields."""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            fm = text[4:end]
            body = text[end + 4:]
            for k, v in updates.items():
                if re.search(rf"^{k}:", fm, re.MULTILINE):
                    fm = re.sub(rf"^{k}:.*$", f"{k}: {v}", fm, flags=re.MULTILINE)
                else:
                    fm = fm.rstrip() + f"\n{k}: {v}"
            return f"---\n{fm.strip()}\n---\n{body}"
    # No frontmatter — create
    fm_lines = "\n".join(f"{k}: {v}" for k, v in updates.items())
    return f"---\n{fm_lines}\n---\n\n{text}"


def main():
    # Находим файл
    if INPUT_FILE and Path(INPUT_FILE).exists():
        file_path = Path(INPUT_FILE)
    else:
        inbox = Path("inbox")
        files = sorted(
            [f for f in inbox.glob("*.md") if f.name != "README.md"],
            key=lambda f: f.stat().st_mtime,
            reverse=True,
        )
        pending = []
        for f in files:
            raw = f.read_text(encoding="utf-8")
            status = ""
            m = re.search(r"^status:\s*(.+)$", raw, re.MULTILINE)
            if m:
                status = m.group(1).strip()
            if status not in ("routed", "skip", "completed"):
                pending.append(f)
        if not pending:
            print("📭 Нет файлов для роутинга")
            return
        file_path = pending[0]

    print(f"📄 Классифицирую: {file_path}")
    raw = file_path.read_text(encoding="utf-8")
    body = strip_frontmatter(raw)[:1500]

    if not OPENROUTER_KEY:
        print("❌ OPENROUTER_API_KEY не задан")
        sys.exit(1)

    prompt = f"""Ты — роутер заметок для Родиона Яланского (Axiom:Void, веб-разработка).

Определи категорию заметки ОДНИМ словом:
- "business" → бизнес Axiom:Void: клиенты, проекты, финансы, веб-разработка, маркетинг, продажи
- "tech" → техника: код, GitHub, AI, автоматизация, программы, сайт
- "personal" → личное: цели, здоровье, семья, хобби, отношения
- "task" → это конкретная задача/инструкция (нужно что-то сделать/создать)

ЗАМЕТКА:
{body}

Ответь СТРОГО одним словом: business, tech, personal, или task"""

    category = call_openrouter(prompt)
    category = re.sub(r"[^a-z]", "", category)
    if category not in ("business", "tech", "personal", "task"):
        category = "business"
    print(f"📂 Категория: {category}")

    name = file_path.stem
    dest_map = {
        "business": f"🤖 AI Задачи/{name}.md",
        "task":     f"tasks/{name}.md",
        "tech":     f"📋 AI Делегат/tech_{name}.md",
        "personal": f"📋 AI Делегат/personal_{name}.md",
    }
    dest = Path(dest_map[category])
    dest.parent.mkdir(exist_ok=True)

    # Обновляем frontmatter назначения
    new_raw = add_or_update_frontmatter(raw, {"status": "pending", "routed_from": "inbox"})
    dest.write_text(new_raw, encoding="utf-8")

    # Помечаем исходный как обработанный
    marked = add_or_update_frontmatter(raw, {"status": "routed", "routed_to": category})
    file_path.write_text(marked, encoding="utf-8")

    Path("/tmp/router_category.txt").write_text(category)
    Path("/tmp/router_dest.txt").write_text(str(dest))
    print(f"✅ Создано: {dest}")


if __name__ == "__main__":
    main()
