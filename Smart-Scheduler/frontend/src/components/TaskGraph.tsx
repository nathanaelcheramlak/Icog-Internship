import { useEffect, useState } from "react";
import ReactFlow, { Background, Controls } from "reactflow";
import "reactflow/dist/style.css";
import { getTasks } from "../api/tasks";

export default function TaskGraph() {
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);

  useEffect(() => {
    async function fetchData() {
      const res = await getTasks();
      if (res.tasks) {
        const taskData = res.tasks;

        // Create nodes
        const graphNodes = Object.entries(taskData).map(([id, task], idx) => ({
          id: id.toString(),
          data: { label: `${task.name}\n(${task.priority})` },
          position: { x: idx * 150, y: idx * 100 }, // simple layout
          style: {
            border: "1px solid #3b82f6",
            borderRadius: "12px",
            padding: "8px",
            background: "#f9fafb",
          },
        }));

        // Create edges
        const graphEdges = [];
        Object.entries(taskData).forEach(([id, task]) => {
          if (task.dependencies) {
            task.dependencies.forEach((dep) => {
              graphEdges.push({
                id: `e${dep}-${id}`,
                source: dep.toString(),
                target: id.toString(),
                animated: true,
                style: { stroke: "#3b82f6" },
              });
            });
          }
        });

        setNodes(graphNodes);
        setEdges(graphEdges);
      }
    }

    fetchData();
  }, []);

  return (
    <div className="h-screen w-full">
      <ReactFlow nodes={nodes} edges={edges} fitView>
        <Background gap={16} color="#e5e7eb" />
        <Controls />
      </ReactFlow>
    </div>
  );
}
