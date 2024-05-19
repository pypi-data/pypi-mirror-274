from pathlib import Path

from .lib import Captcha


_classificater = Captcha(show_ad=False).classification


def solve_bytes(image_bytes: bytes, /):
    captcha = str(_classificater(image_bytes)).upper()
    return captcha


def solve_path(image_path: Path, /):
    return solve_bytes(image_path.read_bytes())
