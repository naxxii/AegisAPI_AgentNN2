"""
NoSQL Database Integration for AegisAPI AgentNN
Supports MongoDB with flexible document storage for telemetry and test results
"""
import time
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from pymongo import MongoClient, DESCENDING
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from pathlib import Path

class MongoDBIntegration:
    """MongoDB integration for AegisAPI AgentNN"""

    def __init__(self, connection_string: str = "mongodb://localhost:27017/",
                 database_name: str = "aegisapi"):
        """
        Initialize MongoDB connection

        Args:
            connection_string: MongoDB connection string
            database_name: Name of the database to use
        """
        self.connection_string = connection_string
        self.database_name = database_name

        try:
            self.client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)
            # Test the connection
            self.client.admin.command('ping')
            print("✅ Connected to MongoDB successfully")

            self.db = self.client[database_name]

            # Create collections with indexes
            self._setup_collections()

        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            print(f"❌ MongoDB connection failed: {e}")
            print("📝 Falling back to file-based storage")
            self.client = None
            self.db = None

    def _setup_collections(self):
        """Setup collections and indexes"""
        if not self.db:
            return

        # API Tests collection
        self.api_tests = self.db.api_tests
        self.api_tests.create_index([("name", 1), ("created_at", -1)])
        self.api_tests.create_index([("status", 1)])

        # Test Runs collection
        self.test_runs = self.db.test_runs
        self.test_runs.create_index([("api_test_id", 1), ("run_timestamp", -1)])
        self.test_runs.create_index([("status", 1)])

        # Test Results collection
        self.test_results = self.db.test_results
        self.test_results.create_index([("test_run_id", 1), ("test_name", 1)])
        self.test_results.create_index([("status", 1)])

        # Telemetry Events collection
        self.telemetry_events = self.db.telemetry_events
        self.telemetry_events.create_index([("event_type", 1), ("timestamp", -1)])
        self.telemetry_events.create_index([("timestamp", -1)])

        # Healing Records collection
        self.healing_records = self.db.healing_records
        self.healing_records.create_index([("api_test_id", 1), ("healing_timestamp", -1)])
        self.healing_records.create_index([("status", 1)])

        # Dashboard Metrics collection
        self.dashboard_metrics = self.db.dashboard_metrics
        self.dashboard_metrics.create_index([("metric_name", 1), ("timestamp", -1)])

    def register_api_test(self, name: str, spec_path: str = None,
                         base_url: str = None, description: str = None,
                         version: str = None, metadata: Dict[str, Any] = None) -> str:
        """Register a new API test specification"""
        if not self.db:
            return self._fallback_register_api(name, spec_path, base_url, description)

        api_doc = {
            "name": name,
            "spec_path": spec_path,
            "base_url": base_url,
            "description": description,
            "version": version,
            "created_at": time.time(),
            "updated_at": time.time(),
            "status": "active",
            "metadata": metadata or {},
            "test_count": 0,
            "last_run": None,
            "success_rate": 0.0
        }

        result = self.api_tests.insert_one(api_doc)
        return str(result.inserted_id)

    def record_test_run(self, api_test_id: str, status: str,
                       duration: float = None, exit_code: int = 0,
                       pytest_output: str = None, test_count: int = 0,
                       passed_count: int = 0, failed_count: int = 0,
                       error_count: int = 0, environment: Dict[str, Any] = None) -> str:
        """Record a test run"""
        if not self.db:
            return self._fallback_record_test_run(api_test_id, status, duration, exit_code,
                                                pytest_output, test_count, passed_count,
                                                failed_count, error_count)

        run_doc = {
            "api_test_id": api_test_id,
            "status": status,
            "duration": duration,
            "exit_code": exit_code,
            "pytest_output": pytest_output,
            "test_count": test_count,
            "passed_count": passed_count,
            "failed_count": failed_count,
            "error_count": error_count,
            "run_timestamp": time.time(),
            "environment": environment or {},
            "created_at": time.time()
        }

        result = self.test_runs.insert_one(run_doc)

        # Update API test statistics
        self._update_api_stats(api_test_id)

        return str(result.inserted_id)

    def record_test_result(self, test_run_id: str, test_name: str,
                          status: str, duration: float = None,
                          error_message: str = None, stack_trace: str = None,
                          endpoint: str = None, method: str = None,
                          response_status: int = None, response_time: float = None,
                          metadata: Dict[str, Any] = None) -> str:
        """Record individual test result"""
        if not self.db:
            return self._fallback_record_test_result(test_run_id, test_name, status,
                                                   duration, error_message, stack_trace,
                                                   endpoint, method, response_status,
                                                   response_time)

        result_doc = {
            "test_run_id": test_run_id,
            "test_name": test_name,
            "status": status,
            "duration": duration,
            "error_message": error_message,
            "stack_trace": stack_trace,
            "endpoint": endpoint,
            "method": method,
            "response_status": response_status,
            "response_time": response_time,
            "metadata": metadata or {},
            "created_at": time.time()
        }

        result = self.test_results.insert_one(result_doc)
        return str(result.inserted_id)

    def log_telemetry_event(self, event_type: str, summary: str = None,
                           metadata: Dict[str, Any] = None) -> str:
        """Log telemetry event to MongoDB"""
        if not self.db:
            return self._fallback_log_telemetry(event_type, summary, metadata)

        event_doc = {
            "event_type": event_type,
            "summary": summary,
            "timestamp": time.time(),
            "metadata": metadata or {},
            "created_at": time.time()
        }

        result = self.telemetry_events.insert_one(event_doc)
        return str(result.inserted_id)

    def record_healing(self, api_test_id: str, old_spec_path: str,
                      new_spec_path: str, confidence_score: float,
                      changes: Dict[str, Any], status: str = 'proposed',
                      metadata: Dict[str, Any] = None) -> str:
        """Record healing action"""
        if not self.db:
            return self._fallback_record_healing(api_test_id, old_spec_path, new_spec_path,
                                               confidence_score, changes, status)

        healing_doc = {
            "api_test_id": api_test_id,
            "old_spec_path": old_spec_path,
            "new_spec_path": new_spec_path,
            "confidence_score": confidence_score,
            "changes": changes,
            "status": status,
            "healing_timestamp": time.time(),
            "field_renames": changes.get('field_renames', []),
            "status_changes": changes.get('status_changes', []),
            "metadata": metadata or {},
            "created_at": time.time()
        }

        result = self.healing_records.insert_one(healing_doc)
        return str(result.inserted_id)

    def get_dashboard_stats(self) -> Dict[str, Any]:
        """Get comprehensive dashboard statistics"""
        if not self.db:
            return self._fallback_get_stats()

        stats = {
            "api_count": self.api_tests.count_documents({}),
            "total_runs": self.test_runs.count_documents({}),
            "successful_runs": self.test_runs.count_documents({"status": "success"}),
            "failed_runs": self.test_runs.count_documents({"status": "failed"}),
            "healing_count": self.healing_records.count_documents({}),
            "applied_healings": self.healing_records.count_documents({"status": "applied"}),
            "telemetry_events_count": self.telemetry_events.count_documents({}),
            "recent_events": []
        }

        # Get recent events
        recent_events = list(self.telemetry_events
                           .find({})
                           .sort("timestamp", DESCENDING)
                           .limit(10))

        stats["recent_events"] = [
            {
                "type": event["event_type"],
                "summary": event.get("summary", ""),
                "timestamp": event["timestamp"]
            } for event in recent_events
        ]

        # Get success rates
        pipeline = [
            {"$group": {"_id": "$api_test_id", "avg_duration": {"$avg": "$duration"}, "count": {"$sum": 1}}}
        ]
        duration_stats = list(self.test_runs.aggregate(pipeline))

        stats["avg_test_duration"] = sum(stat.get("avg_duration", 0) for stat in duration_stats) / len(duration_stats) if duration_stats else 0

        return stats

    def get_test_history(self, api_test_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get test run history for an API"""
        if not self.db:
            return self._fallback_get_history(api_test_id, limit)

        runs = list(self.test_runs
                  .find({"api_test_id": api_test_id})
                  .sort("run_timestamp", DESCENDING)
                  .limit(limit))

        return [
            {
                "id": str(run["_id"]),
                "timestamp": run["run_timestamp"],
                "status": run["status"],
                "duration": run.get("duration"),
                "test_count": run.get("test_count", 0),
                "passed_count": run.get("passed_count", 0),
                "failed_count": run.get("failed_count", 0)
            } for run in runs
        ]

    def search_events(self, event_type: str = None, start_time: float = None,
                     end_time: float = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Search telemetry events with filters"""
        if not self.db:
            return []

        query = {}
        if event_type:
            query["event_type"] = event_type
        if start_time or end_time:
            query["timestamp"] = {}
            if start_time:
                query["timestamp"]["$gte"] = start_time
            if end_time:
                query["timestamp"]["$lte"] = end_time

        events = list(self.telemetry_events
                    .find(query)
                    .sort("timestamp", DESCENDING)
                    .limit(limit))

        return [
            {
                "id": str(event["_id"]),
                "type": event["event_type"],
                "summary": event.get("summary", ""),
                "timestamp": event["timestamp"],
                "metadata": event.get("metadata", {})
            } for event in events
        ]

    def export_data(self, collection_name: str = None) -> Dict[str, Any]:
        """Export data from MongoDB"""
        if not self.db:
            return {}

        data = {
            "export_timestamp": time.time(),
            "collections": {}
        }

        collections_to_export = [
            "api_tests", "test_runs", "test_results",
            "telemetry_events", "healing_records"
        ]

        if collection_name:
            collections_to_export = [collection_name]

        for collection_name in collections_to_export:
            collection = getattr(self, collection_name)
            documents = list(collection.find({}))
            data["collections"][collection_name] = documents

        return data

    def _update_api_stats(self, api_test_id: str):
        """Update API test statistics"""
        if not self.db:
            return

        # Get recent runs for this API
        recent_runs = list(self.test_runs
                         .find({"api_test_id": api_test_id})
                         .sort("run_timestamp", DESCENDING)
                         .limit(10))

        if recent_runs:
            success_count = sum(1 for run in recent_runs if run.get("status") == "success")
            success_rate = success_count / len(recent_runs)

            self.api_tests.update_one(
                {"_id": api_test_id if api_test_id else None},
                {
                    "$set": {
                        "last_run": recent_runs[0]["run_timestamp"],
                        "success_rate": success_rate,
                        "test_count": recent_runs[0].get("test_count", 0),
                        "updated_at": time.time()
                    }
                }
            )

    # Fallback methods for when MongoDB is not available
    def _fallback_register_api(self, name: str, spec_path: str, base_url: str, description: str) -> str:
        """Fallback API registration to file"""
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        api_file = data_dir / "api_tests.json"

        apis = []
        if api_file.exists():
            apis = json.loads(api_file.read_text())

        api_doc = {
            "id": str(time.time()),
            "name": name,
            "spec_path": spec_path,
            "base_url": base_url,
            "description": description,
            "created_at": time.time(),
            "status": "active"
        }

        apis.append(api_doc)
        api_file.write_text(json.dumps(apis, indent=2))
        return api_doc["id"]

    def _fallback_record_test_run(self, api_test_id: str, status: str, duration: float,
                                exit_code: int, pytest_output: str, test_count: int,
                                passed_count: int, failed_count: int, error_count: int) -> str:
        """Fallback test run recording"""
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        runs_file = data_dir / "test_runs.json"

        runs = []
        if runs_file.exists():
            runs = json.loads(runs_file.read_text())

        run_doc = {
            "id": str(time.time()),
            "api_test_id": api_test_id,
            "status": status,
            "duration": duration,
            "exit_code": exit_code,
            "test_count": test_count,
            "run_timestamp": time.time()
        }

        runs.append(run_doc)
        runs_file.write_text(json.dumps(runs, indent=2))
        return run_doc["id"]

    def _fallback_record_test_result(self, test_run_id: str, test_name: str, status: str,
                                   duration: float, error_message: str, stack_trace: str,
                                   endpoint: str, method: str, response_status: int,
                                   response_time: float) -> str:
        """Fallback test result recording"""
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        results_file = data_dir / "test_results.json"

        results = []
        if results_file.exists():
            results = json.loads(results_file.read_text())

        result_doc = {
            "id": str(time.time()),
            "test_run_id": test_run_id,
            "test_name": test_name,
            "status": status,
            "duration": duration,
            "endpoint": endpoint,
            "method": method,
            "response_status": response_status,
            "created_at": time.time()
        }

        results.append(result_doc)
        results_file.write_text(json.dumps(results, indent=2))
        return result_doc["id"]

    def _fallback_log_telemetry(self, event_type: str, summary: str, metadata: Dict[str, Any]) -> str:
        """Fallback telemetry logging"""
        from ..telemetry import log_event
        event = {
            "type": event_type,
            "summary": summary,
            "ts": time.time(),
            **metadata
        }
        log_event(event)
        return str(time.time())

    def _fallback_record_healing(self, api_test_id: str, old_spec_path: str, new_spec_path: str,
                               confidence_score: float, changes: Dict[str, Any], status: str) -> str:
        """Fallback healing recording"""
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        healing_file = data_dir / "healing_records.json"

        healings = []
        if healing_file.exists():
            healings = json.loads(healing_file.read_text())

        healing_doc = {
            "id": str(time.time()),
            "api_test_id": api_test_id,
            "old_spec_path": old_spec_path,
            "new_spec_path": new_spec_path,
            "confidence_score": confidence_score,
            "changes": changes,
            "status": status,
            "healing_timestamp": time.time()
        }

        healings.append(healing_doc)
        healing_file.write_text(json.dumps(healings, indent=2))
        return healing_doc["id"]

    def _fallback_get_stats(self) -> Dict[str, Any]:
        """Fallback statistics"""
        data_dir = Path("data")
        stats = {
            "api_count": 0,
            "total_runs": 0,
            "successful_runs": 0,
            "failed_runs": 0,
            "healing_count": 0,
            "applied_healings": 0,
            "recent_events": []
        }

        # Count files if they exist
        for file_name in ["api_tests.json", "test_runs.json", "healing_records.json"]:
            file_path = data_dir / file_name
            if file_path.exists():
                data = json.loads(file_path.read_text())
                if "api_tests.json" in file_name:
                    stats["api_count"] = len(data)
                elif "test_runs.json" in file_name:
                    stats["total_runs"] = len(data)
                    stats["successful_runs"] = sum(1 for run in data if run.get("status") == "success")
                    stats["failed_runs"] = sum(1 for run in data if run.get("status") == "failed")
                elif "healing_records.json" in file_name:
                    stats["healing_count"] = len(data)
                    stats["applied_healings"] = sum(1 for healing in data if healing.get("status") == "applied")

        return stats

    def _fallback_get_history(self, api_test_id: str, limit: int) -> List[Dict[str, Any]]:
        """Fallback test history"""
        data_dir = Path("data")
        runs_file = data_dir / "test_runs.json"

        if not runs_file.exists():
            return []

        runs = json.loads(runs_file.read_text())
        api_runs = [run for run in runs if run.get("api_test_id") == api_test_id]
        api_runs.sort(key=lambda x: x.get("run_timestamp", 0), reverse=True)

        return api_runs[:limit]

# Convenience functions
def create_mongodb_integration(connection_string: str = "mongodb://localhost:27017/",
                              database_name: str = "aegisapi") -> MongoDBIntegration:
    """Create MongoDB integration"""
    return MongoDBIntegration(connection_string, database_name)

# Enhanced telemetry logger for MongoDB
class MongoTelemetryLogger:
    """Enhanced telemetry logger that writes to MongoDB"""

    def __init__(self, mongo_integration: MongoDBIntegration):
        self.mongo_integration = mongo_integration

    def log_event(self, event: Dict[str, Any]) -> None:
        """Log event to MongoDB"""
        try:
            self.mongo_integration.log_telemetry_event(
                event_type=event.get('type', 'unknown'),
                summary=event.get('summary', ''),
                metadata=event
            )
        except Exception as e:
            print(f"MongoDB logging failed: {e}")

    def get_recent_events(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent events from MongoDB"""
        return self.mongo_integration.search_events(limit=limit)

# Migration utilities
def migrate_from_jsonl_to_mongo(mongo_integration: MongoDBIntegration,
                               jsonl_path: str = "data/telemetry.jsonl") -> None:
    """Migrate existing JSONL telemetry data to MongoDB"""
    if not Path(jsonl_path).exists():
        print(f"No JSONL file found at {jsonl_path}")
        return

    print(f"Migrating telemetry data from {jsonl_path} to MongoDB...")

    with open(jsonl_path, 'r', encoding='utf-8') as f:
        migrated_count = 0
        for line in f:
            if line.strip():
                try:
                    event = json.loads(line.strip())
                    mongo_integration.log_telemetry_event(
                        event_type=event.get('type', 'unknown'),
                        summary=event.get('summary', ''),
                        metadata=event
                    )
                    migrated_count += 1
                except Exception as e:
                    print(f"Failed to migrate event: {e}")

    print(f"✅ Migrated {migrated_count} telemetry events to MongoDB")

# Example usage
if __name__ == "__main__":
    # MongoDB example
    try:
        mongo_db = create_mongodb_integration()

        # Register an API
        api_id = mongo_db.register_api_test(
            name="Pet Store API",
            spec_path="examples/openapi_v1.yaml",
            base_url="http://localhost:4010",
            description="Demo API for testing AegisAPI AgentNN",
            version="1.0.0",
            metadata={"tags": ["demo", "petstore"], "owner": "aegisapi"}
        )

        # Record a test run
        run_id = mongo_db.record_test_run(
            api_test_id=api_id,
            status="success",
            duration=2.34,
            test_count=3,
            passed_count=3,
            environment={"python_version": "3.9", "os": "linux"}
        )

        # Record test results
        mongo_db.record_test_result(
            test_run_id=run_id,
            test_name="test_get_users",
            status="passed",
            duration=0.45,
            endpoint="/users",
            method="GET",
            response_status=200,
            response_time=0.23,
            metadata={"response_size": 1024}
        )

        # Log telemetry
        mongo_db.log_telemetry_event(
            event_type="api_test_completed",
            summary="Successfully tested Pet Store API",
            metadata={"api_id": api_id, "run_id": run_id, "performance_score": 95.5}
        )

        # Record healing
        mongo_db.record_healing(
            api_test_id=api_id,
            old_spec_path="examples/openapi_v1.yaml",
            new_spec_path="examples/openapi_v2_drift.yaml",
            confidence_score=1.0,
            changes={"field_renames": [{"from": "userName", "to": "username"}]},
            status="applied",
            metadata={"auto_healing": True}
        )

        # Get dashboard stats
        stats = mongo_db.get_dashboard_stats()
        print("Dashboard Stats:", json.dumps(stats, indent=2))

        # Get test history
        history = mongo_db.get_test_history(api_id, limit=5)
        print("Test History:", json.dumps(history, indent=2))

        print("✅ MongoDB integration completed!")

    except Exception as e:
        print(f"❌ MongoDB integration failed: {e}")
        print("💡 Make sure MongoDB is running and accessible")
