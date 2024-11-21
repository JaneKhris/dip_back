import os.path
from settings.settings import storage_path

def get_user_path(username):
    user_path = f'{storage_path}/{username}/'
    if not os.path.exists(user_path):
        os.mkdir(user_path)
    return user_path
    
    