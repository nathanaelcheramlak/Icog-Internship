import React, { useState } from 'react';
import { Calendar, Target, Clock, CheckCircle, ArrowRight } from 'lucide-react';
import type { ScheduleResponse, GraphResponse } from '../lib/api';
import type { Task } from '../types/task';

interface ScheduleDisplayProps {
  scheduleData: ScheduleResponse;
  graphData: GraphResponse;
  tasks: Task[]; // Add tasks to get completion status
  onClose: () => void;
}

type PriorityOption = 'deadline' | 'priority';

const ScheduleDisplay: React.FC<ScheduleDisplayProps> = ({ scheduleData, graphData, tasks, onClose }) => {
  const [priorityOption, setPriorityOption] = useState<PriorityOption>('priority');
  const [expandedLayers, setExpandedLayers] = useState<Set<number>>(new Set([0])); // First layer expanded by default

  const nodes = graphData?.graph?.nodes || {};

  // Create a map of task completion status
  const taskCompletionMap = new Map(tasks.map(task => [task.id, task.completed]));

  // Filter out completed tasks from the schedule
  const filteredSchedule = scheduleData.schedule.map(layer => 
    layer.filter(taskId => !taskCompletionMap.get(taskId))
  ).filter(layer => layer.length > 0); // Remove empty layers

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'High': return 'bg-red-100 text-red-800 border-red-300';
      case 'Medium': return 'bg-yellow-100 text-yellow-800 border-yellow-300';
      case 'Low': return 'bg-green-100 text-green-800 border-green-300';
      default: return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  const formatDeadline = (deadline: string) => {
    if (!deadline) return '';
    const year = deadline.slice(0, 4);
    const month = deadline.slice(4, 6);
    const day = deadline.slice(6, 8);
    return `${month}/${day}/${year}`;
  };

  const sortTasksInLayer = (taskIds: number[]) => {
    return taskIds.sort((a, b) => {
      const taskA = nodes[a];
      const taskB = nodes[b];
      
      if (!taskA || !taskB) return 0;
      
      if (priorityOption === 'deadline') {
        return taskA.deadline.localeCompare(taskB.deadline);
      } else {
        const priorityOrder = { 'High': 3, 'Medium': 2, 'Low': 1 };
        const aPriority = priorityOrder[taskA.priority as keyof typeof priorityOrder] || 0;
        const bPriority = priorityOrder[taskB.priority as keyof typeof priorityOrder] || 0;
        return bPriority - aPriority; // Higher priority first
      }
    });
  };

  const toggleLayer = (layerIndex: number) => {
    const newExpanded = new Set(expandedLayers);
    if (newExpanded.has(layerIndex)) {
      newExpanded.delete(layerIndex);
    } else {
      newExpanded.add(layerIndex);
    }
    setExpandedLayers(newExpanded);
  };

  const getLayerStatus = (layerIndex: number) => {
    if (layerIndex === 0) return 'Ready to Start';
    if (layerIndex === filteredSchedule.length - 1) return 'Final Tasks';
    return `Step ${layerIndex + 1}`;
  };

  // Count completed tasks that were in the original schedule
  const completedTasksInSchedule = scheduleData.schedule.flat().filter(taskId => 
    taskCompletionMap.get(taskId)
  ).length;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl max-w-4xl w-full max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Smart Schedule</h2>
            <p className="text-gray-600">Optimized task execution order based on dependencies</p>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Controls */}
        <div className="p-6 bg-gray-50 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <label className="text-sm font-medium text-gray-700">Prioritize by:</label>
              <select
                value={priorityOption}
                onChange={(e) => setPriorityOption(e.target.value as PriorityOption)}
                className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="priority">Priority (High → Low)</option>
                <option value="deadline">Deadline (Earliest → Latest)</option>
              </select>
            </div>
            <div className="text-sm text-gray-600">
              {filteredSchedule.length} execution layers
              {completedTasksInSchedule > 0 && (
                <span className="ml-2 text-green-600">
                  • {completedTasksInSchedule} task{completedTasksInSchedule !== 1 ? 's' : ''} completed
                </span>
              )}
            </div>
          </div>
        </div>

        {/* Completed Tasks Summary */}
        {completedTasksInSchedule > 0 && (
          <div className="p-4 bg-green-50 border-b border-green-200">
            <div className="flex items-center space-x-2">
              <CheckCircle className="w-5 h-5 text-green-600" />
              <span className="text-green-800 font-medium">
                {completedTasksInSchedule} task{completedTasksInSchedule !== 1 ? 's' : ''} already completed
              </span>
              <span className="text-green-600 text-sm">
                (excluded from schedule)
              </span>
            </div>
          </div>
        )}

        {/* Schedule Content */}
        <div className="p-6 overflow-y-auto max-h-[60vh]">
          {filteredSchedule.length === 0 ? (
            <div className="text-center py-12">
              <CheckCircle className="w-12 h-12 text-green-500 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">All tasks completed!</h3>
              <p className="text-gray-500">Great job! All scheduled tasks have been finished.</p>
            </div>
          ) : (
            <div className="space-y-6">
              {filteredSchedule.map((layer, layerIndex) => {
                const sortedTasks = sortTasksInLayer(layer);
                const isExpanded = expandedLayers.has(layerIndex);
                
                return (
                  <div key={layerIndex} className="bg-white border border-gray-200 rounded-lg overflow-hidden">
                    {/* Layer Header */}
                    <div 
                      className="flex items-center justify-between p-4 bg-gradient-to-r from-blue-50 to-indigo-50 cursor-pointer hover:from-blue-100 hover:to-indigo-100 transition-colors"
                      onClick={() => toggleLayer(layerIndex)}
                    >
                      <div className="flex items-center space-x-3">
                        <div className="w-8 h-8 bg-blue-500 text-white rounded-full flex items-center justify-center text-sm font-bold">
                          {layerIndex + 1}
                        </div>
                        <div>
                          <h3 className="font-semibold text-blue-900">{getLayerStatus(layerIndex)}</h3>
                          <p className="text-sm text-blue-700">
                            {layer.length} task{layer.length !== 1 ? 's' : ''} available
                          </p>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span className="text-sm text-blue-600 font-medium">
                          {isExpanded ? 'Collapse' : 'Expand'}
                        </span>
                        <svg 
                          className={`w-5 h-5 text-blue-600 transition-transform ${isExpanded ? 'rotate-180' : ''}`}
                          fill="none" 
                          stroke="currentColor" 
                          viewBox="0 0 24 24"
                        >
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                        </svg>
                      </div>
                    </div>

                    {/* Layer Tasks */}
                    {isExpanded && (
                      <div className="p-4 space-y-3">
                        {sortedTasks.map((taskId, taskIndex) => {
                          const task = nodes[taskId];
                          if (!task) return null;

                          return (
                            <div key={taskId} className="flex items-center space-x-4 p-3 bg-gray-50 rounded-lg border border-gray-200">
                              <div className="flex items-center space-x-3 flex-1">
                                <div className="w-6 h-6 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-xs font-bold">
                                  {taskIndex + 1}
                                </div>
                                <div className="flex-1">
                                  <h4 className="font-medium text-gray-900">{task.name}</h4>
                                  {task.description && (
                                    <p className="text-sm text-gray-600 mt-1">{task.description}</p>
                                  )}
                                </div>
                              </div>
                              
                              <div className="flex items-center space-x-3">
                                <span className={`px-2 py-1 text-xs font-medium rounded-full border ${getPriorityColor(task.priority)}`}>
                                  {task.priority}
                                </span>
                                <div className="flex items-center text-xs text-gray-500">
                                  <Calendar className="w-3 h-3 mr-1" />
                                  {formatDeadline(task.deadline)}
                                </div>
                              </div>
                            </div>
                          );
                        })}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-6 bg-gray-50 border-t border-gray-200">
          <div className="flex items-center justify-between">
            <div className="text-sm text-gray-600">
              Total tasks: {Object.keys(nodes).length} • 
              Dependencies: {graphData?.graph?.edges?.length || 0}
              {completedTasksInSchedule > 0 && (
                <span className="text-green-600">
                  • Completed: {completedTasksInSchedule}
                </span>
              )}
            </div>
            <button
              onClick={onClose}
              className="btn-primary"
            >
              Close Schedule
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ScheduleDisplay;
