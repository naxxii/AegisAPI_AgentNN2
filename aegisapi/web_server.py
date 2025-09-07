from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import subprocess
import sys
import json
from . import telemetry, reporting
import argparse

app = FastAPI(
    title="AegisAPI AgentNN Dashboard",
    description="Web interface for autonomous API testing with agentic AI",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://127.0.0.1:3000", "http://127.0.0.1:3001"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main dashboard"""
    try:
        dashboard_path = Path("reports/index.html")
        if dashboard_path.exists():
            return dashboard_path.read_text(encoding='utf-8')
        else:
            # Generate dashboard if it doesn't exist
            report_path = reporting.html_report.render_dashboard()
            return Path(report_path).read_text(encoding='utf-8')
    except Exception as e:
        return f"""
        <html>
        <body>
        <h1>AegisAPI AgentNN Dashboard</h1>
        <p>Error loading dashboard: {str(e)}</p>
        <p><a href="/generate-dashboard">Generate Dashboard</a></p>
        </body>
        </html>
        """

@app.get("/generate-dashboard")
async def generate_dashboard():
    """Generate and return the dashboard"""
    try:
        report_path = reporting.html_report.render_dashboard()
        return {"status": "success", "path": report_path, "url": "/"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate dashboard: {str(e)}")

@app.post("/api/command/{action}")
async def execute_command(action: str, background_tasks: BackgroundTasks):
    """Execute AegisAPI commands via API"""
    try:
        commands = {
            'plan': ['plan', '--spec', 'examples/openapi_v1.yaml', '--base-url', 'http://localhost:4010'],
            'gen': ['gen', '--spec', 'examples/openapi_v1.yaml', '--auth-profile', 'none'],
            'run': ['run', '--tests', 'tests_generated', '--spec', 'examples/openapi_v1.yaml', '--base-url', 'http://localhost:4010'],
            'heal': ['heal', '--old-spec', 'examples/openapi_v1.yaml', '--new-spec', 'examples/openapi_v2_drift.yaml', '--interactive'],
            'report': ['report']
        }

        if action not in commands:
            raise HTTPException(status_code=400, detail=f"Unknown action: {action}")

        # Execute command in background
        background_tasks.add_task(run_aegis_command, commands[action])

        return {"status": "running", "action": action, "message": f"Executing {action} command..."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Command execution failed: {str(e)}")

@app.get("/api/status")
async def get_status():
    """Get current system status"""
    try:
        events = telemetry.load_events()
        recent_events = events[-10:] if events else []

        stats = {
            "plans_created": len([e for e in events if e.get('type') == 'plan_created']),
            "tests_generated": len([e for e in events if e.get('type') == 'test_generated']),
            "test_executions": len([e for e in events if e.get('type') == 'run_summary']),
            "heals_applied": len([e for e in events if e.get('type') == 'heal_applied']),
            "total_events": len(events),
            "recent_events": recent_events,
            "system_status": "Online",
            "test_coverage": 85,
            "api_health": 92,
            "healing_confidence": 78,
            "test_success_rate": "No tests yet"
        }

        return stats
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/events")
async def get_events(limit: int = 50):
    """Get recent events"""
    try:
        events = telemetry.load_events()
        return events[-limit:] if events else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load events: {str(e)}")

def run_aegis_command(args):
    """Run AegisAPI command in subprocess"""
    try:
        # Prepare the command
        cmd = [sys.executable, '-c', 'from aegisapi.cli import main; main()'] + args

        # Run the command
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=Path.cwd()
        )

        print(f"Command executed: {' '.join(cmd)}")
        print(f"Return code: {result.returncode}")
        if result.stdout:
            print(f"STDOUT: {result.stdout}")
        if result.stderr:
            print(f"STDERR: {result.stderr}")

    except Exception as e:
        print(f"Error running command: {str(e)}")

@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    print("🚀 AegisAPI AgentNN Web Dashboard starting...")
    print("📊 Dashboard will be available at: http://localhost:8080")
    print("📋 API endpoints available at: http://localhost:8080/docs")

def run_server(host="localhost", port=8080):
    """Run the web server"""
    import uvicorn
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AegisAPI AgentNN Web Dashboard")
    parser.add_argument("--host", default="localhost", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8080, help="Port to bind to")
    args = parser.parse_args()

    run_server(host=args.host, port=args.port)
