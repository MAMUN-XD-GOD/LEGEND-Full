import subprocess, time, os
SERVICES = [
    ('bridge', 'uvicorn backend.bridge_server:app --host 0.0.0.0 --port 8765'),
    ('frontend', 'uvicorn backend.frontend_server:app --host 0.0.0.0 --port 8000')
]
procs = {}
for name,cmd in SERVICES:
    p = subprocess.Popen(cmd, shell=True)
    procs[name]=p
print('Started services')
try:
    while True:
        time.sleep(5)
        for name,p in list(procs.items()):
            if p.poll() is not None:
                print(name,'exited; restarting')
                p = subprocess.Popen([s for n,s in SERVICES if n==name][0], shell=True)
                procs[name]=p
except KeyboardInterrupt:
    for p in procs.values(): p.terminate()
