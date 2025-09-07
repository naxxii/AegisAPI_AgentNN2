# AegisAPI AgentNN - Database & Integration Guide

This directory contains comprehensive integration modules for AegisAPI AgentNN, supporting Postman collections, SQL databases, NoSQL databases, and flexible telemetry storage systems.

## 📁 Integration Modules

| Module | Description | Use Case |
|--------|-------------|----------|
| `postman_integration.py` | Import/export Postman collections | Convert existing Postman tests to AegisAPI |
| `sql_integration.py` | SQL database storage (SQLite, PostgreSQL, MySQL) | Enterprise-grade data persistence |
| `nosql_integration.py` | MongoDB integration | Flexible document storage |
| `telemetry_backends.py` | Multi-backend telemetry system | Distributed logging and monitoring |
| `integration_examples.py` | Complete working examples | Get started quickly |

## 🚀 Quick Start

### 1. Basic Setup
```bash
# Install additional dependencies for integrations
pip install pymongo redis sqlalchemy psycopg2-binary mysql-connector-python
```

### 2. Choose Your Integration

#### Option A: Postman Integration
```python
from aegisapi.integrations.postman_integration import PostmanIntegration

# Load Postman collection
integration = PostmanIntegration()
collection = integration.load_collection("my_collection.json")

# Convert to AegisAPI tests
test_dir = integration.generate_aegis_tests(collection.name)
```

#### Option B: SQL Database Integration
```python
from aegisapi.integrations.sql_integration import create_sqlite_integration

# Create database connection
db = create_sqlite_integration("aegisapi.db")

# Register API and record test results
api_id = db.register_api_test("My API", "spec.yaml", "https://api.example.com")
run_id = db.record_test_run(api_id, "success", test_count=5, passed_count=5)
```

#### Option C: NoSQL Database Integration
```python
from aegisapi.integrations.nosql_integration import create_mongodb_integration

# Create MongoDB connection
mongo_db = create_mongodb_integration()

# Store test results
api_id = mongo_db.register_api_test("My API", "spec.yaml", "https://api.example.com")
run_id = mongo_db.record_test_run(api_id, "success", test_count=5)
```

## 🔧 Configuration

### Database Configuration
```python
# config.py
DATABASE_CONFIG = {
    # SQL Database
    "sql_enabled": True,
    "sql_connection_string": "postgresql://user:pass@localhost/aegisapi",

    # NoSQL Database
    "nosql_enabled": True,
    "nosql_connection_string": "mongodb://localhost:27017/",
    "nosql_database": "aegisapi",

    # Redis Cache
    "redis_enabled": True,
    "redis_host": "localhost",
    "redis_port": 6379,
    "redis_db": 0,

    # File Fallback
    "file_enabled": True,
    "telemetry_dir": "data",
    "telemetry_file": "telemetry.jsonl"
}
```

### Telemetry Setup
```python
from aegisapi.integrations.telemetry_backends import setup_telemetry_backends

# Setup multiple telemetry backends
setup_telemetry_backends(DATABASE_CONFIG)

# Log events (automatically distributed to all backends)
from aegisapi.integrations.telemetry_backends import log_event
log_event("test_started", "Starting API test", {"api_name": "petstore"})
```

## 📊 Integration Examples

### 1. Postman → AegisAPI → SQL Database
```python
from aegisapi.integrations.postman_integration import PostmanIntegration
from aegisapi.integrations.sql_integration import create_sqlite_integration

# 1. Import Postman collection
postman = PostmanIntegration()
collection = postman.load_collection("petstore_collection.json")

# 2. Convert to AegisAPI tests
test_dir = postman.generate_aegis_tests(collection.name)

# 3. Setup SQL storage
db = create_sqlite_integration("petstore_results.db")
api_id = db.register_api_test(collection.name, base_url="https://petstore.swagger.io/v2")

# 4. Run tests and store results
# (Use regular AegisAPI CLI commands)
```

