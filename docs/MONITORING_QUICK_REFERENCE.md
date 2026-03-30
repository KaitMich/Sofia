> **CORRECTED March 27, 2026** -- See SOPHIA_TRUTH_FRAMEWORK.md for project-wide corrections.

# Monitoring Quick Reference Card

**Problem:** You need to see what Sophia is actually doing/thinking after autonomous learning sessions.

**Full Guide:** `/docs/PARENTAL_MONITORING_GUIDE.md`

---

## After Every Learning Session

```bash
# 1. Check latest session report (AUTO-GENERATED)
cat data/logs/session_reports/REPORT_*.md

# 2. Check for high-surprise events (>0.9)
grep "0.9" data/logs/session_reports/REPORT_*.md

# 3. Check recent values (last 24h)
python3 -c "
import json
from datetime import datetime, timedelta
with open('data/personal_values.json', 'r') as f:
    values = json.load(f)
cutoff = (datetime.now() - timedelta(hours=24)).isoformat()
recent = [v for v in values if v.get('formation_context', {}).get('formation_time', '9999') > cutoff]
print(f'{len(recent)} values formed in last 24h')
for v in recent:
    print(f'  • {v[\"statement\"][:80]}')
"
```

---

## Memory Growth Check

```bash
python3 -c "
import json
for fname in ['logic_memory.json', 'symbolic_memory.json', 'bridge_memory.json']:
    with open(f'data/{fname}', 'r') as f:
        data = json.load(f)
        count = len(data) if isinstance(data, list) else len(data.get('items', []))
        print(f'{fname:25s}: {count:>8,}')
"
```

---

## Existing Monitoring Tools

| **What** | **Command** |
|----------|-------------|
| Session reports | Auto-generated in `data/logs/session_reports/` |
| Memory analytics | `python3 -c "from memory_analytics import MemoryAnalyzer; ..."` |
| Symbol learning | `python3 learning_dashboard.py` |
| Brain metrics | `python3 -c "from brain_metrics import BrainMetricsCollector; ..."` |

**DO NOT create new monitoring scripts.** 100+ scripts already exist.

---

**See Full Guide:** `/docs/PARENTAL_MONITORING_GUIDE.md`
