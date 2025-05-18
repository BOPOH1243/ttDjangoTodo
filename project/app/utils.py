# app/utils.py
import time
import hashlib

def generate_pk(*args) -> int:
    """
    Генерируем числовой PK как:
      hash( concat(str(arg)…) + текущее process_time )
    Возвращаем 64-битный положительный int.
    """
    payload = ".".join(str(a) for a in args)
    timestamp = repr(time.process_time())
    raw = payload + "|" + timestamp
    # MD5 даёт 128-бит, обрежем до 64-бит
    h = hashlib.md5(raw.encode('utf-8')).hexdigest()
    return int(h[:16], 16)
