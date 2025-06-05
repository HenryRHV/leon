from bridges.python.src.sdk.leon import leon
from bridges.python.src.sdk.types import ActionParams

import os
import whisper


def run(params: ActionParams) -> None:
    """Transcribe an audio/video file"""
    file_path = None
    for ent in params['entities']:
        if ent['entity'] == 'file':
            file_path = ent['resolution']['value']
            break
    if file_path is None:
        return leon.answer({'key': 'error'})

    try:
        model = whisper.load_model('base')
        result = model.transcribe(file_path)
        leon.answer({'key': 'done'})
    except Exception:
        leon.answer({'key': 'error'})
