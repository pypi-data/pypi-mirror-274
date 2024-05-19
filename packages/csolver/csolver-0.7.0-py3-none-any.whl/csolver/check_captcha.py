from pathlib import Path

from . import read_captcha


BASE_DIR = Path(__file__).parent


def check_captcha(captchas_path: Path):
    success, fail = [], []
    for image in (x for x in captchas_path.iterdir() if x.is_file()):
        _captcha = read_captcha.solve_path(Path(image))
        _info = [image.stem, _captcha]
        if _captcha == image.stem:
            success.append(_info)
        else:
            fail.append(_info)

    print(f'success: {len(success)}')
    print(f'fail:    {len(fail)}')

    if fail:
        print(fail)


if __name__ == '__main__':
    check_captcha(BASE_DIR.parent / 'captchas-incorrect')
