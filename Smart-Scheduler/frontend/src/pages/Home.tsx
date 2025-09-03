import { useEffect, useState } from "react";
import { getTasks } from "../api/tasks";
import TaskForm from "../components/TaskForm";
import TaskList from "../components/TaskList";

export default function Home() {
  const [tasks, setTasks] = useState({});

  async function refresh() {
    const res = await getTasks();
    setTasks(res.tasks || {});
  }

  useEffect(() => {
    refresh();
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Task Scheduler</h1>
      <TaskForm onTaskAdded={refresh} />
      <TaskList tasks={tasks} refresh={refresh} />
    </div>
  );
}
