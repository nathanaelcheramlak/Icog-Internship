import React from 'react';
import { CheckCircle, Circle, Trash2, Calendar, AlertTriangle, Clock } from 'lucide-react';
import type { Task } from '../types/task';

interface TaskListProps {
  tasks: Task[];
  onToggleComplete: (taskId: number) => void;
  onDelete: (taskId: number) => void;
}

const TaskList: React.FC<TaskListProps> = ({ tasks, onToggleComplete, onDelete }) => {
  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'High': return 'bg-orange-100 text-orange-800 border-orange-200';
      case 'Medium': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'Low': return 'bg-green-100 text-green-800 border-green-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const isOverdue = (deadline: string) => {
    const today = new Date().toISOString().split('T')[0];
    return deadline < today;
  };

  const isDueToday = (deadline: string) => {
    const today = new Date().toISOString().split('T')[0];
    return deadline === today;
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  };

  if (tasks.length === 0) {
    return (
      <div className="text-center py-12">
        <Circle className="w-12 h-12 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">No tasks yet</h3>
        <p className="text-gray-500">Create your first task to get started!</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {tasks.map(task => (
        <div
          key={task.id}
          className={`p-4 rounded-lg border transition-all duration-200 ${
            task.completed
              ? 'bg-gray-50 border-gray-200 opacity-75'
              : 'bg-white border-gray-200 hover:border-gray-300 hover:shadow-sm'
          }`}
        >
          <div className="flex items-start space-x-3">
            {/* Checkbox */}
            <button
              onClick={() => onToggleComplete(task.id)}
              className={`mt-1 p-1 rounded-full transition-colors ${
                task.completed
                  ? 'text-green-600 hover:text-green-700'
                  : 'text-gray-400 hover:text-gray-600'
              }`}
            >
              {task.completed ? (
                <CheckCircle className="w-5 h-5" />
              ) : (
                <Circle className="w-5 h-5" />
              )}
            </button>

            {/* Task Content */}
            <div className="flex-1 min-w-0">
              <div className="flex items-start justify-between">
                <div className="flex-1 min-w-0">
                  <h3 className={`text-sm font-medium ${
                    task.completed ? 'text-gray-500 line-through' : 'text-gray-900'
                  }`}>
                    {task.name}
                  </h3>
                  {task.description && (
                    <p className={`text-sm mt-1 ${
                      task.completed ? 'text-gray-400' : 'text-gray-600'
                    }`}>
                      {task.description}
                    </p>
                  )}
                </div>

                {/* Priority Badge */}
                <span className={`ml-2 px-2 py-1 text-xs font-medium rounded-full border ${
                  getPriorityColor(task.priority)
                }`}>
                  {task.priority}
                </span>
              </div>

              {/* Task Meta */}
              <div className="flex items-center space-x-4 mt-3">
                {/* Deadline */}
                <div className="flex items-center space-x-1">
                  <Calendar className="w-4 h-4 text-gray-400" />
                  <span className={`text-xs ${
                    task.completed ? 'text-gray-400' : 'text-gray-600'
                  }`}>
                    {formatDate(task.deadline)}
                  </span>
                  {!task.completed && isOverdue(task.deadline) && (
                    <AlertTriangle className="w-4 h-4 text-red-500" />
                  )}
                  {!task.completed && isDueToday(task.deadline) && (
                    <Clock className="w-4 h-4 text-yellow-500" />
                  )}
                </div>

                {/* Dependencies */}
                {task.dependencies.length > 0 && (
                  <div className="flex items-center space-x-1">
                    <span className="text-xs text-gray-500">Depends on:</span>
                    <div className="flex space-x-1">
                      {task.dependencies.map(depId => {
                        const depTask = tasks.find(t => t.id === depId);
                        return (
                          <span
                            key={depId}
                            className={`w-2 h-2 rounded-full ${
                              depTask?.completed ? 'bg-green-400' : 'bg-gray-300'
                            }`}
                            title={depTask?.name.slice(0, -2) || `Task ${depId}`}
                          />
                        );
                      })}
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Delete Button */}
            <button
              onClick={() => onDelete(task.id)}
              className="text-gray-400 hover:text-red-500 transition-colors p-1"
              title="Delete task"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          </div>
        </div>
      ))}
    </div>
  );
};

export default TaskList;
