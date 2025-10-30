## Search Algorithms Visualizer + Minimax Tic‑Tac‑Toe

An interactive, Pygame-based visualizer for classic graph search algorithms alongside a tic‑tac‑toe game powered by minimax with alpha‑beta pruning.

### Contents

- Visualized algorithms: BFS, DFS, Uniform Cost Search (UCS/Dijkstra), A\*
- Weighted grid support with paintable per‑cell costs
- Clean controls and live HUD (frontier, expanded, path length, cost)
- Tic‑Tac‑Toe with optimal AI (minimax + alpha‑beta)
- Connect Four with optimal AI (minimax + alpha‑beta, depth‑limited)

---

## Getting Started

Requirements: Python 3.12+, Pygame 2.6+

Run the visualizer:

```bash
python main.py
```

Run the tic‑tac‑toe game:

```bash
python tictactoe.py
```

Run the Connect Four game:

```bash
python connect_four.py
```

Project entry point for visualization is `main.py`, which launches `utils/visualizer.py`.

---

## Grid, States, and Weights

- Grid size: 28×20 cells. Start is a yellow circle, goal is a red circle.
- Walls: impassable cells you paint on the grid.
- Weights: per‑cell movement cost (≥1). The cost to move into a cell equals that cell’s weight.
  - Default weight is 1 (unweighted).
  - For A\* and UCS, total path cost is the sum of weights for all cells entered after the start.

---

## Controls (Visualizer)

- Algorithm select: B = BFS, D = DFS, A = A\*, U = UCS
- Start/Pause: Space
- Set start/goal: press S or G, then click a valid cell
- Draw walls: toggle to WALL mode (X to toggle modes), then Left‑drag to draw, Left‑click to toggle
- Paint weights: toggle to WEIGHT mode (X)
  - 1–9 set the current paint weight
  - Left‑click paints the selected weight on a cell (weights > 1 tinted and labeled)
  - Right‑click resets a cell’s weight to 1
  - C clears all weights
- Reset maze: R (also clears weights)
- Speed: + / –
- Quit: Esc

HUD (bottom bar) shows: Frontier size, Expanded (visited) count, Path length (number of nodes), Path cost (sum of cell weights), and Running state.

---

## Algorithms Explained

Below, n is the number of nodes explored; b is branching factor; d is shallowest goal depth; C\* is the optimal solution cost; w_min is the minimum positive edge cost (here, ≥1 by design).

### BFS (Breadth‑First Search)

- Strategy: Explore level by level from the start.
- Optimal? Yes, on unweighted graphs (or unit weights). Not optimal with arbitrary weights.
- Complete? Yes (finite branching, detects goal once dequeued).
- Time/Space: O(b^d) in worst case.
- In this app: Ignores weights by design (classic shortest path in hops), great for demonstrating breadth‑wise expansion.

### DFS (Depth‑First Search)

- Strategy: Dive deep along one branch, backtrack upon dead ends.
- Optimal? No.
- Complete? Not in infinite spaces; in finite grids it will terminate. Exploration order affects path found.
- Time: O(b^m) where m is max depth; Space: O(m).
- In this app: Uses a stack with “visited on pop” semantics to reflect true expansions. Visualization tracks a separate frontier set for clarity.

### UCS (Uniform Cost Search / Dijkstra)

- Strategy: Always expand the frontier node with lowest path cost so far.
- Optimal? Yes, if all edge costs are non‑negative (they are here: weights ≥ 1).
- Complete? Yes, with non‑negative costs.
- Time/Space: O(n log n) with a binary heap in practice; can be large depending on graph density.
- In this app: Moving into a cell costs that cell’s weight. Finds the true least‑cost path on the weighted grid.

### A\* Search

- Strategy: Greedy best‑first guided by f(n) = g(n) + h(n), where g is cost so far and h is heuristic.
- Heuristic: Manhattan distance scaled by the minimum positive weight to remain admissible: h(n) = w_min · Manhattan(n, goal). With weights ≥1, w_min ≥1, so A\* remains optimistic.
- Optimal? Yes, if h is admissible and consistent (Manhattan on 4‑connected grids is consistent; scaling preserves this).
- Complete? Yes, with non‑negative costs.
- Time/Space: Often far better than UCS in practice when heuristic is informative.
- In this app: A\* respects painted weights and typically explores much less than UCS.

---

## Visualization Details

- Frontier cells are cyan, visited cells are indigo, final path is orange.
- Walls are deep blue. Weighted cells (>1) are warm‑tinted with a numeric label showing the weight.
- The top HUD shows the selected algorithm, mode (WALL/WEIGHT), speed, and quick help.
- The bottom HUD shows live metrics and final path statistics, including total weighted cost.

---

## Tic‑Tac‑Toe (Minimax + Alpha‑Beta)

Run:

```bash
python tictactoe.py
```

- Human is X, AI is O. The AI is optimal using minimax with alpha‑beta pruning.
- Controls: Click to play. R or H: restart with human first. A: AI goes first. Esc: quit.
- Heuristic: Terminal evaluation only; intermediate nodes are scored indirectly by depth tie‑breaks: the AI prefers faster wins and slower losses.
- Alpha‑beta pruning significantly reduces the number of explored states by pruning branches that cannot improve the current best outcome.

---

## Connect Four (Minimax + Alpha‑Beta)

Run:

```bash
python connect_four.py
```

- Human plays Red, AI plays Yellow. AI uses minimax with alpha‑beta pruning and move ordering.
- Depth‑limited search (default 5) for strong play and good responsiveness; prefers center columns for better pruning.
- Controls: Click a column to drop a piece. R or H: restart with human first. A: AI first. Esc: quit.
- Evaluation: line‑based heuristic scoring (fours, threes, twos, center control), with large terminal rewards/penalties.

---

## File Overview

- `main.py`: launches the visualizer
- `utils/visualizer.py`: UI, controls, drawing, and state management
- `utils/helpers.py`: grid math (neighbors, bounds, Manhattan)
- `algorithms/bfs.py`: breadth‑first search generator
- `algorithms/dfs.py`: depth‑first search generator
- `algorithms/ucs.py`: uniform cost search (Dijkstra) generator with weights
- `algorithms/a_star.py`: A\* search generator with weighted admissible heuristic
- `tictactoe.py`: standalone game with minimax + alpha‑beta pruning
- `connect_four.py`: standalone Connect Four with minimax + alpha‑beta pruning

---

## Notes on Correctness and Robustness

- Start equals goal: all algorithms immediately return the trivial path.
- Walls are never traversed; painting weights on walls has no effect.
- A\*’s heuristic is scaled by the minimum positive weight to keep it admissible and consistent.
- Visualization state is driven directly by algorithm yields, ensuring accurate displays of frontier and visited sets.

---

## Author

Nathanael @ 2025
