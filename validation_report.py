import json

def generate_report(metrics, out='validation_report.json'):
    with open(out,'w') as f:
        json.dump(metrics, f, indent=2)
    return out
