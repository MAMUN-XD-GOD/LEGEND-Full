import requests, time

def check(url, timeout=3):
    try:
        r = requests.get(url, timeout=timeout)
        return r.status_code == 200
    except Exception:
        return False

if __name__=='__main__':
    # simple running example
    services = ['http://127.0.0.1:8765/','http://127.0.0.1:8000/']
    for s in services:
        ok = check(s)
        print(s, 'OK' if ok else 'DOWN')
