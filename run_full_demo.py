#!/usr/bin/env python3
"""
Complete AegisAPI AgentNN Demo Runner
Starts both backend and React frontend for full demonstration
"""
import subprocess
import sys
import time
import os
import signal
from pathlib import Path

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking requirements...")

    # Check if Node.js is installed
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js found: {result.stdout.strip()}")
        else:
            print("❌ Node.js not found. Please install Node.js 16+ from https://nodejs.org")
            return False
    except FileNotFoundError:
        print("❌ Node.js not found. Please install Node.js 16+ from https://nodejs.org")
        return False

    # Check if npm is installed
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ npm found: {result.stdout.strip()}")
        else:
            print("❌ npm not found. Please install npm with Node.js")
            return False
    except FileNotFoundError:
        print("❌ npm not found. Please install npm with Node.js")
        return False

    # Check if dashboard directory exists
    if not Path("dashboard").exists():
        print("❌ dashboard/ directory not found. Please ensure you're in the correct directory.")
        return False

    print("✅ All requirements met!")
    return True

def setup_dashboard():
    """Setup React dashboard if needed"""
    dashboard_path = Path("dashboard")

    # Check if node_modules exists
    if not (dashboard_path / "node_modules").exists():
        print("📦 Installing React dashboard dependencies...")
        os.chdir(dashboard_path)
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "../requirements.txt"], cwd="..")
        if result.returncode != 0:
            print("❌ Failed to install Python dependencies")
            return False

        result = subprocess.run(["npm", "install"])
        if result.returncode != 0:
            print("❌ Failed to install React dependencies")
            return False
        os.chdir("..")
        print("✅ Dependencies installed successfully!")
    else:
        print("✅ React dependencies already installed")

    return True

def start_mock_server():
    """Start the mock API server"""
    print("🚀 Starting mock API server...")
    try:
        # Set environment variable for demo
        os.environ["DEMO_VERSION"] = "v1"

        # Start mock server
        mock_process = subprocess.Popen([
            sys.executable, "-c",
            "from aegisapi.mocks.server import app; import uvicorn; uvicorn.run(app, host='localhost', port=4010)"
        ])

        # Wait a moment for server to start
        time.sleep(2)

        # Test if server is responding
        import requests
        try:
            response = requests.get("http://localhost:4010/users", timeout=5)
            if response.status_code == 200:
                print("✅ Mock API server started successfully on http://localhost:4010")
                return mock_process
            else:
                print(f"❌ Mock server responded with status {response.status_code}")
                mock_process.terminate()
                return None
        except requests.exceptions.RequestException:
            print("❌ Mock server not responding")
            mock_process.terminate()
            return None

    except Exception as e:
        print(f"❌ Failed to start mock server: {e}")
        return None

def start_aegisapi_backend():
    """Start AegisAPI backend server"""
    print("🧠 Starting AegisAPI AgentNN backend...")
    try:
        backend_process = subprocess.Popen([
            sys.executable, "-c",
            "from aegisapi.cli import main; main()",
            "web", "--host", "localhost", "--port", "8080"
        ])

        # Wait for backend to start
        time.sleep(3)

        # Test backend
        import requests
        try:
            response = requests.get("http://localhost:8080/api/status", timeout=5)
            if response.status_code == 200:
                print("✅ AegisAPI backend started successfully on http://localhost:8080")
                return backend_process
            else:
                print(f"❌ Backend responded with status {response.status_code}")
                backend_process.terminate()
                return None
        except requests.exceptions.RequestException:
            print("❌ Backend server not responding")
            backend_process.terminate()
            return None

    except Exception as e:
        print(f"❌ Failed to start AegisAPI backend: {e}")
        return None

def start_react_dashboard():
    """Start React dashboard"""
    print("⚛️ Starting React dashboard...")
    try:
        os.chdir("dashboard")
        dashboard_process = subprocess.Popen(["npm", "start"])

        # Wait for React dev server to start
        time.sleep(10)  # React takes longer to start

        # Test if dashboard is accessible
        import requests
        try:
            response = requests.get("http://localhost:3000", timeout=5)
            if response.status_code == 200:
                print("✅ React dashboard started successfully on http://localhost:3000")
                return dashboard_process
            else:
                print(f"❌ Dashboard responded with status {response.status_code}")
                dashboard_process.terminate()
                return None
        except requests.exceptions.RequestException:
            print("❌ Dashboard server not responding")
            dashboard_process.terminate()
            return None
        finally:
            os.chdir("..")

    except Exception as e:
        print(f"❌ Failed to start React dashboard: {e}")
        os.chdir("..")
        return None

