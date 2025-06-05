from bridges.python.src.sdk.leon import leon
from bridges.python.src.sdk.types import ActionParams

import os
import requests
from xmindparser import xmind_to_dict

OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'mistral')


def tag_node(text: str) -> str:
    try:
        resp = requests.post(
            'http://localhost:11434/api/generate',
            json={'model': OLLAMA_MODEL, 'prompt': f'Tag the following node:\n{text}', 'stream': False},
            timeout=10
        )
        if resp.ok:
            return resp.json().get('response', '').strip()
    except Exception:
        pass
    return ''


def run(params: ActionParams) -> None:
    """Parse a mindmap and tag nodes"""
    file_path = None
    for ent in params['entities']:
        if ent['entity'] == 'file':
            file_path = ent['resolution']['value']
            break
    if file_path is None:
        return leon.answer({'key': 'error'})

    try:
        data = xmind_to_dict(file_path)
        for sheet in data:
            for topic in sheet.get('topic', {}).get('topics', []):
                title = topic.get('title', '')
                topic['tag'] = tag_node(title)
        leon.answer({'key': 'done'})
    except Exception:
        leon.answer({'key': 'error'})
