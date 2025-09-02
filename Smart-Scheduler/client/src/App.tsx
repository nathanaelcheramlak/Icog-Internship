import React, { useState, useEffect } from 'react';
import { Plus, Calendar, Clock, Target, CheckCircle, Circle, AlertTriangle } from 'lucide-react';
import TaskForm from './components/TaskForm';
import TaskList from './components/TaskList';
import TaskVisualization from './components/TaskVisualization';
import TaskRecommendations from './components/TaskRecommendations';
import type { Task, TaskFormData } from './types/task';

function App() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [nextId, setNextId] = useState(1);

  const addTask = (taskData: TaskFormData) => {
    const newTask: Task = {
      ...taskData,
      id: nextId,
      completed: false,
      createdAt: new Date(),
    };
    setTasks(prev => [...prev, newTask]);
    setNextId(prev => prev + 1);
    setShowForm(false);
  };

  const toggleTaskCompletion = (taskId: number) => {
    setTasks(prev => prev.map(task => 
      task.id === taskId ? { ...task, completed: !task.completed } : task
    ));
  };

  const deleteTask = (taskId: number) => {
    setTasks(prev => prev.filter(task => task.id !== taskId));
  };

  const getNextRecommendedTask = (): Task | null => {
    const incompleteTasks = tasks.filter(task => !task.completed);
    if (incompleteTasks.length === 0) return null;

    // Simple recommendation logic: prioritize by deadline and priority
    return incompleteTasks.sort((a, b) => {
      const priorityOrder = { 'Critical': 4, 'High': 3, 'Medium': 2, 'Low': 1 };
      const aPriority = priorityOrder[a.priority];
      const bPriority = priorityOrder[b.priority];
      
      if (aPriority !== bPriority) return bPriority - aPriority;
      
      // If same priority, sort by deadline
      return new Date(a.deadline).getTime() - new Date(b.deadline).getTime();
    })[0];
  };

  const completedTasks = tasks.filter(task => task.completed);
  const pendingTasks = tasks.filter(task => !task.completed);
  const recommendedTask = getNextRecommendedTask();

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Smart Task Scheduler
          </h1>
          <p className="text-lg text-gray-600">
            Intelligent task management with dependency tracking and optimization
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="card">
            <div className="flex items-center">
              <div className="p-2 bg-blue-100 rounded-lg">
                <Target className="w-6 h-6 text-blue-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Tasks</p>
                <p className="text-2xl font-bold text-gray-900">{tasks.length}</p>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center">
              <div className="p-2 bg-yellow-100 rounded-lg">
                <Clock className="w-6 h-6 text-yellow-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Pending</p>
                <p className="text-2xl font-bold text-gray-900">{pendingTasks.length}</p>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center">
              <div className="p-2 bg-green-100 rounded-lg">
                <CheckCircle className="w-6 h-6 text-green-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Completed</p>
                <p className="text-2xl font-bold text-gray-900">{completedTasks.length}</p>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center">
              <div className="p-2 bg-purple-100 rounded-lg">
                <Calendar className="w-6 h-6 text-purple-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Due Today</p>
                <p className="text-2xl font-bold text-gray-900">
                  {tasks.filter(task => {
                    const today = new Date().toISOString().split('T')[0];
                    return task.deadline === today && !task.completed;
                  }).length}
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Task List */}
            <div className="card">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-semibold text-gray-900">Task List</h2>
                <button
                  onClick={() => setShowForm(true)}
                  className="btn-primary flex items-center"
                >
                  <Plus className="w-4 h-4 mr-2" />
                  Add Task
                </button>
              </div>
              <TaskList
                tasks={tasks}
                onToggleComplete={toggleTaskCompletion}
                onDelete={deleteTask}
              />
            </div>

            {/* Task Visualization */}
            {tasks.length > 0 && (
              <div className="card">
                <h2 className="text-xl font-semibold text-gray-900 mb-6">Dependency Graph</h2>
                <TaskVisualization tasks={tasks} />
              </div>
            )}
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Recommendations */}
            <div className="card">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">Next Task</h2>
              <TaskRecommendations
                recommendedTask={recommendedTask}
                tasks={tasks}
              />
            </div>

            {/* Quick Actions */}
            <div className="card">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">Quick Actions</h2>
              <div className="space-y-3">
                <button className="w-full btn-secondary text-left">
                  <AlertTriangle className="w-4 h-4 inline mr-2" />
                  View Overdue Tasks
                </button>
                <button className="w-full btn-secondary text-left">
                  <Calendar className="w-4 h-4 inline mr-2" />
                  Today's Schedule
                </button>
                <button className="w-full btn-secondary text-left">
                  <Target className="w-4 h-4 inline mr-2" />
                  Priority Queue
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Task Form Modal */}
        {showForm && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-xl p-6 w-full max-w-md mx-4">
              <TaskForm
                onSubmit={addTask}
                onCancel={() => setShowForm(false)}
                availableTasks={tasks}
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
