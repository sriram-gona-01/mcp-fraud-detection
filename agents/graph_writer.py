import os
from neo4j import GraphDatabase
from langgraph import Agent

driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
)

class GraphWriter(Agent):
    def run(self, enriched_txn):
        with driver.session() as session:
            session.write_transaction(self._write_txn, enriched_txn)

    @staticmethod
    def _write_txn(tx, txn):
        tx.run(
            """
            MERGE (a:Account {id: $acct})
            CREATE (t:Transaction {id: $id, amount: $amt, info: $enrich})
            MERGE (a)-[:MADE]->(t)
            """,
            acct=txn["account_id"],
            id=txn["txn_id"],
            amt=txn["amount"],
            enrich=txn["enrichment"]
        )
