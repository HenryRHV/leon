from bridges.python.src.sdk.leon import leon
from bridges.python.src.sdk.types import ActionParams

import os
import mailbox
import email
from email import policy
import requests

OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'mistral')


def extract_bodies(path: str) -> list[str]:
    messages = []
    if path.endswith('.eml'):
        with open(path, 'rb') as f:
            msg = email.message_from_binary_file(f, policy=policy.default)
            messages.append(msg)
    else:
        mbox = mailbox.mbox(path)
        for msg in mbox:
            messages.append(msg)
    bodies: list[str] = []
    for msg in messages[-5:]:
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == 'text/plain':
                    bodies.append(part.get_payload(decode=True).decode(errors='ignore'))
                    break
        else:
            bodies.append(msg.get_payload(decode=True).decode(errors='ignore'))
    return bodies


def run(params: ActionParams) -> None:
    """Parse emails and summarize threads."""
    path = None
    for ent in params['entities']:
        if ent['entity'] == 'path':
            path = ent['resolution']['value']
            break
    if path is None:
        return leon.answer({'key': 'error'})

    try:
        bodies = extract_bodies(path)
        prompt = 'Summarize the following emails:\n' + '\n\n'.join(bodies)
        resp = requests.post(
            'http://localhost:11434/api/generate',
            json={'model': OLLAMA_MODEL, 'prompt': prompt, 'stream': False},
            timeout=20
        )
        if resp.ok:
            summary = resp.json().get('response', '').strip()
            leon.answer({'key': 'summary', 'data': {'summary': summary}})
        else:
            leon.answer({'key': 'error'})
    except Exception:
        leon.answer({'key': 'error'})
