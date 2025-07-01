import json, subprocess
from langgraph import Agent

class SemanticEnricher(Agent):
    def run(self, raw_txn):
        # Serialize transaction as JSON prompt
        prompt = json.dumps({
            "task": "Analyze for anomalies",
            "transaction": raw_txn
        })

        # Call Ollama
        proc = subprocess.run([
            "ollama", "run", "llama2:7b",
            "--quantize", "4bit",
            "--prompt", prompt
        ], capture_output=True, text=True)

        if proc.returncode != 0:
            self.logger.error(f"Ollama error: {proc.stderr}")
            return

        enriched_text = proc.stdout.strip()
        enriched_record = {**raw_txn, "enrichment": enriched_text}
        self.emit("enriched_txn", enriched_record)
