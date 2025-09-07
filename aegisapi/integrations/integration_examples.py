"""
Complete Integration Examples for AegisAPI AgentNN
Demonstrates Postman, SQL, NoSQL, and multi-backend telemetry integration
"""
import time
import json
from pathlib import Path
from typing import Dict, List, Any

def postman_to_aegisapi_example():
    """
    Complete example: Import Postman collection → Generate AegisAPI tests → Run with SQL storage
    """
    print("🚀 Postman to AegisAPI Integration Example")
    print("=" * 50)

    try:
        from .postman_integration import PostmanIntegration
        from .sql_integration import create_sqlite_integration
        from ..generator import generate_tests
        from ..executor import run_tests

        # Step 1: Import Postman collection
        print("📋 Step 1: Importing Postman collection...")
        postman_integration = PostmanIntegration()
        collection = postman_integration.load_collection("examples/sample_postman_collection.json")

        print(f"✅ Loaded collection: {collection.name} with {len(collection.requests)} requests")

        # Step 2: Convert to OpenAPI
        print("🔄 Step 2: Converting to OpenAPI specification...")
        openapi_spec = postman_integration.convert_to_openapi(collection.name)

        # Save OpenAPI spec
        spec_path = Path("generated_specs") / f"{collection.name.replace(' ', '_')}.yaml"
        spec_path.parent.mkdir(exist_ok=True)

        import yaml
        with open(spec_path, 'w') as f:
            yaml.dump(openapi_spec, f)

        print(f"✅ Saved OpenAPI spec to: {spec_path}")

        # Step 3: Setup SQL database for results
        print("🗄️ Step 3: Setting up SQL database...")
        sql_db = create_sqlite_integration("aegisapi_postman.db")

        # Register API in database
        api_id = sql_db.register_api_test(
            name=collection.name,
            spec_path=str(spec_path),
            base_url="https://api.example.com",  # Replace with actual URL
            description=f"Imported from Postman collection: {collection.name}"
        )

        print(f"✅ Registered API in database with ID: {api_id}")

        # Step 4: Generate AegisAPI tests
        print("🤖 Step 4: Generating AegisAPI tests...")
        test_dir = Path("tests_from_postman") / collection.name.replace(' ', '_')
        generate_tests(str(spec_path), test_dir, "none")

        print(f"✅ Generated tests in: {test_dir}")

        # Step 5: Run tests and store results
        print("⚡ Step 5: Running tests and storing results...")
        exit_code = run_tests(str(test_dir), spec=str(spec_path), base_url="https://api.example.com")

        # Record test run in database
        run_id = sql_db.record_test_run(
            api_test_id=api_id,
            status="success" if exit_code == 0 else "failed",
            duration=5.23,  # Replace with actual duration
            exit_code=exit_code,
            test_count=len(list(test_dir.glob("test_*.py"))),
            passed_count=len(list(test_dir.glob("test_*.py"))) if exit_code == 0 else 0,
            failed_count=0 if exit_code == 0 else len(list(test_dir.glob("test_*.py")))
        )

        print(f"✅ Test run recorded in database with ID: {run_id}")

        # Step 6: Export results back to Postman format
        print("📤 Step 6: Exporting results to Postman format...")
        test_results = {
            "overall_status": "success" if exit_code == 0 else "failed",
            "test_count": len(list(test_dir.glob("test_*.py"))),
            "timestamp": time.time(),
            "api_name": collection.name
        }

        postman_export = postman_integration.export_test_results(collection.name, test_results)

        export_path = Path("exports") / f"{collection.name.replace(' ', '_')}_results.json"
        export_path.parent.mkdir(exist_ok=True)
        with open(export_path, 'w') as f:
            json.dump(postman_export, f, indent=2)

        print(f"✅ Exported results to: {export_path}")

        # Step 7: Display results
        print("\n📊 Results Summary:")
        print(f"   Collection: {collection.name}")
        print(f"   Requests: {len(collection.requests)}")
        print(f"   Tests Generated: {len(list(test_dir.glob('test_*.py')))}")
        print(f"   Test Status: {'✅ PASSED' if exit_code == 0 else '❌ FAILED'}")
        print(f"   Database ID: {api_id}")
        print(f"   Export Location: {export_path}")

        return {
            "success": True,
            "collection_name": collection.name,
            "api_id": api_id,
            "test_count": len(list(test_dir.glob("test_*.py"))),
            "status": "success" if exit_code == 0 else "failed"
        }

    except Exception as e:
        print(f"❌ Integration failed: {e}")
        return {"success": False, "error": str(e)}

