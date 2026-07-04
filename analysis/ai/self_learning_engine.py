import json
import logging


class SelfLearningEngine:

    def __init__(self, file_path="learning_memory.json"):
        self.file_path = file_path
        self.logger = logging.getLogger("AI_LEARN")

    # ======================================================
    # SAVE RESULT
    # ======================================================
    def record_trade(self, signal, result):

        entry = {
            "symbol": signal.symbol,
            "signal": signal.signal,
            "confidence": signal.confidence_score,
            "result": result
        }

        try:
            data = []

            try:
                with open(self.file_path, "r") as f:
                    data = json.load(f)
            except:
                data = []

            data.append(entry)

            with open(self.file_path, "w") as f:
                json.dump(data, f, indent=2)

            self.logger.info("TRADE RECORDED")

        except Exception as e:
            self.logger.error(f"Learning error: {e}")

    # ======================================================
    # SIMPLE ADAPTATION RULE
    # ======================================================
    def adjust_confidence(self, signal):

        try:
            with open(self.file_path, "r") as f:
                data = json.load(f)

            wins = 0
            total = 0

            for t in data[-50:]:
                if t["signal"] == signal.signal:
                    total += 1
                    if "PROFIT" in t["result"]:
                        wins += 1

            if total == 0:
                return signal.confidence_score

            win_rate = wins / total

            adjusted = signal.confidence_score * (0.5 + win_rate)

            return min(100, adjusted)

        except:
            return signal.confidence_score
