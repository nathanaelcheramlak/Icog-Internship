export interface Task {
  id: number;
  name: string;
  description: string;
  priority: 'Low' | 'Medium' | 'High' | 'Critical';
  deadline: string;
  dependencies: number[];
  completed: boolean;
  createdAt: Date;
}

export interface TaskFormData {
  name: string;
  description: string;
  priority: 'Low' | 'Medium' | 'High' | 'Critical';
  deadline: string;
  dependencies: number[];
}

export interface TaskRecommendation {
  taskId: number;
  reason: string;
  priority: number;
}

export interface DependencyNode {
  id: number;
  name: string;
  completed: boolean;
  dependencies: number[];
}
