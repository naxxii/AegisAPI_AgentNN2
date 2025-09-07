"""
SQL Database Integration for AegisAPI AgentNN
Supports SQLite, PostgreSQL, MySQL with full telemetry and test result storage
"""
import time
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.pool import StaticPool
from pathlib import Path

Base = declarative_base()

class APITest(Base):
    """Model for API test specifications"""
    __tablename__ = 'api_tests'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    spec_path = Column(String(500))
    base_url = Column(String(500), nullable=False)
    description = Column(Text)
    created_at = Column(Float, default=time.time)
    updated_at = Column(Float, default=time.time, onupdate=time.time)
    status = Column(String(50), default='active')
    version = Column(String(50))

    # Relationships
    test_runs = relationship("TestRun", back_populates="api_test")
    healings = relationship("HealingRecord", back_populates="api_test")

class TestRun(Base):
    """Model for test execution runs"""
    __tablename__ = 'test_runs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    api_test_id = Column(Integer, ForeignKey('api_tests.id'), nullable=False)
    run_timestamp = Column(Float, default=time.time)
    duration = Column(Float)
    status = Column(String(50), nullable=False)  # 'success', 'failed', 'error'
    exit_code = Column(Integer, default=0)
    pytest_output = Column(Text)
    error_message = Column(Text)
    environment = Column(JSON)  # Store environment variables and system info
    test_count = Column(Integer, default=0)
    passed_count = Column(Integer, default=0)
    failed_count = Column(Integer, default=0)
    error_count = Column(Integer, default=0)

    # Relationships
    api_test = relationship("APITest", back_populates="test_runs")
    test_results = relationship("TestResult", back_populates="test_run")

class TestResult(Base):
    """Model for individual test results"""
    __tablename__ = 'test_results'

    id = Column(Integer, primary_key=True, autoincrement=True)
    test_run_id = Column(Integer, ForeignKey('test_runs.id'), nullable=False)
    test_name = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False)  # 'passed', 'failed', 'error', 'skipped'
    duration = Column(Float)
    error_message = Column(Text)
    stack_trace = Column(Text)
    endpoint = Column(String(500))
    method = Column(String(10))
    response_status = Column(Integer)
    response_time = Column(Float)

    # Relationships
    test_run = relationship("TestRun", back_populates="test_results")

class TelemetryEvent(Base):
    """Model for telemetry events"""
    __tablename__ = 'telemetry_events'

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_type = Column(String(100), nullable=False)
    summary = Column(Text)
    timestamp = Column(Float, default=time.time)
    metadata = Column(JSON)  # Store additional event data

class HealingRecord(Base):
    """Model for self-healing actions"""
    __tablename__ = 'healing_records'

    id = Column(Integer, primary_key=True, autoincrement=True)
    api_test_id = Column(Integer, ForeignKey('api_tests.id'), nullable=False)
    old_spec_path = Column(String(500))
    new_spec_path = Column(String(500))
    healing_timestamp = Column(Float, default=time.time)
    confidence_score = Column(Float)
    status = Column(String(50))  # 'proposed', 'applied', 'rejected'
    changes = Column(JSON)  # Store the actual changes made
    field_renames = Column(JSON)
    status_changes = Column(JSON)

    # Relationships
    api_test = relationship("APITest", back_populates="healings")

class DashboardMetric(Base):
    """Model for dashboard metrics"""
    __tablename__ = 'dashboard_metrics'

    id = Column(Integer, primary_key=True, autoincrement=True)
    metric_name = Column(String(100), nullable=False)
    metric_value = Column(Float)
    timestamp = Column(Float, default=time.time)
    metadata = Column(JSON)

