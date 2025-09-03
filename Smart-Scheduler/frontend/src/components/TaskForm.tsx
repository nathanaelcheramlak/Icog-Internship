import { useState } from "react";
import { createTask } from "../api/tasks";

export default function TaskForm({ onTaskAdded }) {
	const [name, setName] = useState("");
	const [desc, setDesc] = useState("");
	const [priority, setPriority] = useState("Medium");
	const [deadline, setDeadline] = useState("");

	async function handleSubmit(e) {
		e.preventDefault();

		// Convert YYYY-MM-DD → YYYYMMDD
		const formattedDeadline = deadline.replaceAll("-", "");

		const task = {
			name,
			description: desc || "No Description",
			priority,
			deadline: formattedDeadline,
			dependencies: [],
		};

		const res = await createTask(task);
		if (!res.error) {
			onTaskAdded();
			setName("");
			setDesc("");
			setPriority("Medium");
			setDeadline("");
		} else {
			alert(res.error);
		}
	}

	return (
		<form
			onSubmit={handleSubmit}
			className="p-4 border rounded-xl shadow-md bg-white flex flex-col gap-3"
		>
			<input
				value={name}
				onChange={(e) => setName(e.target.value)}
				placeholder="Task name"
				className="border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
				required
			/>
			<input
				value={desc}
				onChange={(e) => setDesc(e.target.value)}
				placeholder="Description"
				className="border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
			/>
			<select
				value={priority}
				onChange={(e) => setPriority(e.target.value)}
				className="border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
			>
				<option value="Low">Low</option>
				<option value="Medium">Medium</option>
				<option value="High">High</option>
			</select>
			<input
				type="date"
				value={deadline}
				onChange={(e) => setDeadline(e.target.value)}
				className="border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
				required
			/>
			<button
				type="submit"
				className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition"
			>
				Add Task
			</button>
		</form>
	);
}
