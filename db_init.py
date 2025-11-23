import sqlite3

def init(path='quantumapex.db'):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS candles (id INTEGER PRIMARY KEY, pair TEXT, ts INTEGER, open REAL, high REAL, low REAL, close REAL, volume REAL)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS signals (id INTEGER PRIMARY KEY, pair TEXT, direction TEXT, confidence REAL, reasons TEXT, entry_ts INTEGER, result TEXT, resolved_ts INTEGER)''')
    conn.commit(); conn.close()

if __name__=='__main__':
    init()
    print('DB initialized')
