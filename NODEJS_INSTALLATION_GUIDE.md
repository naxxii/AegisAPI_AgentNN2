# 🚀 Node.js Installation Guide for AegisAPI AgentNN

## 🎯 Why Do You Need Node.js?

Node.js is required to run the **React Dashboard** - the beautiful, interactive web interface for AegisAPI AgentNN. Without Node.js, you'll only have access to the basic HTML dashboard.

### **What You Get With Node.js:**
- ✅ **Interactive React Dashboard** with real-time updates
- ✅ **Beautiful animations** and modern UI components
- ✅ **Live controls** to execute AegisAPI commands
- ✅ **Professional interface** perfect for demos

---

## 📦 Installation Methods

### **Method 1: Official Website (Recommended)**
```bash
# 1. Visit the official Node.js website
# Open your browser and go to: https://nodejs.org/

# 2. Download the LTS version
# - Click the green "Download Node.js (LTS)" button
# - Choose the Windows Installer (.msi) file
# - Download size: ~25-30MB

# 3. Install Node.js
# - Run the downloaded .msi file
# - Follow the installation wizard:
#   - Click "Next" on welcome screen
#   - Accept license agreement
#   - Choose installation directory (default is fine)
#   - Select components (keep defaults)
#   - Click "Next" and "Install"
# - Installation takes 1-2 minutes

# 4. Verify Installation
node --version    # Should show: v18.17.0 or similar
npm --version     # Should show: 9.6.7 or similar
```

### **Method 2: Windows Package Managers**

#### **Using Chocolatey (if you have it):**
```bash
# Open PowerShell/Command Prompt as Administrator
choco install nodejs --yes

# Verify
node --version
npm --version
```

#### **Using Winget (Windows 10/11 built-in):**
```bash
# Open PowerShell/Command Prompt
winget install OpenJS.NodeJS

# Verify
node --version
npm --version
```

#### **Using Scoop:**
```bash
# If you have Scoop installed
scoop install nodejs

# Verify
node --version
npm --version
```

### **Method 3: Package Managers (Advanced)**

#### **Using NVM (Node Version Manager):**
```bash
# 1. Download NVM for Windows
# Go to: https://github.com/coreybutler/nvm-windows/releases
# Download: nvm-setup.zip
# Extract and run setup.exe

# 2. Install Node.js
nvm install lts
nvm use lts

# 3. Verify
node --version
npm --version
```

---

## 🧪 Test Your Installation

### **Step 1: Open Command Prompt/PowerShell**
```bash
# Open Windows PowerShell or Command Prompt
# Navigate to your AegisAPI project directory
cd D:\AegisAPI_AgentNN_Mod_9
```

### **Step 2: Test Node.js**
```bash
# Test Node.js
node --version
# Expected output: v18.17.0 (or similar version)

# Test npm
npm --version
# Expected output: 9.6.7 (or similar version)
```

### **Step 3: Test AegisAPI React Dashboard**
```bash
# Navigate to dashboard directory
cd dashboard

# Install React dependencies
npm install

# Start the React development server
npm start

# Expected output:
# Compiled successfully!
# You can now view aegisapi-dashboard in the browser.
# Local: http://localhost:3000/
```

---

## 🌐 Access Your Dashboards

### **With Node.js (Full Experience):**
- **React Dashboard**: http://localhost:3000 (Beautiful, interactive)
- **HTML Dashboard**: http://localhost:8000 (Basic, always available)

### **Without Node.js (Limited):**
- **HTML Dashboard Only**: http://localhost:8000

---

## 🚀 Quick Start After Installation

### **1. Start AegisAPI Backend**
```bash
# Start the backend server on port 8000
python -c "from aegisapi.cli import main; main()" web --port 8000
```

### **2. Start React Dashboard**
```bash
# Navigate to dashboard directory
cd dashboard

# Install dependencies (first time only)
npm install

# Start React development server
npm start
```

### **3. Access Your Dashboards**
- **React Dashboard**: http://localhost:3000
- **HTML Dashboard**: http://localhost:8000

---

## 🛠️ Troubleshooting

### **Problem: "node is not recognized"**
**Solution:**
```bash
# Add Node.js to your PATH
# 1. Search for "Environment Variables"
# 2. Click "Edit the system environment variables"
# 3. Click "Environment Variables"
# 4. Under "System Variables", find "Path"
# 5. Click "Edit"
# 6. Add: C:\Program Files\nodejs\
# 7. Restart your command prompt
```

### **Problem: Permission Errors**
**Solution:**
```bash
# Run Command Prompt/PowerShell as Administrator
# Right-click → Run as administrator
```

### **Problem: Port 3000 Already in Use**
**Solution:**
```bash
# Kill process using port 3000
netstat -ano | findstr :3000
# Note the PID, then:
taskkill /PID <PID_NUMBER> /F

# Or use a different port
npm start -- --port 3001
```

### **Problem: npm install fails**
**Solution:**
```bash
# Clear npm cache
npm cache clean --force

# Try installing again
npm install

# If still fails, try with legacy peer deps
npm install --legacy-peer-deps
```

---

## 📋 System Requirements

### **Minimum Requirements:**
- **Windows**: 7, 8.1, 10, 11
- **RAM**: 4GB minimum, 8GB recommended
- **Disk Space**: 500MB free space
- **Network**: Internet connection for npm packages

### **Recommended Setup:**
- **Windows 10/11** with latest updates
- **8GB RAM** or more
- **SSD storage** for faster npm installs
- **Stable internet connection**

---

## 🎯 Next Steps After Installation

### **1. Test AegisAPI**
```bash
# Generate some test data
python -c "from aegisapi.cli import main; main()" plan --spec examples/openapi_v1.yaml --base-url http://localhost:4010
python -c "from aegisapi.cli import main; main()" gen --spec examples/openapi_v1.yaml --auth-profile none
python -c "from aegisapi.cli import main; main()" run --tests tests_generated --spec examples/openapi_v1.yaml --base-url http://localhost:4010
python -c "from aegisapi.cli import main; main()" report
```

### **2. View Dashboards**
- **React Dashboard**: http://localhost:3000 (Interactive!)
- **HTML Dashboard**: http://localhost:8000 (Basic)

### **3. Start Building**
```bash
# Your AegisAPI AgentNN is ready!
# Start creating your own API tests...
```

---

## 💬 Support

### **Common Questions:**

**Q: Do I need Node.js to use AegisAPI?**
A: No! AegisAPI works perfectly without Node.js. You'll just have the HTML dashboard instead of the React one.

**Q: Can I use a different port?**
A: Yes! Change the port in the web command: `--port 8080`

**Q: npm install is slow?**
A: Use `npm install --verbose` to see progress, or try a different network.

**Q: React dashboard not loading?**
A: Check that the AegisAPI backend is running on port 8000 first.

---

## 🎉 You're All Set!

**With Node.js installed, you now have access to:**
- ✅ **Beautiful React Dashboard** with real-time updates
- ✅ **Interactive controls** for all AegisAPI commands
- ✅ **Professional animations** and modern UI
- ✅ **Live data visualization** and analytics
- ✅ **Perfect for demos and presentations**

**🚀 Your AegisAPI AgentNN is now a complete enterprise-grade API testing platform!**

---

*Last updated: 2024 | AegisAPI AgentNN Team*
