#!/usr/bin/env python3
"""
QSNera AI Pipeline — Task Processor v2
Supports: openrouter (text), vision, images (Together AI), code/antigravity (local delegation)
"""

import os
import re
import sys
import json
import base64
import requests
from pathlib import Path
from datetime import datetime, timezone

OPENROUTER_KEY = os.environ.get("OPENROUTER_API_KEY", "")
TOGETHER_KEY   = os.environ.get("TOGETHER_API_KEY", "")
TASK_FILE      = os.environ.get("TASK_FILE", "")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
TOGETHER_URL   = "https://api.together.xyz/v1/images/generations"

HEADERS_OR = {
    "Authorization": f"Bearer {OPENROUTER_KEY}",
    "HTTP-Referer": "https://github.com/rodion2yalanskiy-netizen/qsnera-vault",
    "X-Title": "QSNera AI Pipeline",
    "Content-Type": "application/json",
}


def strip_frontmatter(text):
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4:].strip()
    return text.strip()


def get_field(text, field):
    m = re.search(rf"^{field}:\s*(.+)$", text, re.MULTILINE)
    return m.group(1).strip() if m else ""


def find_task():
    if TASK_FILE:
        p = Path(TASK_FILE)
        if p.exists():
            return p
        print(f"⚠️  File not found: {TASK_FILE}")
    tasks_dir = Path("🤖 AI Задачи")
    files = sorted(
        [f for f in tasks_dir.glob("*.md") if f.name != "README.md"],
        key=lambda f: f.stat().st_mtime, reverse=True
    )
    if not files:
        print("❌ No tasks found")
        sys.exit(1)
    return files[0]


def call_openrouter(prompt, model="anthropic/claude-sonnet-4.5", images=None):
    """Call OpenRouter — supports both text and vision (multimodal) tasks."""
    if not OPENROUTER_KEY:
        raise RuntimeError("OPENROUTER_API_KEY not set")

    if images:
        content = [{"type": "text", "text": prompt}]
        for img in images:
            if img.startswith("http"):
                content.append({"type": "image_url", "image_url": {"url": img}})
            elif Path(img).exists():
                ext = Path(img).suffix.lstrip(".")
                b64 = base64.b64encode(Path(img).read_bytes()).decode()
                content.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:image/{ext};base64,{b64}"}
                })
        messages = [{"role": "user", "content": content}]
    else:
        messages = [{"role": "user", "content": prompt}]

    resp = requests.post(OPENROUTER_URL, headers=HEADERS_OR, json={
        "model": model,
        "messages": messages,
        "max_tokens": 2000,
        "stream": False,
    }, timeout=90)
    resp.raise_for_status()
    data = resp.json()
    usage = data.get("usage", {})
    print(f"✅ Tokens: {usage.get('prompt_tokens','?')} in / {usage.get('completion_tokens','?')} out")
    return data["choices"][0]["message"]["content"]


def generate_images_together(prompt, n=1):
    """Generate images via Together AI (FLUX.1-schnell, free tier)."""
    if not TOGETHER_KEY:
        return None, "TOGETHER_API_KEY not configured in GitHub Secrets"

    resp = requests.post(TOGETHER_URL, headers={
        "Authorization": f"Bearer {TOGETHER_KEY}",
        "Content-Type": "application/json",
    }, json={
        "model": "black-forest-labs/FLUX.1-schnell",
        "prompt": prompt,
        "n": n,
        "width": 1024,
        "height": 1024,
    }, timeout=120)
    resp.raise_for_status()
    urls = [img["url"] for img in resp.json().get("data", [])]
    return urls, None


def delegate_local(content, task_name, tool):
    """Write delegated task to 📋 AI Делегат/ for local Mac agent."""
    d = Path("📋 AI Делегат")
    d.mkdir(exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    f = d / f"делегат_{ts}_{task_name}.md"
    f.write_text(f"""---
status: delegated
tool: {tool}
task_name: {task_name}
source_file: {TASK_FILE}
delegated_at: {datetime.now(timezone.utc).isoformat()}
---

{content}
""", encoding="utf-8")
    return str(f)


def main():
    task_path = find_task()
    task_name = task_path.stem
    raw = task_path.read_text(encoding="utf-8").strip()

    tool    = get_field(raw, "tool") or "openrouter"
    model   = get_field(raw, "model") or "anthropic/claude-sonnet-4.5"
    content = strip_frontmatter(raw)

    print(f"📄 Task: {task_name}")
    print(f"🔧 Tool: {tool}  |  Model: {model}")

    # Save metadata for later steps
    Path("/tmp/agent_task_name.txt").write_text(task_name)
    Path("/tmp/agent_task_file.txt").write_text(str(task_path))

    # === ROUTING ===

    if tool in ("code", "antigravity"):
        # Delegate to local Mac agent — Actions only creates the delegation file
        delegate_path = delegate_local(content, task_name, tool)
        response = (
            f"## ⏳ Делегировано локальному агенту\n\n"
            f"**Инструмент:** `{tool}`\n"
            f"**Файл делегата:** `{delegate_path}`\n\n"
            f"Задача передана на Mac. Локальный агент выполнит её через "
            f"{'Claude Code' if tool == 'code' else 'Antigravity'} "
            f"и отчёт появится в Obsidian автоматически."
        )
        Path("/tmp/agent_response.txt").write_text(response)
        Path("/tmp/agent_delegated.txt").write_text(delegate_path)
        print(f"📤 Delegated → {delegate_path}")
        return

    if tool == "images":
        # Image generation via Together AI
        print("🎨 Generating images via Together AI (FLUX)...")
        urls, err = generate_images_together(content, n=1)
        if err:
            response = f"❌ Ошибка генерации: {err}"
        else:
            urls_md = "\n".join(f"![]({u})" for u in urls)
            response = (
                f"## 🎨 Изображения сгенерированы\n\n"
                f"**Модель:** FLUX.1-schnell (Together AI)\n\n"
                f"### Результат:\n{urls_md}"
            )
        Path("/tmp/agent_response.txt").write_text(response)
        return

    if tool == "vision":
        # Vision — extract image URLs from task content
        image_urls = re.findall(
            r'https?://\S+?(?:\.jpg|\.jpeg|\.png|\.webp|\.gif)(?:\?[^\s]*)?',
            content
        )
        vision_model = model if "claude" in model or "gemini" in model else "anthropic/claude-opus-4-5"
        print(f"👁️  Vision task, model: {vision_model}, images: {len(image_urls)}")
        prompt = (
            f"Ты — AI-агент QSNera. Выполни задачу:\n\n{content}\n\n"
            f"Ответ в Markdown с разделами: ## ✅ Выполнено\n## 📋 Детали\n## 💡 Рекомендации"
        )
        response = call_openrouter(prompt, model=vision_model, images=image_urls or None)
        Path("/tmp/agent_response.txt").write_text(response)
        return

    # === Default: text via OpenRouter ===
    prompt = (
        f"Ты — AI-агент для задач бизнеса QSNera (студия укладки премиум-плитки).\n\n"
        f"Задача: **{task_name}**\n\n{content}\n\n"
        f"Выполни задачу. Ответ в Markdown:\n"
        f"## ✅ Выполнено\n## 📋 Детали\n## 💡 Рекомендации (если есть)"
    )
    print(f"📤 Sending to OpenRouter ({model})...")
    response = call_openrouter(prompt, model=model)
    Path("/tmp/agent_response.txt").write_text(response)
    print("✅ Done.")


if __name__ == "__main__":
    main()
