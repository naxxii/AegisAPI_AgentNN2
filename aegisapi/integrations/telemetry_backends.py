"""
Flexible Telemetry Storage Backends for AegisAPI AgentNN
Supports multiple storage systems: File, SQL, NoSQL, Redis, etc.
"""
import time
import json
import threading
from typing import Dict, List, Any, Optional, Protocol
from pathlib import Path
from abc import ABC, abstractmethod
from queue import Queue
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TelemetryBackend(Protocol):
    """Protocol for telemetry storage backends"""

    def log_event(self, event: Dict[str, Any]) -> None:
        """Log a telemetry event"""
        ...

    def get_recent_events(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent events"""
        ...

    def search_events(self, event_type: str = None, start_time: float = None,
                     end_time: float = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Search events with filters"""
        ...

    def get_stats(self) -> Dict[str, Any]:
        """Get telemetry statistics"""
        ...

class FileBackend:
    """File-based telemetry storage (original implementation)"""

    def __init__(self, telemetry_dir: str = "data", telemetry_file: str = "telemetry.jsonl"):
        self.telemetry_dir = Path(telemetry_dir)
        self.telemetry_file = self.telemetry_dir / telemetry_file
        self.telemetry_dir.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def log_event(self, event: Dict[str, Any]) -> None:
        """Log event to JSONL file"""
        with self._lock:
            event.setdefault("ts", time.time())
            try:
                with open(self.telemetry_file, 'a', encoding='utf-8') as f:
                    f.write(json.dumps(event, default=str) + '\n')
            except Exception as e:
                logger.error(f"Failed to write telemetry event: {e}")

    def get_recent_events(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent events from file"""
        if not self.telemetry_file.exists():
            return []

        try:
            with open(self.telemetry_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()[-limit:]
                return [json.loads(line.strip()) for line in lines if line.strip()]
        except Exception as e:
            logger.error(f"Failed to read telemetry events: {e}")
            return []

    def search_events(self, event_type: str = None, start_time: float = None,
                     end_time: float = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Search events in file"""
        events = self.get_recent_events(limit * 10)  # Get more to filter

        filtered_events = []
        for event in events:
            if event_type and event.get('type') != event_type:
                continue
            if start_time and event.get('ts', 0) < start_time:
                continue
            if end_time and event.get('ts', 0) > end_time:
                continue
            filtered_events.append(event)
            if len(filtered_events) >= limit:
                break

        return filtered_events

    def get_stats(self) -> Dict[str, Any]:
        """Get telemetry statistics"""
        events = self.get_recent_events(1000)
        event_types = {}

        for event in events:
            event_type = event.get('type', 'unknown')
            event_types[event_type] = event_types.get(event_type, 0) + 1

        return {
            "total_events": len(events),
            "event_types": event_types,
            "oldest_event": min([e.get('ts', time.time()) for e in events]) if events else None,
            "newest_event": max([e.get('ts', time.time()) for e in events]) if events else None
        }

class AsyncTelemetryLogger:
    """Asynchronous telemetry logger with queue and multiple backends"""

    def __init__(self, backends: List[TelemetryBackend] = None):
        self.backends = backends or [FileBackend()]
        self.queue = Queue()
        self.running = True

        # Start background worker thread
        self.worker_thread = threading.Thread(target=self._process_queue, daemon=True)
        self.worker_thread.start()

    def log_event(self, event: Dict[str, Any]) -> None:
        """Log event asynchronously"""
        self.queue.put(event)

    def _process_queue(self):
        """Background worker to process telemetry events"""
        while self.running:
            try:
                # Get event from queue with timeout
                event = self.queue.get(timeout=1)

                # Send to all backends
                for backend in self.backends:
                    try:
                        backend.log_event(event)
                    except Exception as e:
                        logger.error(f"Backend {backend.__class__.__name__} failed: {e}")

                self.queue.task_done()

            except Exception:
                # Timeout or other error, continue processing
                continue

    def shutdown(self):
        """Shutdown the logger"""
        self.running = False
        if self.worker_thread.is_alive():
            self.worker_thread.join(timeout=5)

        # Process remaining events
        while not self.queue.empty():
            try:
                event = self.queue.get_nowait()
                for backend in self.backends:
                    try:
                        backend.log_event(event)
                    except Exception as e:
                        logger.error(f"Backend {backend.__class__.__name__} failed during shutdown: {e}")
                self.queue.task_done()
            except Exception:
                break

class TelemetryManager:
    """Central telemetry management system"""

    def __init__(self):
        self.logger = AsyncTelemetryLogger()
        self.backends = {}

    def add_backend(self, name: str, backend: TelemetryBackend):
        """Add a telemetry backend"""
        self.backends[name] = backend
        self.logger.backends.append(backend)
        logger.info(f"Added telemetry backend: {name}")

    def remove_backend(self, name: str):
        """Remove a telemetry backend"""
        if name in self.backends:
            backend = self.backends[name]
            if backend in self.logger.backends:
                self.logger.backends.remove(backend)
            del self.backends[name]
            logger.info(f"Removed telemetry backend: {name}")

    def log_event(self, event_type: str, summary: str = None,
                  metadata: Dict[str, Any] = None):
        """Log a telemetry event"""
        event = {
            "type": event_type,
            "summary": summary or "",
            "metadata": metadata or {},
            "ts": time.time()
        }

        self.logger.log_event(event)

    def get_recent_events(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent events from primary backend"""
        if self.logger.backends:
            return self.logger.backends[0].get_recent_events(limit)
        return []

    def get_stats(self) -> Dict[str, Any]:
        """Get telemetry statistics"""
        stats = {}
        for name, backend in self.backends.items():
            try:
                backend_stats = backend.get_stats()
                stats[name] = backend_stats
            except Exception as e:
                logger.error(f"Failed to get stats from {name}: {e}")
                stats[name] = {"error": str(e)}

        return stats

    def search_events(self, event_type: str = None, start_time: float = None,
                     end_time: float = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Search events across backends"""
        all_events = []
        for backend in self.logger.backends:
            try:
                events = backend.search_events(event_type, start_time, end_time, limit)
                all_events.extend(events)
            except Exception as e:
                logger.error(f"Failed to search backend {backend.__class__.__name__}: {e}")

        # Sort by timestamp and limit
        all_events.sort(key=lambda x: x.get('ts', 0), reverse=True)
        return all_events[:limit]

# SQL Backend Adapter
class SQLTelemetryBackend:
    """SQL database backend adapter"""

    def __init__(self, sql_integration):
        self.sql_integration = sql_integration

    def log_event(self, event: Dict[str, Any]) -> None:
        """Log event to SQL database"""
        try:
            self.sql_integration.log_telemetry_event(
                event_type=event.get('type', 'unknown'),
                summary=event.get('summary', ''),
                metadata=event
            )
        except Exception as e:
            logger.error(f"SQL telemetry logging failed: {e}")

    def get_recent_events(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent events from SQL"""
        try:
            return self.sql_integration.get_recent_events(limit)
        except Exception as e:
            logger.error(f"Failed to get SQL events: {e}")
            return []

    def search_events(self, event_type: str = None, start_time: float = None,
                     end_time: float = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Search SQL events"""
        try:
            events = self.sql_integration.get_recent_events(limit * 2)  # Get more to filter

            filtered_events = []
            for event in events:
                if event_type and event.get('event_type') != event_type:
                    continue
                if start_time and event.get('timestamp', 0) < start_time:
                    continue
                if end_time and event.get('timestamp', 0) > end_time:
                    continue
                filtered_events.append(event)
                if len(filtered_events) >= limit:
                    break

            return filtered_events
        except Exception as e:
            logger.error(f"SQL event search failed: {e}")
            return []

    def get_stats(self) -> Dict[str, Any]:
        """Get SQL telemetry statistics"""
        try:
            return self.sql_integration.get_dashboard_stats()
        except Exception as e:
            logger.error(f"Failed to get SQL stats: {e}")
            return {"error": str(e)}

# NoSQL Backend Adapter
class NoSQLTelemetryBackend:
    """NoSQL database backend adapter"""

    def __init__(self, nosql_integration):
        self.nosql_integration = nosql_integration

    def log_event(self, event: Dict[str, Any]) -> None:
        """Log event to NoSQL database"""
        try:
            self.nosql_integration.log_telemetry_event(
                event_type=event.get('type', 'unknown'),
                summary=event.get('summary', ''),
                metadata=event
            )
        except Exception as e:
            logger.error(f"NoSQL telemetry logging failed: {e}")

    def get_recent_events(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent events from NoSQL"""
        try:
            return self.nosql_integration.search_events(limit=limit)
        except Exception as e:
            logger.error(f"Failed to get NoSQL events: {e}")
            return []

    def search_events(self, event_type: str = None, start_time: float = None,
                     end_time: float = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Search NoSQL events"""
        try:
            return self.nosql_integration.search_events(
                event_type=event_type,
                start_time=start_time,
                end_time=end_time,
                limit=limit
            )
        except Exception as e:
            logger.error(f"NoSQL event search failed: {e}")
            return []

    def get_stats(self) -> Dict[str, Any]:
        """Get NoSQL telemetry statistics"""
        try:
            return self.nosql_integration.get_dashboard_stats()
        except Exception as e:
            logger.error(f"Failed to get NoSQL stats: {e}")
            return {"error": str(e)}

# Redis Backend (for high-performance caching and real-time data)
try:
    import redis
    from redis.exceptions import ConnectionError

    class RedisTelemetryBackend:
        """Redis backend for high-performance telemetry"""

        def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0):
            try:
                self.redis = redis.Redis(host=host, port=port, db=db, decode_responses=True)
                self.redis.ping()  # Test connection
                self.key_prefix = "aegisapi:telemetry:"
            except ConnectionError:
                logger.error("Redis connection failed, Redis backend disabled")
                self.redis = None

        def log_event(self, event: Dict[str, Any]) -> None:
            """Log event to Redis"""
            if not self.redis:
                return

            try:
                event_id = str(time.time())
                event_key = f"{self.key_prefix}event:{event_id}"

                # Store event data
                self.redis.hmset(event_key, {
                    'type': event.get('type', 'unknown'),
                    'summary': event.get('summary', ''),
                    'timestamp': event.get('ts', time.time()),
                    'metadata': json.dumps(event.get('metadata', {}))
                })

                # Add to event type index
                event_type = event.get('type', 'unknown')
                self.redis.zadd(f"{self.key_prefix}events:{event_type}", {event_id: event.get('ts', time.time())})

                # Add to global timeline
                self.redis.zadd(f"{self.key_prefix}timeline", {event_id: event.get('ts', time.time())})

                # Keep only last 1000 events to prevent memory issues
                self.redis.zremrangebyrank(f"{self.key_prefix}timeline", 0, -1001)

            except Exception as e:
                logger.error(f"Redis telemetry logging failed: {e}")

        def get_recent_events(self, limit: int = 100) -> List[Dict[str, Any]]:
            """Get recent events from Redis"""
            if not self.redis:
                return []

            try:
                event_ids = self.redis.zrevrange(f"{self.key_prefix}timeline", 0, limit - 1)
                events = []

                for event_id in event_ids:
                    event_data = self.redis.hgetall(f"{self.key_prefix}event:{event_id}")
                    if event_data:
                        events.append({
                            'id': event_id,
                            'type': event_data.get('type'),
                            'summary': event_data.get('summary'),
                            'timestamp': float(event_data.get('timestamp', 0)),
                            'metadata': json.loads(event_data.get('metadata', '{}'))
                        })

                return events
            except Exception as e:
                logger.error(f"Failed to get Redis events: {e}")
                return []

        def search_events(self, event_type: str = None, start_time: float = None,
                         end_time: float = None, limit: int = 100) -> List[Dict[str, Any]]:
            """Search Redis events"""
            if not self.redis:
                return []

            try:
                if event_type:
                    # Search specific event type
                    event_ids = self.redis.zrevrange(f"{self.key_prefix}events:{event_type}", 0, limit - 1)
                else:
                    # Search all events
                    event_ids = self.redis.zrevrange(f"{self.key_prefix}timeline", 0, limit - 1)

                events = []
                for event_id in event_ids:
                    event_data = self.redis.hgetall(f"{self.key_prefix}event:{event_id}")
                    if event_data:
                        timestamp = float(event_data.get('timestamp', 0))

                        # Apply time filters
                        if start_time and timestamp < start_time:
                            continue
                        if end_time and timestamp > end_time:
                            continue

                        events.append({
                            'id': event_id,
                            'type': event_data.get('type'),
                            'summary': event_data.get('summary'),
                            'timestamp': timestamp,
                            'metadata': json.loads(event_data.get('metadata', '{}'))
                        })

                return events
            except Exception as e:
                logger.error(f"Redis event search failed: {e}")
                return []

        def get_stats(self) -> Dict[str, Any]:
            """Get Redis telemetry statistics"""
            if not self.redis:
                return {"error": "Redis not connected"}

            try:
                total_events = self.redis.zcard(f"{self.key_prefix}timeline")

                # Get event type distribution
                event_types = {}
                keys = self.redis.keys(f"{self.key_prefix}events:*")
                for key in keys:
                    event_type = key.replace(f"{self.key_prefix}events:", "")
                    count = self.redis.zcard(key)
                    event_types[event_type] = count

                return {
                    "total_events": total_events,
                    "event_types": event_types,
                    "backend": "redis"
                }
            except Exception as e:
                logger.error(f"Failed to get Redis stats: {e}")
                return {"error": str(e)}

except ImportError:
    logger.warning("Redis not available, RedisTelemetryBackend disabled")
    RedisTelemetryBackend = None

# Global telemetry manager instance
telemetry_manager = TelemetryManager()

def get_telemetry_manager() -> TelemetryManager:
    """Get the global telemetry manager instance"""
    return telemetry_manager

def setup_telemetry_backends(config: Dict[str, Any]):
    """Setup telemetry backends based on configuration"""
    manager = get_telemetry_manager()

    # Always keep file backend as fallback
    manager.add_backend("file", FileBackend())

    # Setup SQL backend
    if config.get("sql_enabled", False):
        try:
            from .sql_integration import SQLIntegration
            sql_integration = SQLIntegration(config.get("sql_connection_string", "sqlite:///telemetry.db"))
            manager.add_backend("sql", SQLTelemetryBackend(sql_integration))
            logger.info("SQL telemetry backend enabled")
        except Exception as e:
            logger.error(f"Failed to setup SQL telemetry backend: {e}")

    # Setup NoSQL backend
    if config.get("nosql_enabled", False):
        try:
            from .nosql_integration import MongoDBIntegration
            nosql_integration = MongoDBIntegration(
                config.get("nosql_connection_string", "mongodb://localhost:27017/"),
                config.get("nosql_database", "aegisapi_telemetry")
            )
            if nosql_integration.db:  # Only add if MongoDB is available
                manager.add_backend("nosql", NoSQLTelemetryBackend(nosql_integration))
                logger.info("NoSQL telemetry backend enabled")
        except Exception as e:
            logger.error(f"Failed to setup NoSQL telemetry backend: {e}")

    # Setup Redis backend
    if config.get("redis_enabled", False) and RedisTelemetryBackend:
        try:
            redis_backend = RedisTelemetryBackend(
                host=config.get("redis_host", "localhost"),
                port=config.get("redis_port", 6379),
                db=config.get("redis_db", 0)
            )
            if redis_backend.redis:  # Only add if Redis is available
                manager.add_backend("redis", redis_backend)
                logger.info("Redis telemetry backend enabled")
        except Exception as e:
            logger.error(f"Failed to setup Redis telemetry backend: {e}")

# Convenience functions
def log_event(event_type: str, summary: str = None, metadata: Dict[str, Any] = None):
    """Log a telemetry event"""
    get_telemetry_manager().log_event(event_type, summary, metadata)

def get_recent_events(limit: int = 100) -> List[Dict[str, Any]]:
    """Get recent telemetry events"""
    return get_telemetry_manager().get_recent_events(limit)

def search_events(event_type: str = None, start_time: float = None,
                 end_time: float = None, limit: int = 100) -> List[Dict[str, Any]]:
    """Search telemetry events"""
    return get_telemetry_manager().search_events(event_type, start_time, end_time, limit)

# Example configuration
DEFAULT_TELEMETRY_CONFIG = {
    "file_enabled": True,
    "sql_enabled": False,
    "sql_connection_string": "sqlite:///telemetry.db",
    "nosql_enabled": False,
    "nosql_connection_string": "mongodb://localhost:27017/",
    "nosql_database": "aegisapi_telemetry",
    "redis_enabled": False,
    "redis_host": "localhost",
    "redis_port": 6379,
    "redis_db": 0
}

if __name__ == "__main__":
    # Example usage
    print("🚀 AegisAPI AgentNN Telemetry Backends Demo")

    # Setup backends
    setup_telemetry_backends(DEFAULT_TELEMETRY_CONFIG)

    # Log some test events
    log_event("test_started", "Starting API test", {"api_name": "petstore"})
    log_event("test_completed", "API test completed successfully", {"api_name": "petstore", "duration": 2.5})
    log_event("healing_applied", "Self-healing applied", {"confidence": 0.95})

    # Get recent events
    events = get_recent_events(5)
    print(f"📊 Recent Events: {len(events)}")
    for event in events:
        print(f"  - {event.get('type')}: {event.get('summary')}")

    # Get stats
    stats = get_telemetry_manager().get_stats()
    print(f"📈 Telemetry Stats: {stats}")

    print("✅ Telemetry backends demo completed!")
