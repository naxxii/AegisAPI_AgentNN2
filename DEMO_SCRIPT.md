# AegisAPI AgentNN - Live Demo Script

## 🎬 Demo Overview (3-5 Minutes)

**Theme:** "From API Drift to Autonomous Healing - Agentic AI in Action"

---

## 📋 Pre-Demo Setup (Not in Video)

1. **Environment Preparation:**
   ```bash
   # Ensure mock server is ready
   python mocks/server.py &

   # Clean previous demo artifacts
   rm -rf tests_generated reports healer_patches.yaml

   # Pre-configure aegis.yaml
   cp examples/openapi_v1.yaml demo_original.yaml
   ```

2. **Demo Data Preparation:**
   - `examples/openapi_v1.yaml` - Original API spec
   - `examples/openapi_v2_drift.yaml` - API with intentional drift
   - Mock server running on localhost:4010

---

## 🎯 Demo Script (Video Timeline)

### [0:00 - 0:30] **Opening - The Problem**
**Narrator:** "Imagine you're maintaining API tests for a rapidly evolving microservices architecture. APIs change frequently, but your test suites break and require constant manual maintenance. This is where AegisAPI AgentNN comes in - an agentic AI that autonomously maintains your API tests."

**Visual:** Show broken test output, API drift examples, manual maintenance pain points

---

### [0:30 - 1:00] **Demo Setup & Planning**
**Narrator:** "Let's see AegisAPI in action. First, we'll analyze an API specification and create a strategic testing plan."

**Terminal Commands:**
```bash
# 1. Analyze API and create testing strategy
echo "🚀 Starting AegisAPI AgentNN Demo"
echo "📋 Step 1: Analyzing API specification..."

python -m aegisapi plan --spec examples/openapi_v1.yaml --base-url http://localhost:4010
```

**Visual:** Show plan.json output, highlight strategic analysis

---

### [1:00 - 1:45] **AI-Powered Test Generation**
**Narrator:** "Now watch as AegisAPI autonomously generates comprehensive test suites using AI analysis."

**Terminal Commands:**
```bash
# 2. Generate comprehensive test suite
echo "🤖 Step 2: AI-powered test generation..."
python -m aegisapi gen --spec examples/openapi_v1.yaml --auth-profile none
```

**Visual:**
- Show generated test files
- Highlight AI-generated test logic
- Display property-based testing examples

---

### [1:45 - 2:15] **Test Execution & Monitoring**
**Narrator:** "Let's run these tests against the live API to establish our baseline."

**Terminal Commands:**
```bash
# 3. Execute tests against live API
echo "⚡ Step 3: Running tests against live API..."
python -m aegisapi run --tests tests_generated --spec examples/openapi_v1.yaml --base-url http://localhost:4010
```

**Visual:** Show passing tests, telemetry data, coverage metrics

---

### [2:15 - 2:45] **API Drift Simulation**
**Narrator:** "Now let's simulate real-world API drift - when APIs evolve and break existing tests."

**Terminal Commands:**
```bash
# 4. Simulate API drift
echo "🔄 Step 4: Simulating API drift..."
python -m aegisapi run --tests tests_generated --spec examples/openapi_v2_drift.yaml --base-url http://localhost:4010
```

**Visual:** Show failing tests due to API changes

---

### [2:45 - 3:15] **Autonomous Self-Healing**
**Narrator:** "Here's where the magic happens. AegisAPI will detect the drift and autonomously propose healing solutions."

**Terminal Commands:**
```bash
# 5. Demonstrate self-healing with human oversight
echo "🔧 Step 5: Autonomous self-healing..."
python -m aegisapi heal --old-spec examples/openapi_v1.yaml --new-spec examples/openapi_v2_drift.yaml --interactive
```

**Visual:**
- Show proposed healing changes
- Demonstrate human oversight process
- Display confidence scoring

---

### [3:15 - 3:45] **Healing Application & Verification**
**Narrator:** "Let's apply the approved healing changes and verify everything works."

**Terminal Commands:**
```bash
# 6. Apply healing and verify
echo "✅ Step 6: Applying healing changes..."
python -m aegisapi heal --old-spec examples/openapi_v1.yaml --new-spec examples/openapi_v2_drift.yaml --apply --auto-apply

# 7. Re-run tests to verify healing
echo "🔍 Step 7: Verifying healed tests..."
python -m aegisapi run --tests tests_generated --spec examples/openapi_v2_drift.yaml --base-url http://localhost:4010
```

**Visual:** Show tests now passing after healing

---

### [3:45 - 4:00] **Dashboard & Reporting**
**Narrator:** "Finally, let's see the comprehensive dashboard that shows our entire testing journey."

**Terminal Commands:**
```bash
# 8. Generate comprehensive report
echo "📊 Step 8: Generating dashboard..."
python -m aegisapi report
```

**Visual:** Open reports/index.html showing complete analytics

---

## 🎯 Key Demo Highlights to Emphasize

### **Agentic AI Features:**
- ✅ Autonomous test generation
- ✅ Intelligent API analysis
- ✅ Self-healing capabilities
- ✅ Human oversight integration
- ✅ Comprehensive telemetry

### **Problem Solving:**
- ✅ API drift detection
- ✅ Confidence-based healing
- ✅ Interactive approval process
- ✅ Audit trail maintenance

### **Enterprise Readiness:**
- ✅ PII protection
- ✅ Rate limiting
- ✅ Authentication support
- ✅ Scalable architecture

---

## 📝 Demo Narration Script

**Opening Hook:**
"APIs are the lifeblood of modern applications, but maintaining test suites as they evolve is a constant battle. Today I'll show you how AegisAPI AgentNN uses agentic AI to autonomously maintain API tests."

**Technical Deep Dive:**
"We're not just running tests - we're using AI to understand API behavior, detect when things change, and automatically propose fixes with human oversight."

**Closing:**
"AegisAPI AgentNN doesn't just test APIs - it evolves with them, ensuring your test suites stay reliable as your APIs grow and change."

---

## 🎬 Video Production Notes

### **Technical Requirements:**
- Screen recording software (OBS, Camtasia)
- Clear terminal font (Consolas, Fira Code)
- Highlighted commands and outputs
- Smooth transitions between steps

### **Visual Enhancements:**
- Add annotations for key concepts
- Zoom in on important outputs
- Use callouts for confidence scores
- Show before/after comparisons

### **Timing Guidelines:**
- Keep each step under 30 seconds
- Pause for 2-3 seconds after key outputs
- Allow time for audience to process information
- End with clear next steps

---

## 🚀 Post-Demo Engagement

### **Q&A Preparation:**
- "How does confidence scoring work?"
- "What's the human oversight process?"
- "How scalable is this for enterprise use?"
- "What APIs does it support?"

### **Follow-up Actions:**
- Provide GitHub repository link
- Share demo script for self-testing
- Offer live demo sessions
- Provide contact for enterprise inquiries

---

**Demo Length:** 4 minutes
**Key Takeaway:** AegisAPI AgentNN autonomously maintains API test suites through intelligent analysis, self-healing, and human oversight.
