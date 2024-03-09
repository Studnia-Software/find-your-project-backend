from generate_key import generate
import os

PROJECT_PATH = os.path.abspath(os.path.dirname(__name__))

def load():
    try:
        with open(PROJECT_PATH + '/.env.example', 'r') as env_example:
            content = env_example.read()

        with open(PROJECT_PATH + '/.env', 'w') as env:
            env.write(content)
            print('.env loaded successfully.')

        generate()
    except FileNotFoundError as e:
        print(f"Error:{str(e)}.env.example not found.")


if __name__ == '__main__':
    load()
