FC26 Player Chatbot — Systems Final Case
1) Executive Summary

Problem:
The FC 26 video game dataset contains 110 columns with 18,406 rows. Each row is a distinct observation and represents a single player while the 110 columns contain all the features relating the player. With datasets as large as this, it is highly inefficient to download such a big dataset to view simple questions. In addition to this, while playing FC 26, the different cards are filtered by overall including special cards. The dataset only contains the base cards therefore being helpful for those interested to learn more about different players that better fits their team without having to filter out special cards. With this in mind, a chatbot that fulfills basic questions about the dataset would be useful to save storage and unnecessary time.

Solution:
Relating to the "problem", I built a chatbot that specializes in exploring the FC 26 player dataset that excludes special cards. The chatbot is able to answer simple questions such as "Who is the best player?", "What player is the best at a specific field?" (such as dribbling, shooting, passing, etc.), "Who is the best player from a specific country?" (such as England, Spain, Italy, France, etc.), and more. This chatbot is accessible through a link and is being run on an Azure virtual machine for easy deployment and reproducibility.

1) System Overview

Course Concept(s) Used:

Containerization (Docker)

REST APIs (Flask)

Production servers (Gunicorn)

Cloud compute (Azure VM)

Continuous Integration (GitHub Actions)

Data processing pipeline (Pandas)

Architecture Diagram:

 ┌────────────────────────┐
 │      Web Browser       │
 │   (Chat UI: HTML/JS)   │
 └──────────────┬─────────┘
                │ POST /api/chat
                ▼
 ┌────────────────────────┐
 │        Flask API        │
 │      (src/app.py)       │
 └──────────────┬─────────┘
                │
                ▼
 ┌────────────────────────┐
 │     fc26_bot.py        │
 │  Pandas logic & rules  │
 └──────────────┬─────────┘
                │
                ▼
 ┌────────────────────────┐
 │ FC26_20250921.csv      │
 │ Player Statistics Data │
 └────────────────────────┘

 Entire system packaged in Docker → deployed on Azure VM


Data/Models/Services:

Data Source: FC26 dataset (FC26_20250921.csv)

Model: Deterministic rule-based logic (no ML model)

Service: Flask API served via Gunicorn inside Docker

3) How to Run (Local)
Docker

Build:

docker build -t fc26-chatbot .


Run:

docker run -d -p 5001:5001 fc26-chatbot


Health Check:

curl http://localhost:5001/api/health

Direct Python (Alternative)

Environment Setup:

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt


Run App:

python src/app.py

4) Design Decisions
Why This Approach?

Pandas: Fast, flexible CSV manipulation for ranking players.

Flask API: Lightweight and perfect for routing chat requests.

Gunicorn: Production-ready HTTP server for WSGI apps.

Docker: Ensures the environment is identical on local machine, GitHub Actions, and Azure.

Azure VM: Provides public, stable hosting for extra credit.

CI Pipeline: Ensures correctness via automated smoke tests.

Alternatives Considered (and why not chosen):

LLM-based NLP: Too heavy for deterministic grading, non-reproducible.

Azure App Service: VM offers clearer control and easier debugging.

Database: Unnecessary for read-only CSV data.

Tradeoffs:

Performance: Excellent (small CSV, fast lookups).

Complexity: Rule-based logic is simple but rigid.

Maintainability: Modular structure keeps code clean.

Security/Privacy:

No user data stored.

No secrets in source code.

VM limited to only required ports.

Ops:

CI tests validate correctness.

/api/health used for uptime checks.

Docker container guarantees reproducibility.

5) Results & Evaluation
Functionality

The chatbot successfully handles many natural-language queries, including:

Best overall player

Best defender, passer, shooter, dribbler, strongest player

Worst player

Highest potential

Best player by nationality (England, Spain, France, Germany, Italy, etc.)

Top 10 and bottom 10 players

Testing

A smoke test (tests/test_smoke.py) validates that:

The dataset loads

answer_question() returns a valid response

The system does not crash under simple queries

Cloud Deployment

The app is deployed at:

👉 http://20.151.75.201:5001

Fully satisfies Cloud Deployment Extra Credit (+5).

CI Pipeline

GitHub Actions automatically:

Installs dependencies

Runs tests

Ensures system integrity

Fully satisfies CI/Observability Extra Credit (+5).

6) What’s Next

Planned improvements:

Add real NLP (spaCy or TinyLlama)

Add comparison questions (“Compare Player X vs Player Y”)

Add data visualizations (radar charts, scatter plots)

Deploy to Azure App Service for auto-scaling

Add more tests (integration + regression tests)

7) Links (Required)

GitHub Repo:
https://github.com/Khalid-Bakhit/fc26-chatbot

Cloud Deployment URL:
http://20.151.75.201:5001