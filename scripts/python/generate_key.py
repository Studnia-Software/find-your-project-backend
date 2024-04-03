import os.path

from django.core.management.utils import get_random_secret_key
from pathlib import Path

PROJECT_PATH = Path(__file__).resolve().parent.parent.parent


def generate():
    try:
        with open(os.path.join(PROJECT_PATH, '.env'), 'a') as file:
            print('\nSECRET_KEY=' + get_random_secret_key(), file=file)
    except FileNotFoundError:
        print('.env file not found.')


if __name__ == '__main__':
    generate()
