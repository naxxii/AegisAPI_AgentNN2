import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import {
  Target,
  Bot,
  PlayCircle,
  Wrench,
  TrendingUp,
  TrendingDown,
  Minus
} from 'lucide-react';

const Grid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
`;

const StatCard = styled(motion.div)`
  background: rgba(30, 30, 30, 0.95);
  border-radius: 15px;
  padding: 25px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: transform 0.3s ease;
  position: relative;
  overflow: hidden;

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
  }

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, ${props => props.color || '#ff6b6b'}, ${props => props.color2 || '#4ecdc4'});
  }
`;

const StatIcon = styled.div`
  font-size: 2em;
  margin-bottom: 15px;
  color: ${props => props.color || '#3498db'};
`;

const StatNumber = styled.div`
  font-size: 2.5em;
  font-weight: bold;
  color: #e2e8f0;
  margin-bottom: 5px;
  display: flex;
  align-items: center;
  gap: 10px;
`;

const StatLabel = styled.div`
  font-size: 0.9em;
  color: #a0aec0;
  text-transform: uppercase;
  letter-spacing: 1px;
`;

const Trend = styled.div`
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 0.8em;
  margin-top: 5px;

  svg {
    width: 14px;
    height: 14px;
  }
`;

const LoadingSpinner = styled.div`
  width: 20px;
  height: 20px;
  border: 2px solid #f3f3f3;
  border-top: 2px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
`;

const StatsGrid = ({ stats, loading }) => {
  const statCards = [
    {
      icon: Target,
      iconColor: '#ff6b6b',
      gradient: ['#ff6b6b', '#e74c3c'],
      label: 'Test Plans Created',
      value: stats.plans_created || 0,
      key: 'plans'
    },
    {
      icon: Bot,
      iconColor: '#4ecdc4',
      gradient: ['#4ecdc4', '#26a69a'],
      label: 'Tests Generated',
      value: stats.tests_generated || 0,
      key: 'tests'
    },
    {
      icon: PlayCircle,
      iconColor: '#45b7d1',
      gradient: ['#45b7d1', '#2196f3'],
      label: 'Test Executions',
      value: stats.test_executions || 0,
      key: 'runs'
    },
    {
      icon: Wrench,
      iconColor: '#96ceb4',
      gradient: ['#96ceb4', '#4caf50'],
      label: 'Self-Heals Applied',
      value: stats.applied_healings || 0,
      key: 'heals'
    }
  ];

  return (
    <Grid>
      {statCards.map((card, index) => {
        const Icon = card.icon;
        const previousValue = localStorage.getItem(`prev_${card.key}`) || card.value;
        const trend = card.value > previousValue ? 'up' : card.value < previousValue ? 'down' : 'same';

        // Store current value for next comparison
        localStorage.setItem(`prev_${card.key}`, card.value);

        return (
          <StatCard
            key={card.key}
            color={card.gradient[0]}
            color2={card.gradient[1]}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
          >
            <StatIcon color={card.iconColor}>
              <Icon size={40} />
            </StatIcon>
            <StatNumber>
              {loading ? <LoadingSpinner /> : card.value.toLocaleString()}
            </StatNumber>
            <StatLabel>{card.label}</StatLabel>
            {!loading && trend !== 'same' && (
              <Trend style={{
                color: trend === 'up' ? '#27ae60' : '#e74c3c'
              }}>
                {trend === 'up' ? <TrendingUp /> : <TrendingDown />}
                {Math.abs(card.value - previousValue)} from last update
              </Trend>
            )}
          </StatCard>
        );
      })}
    </Grid>
  );
};

export default StatsGrid;
