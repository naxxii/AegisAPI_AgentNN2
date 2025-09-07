import React, { useState, useEffect } from 'react';
import styled, { createGlobalStyle } from 'styled-components';
import { motion } from 'framer-motion';
import Header from './components/Header';
import StatsGrid from './components/StatsGrid';
import ActivityFeed from './components/ActivityFeed';
import SystemHealth from './components/SystemHealth';
import ControlPanel from './components/ControlPanel';
import { AegisAPI } from './services/api';

const GlobalStyle = createGlobalStyle`
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #667eea 100%);
    background-size: 400% 400%;
    animation: gradientShift 15s ease infinite;
    min-height: 100vh;
    color: #333;
    position: relative;
    overflow-x: hidden;
  }

  body::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image:
      radial-gradient(circle at 25% 25%, rgba(102, 126, 234, 0.1) 0%, transparent 50%),
      radial-gradient(circle at 75% 75%, rgba(118, 75, 162, 0.1) 0%, transparent 50%),
      radial-gradient(circle at 50% 50%, rgba(39, 174, 96, 0.05) 0%, transparent 50%);
    animation: particleFloat 20s ease-in-out infinite;
    pointer-events: none;
    z-index: -1;
  }

  @keyframes gradientShift {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
  }

  @keyframes particleFloat {
    0%, 100% {
      transform: translateY(0px) rotate(0deg);
      opacity: 0.1;
    }
    33% {
      transform: translateY(-20px) rotate(120deg);
      opacity: 0.2;
    }
    66% {
      transform: translateY(10px) rotate(240deg);
      opacity: 0.15;
    }
  }
`;

const Container = styled.div`
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
`;

const Grid = styled.div`
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 30px;
  margin-bottom: 30px;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

const MainPanel = styled(motion.div)`
  background: rgba(255, 255, 255, 0.95);
  border-radius: 15px;
  padding: 25px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #667eea, #764ba2, #f093fb, #f5576c);
    opacity: 0;
    transition: opacity 0.3s ease;
  }

  &:hover::before {
    opacity: 1;
  }

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 40px rgba(102, 126, 234, 0.2);
  }
`;

const SidePanel = styled.div`
  display: flex;
  flex-direction: column;
  gap: 20px;
`;

function App() {
  const [stats, setStats] = useState({
    api_count: 0,
    total_runs: 0,
    successful_runs: 0,
    failed_runs: 0,
    healing_count: 0,
    applied_healings: 0,
    recent_events: [],
    system_status: 'Connecting...',
    test_coverage: 0,
    api_health: 0,
    healing_confidence: 0,
    test_success_rate: 'Loading...'
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [connectionStatus, setConnectionStatus] = useState('connecting');

  useEffect(() => {
    loadDashboardData();

    // Set up real-time updates
    const interval = setInterval(loadDashboardData, 10000);
    return () => clearInterval(interval);
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      setConnectionStatus('connecting');
      setError(null);

      const response = await AegisAPI.getStatus();

      if (response.data && !response.data.error) {
        // Map API response to React app format
        const apiData = response.data;
        const mappedStats = {
          api_count: apiData.plans_created || 0,
          total_runs: apiData.test_executions || 0,
          successful_runs: apiData.test_executions || 0, // Simplified mapping
          failed_runs: 0, // We don't track this separately in current API
          healing_count: apiData.heals_applied || 0,
          applied_healings: apiData.heals_applied || 0,
          recent_events: apiData.recent_events || [],
          // Add additional fields from API
          system_status: apiData.system_status || 'Online',
          test_coverage: apiData.test_coverage || 0,
          api_health: apiData.api_health || 0,
          healing_confidence: apiData.healing_confidence || 0,
          test_success_rate: apiData.test_success_rate || 'No tests yet'
        };
        setStats(mappedStats);
        setConnectionStatus('connected');
      } else {
        throw new Error(response.data?.error || 'Invalid API response');
      }
    } catch (err) {
      console.error('Dashboard error:', err);
      setConnectionStatus('error');
      setError(`Connection failed: ${err.message}`);
      // Set default values on error
      setStats(prevStats => ({
        ...prevStats,
        system_status: 'Offline',
        test_success_rate: 'Connection Error'
      }));
    } finally {
      setLoading(false);
    }
  };

  const handleCommand = async (action) => {
    try {
      await AegisAPI.executeCommand(action);
      // Refresh data after command execution
      setTimeout(loadDashboardData, 2000);
    } catch (err) {
      console.error(`Failed to execute ${action}:`, err);
    }
  };

  return (
    <>
      <GlobalStyle />
      <Container>
        <Header connectionStatus={connectionStatus} />
        <StatsGrid stats={stats} loading={loading} />

        <Grid>
          <MainPanel
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <ActivityFeed events={stats.recent_events || []} />
          </MainPanel>

          <SidePanel>
            <ControlPanel onCommand={handleCommand} />
            <SystemHealth stats={stats} />
          </SidePanel>
        </Grid>
      </Container>
    </>
  );
}

export default App;
