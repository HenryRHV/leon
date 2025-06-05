import mailbox
import os
import requests
from email import policy
from email.parser import BytesParser

from bridges.python.src.sdk.leon import leon
from bridges.python.src.sdk.types import ActionParams

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")


def extract_latest(path: str) -> str:
    """Return text of the latest email in an mbox or single .eml file."""
    if path.endswith(".eml"):
        with open(path, "rb") as f:
            msg = BytesParser(policy=policy.default).parse(f)
        payload = msg.get_body(preferencelist=("plain",))
        if payload:
            return payload.get_content()
        return msg.get_payload(decode=True).decode(errors="ignore")
    mbox = mailbox.mbox(path)
    if len(mbox) == 0:
        return ""
    msg = mbox[-1]
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                return part.get_payload(decode=True).decode(errors="ignore")
    return msg.get_payload(decode=True).decode(errors="ignore")


def run(params: ActionParams) -> None:
    """Draft a reply for the latest email."""
    path = None
    for ent in params["entities"]:
        if ent["entity"] == "path":
            path = ent["resolution"]["value"]
            break
    if path is None:
        return leon.answer({"key": "error"})

    try:
        content = extract_latest(path)
        prompt = f"Write a short and polite reply to the following email:\n{content}"
        resp = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=20,
        )
        if resp.ok:
            reply = resp.json().get("response", "").strip()
            leon.answer({"key": "reply", "data": {"reply": reply}})
        else:
            leon.answer({"key": "error"})
    except Exception:
        leon.answer({"key": "error"})
