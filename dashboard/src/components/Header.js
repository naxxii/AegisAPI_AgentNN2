import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { Cpu, Zap, Shield, BarChart3 } from 'lucide-react';

const HeaderContainer = styled(motion.header)`
  text-align: center;
  margin-bottom: 30px;
  color: #2d3748;
  background: rgba(255, 255, 255, 0.9);
  padding: 30px;
  border-radius: 20px;
  box-shadow: 0 10px 40px rgba(102, 126, 234, 0.2);
  backdrop-filter: blur(15px);
  border: 2px solid rgba(102, 126, 234, 0.1);
  margin-top: 20px;
  position: relative;
  overflow: hidden;
`;

const Logo = styled(motion.h1)`
  font-size: 3.5em;
  font-weight: bold;
  margin-bottom: 15px;
  background: linear-gradient(45deg, #667eea, #764ba2, #f093fb, #f5576c);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  position: relative;
  overflow: hidden;
  text-shadow: 0 0 30px rgba(102, 126, 234, 0.3);
  z-index: 2;
`;

const Subtitle = styled(motion.p)`
  font-size: 1.3em;
  opacity: 0.9;
  margin-bottom: 20px;
  color: #4a5568;
  font-weight: 500;
  z-index: 2;
  position: relative;
`;

const StatusIndicator = styled.div`
  position: absolute;
  top: 20px;
  right: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9em;
  font-weight: 500;
  z-index: 3;

  &::before {
    content: '';
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: ${props => {
      switch (props.status) {
        case 'connected': return '#27ae60';
        case 'connecting': return '#f39c12';
        case 'error': return '#e74c3c';
        default: return '#95a5a6';
      }
    }};
    animation: ${props => props.status === 'connecting' ? 'pulse 2s infinite' : 'none'};
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
  }
`;

const Features = styled(motion.div)`
  display: flex;
  justify-content: center;
  gap: 30px;
  flex-wrap: wrap;
  z-index: 2;
  position: relative;

  @media (max-width: 768px) {
    gap: 15px;
  }
`;

const Feature = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
  color: #667eea;
  font-weight: 600;
  background: rgba(102, 126, 234, 0.1);
  padding: 10px 20px;
  border-radius: 25px;
  transition: all 0.3s ease;

  &:hover {
    background: rgba(102, 126, 234, 0.2);
    transform: translateY(-2px);
  }

  svg {
    width: 20px;
    height: 20px;
    color: #667eea;
  }
`;

const Header = ({ connectionStatus = 'connecting' }) => {
  const getStatusText = (status) => {
    switch (status) {
      case 'connected': return 'Connected';
      case 'connecting': return 'Connecting...';
      case 'error': return 'Connection Error';
      default: return 'Unknown';
    }
  };

  return (
    <HeaderContainer
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
    >
      <StatusIndicator status={connectionStatus}>
        {getStatusText(connectionStatus)}
      </StatusIndicator>

      <Logo
        initial={{ scale: 0.8 }}
        animate={{ scale: 1 }}
        transition={{ duration: 0.5, delay: 0.2 }}
      >
        AegisAPI AgentNN
      </Logo>
      <Subtitle
        initial={{ opacity: 0 }}
        animate={{ opacity: 0.8 }}
        transition={{ duration: 0.5, delay: 0.4 }}
      >
        Autonomous API Testing with Agentic AI
      </Subtitle>
      <Features
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.6 }}
      >
        <Feature>
          <Cpu size={20} />
          <span>🧠 Intelligent</span>
        </Feature>
        <Feature>
          <Zap size={20} />
          <span>🔄 Self-Healing</span>
        </Feature>
        <Feature>
          <BarChart3 size={20} />
          <span>📊 Analytics-Driven</span>
        </Feature>
        <Feature>
          <Shield size={20} />
          <span>🛡️ Enterprise-Ready</span>
        </Feature>
      </Features>
    </HeaderContainer>
  );
};

export default Header;
