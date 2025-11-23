from cryptography.fernet import Fernet
import os
KEY_FILE='vault.key'
VAULT_FILE='vault.bin'

def init_key():
    if not os.path.exists(KEY_FILE):
        k = Fernet.generate_key()
        with open(KEY_FILE,'wb') as f: f.write(k)
    else:
        with open(KEY_FILE,'rb') as f: k = f.read()
    return k

def store(secret_dict):
    k = init_key(); f = Fernet(k)
    data = str(secret_dict).encode('utf-8')
    token = f.encrypt(data)
    with open(VAULT_FILE,'wb') as fw: fw.write(token)

def load():
    if not os.path.exists(KEY_FILE) or not os.path.exists(VAULT_FILE):
        return None
    with open(KEY_FILE,'rb') as fk: k = fk.read()
    with open(VAULT_FILE,'rb') as fv: token = fv.read()
    f = Fernet(k)
    data = f.decrypt(token)
    return eval(data.decode('utf-8'))