def run_demo_workflow():
    """Run a complete demo workflow"""
    print("\n🎬 Running AegisAPI AgentNN Demo Workflow...")
    print("=" * 60)

    try:
        # Execute AegisAPI commands
        commands = [
            ("plan", "Creating testing strategy..."),
            ("gen", "Generating AI-powered tests..."),
            ("run", "Running tests against live API..."),
            ("heal", "Demonstrating self-healing..."),
            ("report", "Generating dashboard...")
        ]

        for cmd, description in commands:
            print(f"\n📋 {description}")
            if cmd == "heal":
                # Special handling for heal command with human oversight
                result = subprocess.run([
                    sys.executable, "-c",
                    "from aegisapi.cli import main; main()",
                    cmd, "--old-spec", "examples/openapi_v1.yaml",
                    "--new-spec", "examples/openapi_v2_drift.yaml",
                    "--apply", "--auto-apply"
                ], capture_output=True, text=True, timeout=30)
            else:
                result = subprocess.run([
                    sys.executable, "-c",
                    "from aegisapi.cli import main; main()",
                    cmd
                ], capture_output=True, text=True, timeout=30)

            if result.returncode == 0:
                print(f"✅ {cmd.upper()} completed successfully")
            else:
                print(f"⚠️ {cmd.upper()} completed with warnings")
                if result.stderr:
                    print(f"   Error: {result.stderr.strip()}")

            time.sleep(2)  # Brief pause between commands

        print("\n🎉 Demo workflow completed successfully!")
        print("🌐 Access your dashboard at:")
        print("   📊 HTML Dashboard: http://localhost:8080")
        print("   ⚛️ React Dashboard: http://localhost:3000")

    except Exception as e:
        print(f"❌ Demo workflow failed: {e}")

def main():
    """Main demo runner"""
    print("🚀 AegisAPI AgentNN - Complete Demo Suite")
    print("=" * 60)

    # Check requirements
    if not check_requirements():
        sys.exit(1)

    # Setup dashboard
    if not setup_dashboard():
        sys.exit(1)

    processes = []

    try:
        # Start services
        print("\n🏗️ Starting services...")

        # 1. Start mock API server
        mock_process = start_mock_server()
        if mock_process:
            processes.append(("Mock API", mock_process))

        # 2. Start AegisAPI backend
        backend_process = start_aegisapi_backend()
        if backend_process:
            processes.append(("AegisAPI Backend", backend_process))

        # 3. Start React dashboard
        dashboard_process = start_react_dashboard()
        if dashboard_process:
            processes.append(("React Dashboard", dashboard_process))

        if len(processes) < 3:
            print("❌ Not all services started successfully")
            sys.exit(1)

        # Run demo workflow
        run_demo_workflow()

        print("\n🎊 All services are running!")
        print("\n🌐 Access URLs:")
        print("   📊 HTML Dashboard: http://localhost:8080")
        print("   ⚛️ React Dashboard: http://localhost:3000")
        print("   🔗 Mock API: http://localhost:4010")
        print("   📚 Mock API Docs: http://localhost:4010/docs")

        print("\n⏹️ Press Ctrl+C to stop all services")

        # Keep running until interrupted
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down services...")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        # Cleanup: terminate all processes
        print("🧹 Cleaning up...")
        for name, process in processes:
            try:
                if process.poll() is None:  # Process is still running
                    print(f"⏹️ Stopping {name}...")
                    process.terminate()
                    process.wait(timeout=5)
            except Exception as e:
                print(f"⚠️ Error stopping {name}: {e}")
                try:
                    process.kill()
                except:
                    pass

        print("✅ All services stopped. Goodbye! 👋")

if __name__ == "__main__":
    main()
