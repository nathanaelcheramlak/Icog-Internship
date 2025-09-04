from flask import Flask, Response, request, jsonify
from flask_cors import CORS 
from hyperon import MeTTa

from utils import has_cycle, parse_task_string
from pymetta import get_schedule

app = Flask(__name__)
CORS(app)

# Constants
VALID_PRIORITIES = ['Low', 'Medium', 'High']
DEADLINE_FORMAT_LENGTH = 8

def create_error_response(message: str, status_code: int = 400) -> Response:
    """Create a standardized error response."""
    return jsonify({"error": message}), status_code

metta = MeTTa()
TASK_ID = 1

# --- Routes ---
@app.route("/tasks", methods=["POST"])
def create_task() -> Response:
    """Create a new task with the provided data."""
    global TASK_ID
    data = request.json

    name = data.get("name")
    description = data.get("description")
    priority = data.get("priority")
    deadline = data.get("deadline")
    dependencies = data.get("dependencies", [])

    # Input validation
    if not name or not description or not priority or not deadline:
        return create_error_response("Missing required fields: name, description, priority, deadline")
    
    if priority not in VALID_PRIORITIES:
        return create_error_response(f"Priority must be one of: {', '.join(VALID_PRIORITIES)}")
    

    # Cycle detection
    is_cyclic, cycle_path = has_cycle(metta.space().get_atoms(), TASK_ID, dependencies)
    if is_cyclic:
        return jsonify({"error": "Cycle detected in task dependencies", "cycle_path": cycle_path}), 400

    # Create atoms for the task and its attributes
    task_atom = metta.parse_single(f'(Task {TASK_ID} (Name "{name}") (Description "{description}"))')
    priority_atom = metta.parse_single(f"(Priority {TASK_ID} {priority})")
    deadline_atom = metta.parse_single(f"(Deadline {TASK_ID} {deadline})")
    indegree_atom = metta.parse_single(f"(Indegree {TASK_ID} {len(dependencies)})")

    # Add directed edges for dependencies
    for dependency in dependencies:
        edge_atom = metta.parse_single(f"(DirectedEdge {dependency} {TASK_ID})")
        metta.space().add_atom(edge_atom)
    
    metta.space().add_atom(task_atom)
    metta.space().add_atom(priority_atom)
    metta.space().add_atom(deadline_atom)
    metta.space().add_atom(indegree_atom)

    TASK_ID += 1
    tasks = [str(atom) for atom in metta.space().get_atoms()]
    return jsonify({"message": "Task Added", "tasks": tasks})

