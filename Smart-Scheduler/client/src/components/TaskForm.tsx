import React, { useState } from 'react';
import { X, Calendar, AlertCircle } from 'lucide-react';
import type { TaskFormData, Task } from '../types/task';

interface TaskFormProps {
  onSubmit: (taskData: TaskFormData) => void;
  onCancel: () => void;
  availableTasks: Task[];
}

const TaskForm: React.FC<TaskFormProps> = ({ onSubmit, onCancel, availableTasks }) => {
  const [formData, setFormData] = useState<TaskFormData>({
    name: '',
    description: '',
    priority: 'Medium',
    deadline: '',
    dependencies: [],
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (formData.name.trim() && formData.deadline) {
      onSubmit(formData);
    }
  };

  const handleDependencyChange = (taskId: number, checked: boolean) => {
    if (checked) {
      setFormData(prev => ({
        ...prev,
        dependencies: [...prev.dependencies, taskId],
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        dependencies: prev.dependencies.filter(id => id !== taskId),
      }));
    }
  };

  return (
    <div className="relative">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-semibold text-gray-900">Add New Task</h2>
        <button
          onClick={onCancel}
          className="text-gray-400 hover:text-gray-600 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Task Name */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Task Name *
          </label>
          <input
            type="text"
            value={formData.name}
            onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
            className="input-field"
            placeholder="Enter task name"
            required
          />
        </div>

        {/* Description */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Description
          </label>
          <textarea
            value={formData.description}
            onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
            className="input-field resize-none"
            rows={3}
            placeholder="Enter task description"
          />
        </div>

        {/* Priority */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Priority
          </label>
          <select
            value={formData.priority}
            onChange={(e) => setFormData(prev => ({ ...prev, priority: e.target.value as any }))}
            className="input-field"
          >
            <option value="Low">Low</option>
            <option value="Medium">Medium</option>
            <option value="High">High</option>
            <option value="Critical">Critical</option>
          </select>
        </div>

        {/* Deadline */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Deadline *
          </label>
          <div className="relative">
            <input
              type="date"
              value={formData.deadline}
              onChange={(e) => setFormData(prev => ({ ...prev, deadline: e.target.value }))}
              className="input-field"
              required
            />
            <Calendar className="absolute right-3 top-2.5 w-5 h-5 text-gray-400" />
          </div>
        </div>

        {/* Dependencies */}
        {availableTasks.length > 0 && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Dependencies
            </label>
            <div className="max-h-32 overflow-y-auto border border-gray-300 rounded-lg p-3">
              {availableTasks.map(task => (
                <label key={task.id} className="flex items-center space-x-2 py-1">
                  <input
                    type="checkbox"
                    checked={formData.dependencies.includes(task.id)}
                    onChange={(e) => handleDependencyChange(task.id, e.target.checked)}
                    className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
                  />
                  <span className="text-sm text-gray-700">{task.name}</span>
                </label>
              ))}
            </div>
          </div>
        )}

        {/* Submit Buttons */}
        <div className="flex space-x-3 pt-4">
          <button
            type="submit"
            className="btn-primary flex-1"
          >
            Create Task
          </button>
          <button
            type="button"
            onClick={onCancel}
            className="btn-secondary flex-1"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
};

export default TaskForm;
