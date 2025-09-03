const BASE_URL = "http://localhost:5000";

export async function getTasks() {
	const res = await fetch(`${BASE_URL}/tasks`);
	return res.json();
}

export async function createTask(task) {
	const res = await fetch(`${BASE_URL}/tasks`, {
		method: "POST",
		headers: { "Content-Type": "application/json" },
		body: JSON.stringify(task),
	});
	return res.json();
}

export async function deleteTask(id) {
	const res = await fetch(`${BASE_URL}/tasks/${id}`, { method: "DELETE" });
	return res.json();
}

export async function updateTask(id, task) {
	const res = await fetch(`${BASE_URL}/tasks/${id}`, {
		method: "PUT",
		headers: { "Content-Type": "application/json" },
		body: JSON.stringify(task),
	});
	return res.json();
}

export async function getSchedule() {
	const res = await fetch(`${BASE_URL}/schedule`);
	return res.json();
}