### 2. Multi-Database Enterprise Setup
```python
from aegisapi.integrations.sql_integration import SQLIntegration
from aegisapi.integrations.nosql_integration import MongoDBIntegration
from aegisapi.integrations.telemetry_backends import TelemetryManager

# 1. Setup databases
sql_db = SQLIntegration("postgresql://prod:pass@db.company.com/aegisapi")
nosql_db = MongoDBIntegration("mongodb://db.company.com:27017/aegisapi_prod")

# 2. Setup telemetry
telemetry = TelemetryManager()
telemetry.add_backend("sql", sql_db)
telemetry.add_backend("nosql", nosql_db)

# 3. Register enterprise APIs
apis = [
    {"name": "User API", "base_url": "https://api.company.com/users"},
    {"name": "Product API", "base_url": "https://api.company.com/products"}
]

for api in apis:
    # Register in both databases
    sql_id = sql_db.register_api_test(api["name"], base_url=api["base_url"])
    nosql_id = nosql_db.register_api_test(api["name"], base_url=api["base_url"])
```

### 3. Real-time Monitoring Dashboard
```python
from aegisapi.integrations.telemetry_backends import get_telemetry_manager

# Get real-time statistics
telemetry = get_telemetry_manager()
stats = telemetry.get_stats()

print(f"📊 Active APIs: {stats['file']['total_events']}")
print(f"🗄️ SQL Events: {len(telemetry.search_events('test_completed'))}")
print(f"📈 Recent Events: {len(telemetry.get_recent_events(10))}")
```

## 🗄️ Database Schema

### SQL Database Tables

#### `api_tests`
- `id` - Primary key
- `name` - API name
- `spec_path` - Path to API specification
- `base_url` - API base URL
- `description` - API description
- `created_at` - Creation timestamp
- `status` - API status

#### `test_runs`
- `id` - Primary key
- `api_test_id` - Foreign key to api_tests
- `status` - Test run status
- `duration` - Test execution time
- `test_count` - Number of tests
- `passed_count` - Number of passed tests
- `failed_count` - Number of failed tests

#### `test_results`
- `id` - Primary key
- `test_run_id` - Foreign key to test_runs
- `test_name` - Individual test name
- `status` - Test result status
- `duration` - Test execution time
- `error_message` - Error details if failed

### NoSQL Collections

#### `api_tests` (MongoDB)
```json
{
  "_id": "ObjectId",
  "name": "Pet Store API",
  "spec_path": "/path/to/spec.yaml",
  "base_url": "https://petstore.swagger.io/v2",
  "created_at": 1703123456.789,
  "last_run": 1703123456.789,
  "test_count": 5,
  "success_rate": 0.95
}
```

#### `test_runs` (MongoDB)
```json
{
  "_id": "ObjectId",
  "api_test_id": "ObjectId",
  "status": "success",
  "duration": 3.45,
  "run_timestamp": 1703123456.789,
  "test_count": 5,
  "passed_count": 5,
  "failed_count": 0,
  "environment": {
    "python_version": "3.9",
    "os": "linux"
  }
}
```

## 🔧 Advanced Configuration

### Connection Pooling
```python
# For high-throughput environments
from sqlalchemy.pool import QueuePool
engine = create_engine(
    "postgresql://user:pass@localhost/db",
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20
)
```

### Data Migration
```python
from aegisapi.integrations.sql_integration import migrate_from_jsonl_to_sql

# Migrate existing telemetry data to SQL
migrate_from_jsonl_to_sql(sql_integration, "data/telemetry.jsonl")
```

### Backup and Recovery
```python
# Export all data
sql_data = sql_integration.export_data()
nosql_data = nosql_integration.export_data()

# Save backups
with open("backup_sql.json", 'w') as f:
    json.dump(sql_data, f, default=str)

with open("backup_nosql.json", 'w') as f:
    json.dump(nosql_data, f, default=str)
```

## 📊 Monitoring & Analytics

### Real-time Dashboards
```python
# Get comprehensive statistics
from aegisapi.integrations.sql_integration import create_sqlite_integration

db = create_sqlite_integration("aegisapi.db")
stats = db.get_dashboard_stats()

print(f"APIs: {stats['api_count']}")
print(f"Total Runs: {stats['total_runs']}")
print(f"Success Rate: {stats['successful_runs'] / stats['total_runs'] * 100:.1f}%")
```

