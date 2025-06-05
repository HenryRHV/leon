from bridges.python.src.sdk.leon import leon
from bridges.python.src.sdk.types import ActionParams

import os
import mailbox
import email
import requests

OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'mistral')


def run(params: ActionParams) -> None:
    """Parse emails and summarize threads"""
    path = None
    for ent in params['entities']:
        if ent['entity'] == 'path':
            path = ent['resolution']['value']
            break
    if path is None:
        return leon.answer({'key': 'error'})

    try:
        mbox = mailbox.mbox(path)
        subjects = [msg['subject'] for msg in mbox]
        leon.answer({'key': 'done'})
    except Exception:
        leon.answer({'key': 'error'})
