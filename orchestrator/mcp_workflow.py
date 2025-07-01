from langgraph import Workflow
from agents.data_extractor import DataExtractor
from agents.semantic_enricher import SemanticEnricher
from agents.graph_writer import GraphWriter

wf = Workflow(name="fraud_mcp")

ext = wf.add_agent(DataExtractor())
enc = wf.add_agent(SemanticEnricher())
wrt = wf.add_agent(GraphWriter())

wf.connect(ext,  "raw_txn",    enc, "raw_txn")
wf.connect(enc,  "enriched_txn", wrt, "enriched_txn")

if __name__ == "__main__":
    wf.run(loop=True)
