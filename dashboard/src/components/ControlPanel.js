import React, { useState } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import {
  FileText,
  Bot,
  Play,
  Wrench,
  BarChart3,
  Loader,
  CheckCircle,
  XCircle
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

const ButtonGrid = styled.div`
  display: grid;
  gap: 10px;
`;

const Button = styled(motion.button)`
  padding: 12px 20px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  position: relative;
  overflow: hidden;

  &:disabled {
    cursor: not-allowed;
    opacity: 0.6;
  }
`;

const PrimaryButton = styled(Button)`
  background: linear-gradient(45deg, #ff6b6b, #e74c3c);
  color: white;

  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(255, 107, 107, 0.3);
  }

  &:active {
    transform: translateY(0);
  }
`;

const SuccessButton = styled(Button)`
  background: linear-gradient(45deg, #4ecdc4, #26a69a);
  color: white;

  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(78, 205, 196, 0.3);
  }
`;

const SecondaryButton = styled(Button)`
  background: #2d3748;
  color: #e2e8f0;
  border: 1px solid #4a5568;

  &:hover:not(:disabled) {
    background: #4a5568;
  }
`;

const Icon = styled.span`
  display: flex;
  align-items: center;
  justify-content: center;
`;

const StatusMessage = styled(motion.div)`
  margin-top: 15px;
  padding: 10px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 500;

  ${props => props.type === 'success' && `
    background: rgba(39, 174, 96, 0.1);
    color: #27ae60;
    border: 1px solid rgba(39, 174, 96, 0.2);
  `}

  ${props => props.type === 'error' && `
    background: rgba(231, 76, 60, 0.1);
    color: #e74c3c;
    border: 1px solid rgba(231, 76, 60, 0.2);
  `}

  ${props => props.type === 'info' && `
    background: rgba(52, 152, 219, 0.1);
    color: #3498db;
    border: 1px solid rgba(52, 152, 219, 0.2);
  `}
`;

const CommandDescription = styled.div`
  font-size: 12px;
  color: #666;
  margin-top: 5px;
  font-weight: normal;
`;

const commands = [
  {
    id: 'plan',
    name: 'Plan Tests',
    icon: FileText,
    description: 'Analyze API spec and create testing strategy',
    color: 'primary'
  },
  {
    id: 'gen',
    name: 'Generate Tests',
    icon: Bot,
    description: 'AI-powered test script generation',
    color: 'primary'
  },
  {
    id: 'run',
    name: 'Run Tests',
    icon: Play,
    description: 'Execute tests against live API',
    color: 'success'
  },
  {
    id: 'heal',
    name: 'Self-Heal',
    icon: Wrench,
    description: 'Detect and fix API drift',
    color: 'secondary'
  },
  {
    id: 'report',
    name: 'Update Dashboard',
    icon: BarChart3,
    description: 'Refresh dashboard with latest data',
    color: 'secondary'
  }
];

const ControlPanel = ({ onCommand }) => {
  const [executing, setExecuting] = useState(null);
  const [message, setMessage] = useState(null);

  const handleCommand = async (commandId) => {
    setExecuting(commandId);
    setMessage({ type: 'info', text: `Executing ${commands.find(c => c.id === commandId)?.name}...` });

    try {
      await onCommand(commandId);
      setMessage({
        type: 'success',
        text: `${commands.find(c => c.id === commandId)?.name} completed successfully!`
      });
    } catch (error) {
      setMessage({
        type: 'error',
        text: `Failed to execute ${commands.find(c => c.id === commandId)?.name}: ${error.message}`
      });
    } finally {
      setExecuting(null);
      // Clear message after 5 seconds
      setTimeout(() => setMessage(null), 5000);
    }
  };

  return (
    <Panel
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.3 }}
    >
      <Header>
        <Title>Quick Actions</Title>
      </Header>

      <ButtonGrid>
        {commands.map((command, index) => {
          const CommandIcon = command.icon;
          const ButtonComponent = command.color === 'primary' ? PrimaryButton :
                                 command.color === 'success' ? SuccessButton : SecondaryButton;
          const isExecuting = executing === command.id;

          return (
            <ButtonComponent
              key={command.id}
              onClick={() => handleCommand(command.id)}
              disabled={isExecuting}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: index * 0.1 }}
            >
              <Icon>
                {isExecuting ? (
                  <Loader size={16} className="animate-spin" />
                ) : (
                  <CommandIcon size={16} />
                )}
              </Icon>
              {command.name}
            </ButtonComponent>
          );
        })}
      </ButtonGrid>

      {message && (
        <StatusMessage
          type={message.type}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -10 }}
        >
          {message.type === 'success' && <CheckCircle size={16} />}
          {message.type === 'error' && <XCircle size={16} />}
          {message.type === 'info' && <Loader size={16} className="animate-spin" />}
          <div>
            <div>{message.text}</div>
            <CommandDescription>
              {message.type === 'success' && 'Command completed and results are being processed.'}
              {message.type === 'error' && 'Please check the console for detailed error information.'}
              {message.type === 'info' && 'This may take a few moments...'}
            </CommandDescription>
          </div>
        </StatusMessage>
      )}
    </Panel>
  );
};

export default ControlPanel;
