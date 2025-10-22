# MeTTa Training

This repository contains a collection of MeTTa scripts that implement various algorithms. 

## Algorithms

The repository includes the following algorithms:

- **`is-member.metta`**: Checks if an element is a member of a list.
- **`find-replace.metta`**: Replaces all occurrences of a specific value in a list with a new value.
- **`find-remove.metta`**: Removes the first occurrence of a specific value from a list.
- **`subset.metta`**: Generates the power set of a given set.
- **`path-finding.metta`**: Implements Dijkstra's algorithm to find the shortest paths from a single source node to all other nodes in a weighted graph.

## Path Finding Algorithm

The `path-finding.metta` script provides an implementation of Dijkstra's algorithm. This algorithm is used to find the shortest paths between nodes in a graph.

### Architecture

The implementation is divided into several key components:

- **Graph Representation**: The graph is represented as a collection of atoms in a dedicated space (`&graph`). Each atom represents a weighted edge in the form `(weight (Node start) (Node end))`.

- **Shortest Path Storage**: A separate space (`&shortest`) is used to store the computed shortest paths. This allows for efficient lookup of already processed nodes.

- **Main Function (`dijkstra`)**: The core of the algorithm is the `dijkstra` function. It iteratively explores the graph, maintaining a priority queue (heap) of nodes to visit next based on their distance from the source.

- **Helper Functions**: A number of helper functions are used to support the main algorithm:
    - `get-neighbours`: Retrieves all neighbors of a given node.
    - `get-unseen-neighbours`: Filters out neighbors that have already been visited.
    - `heappush` and `heappop`: Manage the priority queue.
    - `get-weight`: Retrieves the weight of an edge between two nodes.

### How it Works

1.  **Initialization**: The algorithm starts with a source node and a heap containing the initial path (the source node itself with a weight of 0).
2.  **Iteration**: In each step, the algorithm extracts the node with the smallest distance from the heap.
3.  **Exploration**: It then explores the neighbors of the current node, calculates their tentative distances from the source, and updates the heap.
4.  **Termination**: The algorithm terminates when all nodes have been visited or the heap is empty. The shortest paths are stored in the `&shortest` space.

## How to Run

To run these scripts, you will need a MeTTa interpreter. You can execute a script by loading it into the interpreter. For example, to run the path-finding algorithm:

```
metta path-finding.metta
```

The script will then execute and you can query the `&shortest` space to see the results.

## Author
Nathanael Cheramlak @ 2025
