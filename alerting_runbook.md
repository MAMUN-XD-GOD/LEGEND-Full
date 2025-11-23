Alerting runbook

- If Prometheus fires 'NoSignalsForLong':
  1. Check prometheus exporter (monitoring/prometheus_exporter.py)
  2. Check bridge_server (uvicorn logs)
  3. Check DB size and last candle timestamps
  4. If needed, restore from recent backup and re-run demo sender