### Performance Metrics
```python
# Query performance data
from aegisapi.integrations.telemetry_backends import search_events

# Find slow tests
slow_tests = search_events(
    event_type="test_completed",
    metadata_filter={"duration": {"$gt": 5.0}}
)

# API response time trends
response_times = search_events(
    event_type="test_result",
    metadata_filter={"response_time": {"$exists": True}}
)
```

## 🚀 Production Deployment

### Docker Configuration
```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    mongodb-clients \
    redis-tools \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . /app
WORKDIR /app

# Environment variables
ENV SQL_CONNECTION_STRING=postgresql://user:pass@db/aegisapi
ENV MONGODB_CONNECTION_STRING=mongodb://mongodb:27017/aegisapi
ENV REDIS_URL=redis://redis:6379/0

EXPOSE 8080

CMD ["python", "-c", "from aegisapi.cli import main; main() web --host 0.0.0.0"]
```

### Kubernetes Deployment
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: aegisapi-config
data:
  SQL_CONNECTION_STRING: "postgresql://user:pass@postgres/aegisapi"
  MONGODB_CONNECTION_STRING: "mongodb://mongodb:27017/aegisapi"

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: aegisapi
spec:
  replicas: 3
  selector:
    matchLabels:
      app: aegisapi
  template:
    metadata:
      labels:
        app: aegisapi
    spec:
      containers:
      - name: aegisapi
        image: company/aegisapi:latest
        ports:
        - containerPort: 8080
        envFrom:
        - configMapRef:
            name: aegisapi-config
```

## 🔍 Troubleshooting

### Common Issues

#### 1. Database Connection Failed
```python
# Check connection string format
# SQLite: sqlite:///aegisapi.db
# PostgreSQL: postgresql://user:pass@localhost:5432/dbname
# MySQL: mysql://user:pass@localhost:3306/dbname
# MongoDB: mongodb://localhost:27017/dbname
```

#### 2. Import Errors
```bash
# Install missing dependencies
pip install pymongo redis sqlalchemy psycopg2-binary mysql-connector-python
```

#### 3. Permission Errors
```bash
# Ensure write permissions for data directories
chmod 755 data/
chmod 644 data/telemetry.jsonl
```

### Debug Mode
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Enable detailed logging
from aegisapi.integrations.telemetry_backends import log_event
log_event("debug_mode", "Debug logging enabled", {"level": "DEBUG"})
```

## 📚 API Reference

### Postman Integration API
- `PostmanIntegration.load_collection(path)` - Load Postman collection
- `PostmanIntegration.convert_to_openapi(name)` - Convert to OpenAPI
- `PostmanIntegration.generate_aegis_tests(name)` - Generate AegisAPI tests
- `PostmanIntegration.export_test_results(name, results)` - Export results

### SQL Integration API
- `SQLIntegration.register_api_test(name, ...)` - Register API
- `SQLIntegration.record_test_run(api_id, status, ...)` - Record test run
- `SQLIntegration.record_test_result(run_id, test_name, ...)` - Record test result
- `SQLIntegration.get_dashboard_stats()` - Get statistics

### NoSQL Integration API
- `MongoDBIntegration.register_api_test(name, ...)` - Register API
- `MongoDBIntegration.log_telemetry_event(type, summary, ...)` - Log event
- `MongoDBIntegration.search_events(type, ...)` - Search events
- `MongoDBIntegration.export_data()` - Export all data

## 🎯 Best Practices

1. **Use Multiple Backends**: Combine SQL for structure with NoSQL for flexibility
2. **Implement Data Retention**: Configure automatic cleanup of old data
3. **Monitor Performance**: Track database query performance
4. **Backup Regularly**: Export data periodically for backup
5. **Use Connection Pooling**: Configure appropriate connection pool sizes
6. **Implement Retry Logic**: Handle temporary database connection issues

## 📞 Support

- **Documentation**: Check individual module docstrings
- **Examples**: Run `integration_examples.py` for working examples
- **Issues**: Report bugs and request features
- **Community**: Join discussions about integrations

---

**🎉 Ready to integrate AegisAPI AgentNN with your databases and workflows!**
