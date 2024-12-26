import os.path
from settings.settings import storage_path
import re 


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

def filename_50(filename):
    if len(filename) > 49:
        name_splitted = filename.split('.')
        print(name_splitted)
        name = name_splitted[0]
        ext = name_splitted[1]
        return name[:49-len(ext)]+'.'+ ext
    else:
        return filename
    
def rename(filename):

    name_splitted = filename.split('.')
    name = name_splitted[0]
    ext = name_splitted[1]

    match = re.search(r'([^.]+)\((\d+)\)$', name)

    def repl(m,len_ext):
        num = str(int(m.group(2))+1)
        return m.group(1)[:47-len(num)-len_ext] +'('+ num + ')'
    
    if match:
        name_new = re.sub(r'([^.]+)\((\d+)\)$', repl(match,len(ext)) , name)
        return name_new + '.' + ext
    else:
        return name[:46-len(ext)] +'(1).' + ext


