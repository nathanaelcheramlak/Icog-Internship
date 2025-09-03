const API_BASE_URL = (import.meta as any).env?.VITE_API_URL || 'http://localhost:5000';

export type BackendTasksResponse = {
  tasks: Record<string, {
    name: string;
    description: string;
    priority?: 'Low' | 'Medium' | 'High' | string;
    deadline?: string; // e.g., 20231202
    dependencies?: number[];
  }>
};

export interface CreateTaskPayload {
  name: string;
  description: string;
  priority: 'Low' | 'Medium' | 'High' | 'Critical';
  deadline: string; // YYYYMMDD expected by backend
  dependencies: number[];
}

export interface UpdateTaskPayload extends CreateTaskPayload {}

// New graph response types - made more flexible
export interface GraphNode {
  id: number;
  name: string;
  description: string;
  priority: 'Low' | 'Medium' | 'High' | 'Critical';
  deadline: string; // YYYYMMDD format
}

export interface GraphEdge {
  source: number;
  target: number;
}

export interface GraphData {
  nodes: Record<string, GraphNode>;
  edges: GraphEdge[];
  sorted: string; // MeTTa format: "((1) (2) (3))"
}

export interface GraphResponse {
  graph?: GraphData; // Made optional to handle different response structures
  [key: string]: any; // Allow for additional properties
}

// Schedule response types
export interface ScheduleResponse {
  schedule: number[][]; // Layered topological sort: [[1], [2, 3], [4]]
}

function toYYYYMMDD(date: string): string {
  // input: YYYY-MM-DD
  if (/^\d{8}$/.test(date)) return date;
  const d = date.replaceAll('-', '');
  return d;
}

function toYYYY_MM_DD(date: string | undefined): string {
  if (!date) return '';
  if (/^\d{4}-\d{2}-\d{2}$/.test(date)) return date;
  if (/^\d{8}$/.test(date)) return `${date.slice(0,4)}-${date.slice(4,6)}-${date.slice(6,8)}`;
  return date;
}

export async function fetchTasks(): Promise<BackendTasksResponse> {
  const res = await fetch(`${API_BASE_URL}/tasks`);
  if (!res.ok) throw new Error(`Failed to fetch tasks: ${res.status}`);
  return res.json();
}

export async function createTask(payload: Omit<CreateTaskPayload, 'deadline'> & { deadline: string /* YYYY-MM-DD */ }): Promise<void> {
  const body: CreateTaskPayload = { ...payload, deadline: toYYYYMMDD(payload.deadline) } as CreateTaskPayload;
  const res = await fetch(`${API_BASE_URL}/tasks`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error || `Failed to create task: ${res.status}`);
  }
}

export async function updateTask(taskId: number, payload: Omit<UpdateTaskPayload, 'deadline'> & { deadline: string }): Promise<void> {
  const body: UpdateTaskPayload = { ...payload, deadline: toYYYYMMDD(payload.deadline) } as UpdateTaskPayload;
  const res = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error || `Failed to update task: ${res.status}`);
  }
}

export async function deleteTask(taskId: number): Promise<void> {
  const res = await fetch(`${API_BASE_URL}/tasks/${taskId}`, { method: 'DELETE' });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error || `Failed to delete task: ${res.status}`);
  }
}

export async function fetchGraph(): Promise<GraphResponse> {
  const res = await fetch(`${API_BASE_URL}/graph`);
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || 'Failed to fetch graph');
  return data as GraphResponse;
}

export async function fetchSchedule(): Promise<ScheduleResponse> {
  const res = await fetch(`${API_BASE_URL}/schedule`);
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || 'Failed to fetch schedule');
  return data as ScheduleResponse;
}

export type ClientTask = {
  id: number;
  name: string;
  description: string;
  priority: 'Low' | 'Medium' | 'High' | 'Critical';
  deadline: string; // YYYY-MM-DD for UI
  dependencies: number[];
  completed: boolean;
};

export function mapBackendToClient(resp: BackendTasksResponse): ClientTask[] {
  const result: ClientTask[] = [];
  for (const [idStr, t] of Object.entries(resp.tasks || {})) {
    const id = Number(idStr);
    result.push({
      id,
      name: t.name,
      description: t.description,
      priority: (t.priority || 'Medium') as any,
      deadline: toYYYY_MM_DD(t.deadline),
      dependencies: t.dependencies || [],
      completed: false,
    });
  }
  // Sort by id ascending for stable UI
  result.sort((a, b) => a.id - b.id);
  return result;
}
