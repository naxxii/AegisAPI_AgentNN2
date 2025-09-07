# AegisAPI AgentNN - React Dashboard

A modern, interactive **dark-themed** React dashboard for AegisAPI AgentNN that provides real-time monitoring, control, and visualization of autonomous API testing operations.

## 🌟 Features

### 🎨 Modern Dark UI/UX
- **Beautiful Dark Design**: Professional dark interface with vibrant accent colors
- **Smooth Animations**: Framer Motion powered transitions and interactions
- **Responsive Layout**: Works perfectly on desktop, tablet, and mobile devices
- **Accessibility**: WCAG compliant design patterns with high contrast

### 📊 Real-time Monitoring
- **Live Statistics**: Real-time updates of test metrics and system health
- **Activity Feed**: Live stream of system events and operations
- **Health Indicators**: Visual representation of system status
- **Performance Metrics**: Real-time performance monitoring

### 🎮 Interactive Controls
- **One-Click Actions**: Execute AegisAPI commands with a single click
- **Visual Feedback**: Loading states, success/error notifications
- **Command History**: Track executed commands and their results
- **Progress Tracking**: Visual progress indicators for long-running operations

### 🔧 Developer Experience
- **Hot Reload**: Instant updates during development
- **Type Safety**: Modern JavaScript with clear component APIs
- **Modular Architecture**: Easy to extend and customize
- **Comprehensive API**: Well-documented component interfaces

## 🚀 Quick Start

### Prerequisites
```bash
Node.js 16+ and npm/yarn
AegisAPI AgentNN backend running (see main README)
```

### Installation
```bash
# Navigate to dashboard directory
cd dashboard

# Install dependencies
npm install
# or
yarn install
```

### Quick Setup Scripts
For Windows users without npm installed, use our automated setup scripts:

```bash
# Windows Batch script
install_and_run_react_dashboard.bat

# Or PowerShell script
.\install_and_run_react_dashboard.ps1
```

### Development
```bash
# Start development server
npm start
# or
yarn start

# Open http://localhost:3000 in your browser
```

## 🎨 Color Scheme

The dashboard uses a **professional dark theme** with vibrant accent colors:

### Primary Colors
- **Background**: Dark gradient (`#1a1a1a` to `#2d3748`)
- **Cards**: Semi-transparent dark (`rgba(30, 30, 30, 0.95)`)
- **Text**: Light gray (`#e2e8f0`)
- **Accent**: Vibrant colors for different actions

### Accent Colors by Function
- **Planning** (Red): `#ff6b6b` to `#e74c3c`
- **Generation** (Teal): `#4ecdc4` to `#26a69a`
- **Execution** (Blue): `#45b7d1` to `#2196f3`
- **Healing** (Green): `#96ceb4` to `#4caf50`

### Theme Benefits
- **Professional**: Modern dark interface suitable for enterprise
- **Eye-friendly**: Reduces eye strain during long sessions
- **Vibrant**: Accent colors make important actions stand out
- **Consistent**: Unified color language across all components

### Production Build
```bash
# Create production build
npm run build
# or
yarn build

# Serve static files
npx serve -s build -l 3000
```

## 🏗️ Architecture

### Component Structure
```
src/
├── components/
│   ├── Header.js           # Main header with branding
│   ├── StatsGrid.js        # Statistics cards grid
│   ├── ActivityFeed.js     # Live activity feed
│   ├── ControlPanel.js     # Interactive command controls
│   └── SystemHealth.js     # System health indicators
├── services/
│   └── api.js              # API client for backend communication
├── App.js                  # Main application component
└── index.js               # Application entry point
```

### State Management
- **React Hooks**: useState, useEffect for local state management
- **Real-time Updates**: Automatic dashboard refresh every 10 seconds
- **Error Handling**: Comprehensive error boundaries and user feedback

### API Integration
- **Axios Client**: Robust HTTP client with interceptors
- **Error Handling**: Automatic retry logic and user-friendly error messages
- **Loading States**: Visual feedback during API operations

## 🎨 Customization

### Colors and Themes
```javascript
// src/theme.js
export const theme = {
  colors: {
    primary: '#3498db',
    secondary: '#2c3e50',
    success: '#27ae60',
    warning: '#f39c12',
    danger: '#e74c3c',
    background: 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
    card: 'rgba(255, 255, 255, 0.95)',
    text: '#333',
    textLight: '#666'
  },
  shadows: {
    card: '0 8px 32px rgba(0, 0, 0, 0.1)',
    hover: '0 5px 15px rgba(52, 152, 219, 0.3)'
  },
  borderRadius: '15px',
  fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
};
```

### Adding New Components
```javascript
// src/components/NewComponent.js
import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';

const StyledComponent = styled(motion.div)`
  // Your styles here
`;

const NewComponent = ({ data }) => {
  return (
    <StyledComponent
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.3 }}
    >
      {/* Your component content */}
    </StyledComponent>
  );
};

export default NewComponent;
```

### Extending API Client
```javascript
// src/services/api.js
export const AegisAPI = {
  // Existing methods...

  // Add new API endpoints
  getTestDetails: (testId) => api.get(`/api/tests/${testId}`),
  deleteTestRun: (runId) => api.delete(`/api/test-runs/${runId}`),
  getSystemLogs: (lines = 100) => api.get(`/api/system/logs?lines=${lines}`)
};
```