class SQLIntegration:
    """Main SQL database integration class"""

    def __init__(self, connection_string: str = "sqlite:///aegisapi.db"):
        """
        Initialize database connection

        Args:
            connection_string: SQLAlchemy connection string
                Examples:
                - "sqlite:///aegisapi.db" (SQLite file)
                - "postgresql://user:pass@localhost/aegisapi" (PostgreSQL)
                - "mysql://user:pass@localhost/aegisapi" (MySQL)
        """
        self.connection_string = connection_string

        # Configure engine based on database type
        if connection_string.startswith("sqlite"):
            self.engine = create_engine(
                connection_string,
                connect_args={'check_same_thread': False},
                poolclass=StaticPool
            )
        else:
            self.engine = create_engine(connection_string)

        # Create tables
        Base.metadata.create_all(self.engine)

        # Create session
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_session(self):
        """Get database session"""
        return self.SessionLocal()

    def register_api_test(self, name: str, spec_path: str = None,
                         base_url: str = None, description: str = None) -> int:
        """Register a new API test specification"""
        session = self.get_session()
        try:
            api_test = APITest(
                name=name,
                spec_path=spec_path,
                base_url=base_url,
                description=description,
                created_at=time.time(),
                status='active'
            )
            session.add(api_test)
            session.commit()
            return api_test.id
        finally:
            session.close()

    def record_test_run(self, api_test_id: int, status: str,
                       duration: float = None, exit_code: int = 0,
                       pytest_output: str = None, test_count: int = 0,
                       passed_count: int = 0, failed_count: int = 0,
                       error_count: int = 0) -> int:
        """Record a test run"""
        session = self.get_session()
        try:
            test_run = TestRun(
                api_test_id=api_test_id,
                status=status,
                duration=duration,
                exit_code=exit_code,
                pytest_output=pytest_output,
                test_count=test_count,
                passed_count=passed_count,
                failed_count=failed_count,
                error_count=error_count,
                run_timestamp=time.time()
            )
            session.add(test_run)
            session.commit()
            return test_run.id
        finally:
            session.close()

    def record_test_result(self, test_run_id: int, test_name: str,
                          status: str, duration: float = None,
                          error_message: str = None, endpoint: str = None,
                          method: str = None, response_status: int = None,
                          response_time: float = None) -> int:
        """Record individual test result"""
        session = self.get_session()
        try:
            test_result = TestResult(
                test_run_id=test_run_id,
                test_name=test_name,
                status=status,
                duration=duration,
                error_message=error_message,
                endpoint=endpoint,
                method=method,
                response_status=response_status,
                response_time=response_time
            )
            session.add(test_result)
            session.commit()
            return test_result.id
        finally:
            session.close()

    def log_telemetry_event(self, event_type: str, summary: str = None,
                           metadata: Dict[str, Any] = None) -> int:
        """Log telemetry event to database"""
        session = self.get_session()
        try:
            event = TelemetryEvent(
                event_type=event_type,
                summary=summary,
                metadata=metadata or {},
                timestamp=time.time()
            )
            session.add(event)
            session.commit()
            return event.id
        finally:
            session.close()

    def record_healing(self, api_test_id: int, old_spec_path: str,
                      new_spec_path: str, confidence_score: float,
                      changes: Dict[str, Any], status: str = 'proposed') -> int:
        """Record healing action"""
        session = self.get_session()
        try:
            healing = HealingRecord(
                api_test_id=api_test_id,
                old_spec_path=old_spec_path,
                new_spec_path=new_spec_path,
                confidence_score=confidence_score,
                changes=changes,
                status=status,
                healing_timestamp=time.time(),
                field_renames=changes.get('field_renames', []),
                status_changes=changes.get('status_changes', [])
            )
            session.add(healing)
            session.commit()
            return healing.id
        finally:
            session.close()

    def get_dashboard_stats(self) -> Dict[str, Any]:
        """Get dashboard statistics"""
        session = self.get_session()
        try:
            # Count API tests
            api_count = session.query(APITest).count()

            # Count test runs
            total_runs = session.query(TestRun).count()
            successful_runs = session.query(TestRun).filter_by(status='success').count()
            failed_runs = session.query(TestRun).filter_by(status='failed').count()

            # Count healings
            healing_count = session.query(HealingRecord).count()
            applied_healings = session.query(HealingRecord).filter_by(status='applied').count()

            # Recent events
            recent_events = session.query(TelemetryEvent)\
                                 .order_by(TelemetryEvent.timestamp.desc())\
                                 .limit(10)\
                                 .all()

            return {
                'api_count': api_count,
                'total_runs': total_runs,
                'successful_runs': successful_runs,
                'failed_runs': failed_runs,
                'healing_count': healing_count,
                'applied_healings': applied_healings,
                'recent_events': [
                    {
                        'type': event.event_type,
                        'summary': event.summary,
                        'timestamp': event.timestamp
                    } for event in recent_events
                ]
            }
        finally:
            session.close()

    def get_test_history(self, api_test_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """Get test run history for an API"""
        session = self.get_session()
        try:
            runs = session.query(TestRun)\
                        .filter_by(api_test_id=api_test_id)\
                        .order_by(TestRun.run_timestamp.desc())\
                        .limit(limit)\
                        .all()

            return [
                {
                    'id': run.id,
                    'timestamp': run.run_timestamp,
                    'status': run.status,
                    'duration': run.duration,
                    'test_count': run.test_count,
                    'passed_count': run.passed_count,
                    'failed_count': run.failed_count
                } for run in runs
            ]
        finally:
            session.close()

    def export_data(self, format: str = 'json') -> str:
        """Export database data"""
        session = self.get_session()
        try:
            data = {
                'api_tests': [self._model_to_dict(api) for api in session.query(APITest).all()],
                'test_runs': [self._model_to_dict(run) for run in session.query(TestRun).all()],
                'test_results': [self._model_to_dict(result) for result in session.query(TestResult).all()],
                'telemetry_events': [self._model_to_dict(event) for event in session.query(TelemetryEvent).all()],
                'healing_records': [self._model_to_dict(healing) for healing in session.query(HealingRecord).all()],
                'export_timestamp': time.time()
            }

            if format == 'json':
                return json.dumps(data, indent=2, default=str)
            else:
                return json.dumps(data, default=str)

        finally:
            session.close()

    def _model_to_dict(self, model) -> Dict[str, Any]:
        """Convert SQLAlchemy model to dictionary"""
        return {column.name: getattr(model, column.name)
                for column in model.__table__.columns}

# Convenience functions for different database types
def create_sqlite_integration(db_path: str = "aegisapi.db") -> SQLIntegration:
    """Create SQLite integration"""
    return SQLIntegration(f"sqlite:///{db_path}")

def create_postgresql_integration(host: str = "localhost", port: int = 5432,
                                database: str = "aegisapi", user: str = "aegisapi",
                                password: str = "password") -> SQLIntegration:
    """Create PostgreSQL integration"""
    connection_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    return SQLIntegration(connection_string)

def create_mysql_integration(host: str = "localhost", port: int = 3306,
                           database: str = "aegisapi", user: str = "aegisapi",
                           password: str = "password") -> SQLIntegration:
    """Create MySQL integration"""
    connection_string = f"mysql://{user}:{password}@{host}:{port}/{database}"
    return SQLIntegration(connection_string)

# Enhanced telemetry integration
class DatabaseTelemetryLogger:
    """Enhanced telemetry logger that writes to database"""

    def __init__(self, sql_integration: SQLIntegration):
        self.sql_integration = sql_integration
        self.file_logger = None  # Can still keep file logging

    def log_event(self, event: Dict[str, Any]) -> None:
        """Log event to database"""
        try:
            self.sql_integration.log_telemetry_event(
                event_type=event.get('type', 'unknown'),
                summary=event.get('summary', ''),
                metadata=event
            )
        except Exception as e:
            print(f"Database logging failed: {e}")

    def get_recent_events(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent events from database"""
        session = self.sql_integration.get_session()
        try:
            events = session.query(TelemetryEvent)\
                          .order_by(TelemetryEvent.timestamp.desc())\
                          .limit(limit)\
                          .all()

            return [
                {
                    'type': event.event_type,
                    'summary': event.summary,
                    'timestamp': event.timestamp,
                    'metadata': event.metadata
                } for event in events
            ]
        finally:
            session.close()

# Migration utilities
def migrate_from_jsonl_to_sql(sql_integration: SQLIntegration,
                             jsonl_path: str = "data/telemetry.jsonl") -> None:
    """Migrate existing JSONL telemetry data to SQL database"""
    if not Path(jsonl_path).exists():
        print(f"No JSONL file found at {jsonl_path}")
        return

    print(f"Migrating telemetry data from {jsonl_path} to database...")

    with open(jsonl_path, 'r', encoding='utf-8') as f:
        migrated_count = 0
        for line in f:
            if line.strip():
                try:
                    event = json.loads(line.strip())
                    sql_integration.log_telemetry_event(
                        event_type=event.get('type', 'unknown'),
                        summary=event.get('summary', ''),
                        metadata=event
                    )
                    migrated_count += 1
                except Exception as e:
                    print(f"Failed to migrate event: {e}")

    print(f"✅ Migrated {migrated_count} telemetry events to database")

# Example usage
if __name__ == "__main__":
    # SQLite example
    db = create_sqlite_integration("aegisapi.db")

    # Register an API
    api_id = db.register_api_test(
        name="Pet Store API",
        spec_path="examples/openapi_v1.yaml",
        base_url="http://localhost:4010",
        description="Demo API for testing AegisAPI AgentNN"
    )

    # Record a test run
    run_id = db.record_test_run(
        api_test_id=api_id,
        status="success",
        duration=2.34,
        test_count=3,
        passed_count=3
    )

    # Record test results
    db.record_test_result(
        test_run_id=run_id,
        test_name="test_get_users",
        status="passed",
        duration=0.45,
        endpoint="/users",
        method="GET",
        response_status=200,
        response_time=0.23
    )

    # Log telemetry
    db.log_telemetry_event(
        event_type="api_test_completed",
        summary="Successfully tested Pet Store API",
        metadata={"api_id": api_id, "run_id": run_id}
    )

    # Get dashboard stats
    stats = db.get_dashboard_stats()
    print("Dashboard Stats:", json.dumps(stats, indent=2))

    print("✅ SQL database integration completed!")
