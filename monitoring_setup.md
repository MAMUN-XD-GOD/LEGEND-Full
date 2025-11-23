Monitoring setup guide:
1. Start monitoring exporter: python monitoring/prometheus_exporter.py
2. Add Prometheus scrape target to prometheus.yml
3. Import Grafana dashboard JSON into Grafana
4. Configure alertmanager with alert_rules.yaml
