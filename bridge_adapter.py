import json
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

from alphawall import AlphaWall


class AlphaWallBridge:
    """
    Thin wrapper around AlphaWall that produces the routing decision shape
    expected by EnhancedLinkEvaluator in utils/link_evaluator.py.

    Three public methods used by that caller:
      - process_with_alphawall(...)  → bridge_decision dict
      - learn_from_feedback(...)     → persist outcome to JSON
      - get_decision_pattern_analysis() → summary of persisted outcomes
    """

    _SYMBOLIC_STATES = {"grief", "overwhelmed", "angry", "emotionally_recursive"}

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.alphawall = AlphaWall(data_dir=str(self.data_dir))
        self._log_file = self.data_dir / "alphawall_bridge_decisions.json"

    def process_with_alphawall(
        self,
        user_input: str,
        base_logic_score: Optional[float] = None,
        base_symbolic_score: Optional[float] = None,
        user_data: Optional[Dict] = None,
    ) -> Dict:
        zone_result = self.alphawall.process_input(user_input, user_data or "anonymous")
        tags = zone_result.get("zone_output", {}).get("tags", {})
        action = zone_result.get("action", "")

        if action == "QUARANTINED":
            decision_type = "QUARANTINE"
            confidence = 1.0
            logic_score = base_logic_score or 0.0
            symbolic_score = base_symbolic_score or 0.0
        else:
            emotional_state = tags.get("emotional_state", "neutral")
            intent = tags.get("intent", "unknown")

            # Resolve scores: use provided values or derive from zone tags
            logic_score = base_logic_score if base_logic_score is not None else self._derive_logic_score(tags)
            symbolic_score = base_symbolic_score if base_symbolic_score is not None else self._derive_symbolic_score(tags)

            if emotional_state in self._SYMBOLIC_STATES:
                decision_type = "FOLLOW_SYMBOLIC"
                confidence = 0.75
            elif intent == "information_request":
                decision_type = "FOLLOW_LOGIC"
                confidence = 0.80
            elif logic_score > symbolic_score + 0.15:
                decision_type = "FOLLOW_LOGIC"
                confidence = min(0.5 + (logic_score - symbolic_score), 0.95)
            elif symbolic_score > logic_score + 0.15:
                decision_type = "FOLLOW_SYMBOLIC"
                confidence = min(0.5 + (symbolic_score - logic_score), 0.95)
            else:
                decision_type = "FOLLOW_HYBRID"
                confidence = 0.60

        return {
            "decision_id": str(uuid.uuid4()),
            "decision_type": decision_type,
            "confidence": round(confidence, 3),
            "scores": {
                "base_logic": round(logic_score, 3),
                "base_symbolic": round(symbolic_score, 3),
            },
            "weight_adjustments": {
                "final_logic_scale": 2.0,
                "final_symbolic_scale": 1.0,
            },
            "zone_action": action,
            "timestamp": datetime.utcnow().isoformat(),
        }

    def learn_from_feedback(
        self,
        decision_id: str,
        was_successful: bool,
        feedback_type: Optional[str] = None,
    ) -> None:
        records = self._load_log()
        records.append({
            "decision_id": decision_id,
            "was_successful": was_successful,
            "feedback_type": feedback_type,
            "timestamp": datetime.utcnow().isoformat(),
        })
        self._save_log(records[-1000:])

    def get_decision_pattern_analysis(self) -> Dict:
        records = self._load_log()
        total = len(records)
        if total == 0:
            return {"total_decisions": 0, "success_rate": 0.0, "pattern_counts": {}}
        successes = sum(1 for r in records if r.get("was_successful"))
        pattern_counts: Dict[str, int] = {}
        for r in records:
            ft = r.get("feedback_type") or "unspecified"
            pattern_counts[ft] = pattern_counts.get(ft, 0) + 1
        return {
            "total_decisions": total,
            "success_rate": round(successes / total, 3),
            "pattern_counts": pattern_counts,
        }

    def _derive_logic_score(self, tags: Dict) -> float:
        intent = tags.get("intent", "")
        return 0.65 if intent == "information_request" else 0.40

    def _derive_symbolic_score(self, tags: Dict) -> float:
        emotional_state = tags.get("emotional_state", "neutral")
        return 0.65 if emotional_state in self._SYMBOLIC_STATES else 0.35

    def _load_log(self):
        if not self._log_file.exists():
            return []
        try:
            with open(self._log_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return []

    def _save_log(self, records) -> None:
        with open(self._log_file, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2)