def multi_database_integration_example():
    """
    Complete example: Use SQL + NoSQL + File storage simultaneously
    """
    print("\n🗄️ Multi-Database Integration Example")
    print("=" * 50)

    try:
        from .sql_integration import create_sqlite_integration
        from .nosql_integration import create_mongodb_integration
        from .telemetry_backends import TelemetryManager, FileBackend, SQLTelemetryBackend, NoSQLTelemetryBackend

        # Step 1: Setup multiple databases
        print("🗄️ Step 1: Setting up multiple databases...")

        # SQLite for relational data
        sql_db = create_sqlite_integration("multi_db_example.db")

        # MongoDB for document storage (with fallback)
        try:
            nosql_db = create_mongodb_integration(database_name="aegisapi_multi_example")
            nosql_available = nosql_db.db is not None
        except Exception as e:
            print(f"⚠️ MongoDB not available: {e}")
            nosql_db = None
            nosql_available = False

        print(f"✅ SQLite: Connected")
        print(f"✅ MongoDB: {'Connected' if nosql_available else 'Not available (will use file fallback)'}")

        # Step 2: Setup telemetry with multiple backends
        print("📊 Step 2: Setting up multi-backend telemetry...")
        telemetry_manager = TelemetryManager()

        # Add file backend
        telemetry_manager.add_backend("file", FileBackend("data", "multi_backend_telemetry.jsonl"))

        # Add SQL backend
        telemetry_manager.add_backend("sql", SQLTelemetryBackend(sql_db))

        # Add NoSQL backend if available
        if nosql_available:
            telemetry_manager.add_backend("nosql", NoSQLTelemetryBackend(nosql_db))

        # Step 3: Register API in all systems
        print("📋 Step 3: Registering API across all systems...")
        api_name = "Multi-DB Test API"
        spec_path = "examples/openapi_v1.yaml"
        base_url = "http://localhost:4010"

        # SQL registration
        sql_api_id = sql_db.register_api_test(
            name=api_name,
            spec_path=spec_path,
            base_url=base_url,
            description="API registered in multiple database systems"
        )

        # NoSQL registration (if available)
        nosql_api_id = None
        if nosql_available:
            nosql_api_id = nosql_db.register_api_test(
                name=api_name,
                spec_path=spec_path,
                base_url=base_url,
                description="API registered in multiple database systems"
            )

        print(f"✅ SQL API ID: {sql_api_id}")
        if nosql_available:
            print(f"✅ NoSQL API ID: {nosql_api_id}")

        # Step 4: Log events to all backends
        print("📝 Step 4: Logging events to all backends...")
        test_events = [
            {
                "type": "multi_db_test_started",
                "summary": f"Starting multi-database test for {api_name}",
                "metadata": {"sql_api_id": sql_api_id, "nosql_api_id": nosql_api_id}
            },
            {
                "type": "database_connection_test",
                "summary": "Testing connections to all database systems",
                "metadata": {"backends": ["sql", "nosql" if nosql_available else "file_fallback"]}
            },
            {
                "type": "telemetry_distribution_test",
                "summary": "Verifying event distribution across all backends",
                "metadata": {"expected_backends": 2 if nosql_available else 1}
            }
        ]

        for event in test_events:
            telemetry_manager.log_event(
                event_type=event["type"],
                summary=event["summary"],
                metadata=event["metadata"]
            )
            time.sleep(0.1)  # Small delay to ensure proper ordering

        print(f"✅ Logged {len(test_events)} events to all backends")

        # Step 5: Simulate test run and record results
        print("⚡ Step 5: Simulating test run and recording results...")

        # SQL test run
        sql_run_id = sql_db.record_test_run(
            api_test_id=sql_api_id,
            status="success",
            duration=3.45,
            exit_code=0,
            test_count=3,
            passed_count=3,
            failed_count=0,
            environment={"databases": ["sqlite", "mongodb" if nosql_available else "file"]}
        )

        # Record individual test results in SQL
        sql_db.record_test_result(
            test_run_id=sql_run_id,
            test_name="test_get_users",
            status="passed",
            duration=0.45,
            endpoint="/users",
            method="GET",
            response_status=200,
            response_time=0.23
        )

        # NoSQL test run (if available)
        if nosql_available:
            nosql_run_id = nosql_db.record_test_run(
                api_test_id=nosql_api_id,
                status="success",
                duration=3.45,
                exit_code=0,
                test_count=3,
                passed_count=3,
                failed_count=0,
                environment={"databases": ["sqlite", "mongodb"]}
            )

        print(f"✅ SQL Test Run ID: {sql_run_id}")
        if nosql_available:
            print(f"✅ NoSQL Test Run ID: {nosql_run_id}")

        # Step 6: Get statistics from all systems
        print("📊 Step 6: Gathering statistics from all systems...")

        sql_stats = sql_db.get_dashboard_stats()
        telemetry_stats = telemetry_manager.get_stats()

        print("\n📈 SQL Database Stats:")
        print(json.dumps(sql_stats, indent=2))

        print("\n📈 Telemetry Stats:")
        print(json.dumps(telemetry_stats, indent=2))

        if nosql_available:
            nosql_stats = nosql_db.get_dashboard_stats()
            print("\n📈 NoSQL Database Stats:")
            print(json.dumps(nosql_stats, indent=2))

        # Step 7: Export data
        print("📤 Step 7: Exporting data from all systems...")

        # Export SQL data
        sql_export = sql_db.export_data()
        with open("exports/sql_data_export.json", 'w') as f:
            json.dump(sql_export, f, indent=2, default=str)

        # Export telemetry data
        telemetry_export = telemetry_manager.get_recent_events(50)
        with open("exports/telemetry_export.json", 'w') as f:
            json.dump(telemetry_export, f, indent=2, default=str)

        if nosql_available:
            nosql_export = nosql_db.export_data()
            with open("exports/nosql_data_export.json", 'w') as f:
                json.dump(nosql_export, f, indent=2, default=str)

        print("✅ Exported data from all systems to exports/ directory")

        return {
            "success": True,
            "sql_api_id": sql_api_id,
            "nosql_api_id": nosql_api_id,
            "backends_active": ["sql", "nosql" if nosql_available else "file"],
            "events_logged": len(test_events),
            "exports_created": 2 if nosql_available else 1
        }

    except Exception as e:
        print(f"❌ Multi-database integration failed: {e}")
        return {"success": False, "error": str(e)}

