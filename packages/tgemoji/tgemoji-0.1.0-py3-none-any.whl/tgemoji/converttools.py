from tgemoji.preprocess import preprocess


def aiogram2pyrogram(text: str) -> str:
    text = preprocess(text)
    text = text.replace("tg-emoji", "emoji")
    text = text.replace("emoji-id", "id")
    return text


def pyrogram2aiogram(text: str) -> str:
    text = preprocess(text)
    text = text.replace("emoji", "tg-emoji")
    text = text.replace("id", "emoji-id")
    return text
