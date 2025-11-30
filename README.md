FC26 Player Chatbot — Systems Final Case
1) Executive Summary
Problem:
The FC 26 video game dataset contains 110 columns with 18,406 rows. Each row is a distinct observation and represents a single player while the 110 columns contain all the features relating the player. With datasets as large as this, it is highly inefficient to download such a big dataset to view simple questions. In addition to this, while playing FC 26, the different cards are filtered by overall including special cards. The dataset only contains the base cards therefore being helpful for those interested to learn more about different players that better fits their team without having to filter out special cards. With this in mind, a chatbot that fulfills basic questions about the dataset would be useful to save storage and unnecessary time.

Solution:
Relating to the "problem", I built a chatbot that specializes in exploring the FC 26 player dataset that excludes special cards. The chatbot is able to answer simple questions such as "Who is the best player?", "What player is the best at a specific field?" (such as dribbling, shooting, passing, etc.), "Who is the best player from a specific country?" (such as England, Spain, Italy, France, etc.), and more. This chatbot is accessible through a link and is being run on an Azure virtual machine for easy deployment and reproducibility.

2) System Overview
Course Concept(s) Used:
Case 5 - Infrastructure: Storage & Data Management style Case
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
Data Source: data/FC26_20250921.csv (FC26 player stats)
Model: Deterministic rule-based logic (no ML model)
Service: Flask API served via Gunicorn inside Docker

3) How to Run (Local)
Docker
Build:
docker build -t fc26-chatbot .
Run:
docker run -d -p 5001:5001 fc26-chatbot

Health Check (local):
curl http://localhost:5001/api/health

Direct Python (Alternative)

Environment Setup:
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

Run App:
python src/app.py

Open in Browser:
http://127.0.0.1:5001

4) Design Decisions
Why This Concept / Tools?
Pandas for flexible CSV filtering and ranking. Flask for a minimal, easy-to-grade REST API. Gunicorn to run Flask in a production-like WSGI server. Docker to ensure reproducible environment and simple deployment. Azure VM for a stable, public cloud URL and full control over networking. GitHub Actions for automated testing and CI.

Alternatives Considered (and not chosen):
LLM/NLP-based parsing: more complex, less deterministic, harder to grade. Managed PaaS (Azure App Service): VM is simpler to reason about for this project. Relational DB: unnecessary for read-only CSV queries.

Tradeoffs:
Simplicity vs flexibility: rule-based logic is easy to maintain but less expressive. VM requires manual ops (ports, firewall), but gives clear visibility for learning. 

Security / Privacy / Ops:
No user data or secrets stored. Only necessary ports exposed (SSH + app). /api/health endpoint used for simple health checks. Docker image contains only code + dataset; no credentials baked in.

5) Results & Evaluation
5.1 Screenshots / Sample Outputs

Chatbot UI (Cloud-Hosted on Azure VM):
The chatbot runs in the browser and accepts natural-language questions like “What player is the best?” and “Who is the best at defending?”. Responses are computed from the FC26 dataset using Pandas.

API Health Endpoint (Public URL):
The /api/health endpoint returns a simple JSON payload ({"status":"ok"}), confirming that the Flask app and container are running correctly on the Azure VM.

Docker Container Running on Azure VM:
The docker ps screenshot shows the fc26-chatbot container running on the VM, with port mapping 0.0.0.0:5001->5000/tcp, confirming containerization and reproducibility.

GitHub Actions CI Passing:
A GitHub Actions workflow (.github/workflows/ci.yml) runs pytest on each push to main. The green check mark indicates that the smoke tests completed successfully.

5.2 Performance Notes
Dataset size is modest (single CSV), so all queries complete in well under a second. CPU and memory usage of the container are low; a small Azure VM is sufficient. The app loads the CSV once at startup and reuses the in-memory DataFrame.

5.3 Validation / Tests
A smoke test in tests/test_smoke.py imports fc26_bot and verifies that answer_question("What player is the best?") returns a non-empty string. GitHub Actions automatically runs this test on every push. Manual validation was performed for sample queries:
Best overall player
Best player by passing, defending, shooting, dribbling, strength
Top 10 / bottom 10 players
Best player by nationality

6) What’s Next
Planned or possible future improvements:
Add true NLP parsing (e.g., spaCy or a small LLM) for more flexible questions.
Add player comparison queries (e.g., “Compare Player A vs Player B”).
Add data visualizations such as radar charts for top players.
Move to Azure App Service or a managed container platform.
Expand the test suite to include more edge cases and routing tests.

7) Links (Required)
GitHub Repository:
https://github.com/Khalid-Bakhit/fc26-chatbot

Public Cloud App (Azure VM):
http://20.151.75.201:5001

8) Academic Integrity:
ChatGPT model 5.1 was used to help create The Final Case