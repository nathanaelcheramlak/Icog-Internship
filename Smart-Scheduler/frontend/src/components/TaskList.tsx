import { deleteTask } from "../api/tasks.js";

export default function TaskList({ tasks, refresh }) {
  async function handleDelete(id) {
    await deleteTask(id);
    refresh();
  }

  return (
    <ul className="space-y-3 mt-4">
      {Object.entries(tasks).map(([id, task]) => (
        <li key={id} className="p-3 border rounded-xl shadow flex justify-between">
          <div>
            <h3 className="font-bold">{task.name}</h3>
            <p>{task.description}</p>
            <small>Priority: {task.priority}, Deadline: {task.deadline}</small>
          </div>
          <button onClick={() => handleDelete(id)} className="bg-red-500 text-white px-3 py-1 rounded-lg">
            Delete
          </button>
        </li>
      ))}
    </ul>
  );
}
