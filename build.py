#!/usr/bin/env python3
"""Inject tasks.json + activity.json into index.html's embedded data blocks.

The live site fetches the JSON files directly, so this is OPTIONAL — use it only
to bake a self-contained offline snapshot of the board into index.html.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).parent
html_path = ROOT / "index.html"

tasks = json.loads((ROOT / "tasks.json").read_text())
acts = json.loads((ROOT / "activity.json").read_text())
html = html_path.read_text()

def inject(html: str, elem_id: str, payload: str) -> str:
    pattern = re.compile(
        r'(<script id="' + elem_id + r'" type="application/json">).*?(</script>)',
        re.S,
    )
    if not pattern.search(html):
        sys.exit(f"marker <script id={elem_id}> not found in index.html")
    return pattern.sub(lambda m: m.group(1) + "\n" + payload + "\n" + m.group(2), html, count=1)

html = inject(html, "data-tasks", json.dumps(tasks, ensure_ascii=False, indent=1))
html = inject(html, "data-activity", json.dumps(acts, ensure_ascii=False, indent=1))
html_path.write_text(html)

n = len(tasks.get("tasks", []))
done = sum(1 for t in tasks.get("tasks", []) if t.get("status") == "done")
print(f"index.html rebuilt: {n} tasks ({done} done), {len(acts)} activity entries")
