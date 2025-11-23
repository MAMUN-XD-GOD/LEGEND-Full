import hashlib

def file_hash(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        while True:
            b=f.read(8192)
            if not b: break
            h.update(b)
    return h.hexdigest()
