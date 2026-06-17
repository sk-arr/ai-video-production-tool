from pathlib import Path
import json
from datetime import datetime
from typing import Dict, Any, List


HISTORY_PATH = Path("data/history.json")


def load_history() -> List[Dict[str, Any]]:
    if not HISTORY_PATH.exists():
        return []
    try:
        return json.loads(HISTORY_PATH.read_text(encoding="utf-8"))
    except Exception:
        return []


def save_record(record: Dict[str, Any]) -> None:
    HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    history = load_history()
    record["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history.insert(0, record)
    HISTORY_PATH.write_text(
        json.dumps(history[:20], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def build_markdown(record: Dict[str, Any]) -> str:
    topic = record.get("topic", {})
    script = record.get("script", {})
    storyboard = record.get("storyboard", [])

    lines = [
        f"# {topic.get('title', 'AI短剧/短视频方案')}",
        "",
        "## 选题信息",
        f"- 简介：{topic.get('summary', '')}",
        f"- 爆点：{topic.get('hook', '')}",
        f"- 适合平台：{topic.get('platform', '')}",
        "",
        "## 三段式脚本",
        f"### 开场\n{script.get('opening', '')}",
        "",
        f"### 冲突\n{script.get('conflict', '')}",
        "",
        f"### 结尾\n{script.get('ending', '')}",
        "",
        "## 分镜表",
        "",
        "| 镜头 | 画面描述 | 台词/旁白 | 时长 | 运镜建议 |",
        "|---|---|---|---|---|",
    ]

    for item in storyboard:
        lines.append(
            f"| {item.get('shot', '')} | {item.get('visual', '')} | "
            f"{item.get('voice', '')} | {item.get('duration', '')} | {item.get('camera', '')} |"
        )

    return "\n".join(lines)
