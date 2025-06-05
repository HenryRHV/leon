from bridges.python.src.sdk.leon import leon
from bridges.python.src.sdk.types import ActionParams

import os
import pytesseract
from PIL import Image


def run(params: ActionParams) -> None:
    """Read text from an image"""
    file_path = None
    for ent in params['entities']:
        if ent['entity'] == 'file':
            file_path = ent['resolution']['value']
            break
    if file_path is None:
        return leon.answer({'key': 'error'})

    try:
        text = pytesseract.image_to_string(Image.open(file_path))
        leon.answer({'key': 'done'})
    except Exception:
        leon.answer({'key': 'error'})
