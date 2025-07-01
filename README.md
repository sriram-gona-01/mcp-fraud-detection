# MCP Fraud Detection Platform

An end-to-end **Multi-Agent Control Platform (MCP)** for fraud detection in financial transaction data. This project combines:

- **LangGraph** agent orchestration  
- **Ollama + Llama 2 7B (4-bit quantized)** for semantic enrichment  
- **Neo4j** knowledge graph for relationship modeling  

It enables continuous data ingestion, context-aware anomaly analysis, and interactive graph storage to drastically accelerate and improve fraud detection.

---

## 🚀 Features

- **Real-time data ingestion** from Kafka (or any message source)  
- **Semantic enrichment** of each transaction via a local Llama 2 7B model  
- **Graph storage** in Neo4j to visualize account-transaction relationships  
- **Adaptive reasoning** loops via LangGraph, enabling agents to refine patterns over time  
- **Dockerized** for easy local development and testing  
- **Extensible**: add new agents, data sources, or graph schemas with minimal changes  

---

## 📐 Architecture Overview

![20250701_0119_Refined MCP Workflow Diagram_simple_compose_01jz2a6dsgen1spq0qrbz19928](https://github.com/user-attachments/assets/41203240-3178-461b-b24a-7dbde3f36492)



1. **DataExtractor** pulls messages, emits `raw_txn`.  
2. **SemanticEnricher** calls `ollama run llama2:7b --quantize 4bit` on each record, emits `enriched_txn`.  
3. **GraphWriter** writes nodes/relationships into Neo4j.  
4. **LangGraph** ties agents together and orchestrates continuous loops.

---

## 🔧 Prerequisites

- **Python 3.10+**  
- **Docker & Docker Compose** (for Neo4j and optional containerized run)  
- **Kafka** (or another message broker) — you can mock this in tests  
- **Ollama** CLI installed & `llama2:7b` model pulled:  
  ```bash
  ollama pull llama2:7b --quantize 4bit
  ```  

---

## 🛠️ Installation & Setup

1. **Clone the repo**  
   ```bash
   git clone git@github.com:<you>/mcp-fraud-detection.git
   cd mcp-fraud-detection
   ```

2. **Create & activate a virtual environment**  
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Python dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**  
   - Copy `config/secrets.example.env` → `.env`  
   - Fill in your Neo4j credentials and Kafka settings  
   - `config/config.yml` holds data source topics, model name (`llama2:7b`), quantization, batch sizes, etc.

---

## ▶️ Running Locally

### 1. Start Neo4j with Docker  
```bash
docker network create mcp-network
docker run -d --name neo4j --network mcp-network   -p 7474:7474 -p 7687:7687   -e NEO4J_AUTH=neo4j/changeit   neo4j:5.11
```

### 2. Launch the MCP Workflow  
```bash
source venv/bin/activate
python orchestrator/mcp_workflow.py
```

Transactions published to your Kafka topic will flow through the agents and into Neo4j.

---

## 🐳 Containerized Setup (Optional)

1. **Build & start services**  
   ```bash
   cd docker
   docker-compose up --build
   ```
2. **Access Neo4j Browser** at [http://localhost:7474](http://localhost:7474)  
3. **View logs** for the `app` service to confirm agent activity.

---

## 🔬 Testing

- Unit tests live in `tests/`.  
- Mocks `subprocess.run` and `neo4j` driver for offline testing.  
- Run with:
  ```bash
  pytest --maxfail=1 --disable-warnings -q
  ```

---

## ⚙️ Configuration

All runtime settings are in `config/config.yml`:

```yaml
data_sources:
  kafka_topic: txn_topic
  kafka_bootstrap: localhost:9092

enrichment:
  model: llama2:7b
  quantize: 4bit

graph:
  batch_size: 100
```

Adjust topics, bootstrap servers, model names, and batch sizes as needed.

---

## 🤝 Contributing

1. Fork the repository  
2. Create a feature branch (`git checkout -b feature/xyz`)  
3. Commit your changes (`git commit -m "Add xyz"`)  
4. Push and open a Pull Request  
5. Ensure all tests pass and update documentation if necessary

---

## 📜 License

This project is licensed under the **MIT License**.

---

## 🙋‍♂️ Contact

_Sriram Gona_  
- GitHub: [@sriram-gona-01](https://github.com/sriram-gona-01)  
- Email: sriram.gona.01@gmail.com  

Feel free to open issues or reach out with questions, suggestions, or feedback!
