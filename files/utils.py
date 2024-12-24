import os.path
from settings.settings import storage_path

def get_user_path(username):
    user_path = f'{storage_path}/{username}/'
    if not os.path.exists(user_path):
        os.mkdir(user_path)
    return user_path


import random
import string

def generate_random_string(length):
    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(length))
    return rand_string

