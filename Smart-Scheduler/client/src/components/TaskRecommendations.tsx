import React from 'react';
import { Target, Clock, AlertTriangle, CheckCircle, TrendingUp } from 'lucide-react';
import type { Task } from '../types/task';

interface TaskRecommendationsProps {
  recommendedTask: Task | null;
  tasks: Task[];
}

const TaskRecommendations: React.FC<TaskRecommendationsProps> = ({ recommendedTask, tasks }) => {
  const getPriorityIcon = (priority: string) => {
    switch (priority) {
      case 'Critical': return <AlertTriangle className="w-4 h-4 text-red-500" />;
      case 'High': return <Target className="w-4 h-4 text-orange-500" />;
      case 'Medium': return <Clock className="w-4 h-4 text-yellow-500" />;
      case 'Low': return <CheckCircle className="w-4 h-4 text-green-500" />;
      default: return <Target className="w-4 h-4 text-gray-500" />;
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'Critical': return 'text-red-700 bg-red-100 border-red-200';
      case 'High': return 'text-orange-700 bg-orange-100 border-orange-200';
      case 'Medium': return 'text-yellow-700 bg-yellow-100 border-yellow-200';
      case 'Low': return 'text-green-700 bg-green-100 border-green-200';
      default: return 'text-gray-700 bg-gray-100 border-gray-200';
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const today = new Date();
    const diffTime = date.getTime() - today.getTime();
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays < 0) {
      return `${Math.abs(diffDays)} days overdue`;
    } else if (diffDays === 0) {
      return 'Due today';
    } else if (diffDays === 1) {
      return 'Due tomorrow';
    } else {
      return `Due in ${diffDays} days`;
    }
  };

  const getRecommendationReason = (task: Task) => {
    const reasons = [];
    
    if (task.priority === 'High') {
      reasons.push('High priority');
    }
    
    const today = new Date().toISOString().split('T')[0];
    if (task.deadline <= today) {
      reasons.push('Overdue');
    } else if (task.deadline === today) {
      reasons.push('Due today');
    }
    
    // Check if all dependencies are completed
    const incompleteDependencies = task.dependencies.filter(depId => {
      const depTask = tasks.find(t => t.id === depId);
      return depTask && !depTask.completed;
    });
    
    if (incompleteDependencies.length === 0 && task.dependencies.length > 0) {
      reasons.push('All dependencies completed');
    }
    
    return reasons.join(', ');
  };

  if (!recommendedTask) {
    return (
      <div className="text-center py-8">
        <CheckCircle className="w-12 h-12 text-green-500 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">All tasks completed!</h3>
        <p className="text-gray-500">Great job! You've finished all your tasks.</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Recommended Task */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-lg p-4">
        <div className="flex items-center space-x-2 mb-3">
          <TrendingUp className="w-5 h-5 text-blue-600" />
          <h3 className="font-semibold text-blue-900">Recommended Next Task</h3>
        </div>
        
        <div className="space-y-3">
          <div>
            <h4 className="font-medium text-gray-900 mb-1">{recommendedTask.name.slice(0, -2)}</h4>
            {recommendedTask.description && (
              <p className="text-sm text-gray-600">{recommendedTask.description}</p>
            )}
          </div>
          
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              {getPriorityIcon(recommendedTask.priority)}
              <span className={`px-2 py-1 text-xs font-medium rounded-full border ${
                getPriorityColor(recommendedTask.priority)
              }`}>
                {recommendedTask.priority}
              </span>
            </div>
            
            <div className="text-sm text-gray-600">
              {formatDate(recommendedTask.deadline)}
            </div>
          </div>
          
          <div className="text-xs text-gray-500 bg-white rounded px-2 py-1">
            <strong>Why this task:</strong> {getRecommendationReason(recommendedTask)}
          </div>
        </div>
      </div>

      {/* Quick Stats */}
      <div className="space-y-2">
        <div className="flex justify-between text-sm">
          <span className="text-gray-600">Tasks due today:</span>
          <span className="font-medium">
            {tasks.filter(task => {
              const today = new Date().toISOString().split('T')[0];
              return task.deadline === today && !task.completed;
            }).length}
          </span>
        </div>
        
        <div className="flex justify-between text-sm">
          <span className="text-gray-600">Overdue tasks:</span>
          <span className="font-medium text-red-600">
            {tasks.filter(task => {
              const today = new Date().toISOString().split('T')[0];
              return task.deadline < today && !task.completed;
            }).length}
          </span>
        </div>
        
        <div className="flex justify-between text-sm">
          <span className="text-gray-600">Ready to start:</span>
          <span className="font-medium text-green-600">
            {tasks.filter(task => {
              if (task.completed) return false;
              return task.dependencies.length === 0 || 
                task.dependencies.every(depId => {
                  const depTask = tasks.find(t => t.id === depId);
                  return depTask && depTask.completed;
                });
            }).length}
          </span>
        </div>
      </div>

      {/* Productivity Tips */}
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3">
        <h4 className="font-medium text-yellow-800 mb-2">💡 Productivity Tip</h4>
        <p className="text-sm text-yellow-700">
          Focus on one task at a time and complete high-priority items first. 
          Break down complex tasks into smaller, manageable steps.
        </p>
      </div>
    </div>
  );
};

export default TaskRecommendations;
