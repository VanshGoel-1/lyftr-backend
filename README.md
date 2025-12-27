### Run
make up

### Endpoints
POST /webhook  
GET /messages  
GET /stats  
GET /health/live  
GET /health/ready  
GET /metrics  

### Design Decisions
- HMAC SHA256 verified on raw request body
- Idempotency via PRIMARY KEY on message_id
- Pagination uses LIMIT/OFFSET with total count
- Metrics via prometheus_client

Setup Used: VSCode
