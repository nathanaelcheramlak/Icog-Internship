import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';
import type { Task } from '../types/task';

interface TaskVisualizationProps {
  tasks: Task[];
}

const TaskVisualization: React.FC<TaskVisualizationProps> = ({ tasks }) => {
  // Prepare data for priority distribution chart
  const priorityData = tasks.reduce((acc, task) => {
    const priority = task.priority;
    const existing = acc.find(item => item.name === priority);
    if (existing) {
      existing.value += 1;
    } else {
      acc.push({ name: priority, value: 1 });
    }
    return acc;
  }, [] as { name: string; value: number }[]);

  // Prepare data for completion status
  const completionData = [
    { name: 'Completed', value: tasks.filter(t => t.completed).length },
    { name: 'Pending', value: tasks.filter(t => !t.completed).length },
  ];

  const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6'];

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 border border-gray-200 rounded-lg shadow-lg">
          <p className="font-medium">{`${label}: ${payload[0].value}`}</p>
        </div>
      );
    }
    return null;
  };

  // Create dependency graph visualization
  const renderDependencyGraph = () => {
    const nodes = tasks.map(task => ({
      id: task.id,
      name: task.name,
      completed: task.completed,
      dependencies: task.dependencies,
    }));

    return (
      <div className="mt-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Task Dependencies</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {nodes.map(node => (
            <div
              key={node.id}
              className={`p-3 rounded-lg border-2 transition-all ${
                node.completed
                  ? 'bg-green-50 border-green-200'
                  : 'bg-white border-gray-200'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <h4 className={`font-medium text-sm ${
                  node.completed ? 'text-green-800' : 'text-gray-900'
                }`}>
                  {node.name.slice(0, -2)}
                </h4>
                <div className={`w-2 h-2 rounded-full ${
                  node.completed ? 'bg-green-500' : 'bg-gray-400'
                }`} />
              </div>
              
              {node.dependencies.length > 0 ? (
                <div className="text-xs text-gray-600">
                  <span className="font-medium">Depends on:</span>
                  <div className="mt-1 space-y-1">
                    {node.dependencies.map(depId => {
                      const depNode = nodes.find(n => n.id === depId);
                      return (
                        <div key={depId} className="flex items-center space-x-2">
                          <div className={`w-2 h-2 rounded-full ${
                            depNode?.completed ? 'bg-green-500' : 'bg-gray-400'
                          }`} />
                          <span className={depNode?.completed ? 'line-through text-gray-400' : ''}>
                            {depNode?.name.slice(0, -2) || `Task ${depId}`}
                          </span>
                        </div>
                      );
                    })}
                  </div>
                </div>
              ) : (
                <div className="text-xs text-gray-600">
                  <span className="font-medium">No dependencies</span>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="space-y-6">
      {/* Charts Section */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Priority Distribution */}
        <div className="bg-gray-50 rounded-lg p-4">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Priority Distribution</h3>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie
                data={priorityData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {priorityData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip content={<CustomTooltip />} />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Completion Status */}
        <div className="bg-gray-50 rounded-lg p-4">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Completion Status</h3>
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie
                data={completionData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                <Cell fill="#10B981" />
                <Cell fill="#3B82F6" />
              </Pie>
              <Tooltip content={<CustomTooltip />} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Dependency Graph */}
      {tasks.length > 0 && renderDependencyGraph()}
    </div>
  );
};

export default TaskVisualization;