def enterprise_integration_example():
    """
    Enterprise-level integration with proper configuration management
    """
    print("\n🏢 Enterprise Integration Example")
    print("=" * 50)

    try:
        import os
        from pathlib import Path

        # Step 1: Load enterprise configuration
        print("⚙️ Step 1: Loading enterprise configuration...")

        enterprise_config = {
            "databases": {
                "primary_sql": "postgresql://aegisapi:password@localhost:5432/aegisapi_prod",
                "secondary_nosql": "mongodb://localhost:27017/aegisapi_prod",
                "cache_redis": "redis://localhost:6379/0"
            },
            "telemetry": {
                "file_enabled": True,
                "sql_enabled": True,
                "nosql_enabled": True,
                "redis_enabled": True,
                "retention_days": 90
            },
            "apis": [
                {
                    "name": "User Management API",
                    "spec_path": "specs/user_api.yaml",
                    "base_url": "https://api.company.com/users",
                    "auth_profile": "oauth2",
                    "environment": "production"
                },
                {
                    "name": "Product Catalog API",
                    "spec_path": "specs/product_api.yaml",
                    "base_url": "https://api.company.com/products",
                    "auth_profile": "api_key",
                    "environment": "production"
                }
            ],
            "monitoring": {
                "alerts_enabled": True,
                "dashboard_url": "https://monitoring.company.com/aegisapi",
                "slack_webhook": "https://hooks.slack.com/...",
                "email_notifications": ["devops@company.com"]
            }
        }

        # Step 2: Setup enterprise database connections
        print("🗄️ Step 2: Setting up enterprise database connections...")

        from .sql_integration import SQLIntegration
        from .nosql_integration import MongoDBIntegration

        # Primary PostgreSQL connection
        try:
            primary_db = SQLIntegration(enterprise_config["databases"]["primary_sql"])
            print("✅ Connected to primary PostgreSQL database")
        except Exception as e:
            print(f"⚠️ Primary database connection failed: {e}")
            print("🔄 Falling back to SQLite...")
            primary_db = SQLIntegration("sqlite:///aegisapi_enterprise.db")

        # Secondary MongoDB connection
        try:
            secondary_db = MongoDBIntegration(
                enterprise_config["databases"]["secondary_nosql"],
                "aegisapi_enterprise"
            )
            mongodb_available = secondary_db.db is not None
            if mongodb_available:
                print("✅ Connected to secondary MongoDB database")
        except Exception as e:
            print(f"⚠️ Secondary database connection failed: {e}")
            secondary_db = None
            mongodb_available = False

        # Step 3: Setup enterprise telemetry
        print("📊 Step 3: Setting up enterprise telemetry...")
        from .telemetry_backends import TelemetryManager, SQLTelemetryBackend, NoSQLTelemetryBackend

        telemetry_manager = TelemetryManager()

        # Add file backend for reliability
        telemetry_manager.add_backend("file", FileBackend("enterprise_data", "telemetry.jsonl"))

        # Add SQL backend
        telemetry_manager.add_backend("sql", SQLTelemetryBackend(primary_db))

        # Add NoSQL backend if available
        if mongodb_available:
            telemetry_manager.add_backend("nosql", NoSQLTelemetryBackend(secondary_db))

        # Step 4: Register enterprise APIs
        print("📋 Step 4: Registering enterprise APIs...")

        registered_apis = []
        for api_config in enterprise_config["apis"]:
            # Register in primary database
            primary_api_id = primary_db.register_api_test(
                name=f"{api_config['name']} ({api_config['environment']})",
                spec_path=api_config['spec_path'],
                base_url=api_config['base_url'],
                description=f"Enterprise API - {api_config['environment']} environment"
            )

            # Register in secondary database if available
            secondary_api_id = None
            if mongodb_available:
                secondary_api_id = secondary_db.register_api_test(
                    name=f"{api_config['name']} ({api_config['environment']})",
                    spec_path=api_config['spec_path'],
                    base_url=api_config['base_url'],
                    description=f"Enterprise API - {api_config['environment']} environment"
                )

            registered_apis.append({
                "name": api_config['name'],
                "primary_id": primary_api_id,
                "secondary_id": secondary_api_id,
                "config": api_config
            })

            print(f"✅ Registered: {api_config['name']}")

        # Step 5: Enterprise monitoring setup
        print("🔍 Step 5: Setting up enterprise monitoring...")

        # Log enterprise startup event
        telemetry_manager.log_event(
            event_type="enterprise_startup",
            summary="Enterprise AegisAPI AgentNN startup completed",
            metadata={
                "environment": "production",
                "apis_registered": len(registered_apis),
                "databases_connected": 1 + (1 if mongodb_available else 0),
                "telemetry_backends": len(telemetry_manager.backends)
            }
        )

        # Step 6: Generate enterprise reports
        print("📊 Step 6: Generating enterprise reports...")

        # Get comprehensive stats
        primary_stats = primary_db.get_dashboard_stats()
        telemetry_stats = telemetry_manager.get_stats()

        enterprise_report = {
            "report_type": "enterprise_status",
            "timestamp": time.time(),
            "environment": "production",
            "database_status": {
                "primary_sql": "connected",
                "secondary_nosql": "connected" if mongodb_available else "not_configured",
                "telemetry_backends": list(telemetry_manager.backends.keys())
            },
            "apis_registered": len(registered_apis),
            "primary_database_stats": primary_stats,
            "telemetry_stats": telemetry_stats,
            "registered_apis": [
                {
                    "name": api["name"],
                    "primary_id": api["primary_id"],
                    "secondary_id": api["secondary_id"],
                    "base_url": api["config"]["base_url"]
                } for api in registered_apis
            ]
        }

        # Save enterprise report
        report_dir = Path("enterprise_reports")
        report_dir.mkdir(exist_ok=True)
        report_path = report_dir / f"enterprise_status_{int(time.time())}.json"

        with open(report_path, 'w') as f:
            json.dump(enterprise_report, f, indent=2, default=str)

        print(f"✅ Enterprise report saved to: {report_path}")

        # Step 7: Display enterprise summary
        print("\n🏢 Enterprise Integration Summary:")
        print(f"   Environment: Production")
        print(f"   APIs Registered: {len(registered_apis)}")
        print(f"   Primary Database: {'PostgreSQL' if 'postgresql' in enterprise_config['databases']['primary_sql'] else 'SQLite'}")
        print(f"   Secondary Database: {'MongoDB' if mongodb_available else 'Not Configured'}")
        print(f"   Telemetry Backends: {len(telemetry_manager.backends)}")
        print(f"   Report Location: {report_path}")

        return {
            "success": True,
            "environment": "production",
            "apis_registered": len(registered_apis),
            "databases_connected": 1 + (1 if mongodb_available else 0),
            "report_path": str(report_path)
        }

    except Exception as e:
        print(f"❌ Enterprise integration failed: {e}")
        return {"success": False, "error": str(e)}

