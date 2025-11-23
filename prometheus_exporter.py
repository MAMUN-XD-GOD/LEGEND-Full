from prometheus_client import start_http_server, Gauge
import time, psutil, sqlite3

UPTIME = Gauge('quantum_uptime_seconds', 'Uptime seconds')
CPU = Gauge('quantum_cpu_percent', 'CPU percent')
MEM = Gauge('quantum_mem_percent', 'Memory percent')
SIGNALS = Gauge('quantum_signals_total', 'Total signals emitted')
LAST_SIGNAL = Gauge('quantum_last_signal_ts', 'Last signal timestamp')
DB_PATH = 'quantumapex.db'

def collect_db_metrics():
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM signals')
        total = cur.fetchone()[0]
        cur.execute('SELECT MAX(resolved_ts) FROM signals')
        last = cur.fetchone()[0] or 0
        conn.close()
        return total, last
    except Exception:
        return 0, 0

def start_exporter(port=9100):
    start_http_server(port)
    start = time.time()
    while True:
        UPTIME.set(int(time.time() - start))
        CPU.set(psutil.cpu_percent(interval=1))
        MEM.set(psutil.virtual_memory().percent)
        total, last = collect_db_metrics()
        SIGNALS.set(total)
        LAST_SIGNAL.set(last)
        time.sleep(2)

if __name__=='__main__':
    start_exporter(9100)
