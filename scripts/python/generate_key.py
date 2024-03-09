from django.core.management.utils import get_random_secret_key
import os


PROJECT_PATH = os.path.abspath(os.path.dirname(__name__))


def generate():
    try:
        with open(PROJECT_PATH + '/.env', 'a') as file:
            print('\nSECRET_KEY=' + get_random_secret_key(), file=file)
    except FileNotFoundError:
        print('.env file not found.')


if __name__ == '__main__':
    generate()
