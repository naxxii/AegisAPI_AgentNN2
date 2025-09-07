import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';
import {
  FileText,
  Bot,
  Play,
  Wrench,
  BarChart3,
  Clock,
  CheckCircle,
  XCircle,
  AlertCircle
} from 'lucide-react';

const FeedContainer = styled(motion.div)`
  max-height: 400px;
  overflow-y: auto;
  margin-top: 20px;

  &::-webkit-scrollbar {
    width: 6px;
  }

  &::-webkit-scrollbar-track {
    background: #2d3748;
    border-radius: 3px;
  }

  &::-webkit-scrollbar-thumb {
    background: #4ecdc4;
    border-radius: 3px;
  }
`;

const Header = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  border-bottom: 2px solid #4a5568;
  padding-bottom: 15px;
`;

const Title = styled.h2`
  font-size: 1.5em;
  font-weight: bold;
  color: #e2e8f0;
  margin: 0;
`;

const StatusIndicator = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
  color: #27ae60;
  font-weight: 500;
`;

const Pulse = styled.div`
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #27ae60;
  animation: pulse 2s infinite;
`;

const ActivityItem = styled(motion.div)`
  display: flex;
  align-items: center;
  padding: 15px;
  border-bottom: 1px solid #f0f0f0;
  transition: background-color 0.2s ease;
  cursor: pointer;

  &:hover {
    background: #f8f9fa;
  }

  &:last-child {
    border-bottom: none;
  }
`;

const ActivityIcon = styled.div`
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
  font-size: 18px;
  color: white;
  background: ${props => props.bgColor || '#3498db'};
  flex-shrink: 0;
`;

const ActivityContent = styled.div`
  flex: 1;
  min-width: 0;
`;

const ActivityTitle = styled.div`
  font-weight: 600;
  margin-bottom: 5px;
  color: #333;
  word-break: break-word;
`;

const ActivityDescription = styled.div`
  color: #666;
  margin-bottom: 5px;
  font-size: 0.9em;
  word-break: break-word;
`;

const ActivityTime = styled.div`
  font-size: 12px;
  color: #999;
  display: flex;
  align-items: center;
  gap: 5px;
`;

const EmptyState = styled.div`
  text-align: center;
  padding: 40px 20px;
  color: #a0aec0;
`;

const EmptyIcon = styled.div`
  font-size: 3em;
  margin-bottom: 15px;
  opacity: 0.5;
`;

const FilterTabs = styled.div`
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  flex-wrap: wrap;
`;

const FilterTab = styled.button`
  padding: 8px 16px;
  border: 1px solid ${props => props.active ? '#3498db' : '#ddd'};
  background: ${props => props.active ? '#3498db' : 'white'};
  color: ${props => props.active ? 'white' : '#333'};
  border-radius: 20px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s ease;

  &:hover {
    border-color: #3498db;
    background: ${props => props.active ? '#3498db' : '#f8f9fa'};
  }
`;

const getEventIcon = (eventType) => {
  if (eventType.includes('plan')) return FileText;
  if (eventType.includes('test_generated')) return Bot;
  if (eventType.includes('run')) return Play;
  if (eventType.includes('heal')) return Wrench;
  if (eventType.includes('report')) return BarChart3;
  return FileText;
};

const getEventColor = (eventType) => {
  if (eventType.includes('plan')) return '#3498db';
  if (eventType.includes('test_generated')) return '#9b59b6';
  if (eventType.includes('run')) return '#2ecc71';
  if (eventType.includes('heal')) return '#e74c3c';
  if (eventType.includes('report')) return '#f39c12';
  return '#95a5a6';
};

const getEventTitle = (eventType) => {
  return eventType.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
};

const formatTimestamp = (timestamp) => {
  if (!timestamp) return 'Unknown time';

  const date = new Date(timestamp * 1000);
  const now = new Date();
  const diff = now - date;
  const minutes = Math.floor(diff / 60000);
  const hours = Math.floor(diff / 3600000);
  const days = Math.floor(diff / 86400000);

  if (days > 0) return `${days} day${days > 1 ? 's' : ''} ago`;
  if (hours > 0) return `${hours} hour${hours > 1 ? 's' : ''} ago`;
  if (minutes > 0) return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
  return 'Just now';
};

const ActivityFeed = ({ events = [] }) => {
  const [filter, setFilter] = useState('all');
  const [filteredEvents, setFilteredEvents] = useState(events);

  useEffect(() => {
    if (filter === 'all') {
      setFilteredEvents(events);
    } else {
      setFilteredEvents(events.filter(event =>
        event.type && event.type.includes(filter)
      ));
    }
  }, [events, filter]);

  const eventTypes = ['all', ...new Set(events.map(e => e.type?.split('_')[0]).filter(Boolean))];

  return (
    <>
      <Header>
        <Title>Recent Activity</Title>
        <StatusIndicator>
          <Pulse />
          <span>Live</span>
        </StatusIndicator>
      </Header>

      <FilterTabs>
        {eventTypes.map(type => (
          <FilterTab
            key={type}
            active={filter === type}
            onClick={() => setFilter(type)}
          >
            {type === 'all' ? 'All Events' : getEventTitle(type)}
          </FilterTab>
        ))}
      </FilterTabs>

      <FeedContainer>
        <AnimatePresence>
          {filteredEvents.length > 0 ? (
            filteredEvents.slice(0, 20).map((event, index) => {
              const Icon = getEventIcon(event.type || '');
              const bgColor = getEventColor(event.type || '');

              return (
                <ActivityItem
                  key={`${event.type}-${event.ts}-${index}`}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: 20 }}
                  transition={{ duration: 0.3, delay: index * 0.05 }}
                >
                  <ActivityIcon bgColor={bgColor}>
                    <Icon size={20} />
                  </ActivityIcon>
                  <ActivityContent>
                    <ActivityTitle>
                      {getEventTitle(event.type || 'Unknown Event')}
                    </ActivityTitle>
                    <ActivityDescription>
                      {event.summary || 'No description available'}
                    </ActivityDescription>
                    <ActivityTime>
                      <Clock size={12} />
                      {formatTimestamp(event.ts)}
                    </ActivityTime>
                  </ActivityContent>
                </ActivityItem>
              );
            })
          ) : (
            <EmptyState>
              <EmptyIcon>📋</EmptyIcon>
              <div>No recent activity</div>
              <div style={{ fontSize: '0.9em', marginTop: '5px' }}>
                Events will appear here as the system runs tests and healing operations.
              </div>
            </EmptyState>
          )}
        </AnimatePresence>
      </FeedContainer>
    </>
  );
};

export default ActivityFeed;
