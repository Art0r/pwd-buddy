import string
import random


def generate_password() -> str:
    special = ['$', '&', '!', '*', '-', '@', '#', '%', '(', ')', '+', '=']

    pwd = ''.join(random.choices(string.ascii_uppercase +
                                 string.digits, k=5))

    pwd = pwd + ''.join(random.choices(string.ascii_lowercase +
                                       string.digits, k=5))

    pwd = pwd + ''.join(random.choices(special, k=2))

    shuffled = list(pwd)
    random.shuffle(shuffled)
    pwd = ''.join(shuffled)

    return pwd