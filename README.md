# Lyftr Backend Assignment

A Dockerized FastAPI service that ingests webhook messages, stores them in SQLite, and exposes query, stats, health, and metrics endpoints.

---

## 📌 Features

* **Webhook ingestion** with HMAC-SHA256 signature verification
* **Idempotent processing** (duplicate `message_id` is ignored)
* **SQLite persistence**
* **Message querying** with pagination and filters
* **Aggregate stats endpoint**
* **Health checks** for liveness and readiness
* **Prometheus metrics**
* Fully **Dockerized**
* **Tested with pytest**

---

## 🏗️ Tech Stack

* **Python 3.11**
* **FastAPI**
* **SQLite**
* **Prometheus client**
* **Docker & Docker Compose**
* **pytest + httpx**

---

## 📁 Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── storage.py
│   ├── models.py
│   ├── schemas.py
│   ├── metrics.py
│   └── logging_utils.py
│
├── tests/
│   ├── conftest.py
│   ├── test_webhook.py
│   ├── test_messages.py
│   ├── test_stats.py
│   └── utils.py
│
├── Dockerfile
├── docker-compose.yml
├── pytest.ini
└── README.md
```

---

## ⚙️ Configuration

The service requires **two environment variables**:

| Variable         | Description                                    |
| ---------------- | ---------------------------------------------- |
| `WEBHOOK_SECRET` | Secret key used to validate webhook signatures |
| `DATABASE_URL`   | SQLite database URL                            |

Example:

```bash
WEBHOOK_SECRET=testsecret
DATABASE_URL=sqlite:////data/app.db
```

---

## ▶️ Running the Service

### 1️⃣ Start Docker Desktop (Windows / macOS)

Ensure Docker is running with **Linux containers**.

---

### 2️⃣ Set environment variables (PowerShell)

```powershell
$env:WEBHOOK_SECRET="testsecret"
$env:DATABASE_URL="sqlite:////data/app.db"
```

---

### 3️⃣ Build and run

```powershell
docker compose up -d --build
```

The API will be available at:

```
http://localhost:8000
```

---

## 🔍 API Endpoints

### Health

* `GET /health/live` → always returns 200 if app is running
* `GET /health/ready` → returns 200 only if env vars & DB are available

---

### Webhook

* `POST /webhook`
* Requires header: `X-Signature`
* Signature = `HMAC_SHA256(secret, raw_request_body)`
* Idempotent by `message_id`

---

### Messages

* `GET /messages`
* Query params:

  * `limit` (default 50)
  * `offset` (default 0)
  * `from`
  * `since` (ISO timestamp)
  * `q` (case-insensitive substring search)

---

### Stats

* `GET /stats`

Returns:

* total messages
* distinct senders
* messages per sender (top 10)
* first and last message timestamps

---

### Metrics

* `GET /metrics`
* Prometheus-compatible metrics including:

  * `http_requests_total`
  * `webhook_requests_total`

---

## 🧪 Running Tests

Tests are executed **inside Docker**.

```powershell
docker compose exec api pytest -v
```

All tests cover:

* Health endpoints
* Webhook signature validation
* Idempotency
* Message pagination & filters
* Stats aggregation

---

## 🧠 Design Decisions

* **SQLite** chosen for simplicity and portability
* **Raw-body HMAC validation** to match real webhook providers
* **SQL-based aggregation** for `/stats` (efficient, simple)
* **Docker-first setup** to ensure evaluator reproducibility
* **Minimal dependencies**, no ORM overhead

---

## 🛑 Stopping & Resetting

```powershell
docker compose down -v
```

This stops the service and removes the database volume.

---

## ✅ Evaluation Notes

* Designed to match the evaluator’s Linux + `curl` environment
* PowerShell quirks avoided in implementation
* Health and metrics endpoints intentionally simple
* All required behaviors covered by tests

---

## 👤 Author

**Your Name**

Vansh Goel

### ✅ You are done