## 📱 Mobile Responsiveness

The dashboard is fully responsive with:
- **Flexible Grid Layouts**: Adapts to screen size automatically
- **Touch-Friendly Controls**: Large buttons optimized for touch
- **Optimized Typography**: Readable text on all screen sizes
- **Progressive Enhancement**: Works on all devices, enhanced on modern ones

## 🎭 Animation & Interactions

### Framer Motion Animations
```javascript
// Smooth page transitions
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.5 }}
>
  Content
</motion.div>

// Hover effects
<motion.button
  whileHover={{ scale: 1.05 }}
  whileTap={{ scale: 0.95 }}
>
  Click me
</motion.button>
```

### Loading States
- **Skeleton Loaders**: Smooth loading experiences
- **Progress Indicators**: Visual feedback for operations
- **Spinners**: Elegant loading animations

## 🔧 Backend Integration

### Connecting to AegisAPI Backend
```javascript
// Start AegisAPI backend first
python -c "from aegisapi.cli import main; main()" web --port 8080

# Then start React dashboard
npm start

# Dashboard will automatically connect to http://localhost:8080
```

### API Endpoints Used
- `GET /api/status` - System status and statistics
- `GET /api/events` - Recent events and activity
- `POST /api/command/{action}` - Execute AegisAPI commands
- `GET /` - Dashboard HTML (fallback)

## 🧪 Testing

```bash
# Run tests
npm test

# Run tests with coverage
npm test -- --coverage

# Run tests in watch mode
npm run test:watch
```

## 📦 Deployment

### Static Hosting
```bash
# Build for production
npm run build

# Deploy build/ directory to:
# - Netlify
# - Vercel
# - GitHub Pages
# - AWS S3 + CloudFront
# - Nginx/Apache
```

### Docker Deployment
```dockerfile
FROM nginx:alpine
COPY build/ /usr/share/nginx/html/
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Docker Compose (Full Stack)
```yaml
version: '3.8'
services:
  aegisapi-backend:
    build: ../
    ports:
      - "8080:8080"
    command: python -c "from aegisapi.cli import main; main()" web --host 0.0.0.0

  aegisapi-frontend:
    build: .
    ports:
      - "3000:80"
    depends_on:
      - aegisapi-backend
```

## 🤝 Contributing

### Development Workflow
1. **Fork** the repository
2. **Create** a feature branch
3. **Make** your changes
4. **Add** tests if applicable
5. **Submit** a pull request

### Code Style
```bash
# Format code
npm run format

# Lint code
npm run lint

# Type check (if using TypeScript)
npm run type-check
```

## 📈 Performance

### Optimization Techniques
- **Code Splitting**: Automatic route-based code splitting
- **Lazy Loading**: Components loaded on demand
- **Image Optimization**: Automatic WebP conversion
- **Bundle Analysis**: `npm run analyze` to inspect bundle size

### Performance Metrics
- **First Contentful Paint**: < 1.5s
- **Largest Contentful Paint**: < 2.5s
- **First Input Delay**: < 100ms
- **Bundle Size**: < 200KB gzipped

## 🔒 Security

### Content Security Policy
```javascript
// Implemented via nginx/apache headers
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline';
```

### Environment Variables
```javascript
// .env file
REACT_APP_API_URL=http://localhost:8080
REACT_APP_ENVIRONMENT=development
REACT_APP_VERSION=1.0.0
```

## 📚 API Documentation

### Component Props
```javascript
StatsGrid.propTypes = {
  stats: PropTypes.shape({
    api_count: PropTypes.number,
    total_runs: PropTypes.number,
    successful_runs: PropTypes.number,
    failed_runs: PropTypes.number,
    healing_count: PropTypes.number,
    applied_healings: PropTypes.number
  }),
  loading: PropTypes.bool
};
```

## 🎯 Roadmap

### Upcoming Features
- [ ] **Real-time WebSocket connections** for instant updates
- [ ] **Advanced charting** with Chart.js or D3.js
- [ ] **Export functionality** (PDF reports, CSV data)
- [ ] **User authentication** and role-based access
- [ ] **Dark mode toggle** with system preference detection
- [ ] **Multi-language support** (i18n)
- [ ] **Offline mode** with service workers

### Long-term Vision
- **AI-powered insights** and recommendations
- **Predictive analytics** for API failure detection
- **Automated reporting** and alerting systems
- **Integration marketplace** for third-party tools

## 📞 Support

- **📚 Documentation**: [Full API Reference](./API_REFERENCE.md)
- **🐛 Issues**: [GitHub Issues](https://github.com/your-org/aegisapi-dashboard/issues)
- **💬 Discussions**: [GitHub Discussions](https://github.com/your-org/aegisapi-dashboard/discussions)
- **📧 Email**: support@aegisapi.com

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

---

**🚀 Ready to revolutionize API testing dashboards? Start building with AegisAPI AgentNN React Dashboard today!**

Built with ❤️ using React, Styled Components, and Framer Motion
