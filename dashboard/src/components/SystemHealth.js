import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import {
  Activity,
  Server,
  Shield,
  TrendingUp,
  Cpu,
  HardDrive,
  Zap
} from 'lucide-react';

const Panel = styled(motion.div)`
  background: rgba(30, 30, 30, 0.95);
  border-radius: 15px;
  padding: 25px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
`;

const Header = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  border-bottom: 2px solid #4a5568;
  padding-bottom: 15px;
`;

const Title = styled.h3`
  font-size: 1.5em;
  font-weight: bold;
  color: #e2e8f0;
  margin: 0;
`;

const HealthItem = styled.div`
  margin-bottom: 20px;

  &:last-child {
    margin-bottom: 0;
  }
`;

const HealthLabel = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  font-weight: 500;
  color: #555;
`;

const HealthValue = styled.span`
  font-weight: bold;
  color: ${props => {
    if (props.status === 'good') return '#27ae60';
    if (props.status === 'warning') return '#f39c12';
    if (props.status === 'danger') return '#e74c3c';
    return '#3498db';
  }};
`;

const ProgressBar = styled.div`
  width: 100%;
  height: 8px;
  background: #eee;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 10px;
`;

const ProgressFill = styled.div`
  height: 100%;
  background: linear-gradient(90deg, #27ae60, #2ecc71);
  transition: width 0.3s ease;
  border-radius: 4px;
`;

const StatusIndicator = styled.div`
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;

  ${props => {
    if (props.status === 'good') {
      return `
        background: rgba(39, 174, 96, 0.1);
        color: #27ae60;
        border: 1px solid rgba(39, 174, 96, 0.2);
      `;
    }
    if (props.status === 'warning') {
      return `
        background: rgba(243, 156, 18, 0.1);
        color: #f39c12;
        border: 1px solid rgba(243, 156, 18, 0.2);
      `;
    }
    if (props.status === 'danger') {
      return `
        background: rgba(231, 76, 60, 0.1);
        color: #e74c3c;
        border: 1px solid rgba(231, 76, 60, 0.2);
      `;
    }
    return `
      background: rgba(52, 152, 219, 0.1);
      color: #3498db;
      border: 1px solid rgba(52, 152, 219, 0.2);
    `;
  }}
`;

const AgenticFeatures = styled.div`
  margin-top: 25px;
  padding-top: 20px;
  border-top: 1px solid #f0f0f0;
`;

const FeatureTitle = styled.h4`
  font-size: 1.1em;
  font-weight: bold;
  color: #333;
  margin-bottom: 15px;
`;

const FeatureList = styled.div`
  display: flex;
  flex-direction: column;
  gap: 10px;
`;

const Feature = styled.div`
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 0;
  font-size: 14px;
`;

const FeatureIcon = styled.span`
  color: #27ae60;
  font-size: 16px;
`;

const FeatureText = styled.span`
  color: #555;
`;

const getStatusFromPercentage = (percentage) => {
  if (percentage >= 90) return 'good';
  if (percentage >= 70) return 'warning';
  return 'danger';
};

const getStatusFromSuccessRate = (successful, total) => {
  if (total === 0) return 'neutral';
  const rate = (successful / total) * 100;
  if (rate >= 90) return 'good';
  if (rate >= 70) return 'warning';
  return 'danger';
};

const SystemHealth = ({ stats }) => {
  const totalRuns = stats.total_runs || 0;
  const successfulRuns = stats.successful_runs || 0;
  const successRate = totalRuns > 0 ? (successfulRuns / totalRuns) * 100 : 0;

  // Mock system metrics (in real app, these would come from backend)
  const systemMetrics = {
    cpu: 45,
    memory: 62,
    disk: 78,
    network: 23
  };

  const features = [
    { icon: '🧠', text: 'Autonomous Test Generation' },
    { icon: '🔄', text: 'Self-Healing API Changes' },
    { icon: '🎯', text: 'Intelligent Drift Detection' },
    { icon: '👥', text: 'Human Oversight Control' },
    { icon: '📊', text: 'Real-time Analytics' }
  ];

  return (
    <Panel
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.3, delay: 0.2 }}
    >
      <Header>
        <Title>System Health</Title>
      </Header>

      <HealthItem>
        <HealthLabel>
          <span>Test Coverage</span>
          <HealthValue status="good">85%</HealthValue>
        </HealthLabel>
        <ProgressBar>
          <ProgressFill style={{ width: '85%' }} />
        </ProgressBar>
      </HealthItem>

      <HealthItem>
        <HealthLabel>
          <span>API Health</span>
          <HealthValue status="good">92%</HealthValue>
        </HealthLabel>
        <ProgressBar>
          <ProgressFill style={{ width: '92%' }} />
        </ProgressBar>
      </HealthItem>

      <HealthItem>
        <HealthLabel>
          <span>Healing Confidence</span>
          <HealthValue status="warning">78%</HealthValue>
        </HealthLabel>
        <ProgressBar>
          <ProgressFill style={{ width: '78%' }} />
        </ProgressBar>
      </HealthItem>

      <HealthItem>
        <HealthLabel>
          <span>Test Success Rate</span>
          <HealthValue status={getStatusFromSuccessRate(successfulRuns, totalRuns)}>
            {totalRuns > 0 ? `${successRate.toFixed(1)}%` : 'No tests yet'}
          </HealthValue>
        </HealthLabel>
        <ProgressBar>
          <ProgressFill style={{ width: `${Math.min(successRate, 100)}%` }} />
        </ProgressBar>
      </HealthItem>

      <HealthItem>
        <HealthLabel>
          <span>System Status</span>
          <StatusIndicator status="good">
            <Activity size={12} />
            Online
          </StatusIndicator>
        </HealthLabel>
      </HealthItem>

      <AgenticFeatures>
        <FeatureTitle>Agentic Features</FeatureTitle>
        <FeatureList>
          {features.map((feature, index) => (
            <Feature key={index}>
              <FeatureIcon>{feature.icon}</FeatureIcon>
              <FeatureText>{feature.text}</FeatureText>
            </Feature>
          ))}
        </FeatureList>
      </AgenticFeatures>
    </Panel>
  );
};

export default SystemHealth;
