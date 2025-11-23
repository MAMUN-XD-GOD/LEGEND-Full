Batch-3 contains:
- backend/backtester.py (run against historical CSV)
- backend/trainer.py (train ensemble model using XGBoost)
- backend/ensemble.py (load model + predict probability for CALL)
- examples/historical_sample.csv (example historical data - replace with your real data)

Run trainer: python backend/trainer.py examples/historical_sample.csv
Run backtester: python backend/backtester.py examples/historical_sample.csv
