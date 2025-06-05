from xmindparser import xmind_to_dict
from bridges.python.src.sdk.leon import leon
from bridges.python.src.sdk.types import ActionParams
from typing import List, Dict


def topics_to_markdown(topics: List[Dict], level: int = 0) -> List[str]:
    lines = []
    prefix = "  " * level + "- "
    for topic in topics:
        title = topic.get("title", "").strip()
        if title:
            lines.append(prefix + title)
        sub = topic.get("topics", [])
        if isinstance(sub, list) and sub:
            lines.extend(topics_to_markdown(sub, level + 1))
    return lines


def run(params: ActionParams) -> None:
    file_path = None
    for item in params["entities"]:
        if item["entity"] == "file":
            file_path = item["resolution"].get("value")
    if not file_path:
        return leon.answer({"key": "file_not_provided"})

    try:
        data = xmind_to_dict(file_path)
        if not data:
            return leon.answer({"key": "parse_error"})
        root = data[0]
        topics = [root.get("topic", {})]
        lines = topics_to_markdown(topics)
        markdown = "\n".join(lines)
        leon.answer({"key": "summary", "data": {"markdown": markdown}})
    except FileNotFoundError:
        leon.answer({"key": "file_not_found"})
    except Exception:
        leon.answer({"key": "parse_error"})
