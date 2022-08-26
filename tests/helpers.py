from random import choice
from string import ascii_letters, digits

HOST = "http://localhost:3000"
FIRST = "Jim"
LAST = "Halpert"
EMAIL = "jim@dundermifflin.com"
PASSWORD = "BAZouVa3saWgW89z"
SITE_NAME = "testing-site"
CREDENTIALS = {"username": EMAIL, "password": PASSWORD}


def random_string(chars: int, letters_only: bool = False) -> str:
    char_set = ascii_letters if letters_only else ascii_letters + digits
    return "".join(choice(char_set) for _ in range(chars))
