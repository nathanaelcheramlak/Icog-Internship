import { useState, useEffect } from 'react';
import { Plus, Calendar, Clock, Target, CheckCircle, RefreshCw, PlayCircle, Network } from 'lucide-react';
import TaskForm from './components/TaskForm';
import TaskList from './components/TaskList';
import TaskVisualization from './components/TaskVisualization';
import TaskRecommendations from './components/TaskRecommendations';
import GraphPage from './pages/GraphPage';
import ScheduleDisplay from './components/ScheduleDisplay';
import type { Task, TaskFormData } from './types/task';
import { fetchTasks as apiFetchTasks, createTask as apiCreateTask, deleteTask as apiDeleteTask, fetchGraph, fetchSchedule, mapBackendToClient } from './lib/api';
import type { GraphResponse, ScheduleResponse } from './lib/api';

function App() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState<'tasks' | 'graph'>('tasks');
  const [scheduleData, setScheduleData] = useState<{ graph: GraphResponse; schedule: ScheduleResponse } | null>(null);
  const [showSchedule, setShowSchedule] = useState(false);

  const loadTasks = async () => {
    try {
      setLoading(true);
      setError(null);
      const resp = await apiFetchTasks();
      const mapped = mapBackendToClient(resp) as unknown as Task[];
      setTasks(mapped);
    } catch (e: any) {
      setError(e.message || 'Failed to load tasks');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Load once on mount only
    loadTasks();
  }, []);

  const addTask = async (taskData: TaskFormData) => {
    try {
      setError(null);
      await apiCreateTask(taskData);
      setShowForm(false);
      await loadTasks();
    } catch (e: any) {
      setError(e.message || 'Failed to create task');
    }
  };

  const toggleTaskCompletion = (taskId: number) => {
    // Backend does not track completion; keep client-side only
    setTasks(prev => prev.map(task => 
      task.id === taskId ? { ...task, completed: !task.completed } : task
    ));
  };

  const deleteTask = async (taskId: number) => {
    try {
      setError(null);
      await apiDeleteTask(taskId);
      await loadTasks();
    } catch (e: any) {
      setError(e.message || 'Failed to delete task');
    }
  };

  const getNextRecommendedTask = (): Task | null => {
    const incompleteTasks = tasks.filter(task => !task.completed);
    if (incompleteTasks.length === 0) return null;

    const priorityOrder = {'High': 3, 'Medium': 2, 'Low': 1 } as const;
    return incompleteTasks.sort((a, b) => {
      const aPriority = priorityOrder[a.priority];
      const bPriority = priorityOrder[b.priority];
      if (aPriority !== bPriority) return bPriority - aPriority;
      return new Date(a.deadline).getTime() - new Date(b.deadline).getTime();
    })[0];
  };

  const completedTasks = tasks.filter(task => task.completed);
  const pendingTasks = tasks.filter(task => !task.completed);
  const recommendedTask = getNextRecommendedTask();

  const handleGenerateSchedule = async () => {
    try {
      setError(null);
      setLoading(true);
      
      // Fetch both graph and schedule data
      const [graphData, scheduleData] = await Promise.all([
        fetchGraph(),
        fetchSchedule()
      ]);
      
      setScheduleData({ graph: graphData, schedule: scheduleData });
      setShowSchedule(true);
    } catch (e: any) {
      setError(e.message || 'Failed to generate schedule');
    } finally {
      setLoading(false);
    }
  };

  // Render Graph Page
  if (currentPage === 'graph') {
    return (
      <GraphPage onBack={() => setCurrentPage('tasks')} />
    );
  }

  // Render Tasks Page
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
          <div className="mt-4 flex items-center justify-center gap-3">
            <button onClick={loadTasks} className="btn-secondary flex items-center">
              <RefreshCw className="w-4 h-4 mr-2" /> Refresh
            </button>
            <button 
              onClick={handleGenerateSchedule} 
              className="btn-primary flex items-center"
              disabled={loading}
            >
              <PlayCircle className={`w-4 h-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
              {loading ? 'Generating...' : 'Generate Schedule'}
            </button>
            <button 
              onClick={() => setCurrentPage('graph')} 
              className="btn-secondary flex items-center"
            >
              <Network className="w-4 h-4 mr-2" /> View Graph
            </button>
          </div>
          {error && (
            <div className="mt-3 text-sm text-red-600">{error}</div>
          )}
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
              {loading ? (
                <div className="text-gray-500">Loading tasks...</div>
              ) : (
                <TaskList
                  tasks={tasks}
                  onToggleComplete={toggleTaskCompletion}
                  onDelete={deleteTask}
                />
              )}
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
                <button 
                  className="w-full btn-secondary text-left" 
                  onClick={handleGenerateSchedule}
                  disabled={loading}
                >
                  <PlayCircle className="w-4 h-4 inline mr-2" />
                  Generate Schedule
                </button>
                <button className="w-full btn-secondary text-left" onClick={loadTasks}>
                  <RefreshCw className="w-4 h-4 inline mr-2" />
                  Refresh From Server
                </button>
                <button 
                  className="w-full btn-secondary text-left" 
                  onClick={() => setCurrentPage('graph')}
                >
                  <Network className="w-4 h-4 inline mr-2" />
                  View Full Graph
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

        {/* Schedule Display Modal */}
        {showSchedule && scheduleData && (
          <ScheduleDisplay
            scheduleData={scheduleData.schedule}
            graphData={scheduleData.graph}
            tasks={tasks}
            onClose={() => setShowSchedule(false)}
          />
        )}
      </div>
    </div>
  );
}

export default App;
