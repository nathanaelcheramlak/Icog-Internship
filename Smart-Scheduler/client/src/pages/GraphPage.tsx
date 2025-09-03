import { useState, useEffect } from 'react';
import { ArrowLeft, RefreshCw, PlayCircle, Target } from 'lucide-react';
import DependencyGraph from '../components/DependencyGraph';
import { fetchGraph } from '../lib/api';
import type { GraphResponse } from '../lib/api';

interface GraphPageProps {
  onBack: () => void;
}

const GraphPage: React.FC<GraphPageProps> = ({ onBack }) => {
  const [graphData, setGraphData] = useState<GraphResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadGraph = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await fetchGraph();
      setGraphData(data);
    } catch (e: any) {
      setError(e.message || 'Failed to load graph data');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadGraph();
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center space-x-4">
            <button
              onClick={onBack}
              className="btn-secondary flex items-center"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back to Tasks
            </button>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                Dependency Graph
              </h1>
              <p className="text-gray-600">
                Visual representation of task dependencies and execution order
              </p>
            </div>
          </div>
          
          <div className="flex items-center space-x-3">
            <button
              onClick={loadGraph}
              className="btn-secondary flex items-center"
              disabled={loading}
            >
              <RefreshCw className={`w-4 h-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </button>
            <button
              onClick={loadGraph}
              className="btn-primary flex items-center"
              disabled={loading}
            >
              <PlayCircle className="w-4 h-4 mr-2" />
              Generate Graph
            </button>
          </div>
        </div>

        {/* Error Display */}
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4">
            <div className="flex items-center">
              <Target className="w-5 h-5 text-red-500 mr-2" />
              <span className="text-red-700">{error}</span>
            </div>
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <div className="text-center py-12">
            <RefreshCw className="w-8 h-8 text-blue-600 animate-spin mx-auto mb-4" />
            <p className="text-gray-600">Generating dependency graph...</p>
          </div>
        )}

        {/* Graph Content */}
        {!loading && graphData && (
          <DependencyGraph graphData={graphData} />
        )}

        {/* Empty State */}
        {!loading && !graphData && !error && (
          <div className="text-center py-12">
            <Target className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No graph data available</h3>
            <p className="text-gray-500 mb-4">
              Generate a dependency graph to visualize your task relationships
            </p>
            <button
              onClick={loadGraph}
              className="btn-primary flex items-center mx-auto"
            >
              <PlayCircle className="w-4 h-4 mr-2" />
              Generate Graph
            </button>
          </div>
        )}

        {/* Help Section */}
        <div className="mt-8 bg-white rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">How to Read the Graph</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-medium text-gray-900 mb-2">Nodes</h4>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Each box represents a task</li>
                <li>• Color-coded by priority (High=Red, Medium=Yellow, Low=Green)</li>
                <li>• Shows task name, description, and deadline</li>
                <li>• Step numbers show execution order</li>
              </ul>
            </div>
            <div>
              <h4 className="font-medium text-gray-900 mb-2">Edges</h4>
              <ul className="text-sm text-gray-600 space-y-1">
                <li>• Curved arrows show dependencies between tasks</li>
                <li>• Point from prerequisite to dependent task</li>
                <li>• Execution order follows arrow direction</li>
                <li>• Tasks with no incoming arrows can start immediately</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GraphPage;