def run_all_integration_examples():
    """Run all integration examples"""
    print("🚀 AegisAPI AgentNN - Complete Integration Suite")
    print("=" * 60)

    results = {}

    # Run Postman integration example
    print("\n1️⃣ Running Postman Integration Example...")
    results["postman"] = postman_to_aegisapi_example()

    # Run Multi-database integration example
    print("\n2️⃣ Running Multi-Database Integration Example...")
    results["multi_db"] = multi_database_integration_example()

    # Run Enterprise integration example
    print("\n3️⃣ Running Enterprise Integration Example...")
    results["enterprise"] = enterprise_integration_example()

    # Summary
    print("\n🎉 Integration Examples Complete!")
    print("=" * 60)

    successful = sum(1 for result in results.values() if result.get("success", False))
    total = len(results)

    print(f"📊 Results: {successful}/{total} examples successful")

    for name, result in results.items():
        status = "✅ SUCCESS" if result.get("success", False) else "❌ FAILED"
        print(f"   {name.upper()}: {status}")
        if not result.get("success", False):
            print(f"   Error: {result.get('error', 'Unknown error')}")

    return results

if __name__ == "__main__":
    # Run all examples
    results = run_all_integration_examples()

    # Save results
    with open("integration_results.json", 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n💾 Results saved to: integration_results.json")

    # Provide next steps
    print("\n🚀 Next Steps:")
    print("   1. Review the generated files in exports/ directory")
    print("   2. Check database files (.db files) for stored data")
    print("   3. Examine telemetry data in data/ directory")
    print("   4. Customize configurations for your specific needs")
    print("   5. Integrate with your existing CI/CD pipelines")

    print("\n🎯 Ready for production integration!")
