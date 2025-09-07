import argparse, json, sys, pathlib, time
from . import planner, generator, executor, healer, reporting, telemetry, web_server
def main():
    p=argparse.ArgumentParser(); sub=p.add_subparsers(dest="cmd")
    a=sub.add_parser("plan"); a.add_argument("--spec",required=True); a.add_argument("--base-url",required=True)
    b=sub.add_parser("gen"); b.add_argument("--spec",required=True); b.add_argument("--out",default="tests_generated"); b.add_argument("--auth-profile",default="none")
    c=sub.add_parser("run"); c.add_argument("--tests",default="tests_generated"); c.add_argument("--spec",required=True); c.add_argument("--base-url",required=True); c.add_argument("--with-fuzz",action="store_true")
    d=sub.add_parser("heal"); d.add_argument("--old-spec",required=True); d.add_argument("--new-spec",required=True); d.add_argument("--apply",action="store_true"); d.add_argument("--interactive",action="store_true",help="Enable interactive human review of each change"); d.add_argument("--auto-apply",action="store_true",help="Automatically apply all high-confidence changes without review"); d.add_argument("--confidence-threshold",type=float,default=0.6)
    e=sub.add_parser("report")
    f=sub.add_parser("web"); f.add_argument("--host",default="localhost"); f.add_argument("--port",type=int,default=8000)
    g=sub.add_parser("import-postman"); g.add_argument("--collection",required=True); g.add_argument("--output-spec",default=None); g.add_argument("--test-dir",default="tests_from_postman")
    h=sub.add_parser("setup-db"); h.add_argument("--type",choices=["sqlite","postgresql","mysql","mongodb"],default="sqlite"); h.add_argument("--connection-string",default=None); h.add_argument("--db-name",default="aegisapi")
    i=sub.add_parser("integrations-demo")
    j=sub.add_parser("demo")
    args=p.parse_args()
    if args.cmd=="plan":
        telemetry.log_event({"type":"run_started","ts":time.time(),"meta":{"action":"plan"}})
        plan=planner.build_plan(args.spec,args.base_url); pathlib.Path("reports").mkdir(parents=True,exist_ok=True); (pathlib.Path("reports")/"plan.json").write_text(json.dumps(plan,indent=2),encoding="utf-8"); print("Plan written")
    elif args.cmd=="gen":
        telemetry.log_event({"type":"run_started","ts":time.time(),"meta":{"action":"gen"}}); generator.generate_tests(args.spec, pathlib.Path(args.out), auth_profile=args.auth_profile); print("Tests generated")
    elif args.cmd=="run":
        telemetry.log_event({"type":"run_started","ts":time.time(),"meta":{"action":"run"}}); sys.exit(executor.run_tests(args.tests, spec=args.spec, base_url=args.base_url, with_fuzz=args.with_fuzz))
    elif args.cmd=="heal":
        telemetry.log_event({"type":"run_started","ts":time.time(),"meta":{"action":"heal"}}); props=healer.diff_and_propose(args.old_spec,args.new_spec); pathlib.Path("reports").mkdir(parents=True,exist_ok=True); (pathlib.Path("reports")/"heals.json").write_text(json.dumps(props,indent=2),encoding="utf-8"); print("Heals written");
        if args.apply:
            healer.apply_heals(props, args.confidence_threshold, args.interactive, args.auto_apply)
    elif args.cmd=="report":
        report_path = reporting.html_report.render_dashboard(); print(f"Report written to {report_path}")
    elif args.cmd=="web":
        web_server.run_server(host=args.host, port=args.port)
    elif args.cmd=="import-postman":
        try:
            from .integrations.postman_integration import import_postman_collection
            result = import_postman_collection(args.collection, args.output_spec)
            print(result)
        except ImportError as e:
            print(f"❌ Postman integration not available: {e}")
            print("Install with: pip install requests")
    elif args.cmd=="setup-db":
        try:
            if args.type == "mongodb":
                from .integrations.nosql_integration import create_mongodb_integration
                db = create_mongodb_integration(args.connection_string, args.db_name)
                if db.db:
                    print(f"✅ MongoDB database '{args.db_name}' ready!")
                else:
                    print("❌ MongoDB connection failed")
            else:
                from .integrations.sql_integration import SQLIntegration
                if args.connection_string:
                    connection_string = args.connection_string
                elif args.type == "sqlite":
                    connection_string = f"sqlite:///{args.db_name}.db"
                elif args.type == "postgresql":
                    connection_string = f"postgresql://user:pass@localhost:5432/{args.db_name}"
                elif args.type == "mysql":
                    connection_string = f"mysql://user:pass@localhost:3306/{args.db_name}"

                db = SQLIntegration(connection_string)
                print(f"✅ {args.type.upper()} database '{args.db_name}' ready!")
                print(f"   Connection: {connection_string}")

        except ImportError as e:
            print(f"❌ Database integration not available: {e}")
            if args.type == "mongodb":
                print("Install with: pip install pymongo")
            else:
                print("Install with: pip install sqlalchemy psycopg2-binary mysql-connector-python")
    elif args.cmd=="integrations-demo":
        try:
            from .integrations.integration_examples import run_all_integration_examples
            results = run_all_integration_examples()
            print(f"\n✅ Integration demo completed! Check exports/ directory for results.")
        except ImportError as e:
            print(f"❌ Integration examples not available: {e}")
    elif args.cmd=="demo":
        try:
            import subprocess
            result = subprocess.run([sys.executable, "run_full_demo.py"], cwd=".")
            sys.exit(result.returncode)
        except Exception as e:
            print(f"❌ Demo failed: {e}")
            sys.exit(1)
    else: p.print_help()
if __name__=="__main__": main()
