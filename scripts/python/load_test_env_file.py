from generate_key import generate
from pathlib import Path

import os

PROJECT_PATH = Path(__file__).resolve().parent.parent.parent


def load():
    try:
        with open(os.path.join(PROJECT_PATH, '.env.example'), 'r') as env_example:
            content = env_example.read()

        with open(os.path.join(PROJECT_PATH, '.env'), 'w') as env:
            env.write(content)
            print('.env loaded successfully.')

        generate()
    except FileNotFoundError as e:
        print(f"Error:{str(e)}.env.example not found.")


if __name__ == '__main__':
    load()
