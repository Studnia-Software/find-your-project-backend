from django.core.management.utils import get_random_secret_key

with open(".env", "a") as file:
    print("\nSECRET_KEY=" + get_random_secret_key(), file=file)
