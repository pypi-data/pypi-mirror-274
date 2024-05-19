from pathlib import Path

from csolver import solve_path


BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / 'data'


def test_solve_path():
    files = (x for x in DATA_DIR.iterdir() if x.is_file() and x.suffix in ['.png', '.jpg', '.jpeg'])
    for file in files:
        print(f'{file.stem = }')
        assert file.stem == solve_path(file)
