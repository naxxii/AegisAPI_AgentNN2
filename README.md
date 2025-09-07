# AegisAPI AgentNN — Agentic API Test Automation

![AegisAPI AgentNN](https://img.shields.io/badge/Agentic--AI-API--Testing-blue)
![Python](https://img.shields.io/badge/Python-3.10+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🎯 Project Overview

**AegisAPI AgentNN** is a revolutionary **Agentic AI-powered API testing framework** that autonomously generates, executes, and maintains API test suites. Unlike traditional testing tools, AegisAPI uses intelligent agents to understand API behavior, adapt to changes, and self-heal when APIs drift or break.

### 🌟 Key Innovation
- **Autonomous Test Generation**: AI agents analyze API specifications and generate comprehensive test suites
- **Self-Healing Capabilities**: Automatically detects and fixes broken tests when APIs evolve
- **Intelligent Adaptation**: Learns from API behavior and adjusts testing strategies
- **Enterprise-Ready**: Built with security, scalability, and compliance in mind

---

## 🚀 Core Features

### 🤖 Agentic AI Pipeline
1. **Plan** - Strategic test planning and API analysis
2. **Generate** - AI-powered test script creation
3. **Execute** - Intelligent test execution with fuzzing
4. **Heal** - Autonomous self-healing of broken tests
5. **Report** - Comprehensive dashboard generation

### 🔧 Technical Capabilities
- **Multi-format Support**: OpenAPI 3.x, Postman Collections, HAR files
- **Authentication**: API Keys, OAuth, JWT, Basic Auth
- **Property-based Testing**: Uses Hypothesis for comprehensive coverage
- **PII Protection**: Built-in sensitive data redaction
- **Rate Limiting**: Configurable request throttling
- **Schema Validation**: JSON Schema compliance checking

---

## 📋 Prerequisites

- **Python**: 3.10 or higher
- **Git**: For version control
- **API Specifications**: OpenAPI/Swagger files, Postman collections, or HAR files

---

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/AegisAPI-AgentNN.git
cd AegisAPI-AgentNN
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
# Copy and edit configuration
cp aegis.yaml aegis.local.yaml
# Edit aegis.local.yaml with your settings
```

---

## 📖 Usage Guide

### Quick Start Example

```bash
# 1. Plan your testing strategy
python -m aegisapi plan --spec examples/openapi_v1.yaml --base-url http://localhost:4010

# 2. Generate test scripts
python -m aegisapi gen --spec examples/openapi_v1.yaml --auth-profile api_key

# 3. Run tests against live API
python -m aegisapi run --tests tests_generated --spec examples/openapi_v1.yaml --base-url http://localhost:4010

# 4. Generate HTML report
python -m aegisapi report
```

### Command Reference

#### `plan` - Strategic Test Planning
```bash
python -m aegisapi plan --spec <api_spec> --base-url <base_url>
```
- Analyzes API specification
- Creates comprehensive testing strategy
- Outputs plan to `reports/plan.json`

#### `gen` - Test Generation
```bash
python -m aegisapi gen --spec <api_spec> --out <output_dir> --auth-profile <profile>
```
- Generates pytest test scripts
- Supports multiple authentication profiles
- Creates property-based tests using Hypothesis

#### `run` - Test Execution
```bash
python -m aegisapi run --tests <test_dir> --spec <api_spec> --base-url <base_url> [--with-fuzz]
```
- Executes generated test suites
- Runs against live APIs
- Optional fuzz testing with `--with-fuzz`

#### `heal` - Self-Healing
```bash
python -m aegisapi heal --old-spec <old_spec> --new-spec <new_spec> [--apply] [--confidence-threshold 0.6]
```
- Compares API specifications
- Proposes healing strategies
- Auto-applies fixes above confidence threshold

#### `report` - Dashboard Generation
```bash
python -m aegisapi report
```
- Generates HTML dashboard
- Shows test results and analytics
- Opens `reports/index.html`

---

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   API Specs     │───▶│   Generator     │───▶│  Test Scripts   │
│ (OpenAPI/Postman│    │   (AI Agent)    │    │   (pytest)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Planner     │    │    Executor     │    │     Healer      │
│ (Strategy AI)   │    │   (Test Runner)  │    │  (Self-Healing) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 ▼
                    ┌─────────────────┐
                    │    Reporter     │
                    │   (Dashboard)   │
                    └─────────────────┘
```

### Core Modules

- **`cli.py`** - Command-line interface and orchestration
- **`generator.py`** - AI-powered test script generation
- **`executor.py`** - Test execution and result collection
- **`healer.py`** - API drift detection and self-healing
- **`planner.py`** - Strategic test planning
- **`telemetry.py`** - Logging and monitoring
- **`reporting/`** - HTML dashboard generation

---

## 🔒 Security & Privacy

### PII Protection
- **Automatic Redaction**: Sensitive fields automatically masked
- **Configurable Fields**: Customize PII detection in `aegis.yaml`
- **Safe Logging**: Telemetry data sanitized before storage

### Authentication Security
- **Secure Storage**: API keys stored in environment variables
- **Multiple Profiles**: Support for various auth methods
- **Token Rotation**: Built-in support for token refresh

---

## 📊 Demo Script (3-5 minutes)

### Scenario: Testing a Pet Store API

```bash
# Setup demo environment
echo "🚀 AegisAPI AgentNN Demo - Pet Store API Testing"

# 1. Start mock server (if available)
# python mocks/server.py &

# 2. Show API specification
echo "📋 Analyzing API specification..."
python -m aegisapi plan --spec examples/openapi_v1.yaml --base-url http://localhost:4010

# 3. Generate tests
echo "🤖 Generating test scripts..."
python -m aegisapi gen --spec examples/openapi_v1.yaml --auth-profile none

# 4. Run tests
echo "⚡ Executing tests..."
python -m aegisapi run --tests tests_generated --spec examples/openapi_v1.yaml --base-url http://localhost:4010

# 5. Demonstrate self-healing
echo "🔧 Testing self-healing with API drift..."
python -m aegisapi heal --old-spec examples/openapi_v1.yaml --new-spec examples/openapi_v2_drift.yaml --apply

# 6. Show final report
echo "📊 Generating dashboard..."
python -m aegisapi report

echo "🎉 Demo complete! Check reports/index.html for results"
```

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run linting
flake8 aegisapi/
```

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with modern Python testing frameworks
- Inspired by the need for autonomous API testing
- Special thanks to the open-source testing community

---

## 📞 Support

- **Documentation**: [Full API Reference](docs/api.md)
- **Issues**: [GitHub Issues](https://github.com/your-username/AegisAPI-AgentNN/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/AegisAPI-AgentNN/discussions)

---

**Ready to revolutionize your API testing? Get started with AegisAPI AgentNN today!** 🚀
