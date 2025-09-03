import React, { useMemo } from "react";
import { ArrowRight, Calendar, Target } from "lucide-react";
import { fetchGraph } from "../lib/api";
import type { GraphResponse } from "../lib/api";

interface DependencyGraphProps {
  graphData: GraphResponse;
}

const DependencyGraph: React.FC<DependencyGraphProps> = ({ graphData }) => {
  // Add null checks and fallbacks
  const graph = graphData?.graph;
  const nodes = graph?.nodes || {};
  const edges = graph?.edges || [];
  const sorted = graph?.sorted || '';

  // Parse the sorted string to get topological order
  const topologicalOrder = useMemo(() => {
    // Parse "((1) (2) (3))" format
    const match = sorted.match(/\(\((.*?)\)\)/);
    if (!match) return [];
    
    const inner = match[1];
    const taskIds = inner.match(/\((\d+)\)/g)?.map(id => parseInt(id.replace(/[()]/g, ''))) || [];
    return taskIds;
  }, [sorted]);

  // Calculate node positions based on execution order
  const nodeArray = useMemo(() => {
    const nodePositions: { [key: number]: { x: number; y: number } } = {};
    const nodeWidth = 250;
    const nodeHeight = 120;
    const horizontalSpacing = 300;
    const verticalSpacing = 200;

    // Position nodes based on topological order
    topologicalOrder.forEach((taskId, index) => {
      const row = Math.floor(index / 3); // 3 nodes per row
      const col = index % 3;
      
      nodePositions[taskId] = {
        x: col * horizontalSpacing + 100,
        y: row * verticalSpacing + 100,
      };
    });

    // Add any nodes that aren't in the topological order
    Object.keys(nodes).forEach((nodeId) => {
      const id = parseInt(nodeId);
      if (!nodePositions[id]) {
        const index = Object.keys(nodePositions).length;
        const row = Math.floor(index / 3);
        const col = index % 3;
        nodePositions[id] = {
          x: col * horizontalSpacing + 100,
          y: row * verticalSpacing + 100,
        };
      }
    });

    return Object.values(nodes).map((node) => ({
      ...node,
      ...nodePositions[node.id],
    }));
  }, [nodes, topologicalOrder]);

  // Get priority color
  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'High': return 'bg-red-100 text-red-800 border-red-300';
      case 'Medium': return 'bg-yellow-100 text-yellow-800 border-yellow-300';
      case 'Low': return 'bg-green-100 text-green-800 border-green-300';
      default: return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  // Get priority border color
  const getPriorityBorderColor = (priority: string) => {
    switch (priority) {
      case 'High': return 'border-red-400';
      case 'Medium': return 'border-yellow-400';
      case 'Low': return 'border-green-400';
      default: return 'border-gray-400';
    }
  };

  // Format deadline
  const formatDeadline = (deadline: string) => {
    if (!deadline) return '';
    const year = deadline.slice(0, 4);
    const month = deadline.slice(4, 6);
    const day = deadline.slice(6, 8);
    return `${month}/${day}/${year}`;
  };

  // Calculate edge positions with curved paths
  const edgePaths = useMemo(() => {
    return edges.map(edge => {
      const sourceNode = nodeArray.find(n => n.id === edge.source);
      const targetNode = nodeArray.find(n => n.id === edge.target);
      
      if (!sourceNode || !targetNode) return null;
      
      // Calculate control points for curved edges
      const startX = sourceNode.x + 250; // Right edge of source node
      const startY = sourceNode.y + 60;   // Middle of source node
      const endX = targetNode.x;         // Left edge of target node
      const endY = targetNode.y + 60;    // Middle of target node
      
      // Control points for smooth curve
      const controlX1 = startX + (endX - startX) * 0.3;
      const controlY1 = startY;
      const controlX2 = startX + (endX - startX) * 0.7;
      const controlY2 = endY;
      
      return {
        path: `M ${startX} ${startY} C ${controlX1} ${controlY1} ${controlX2} ${controlY2} ${endX} ${endY}`,
        id: `${edge.source}-${edge.target}`,
        source: { x: startX, y: startY },
        target: { x: endX, y: endY },
      };
    }).filter(Boolean);
  }, [edges, nodeArray]);

  if (!nodes || Object.keys(nodes).length === 0) {
    return (
      <div className="text-center py-12">
        <Target className="w-12 h-12 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">No tasks to visualize</h3>
        <p className="text-gray-500">Add some tasks with dependencies to see the graph</p>
      </div>
    );
  }

  // Calculate canvas size based on node positions
  const maxX = Math.max(...nodeArray.map(n => n.x)) + 300;
  const maxY = Math.max(...nodeArray.map(n => n.y)) + 200;

  return (
    <div className="space-y-6">
      {/* Graph Container */}
      <div className="relative bg-white rounded-lg border border-gray-200 p-6 overflow-auto">
        <div 
          className="relative min-w-full" 
          style={{ 
            height: `${maxY}px`,
            width: `${maxX}px`,
            minWidth: `${maxX}px`
          }}
        >
          {/* Edges */}
          <svg 
            className="absolute inset-0 w-full h-full pointer-events-none"
            style={{ width: `${maxX}px`, height: `${maxY}px` }}
          >
            <defs>
              <marker
                id="arrowhead"
                markerWidth="12"
                markerHeight="8"
                refX="10"
                refY="4"
                orient="auto"
              >
                <polygon
                  points="0 0, 12 4, 0 8"
                  fill="#4B5563"
                  stroke="#4B5563"
                  strokeWidth="1"
                />
              </marker>
            </defs>
            
            {edgePaths.map((edge) => (
              <g key={edge?.id}>
                <path
                  d={edge?.path}
                  stroke="#4B5563"
                  strokeWidth="3"
                  fill="none"
                  markerEnd="url(#arrowhead)"
                  className="transition-all duration-300 hover:stroke-blue-600"
                />
              </g>
            ))}
          </svg>

          {/* Nodes */}
          <div className="relative z-10">
            {nodeArray.map((node, index) => (
              <div
                key={node.id}
                className={`absolute bg-white border-3 rounded-xl p-5 shadow-lg hover:shadow-xl transition-all duration-300 ${getPriorityBorderColor(node.priority)}`}
                style={{
                  left: `${node.x}px`,
                  top: `${node.y}px`,
                  width: '250px',
                  height: '120px',
                }}
              >
                <div className="flex items-start justify-between mb-3">
                  <h3 className="font-bold text-gray-900 text-sm truncate flex-1 mr-2">
                    {node.name}
                  </h3>
                  <span className={`px-3 py-1 text-xs font-bold rounded-full border-2 ${getPriorityColor(node.priority)}`}>
                    {node.priority}
                  </span>
                </div>
                
                {node.description && (
                  <p className="text-xs text-gray-600 mb-3 line-clamp-2">
                    {node.description}
                  </p>
                )}
                
                <div className="flex items-center justify-between">
                  <div className="flex items-center text-xs text-gray-500">
                    <Calendar className="w-3 h-3 mr-1" />
                    {formatDeadline(node.deadline)}
                  </div>
                  
                  <div className="flex items-center">
                    <div className="w-6 h-6 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-xs font-bold">
                      {topologicalOrder.indexOf(node.id) + 1}
                    </div>
                    <span className="ml-1 text-xs text-gray-400">Step</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Topological Order */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-lg p-6">
        <h3 className="font-bold text-blue-900 mb-4 text-lg">Execution Order</h3>
        <div className="flex items-center space-x-4 flex-wrap">
          {topologicalOrder.map((taskId, index) => (
            <React.Fragment key={taskId}>
              <div className="flex items-center bg-white rounded-lg px-4 py-3 shadow-sm border border-blue-200">
                <div className="w-8 h-8 bg-blue-500 text-white rounded-full flex items-center justify-center text-sm font-bold mr-3">
                  {index + 1}
                </div>
                <div>
                  <span className="text-sm font-semibold text-gray-900">
                    {nodes[taskId]?.name || `Task ${taskId}`}
                  </span>
                  <div className="text-xs text-gray-500">
                    {nodes[taskId]?.priority} Priority
                  </div>
                </div>
              </div>
              {index < topologicalOrder.length - 1 && (
                <ArrowRight className="w-6 h-6 text-blue-400" />
              )}
            </React.Fragment>
          ))}
        </div>
      </div>

      {/* Graph Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg p-6 border border-blue-200">
          <h4 className="text-sm font-bold text-blue-900 mb-2">Total Tasks</h4>
          <p className="text-3xl font-bold text-blue-600">{Object.keys(nodes).length}</p>
        </div>
        <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-lg p-6 border border-green-200">
          <h4 className="text-sm font-bold text-green-900 mb-2">Dependencies</h4>
          <p className="text-3xl font-bold text-green-600">{edges.length}</p>
        </div>
        <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-lg p-6 border border-purple-200">
          <h4 className="text-sm font-bold text-purple-900 mb-2">Execution Steps</h4>
          <p className="text-3xl font-bold text-purple-600">{topologicalOrder.length}</p>
        </div>
      </div>
    </div>
  );
};

export default DependencyGraph;
