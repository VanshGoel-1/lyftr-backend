from prometheus_client import Counter, Histogram, generate_latest

HTTP_COUNTER = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["path", "status"]
)

WEBHOOK_COUNTER = Counter(
    "webhook_requests_total",
    "Webhook outcomes",
    ["result"]
)

LATENCY = Histogram(
    "request_latency_ms",
    "Request latency",
    buckets=(100, 500, 1000, float("inf"))
)