@app.route("/tasks", methods=["GET"])
def get_tasks() -> Response:
    """Retrieve all tasks from the MeTTa space."""
    task_atoms = [str(atom) for atom in metta.space().get_atoms()]
    tasks = {}
    for atom in task_atoms:
        if atom.startswith("(Task"):
            result = parse_task_string(atom)
            task_id = result['task_id']
            tasks[task_id] = {
                "name": result['name'],
                "description": result['description'],
            }
        elif atom.startswith("(Priority"):
            parts = atom.strip("()").split()
            task_id = int(parts[1])
            if task_id in tasks:
                tasks[task_id]["priority"] = parts[2]
        elif atom.startswith("(Deadline"):
            parts = atom.strip("()").split()
            task_id = int(parts[1])
            if task_id in tasks:
                tasks[task_id]["deadline"] = parts[2]
        elif atom.startswith("(DirectedEdge"):
            parts = atom.strip("()").split()
            src = int(parts[1])
            dst = int(parts[2])
            if dst in tasks:
                if "dependencies" not in tasks[dst]:
                    tasks[dst]["dependencies"] = []
                tasks[dst]["dependencies"].append(src)

    return jsonify({"tasks": tasks})

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id: int) -> Response:
    global TASK_ID
    if task_id >= TASK_ID or task_id < 1:
        return jsonify({"error": "Task ID does not exist"}), 404
    
    # Remove all atoms related to the task
    atoms_to_remove = []
    atom_dependencies = []
    for atom in metta.space().get_atoms():
        atom_str = str(atom)
        if atom_str.startswith(f"(DirectedEdge {task_id}"):
            atoms_to_remove.append(atom)
            # Extract the destination task ID to decrement its InDegree
            parts = atom_str.strip("()").split()
            _, _, dest = parts
            atom_dependencies.append(int(dest))
        if atom_str.startswith(f"(DirectedEdge ") and f" {task_id})" in atom_str:
            atoms_to_remove.append(atom)
        if atom_str.startswith(f"(Task {task_id}"):
            atoms_to_remove.append(atom)
        if atom_str.startswith(f"(Priority {task_id}"):
            atoms_to_remove.append(atom)
        if atom_str.startswith(f"(Deadline {task_id}"):
            atoms_to_remove.append(atom)
        if atom_str.startswith(f"(Indegree {task_id}"):
            atoms_to_remove.append(atom)
    
    # Decrement InDegree of dependent tasks
    for dep_id in atom_dependencies:
        for atom in metta.space().get_atoms():
            atom_str = str(atom)
            if atom_str.startswith(f"(Indegree {dep_id}"):
                parts = atom_str.strip("()").split()
                _, _, indegree = parts
                new_indegree = int(indegree) - 1
                metta.space().remove_atom(atom)
                new_indegree_atom = metta.parse_single(f"(Indegree {dep_id} {new_indegree})")
                metta.space().add_atom(new_indegree_atom)
                break

    for atom in atoms_to_remove:
        metta.space().remove_atom(atom)

    tasks = [str(atom) for atom in metta.space().get_atoms()]
    return jsonify({"message": "Task Deleted", "tasks": tasks})

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id: int) -> Response:
    data = request.json

    name = data.get("name")
    description = data.get("description")
    priority = data.get("priority")
    deadline = data.get("deadline")
    dependencies = data.get("dependencies", [])

    # required_fields = ["name", "description", "priority", "deadline"]
    # missing = [f for f in required_fields if not data.get(f)]
    # if missing:
    #     return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    if task_id >= TASK_ID or task_id < 1:
        return jsonify({"error": "Task ID does not exist"}), 404

    # Cycle detection
    is_cyclic, cycle_path = has_cycle(metta.space().get_atoms(), task_id, dependencies)
    if is_cyclic:
        return jsonify({"error": "Cycle detected in task dependencies", "cycle_path": cycle_path}), 400

    # Remove existing atoms related to the task
    atoms_to_remove = []
    atom_dependencies = []
    for atom in metta.space().get_atoms():
        atom_str = str(atom)
        if atom_str.startswith(f"(DirectedEdge {task_id}"):
            atoms_to_remove.append(atom)
            # Extract the destination task ID to decrement its InDegree
            parts = atom_str.strip("()").split()
            _, _, dest = parts
            atom_dependencies.append(int(dest))
        if atom_str.startswith(f"(DirectedEdge ") and f" {task_id})" in atom_str:
            atoms_to_remove.append(atom)
        if atom_str.startswith(f"(Task {task_id}"):
            atoms_to_remove.append(atom)
        if atom_str.startswith(f"(Priority {task_id}"):
            atoms_to_remove.append(atom)
        if atom_str.startswith(f"(Deadline {task_id}"):
            atoms_to_remove.append(atom)
        if atom_str.startswith(f"(Indegree {task_id}"):
            atoms_to_remove.append(atom)

    # Decrement InDegree of dependent tasks
    for dep_id in atom_dependencies:
        for atom in metta.space().get_atoms():
            atom_str = str(atom)
            if atom_str.startswith(f"(Indegree {dep_id}"):
                parts = atom_str.strip("()").split()
                _, _, indegree = parts
                new_indegree = int(indegree) - 1
                metta.space().remove_atom(atom)
                new_indegree_atom = metta.parse_single(f"(Indegree {dep_id} {new_indegree})")
                metta.space().add_atom(new_indegree_atom)
                break

    for atom in atoms_to_remove:
        metta.space().remove_atom(atom)
    
    # Create new atoms for the updated task and its attributes
    task_atom = metta.parse_single(f'(Task {task_id} (Name "{name}") (Description "{description}"))')
    priority_atom = metta.parse_single(f"(Priority {task_id} {priority})")
    deadline_atom = metta.parse_single(f"(Deadline {task_id} {deadline})")
    indegree_atom = metta.parse_single(f"(Indegree {task_id} {len(dependencies)})")
    
    # Add directed edges for dependencies
    for dependency in dependencies:
        edge_atom = metta.parse_single(f"(DirectedEdge {dependency} {task_id})")
        metta.space().add_atom(edge_atom)
    
    # Add new atoms to the space
    metta.space().add_atom(task_atom)
    metta.space().add_atom(priority_atom)
    metta.space().add_atom(deadline_atom)
    metta.space().add_atom(indegree_atom)

    tasks = [str(atom) for atom in metta.space().get_atoms()]
    return jsonify({"message": "Task Updated", "tasks": tasks})


@app.route("/schedule", methods=["GET"])
def schedule_tasks() -> Response:
    metta_space = [str(atom) for atom in metta.space().get_atoms()]
    try:
        s = str(get_schedule(metta_space)[0][0])
        schedule = []
        for layer in s.split(") ("):
            layer = layer.strip("()").split()
            schedule.append([int(task_id) for task_id in layer])
        return jsonify({"schedule": schedule})
    except Exception as e:
        return jsonify({"error": f"Failed to generate schedule: {str(e)}"}), 500

@app.route("/graph", methods=["GET"])
def get_graph() -> Response:
    metta_space = [str(atom) for atom in metta.space().get_atoms()]
    graph = { "nodes": {}, "edges": [] }
    for atom in metta_space:
        if atom.startswith("(Task"):
            result = parse_task_string(atom)
            task_id = result['task_id']
            graph["nodes"][task_id] = { 
                "id": task_id, 
                "name": result['name'],
                "description": result['description']
            }
        elif atom.startswith("(DirectedEdge"):
            parts = atom.strip("()").split()
            src = int(parts[1])
            dst = int(parts[2])
            graph["edges"].append({ "source": src, "target": dst })
        elif atom.startswith("(Priority"):
            parts = atom.strip("()").split()
            task_id = int(parts[1])
            graph["nodes"][task_id]["priority"] = parts[2]
        elif atom.startswith("(Deadline"):
            parts = atom.strip("()").split()
            task_id = int(parts[1])
            graph["nodes"][task_id]["deadline"] = parts[2]

    graph["sorted"] = str(get_schedule(metta_space)[0][0])
    return jsonify({"graph": graph})

if __name__ == "__main__":
    app.run(debug=True)
