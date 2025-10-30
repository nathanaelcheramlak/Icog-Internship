import pygame
import sys
from typing import List, Tuple, Optional, Set, Dict
from .helpers import *
from algorithms import *

# Config
GRID_W, GRID_H = 28, 20  # columns, rows
CELL = 28  # pixel size of a cell
MARGIN = 48  # top margin for controls
WIDTH = GRID_W * CELL
HEIGHT = GRID_H * CELL + MARGIN
FPS = 60

# Colors
BG = (10, 10, 30)
GRID_COLOR = (30, 30, 60)
WALL_COLOR = (20, 20, 120)
PACMAN_COLOR = (255, 220, 0)
GOAL_COLOR = (200, 50, 50)
FRONTIER_COLOR = (60, 200, 200)
VISITED_COLOR = (100, 100, 180)
PATH_COLOR = (255, 180, 0)
TEXT_COLOR = (220, 220, 240)

# Visualization settings
ANIM_SPEED = 1  # steps per frame (can be increased with +)

Pos = Tuple[int, int]
DIRS_4 = [(1, 0), (-1, 0), (0, 1), (0, -1)]

# ----- Pygame Visualization -----
class Visualizer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pac-Man Pathfinding Visualizer")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 20)

        # grid state
        self.walls: Set[Pos] = set()
        self.weights: Dict[Pos, float] = {}
        self.start: Pos = (1, 1)
        self.goal: Pos = (GRID_W - 2, GRID_H - 2)

        # algorithm and generator
        self.algorithm_name = "BFS"
        self.generator = None
        self.running = False
        self.anim_speed = ANIM_SPEED
        self.paint_mode = "wall"  # "wall" or "weight"
        self.current_weight: float = 2.0

        # visualization state
        self.frontier: Set[Pos] = set()
        self.visited: Set[Pos] = set()
        self.current: Optional[Pos] = None
        self.path: Optional[List[Pos]] = None

        # create default maze
        self._make_default_maze()

    def _make_default_maze(self):
        # outer walls
        for x in range(GRID_W):
            self.walls.add((x, 0))
            self.walls.add((x, GRID_H-1))
        for y in range(GRID_H):
            self.walls.add((0, y))
            self.walls.add((GRID_W-1, y))
        # create some corridors
        for x in range(2, GRID_W-2, 2):
            for y in range(2, GRID_H-2, 4):
                self.walls.add((x, y))
        # Add a box in the middle
        midx, midy = GRID_W//2, GRID_H//2
        for dx in range(-3, 4):
            self.walls.add((midx+dx, midy-2))
            self.walls.add((midx+dx, midy+2))
        for dy in range(-1, 2):
            self.walls.add((midx-3, midy+dy))
            self.walls.add((midx+3, midy+dy))
        # clear start/goal region
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                self.walls.discard((self.start[0]+dx, self.start[1]+dy))
                self.walls.discard((self.goal[0]+dx, self.goal[1]+dy))

    def reset_search(self):
        self.generator = None
        self.running = False
        self.frontier.clear()
        self.visited.clear()
        self.current = None
        self.path = None

    def start_algorithm(self):
        self.reset_search()
        if self.algorithm_name == "BFS":
            self.generator = bfs(self.start, self.goal, self.walls)
        elif self.algorithm_name == "DFS":
            self.generator = dfs(self.start, self.goal, self.walls)
        elif self.algorithm_name == "A*":
            self.generator = astar(self.start, self.goal, self.walls, self.weights)
        elif self.algorithm_name == "UCS":
            self.generator = ucs(self.start, self.goal, self.walls, self.weights)
        else:
            return
        self.running = True

    def step_algorithm(self):
        if not self.generator:
            return
        try:
            for _ in range(max(1, self.anim_speed)):
                state = next(self.generator)
                # update visual state
                self.frontier = set(tuple(x) for x in state.get("frontier", []))
                self.visited = set(tuple(x) for x in state.get("visited", []))
                self.current = tuple(state.get("current")) if state.get("current") is not None else None
                if "path" in state:
                    self.path = state["path"]
                # if algorithm finished and path set to None -> no solution
                if state.get("action") == "done":
                    self.running = False
                    return
        except StopIteration:
            self.running = False

    def handle_events(self):
        mouse_pressed = pygame.mouse.get_pressed()
        mx, my = pygame.mouse.get_pos()
        grid_x = mx // CELL
        grid_y = (my - MARGIN) // CELL
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                elif event.key == pygame.K_b:
                    self.algorithm_name = "BFS"; self.reset_search()
                elif event.key == pygame.K_d:
                    self.algorithm_name = "DFS"; self.reset_search()
                elif event.key == pygame.K_a:
                    self.algorithm_name = "A*"; self.reset_search()
                elif event.key == pygame.K_u:
                    self.algorithm_name = "UCS"; self.reset_search()
                elif event.key == pygame.K_SPACE:
                    if not self.running:
                        self.start_algorithm()
                    else:
                        self.running = False
                elif event.key == pygame.K_r:
                    self.walls.clear(); self.weights.clear(); self._make_default_maze(); self.reset_search()
                elif event.key == pygame.K_s:
                    if in_bounds((grid_x, grid_y)):
                        self.start = (grid_x, grid_y); self.reset_search()
                elif event.key == pygame.K_g:
                    if in_bounds((grid_x, grid_y)):
                        self.goal = (grid_x, grid_y); self.reset_search()
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    self.anim_speed = min(20, self.anim_speed + 1)
                elif event.key == pygame.K_MINUS:
                    self.anim_speed = max(1, self.anim_speed - 1)
                elif event.key == pygame.K_x:
                    self.paint_mode = "weight" if self.paint_mode == "wall" else "wall"
                elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9):
                    # numbers exclusively adjust weight and do not switch algorithms
                    try:
                        self.current_weight = float(int(event.unicode))
                    except Exception:
                        pass
                elif event.key == pygame.K_c:
                    self.weights.clear(); self.reset_search()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if in_bounds((grid_x, grid_y)):
                    p = (grid_x, grid_y)
                    if self.paint_mode == "wall":
                        if event.button == 1:
                            if p != self.start and p != self.goal:
                                if p in self.walls:
                                    self.walls.remove(p)
                                else:
                                    self.walls.add(p)
                                self.reset_search()
                    else:
                        # weight painting mode
                        if p != self.start and p != self.goal and p not in self.walls:
                            if event.button == 1:
                                if self.current_weight <= 1.0:
                                    self.weights.pop(p, None)
                                else:
                                    self.weights[p] = float(self.current_weight)
                                self.reset_search()
                            elif event.button == 3:
                                # right click resets to weight 1
                                self.weights.pop(p, None)
                                self.reset_search()
        # drag to draw walls
        if mouse_pressed[0] and in_bounds((grid_x, grid_y)):
            p = (grid_x, grid_y)
            if self.paint_mode == "wall":
                if p != self.start and p != self.goal:
                    self.walls.add(p)
                    self.reset_search()
            else:
                if p != self.start and p != self.goal and p not in self.walls:
                    if self.current_weight <= 1.0:
                        self.weights.pop(p, None)
                    else:
                        self.weights[p] = float(self.current_weight)
                    self.reset_search()

    def draw_grid(self):
        # background
        self.screen.fill(BG)
        # draw top info area
        pygame.draw.rect(self.screen, GRID_COLOR, (0, 0, WIDTH, MARGIN))

        # grid cells
        for x in range(GRID_W):
            for y in range(GRID_H):
                rx = x * CELL
                ry = MARGIN + y * CELL
                rect = pygame.Rect(rx, ry, CELL, CELL)
                pygame.draw.rect(self.screen, GRID_COLOR, rect, 1)
                p = (x, y)
                if p in self.walls:
                    pygame.draw.rect(self.screen, WALL_COLOR, rect)
                else:
                    # shade by weight if > 1
                    w = self.weights.get(p, 1.0)
                    if w > 1.0:
                        # map weight 1..9 to tint intensity
                        alpha = min(1.0, (w - 1.0) / 8.0)
                        base = GRID_COLOR[1]  # use greenish channel baseline
                        r = int(40 + 120 * alpha)
                        g = int(40 + 40 * (1.0 - alpha))
                        b = int(40)
                        pygame.draw.rect(self.screen, (r, g, b), rect)
                        # draw weight number
                        num = self.font.render(str(int(w)), True, (250, 250, 250))
                        self.screen.blit(num, (rx + CELL//2 - 4, ry + CELL//2 - 6))

        # frontier
        for p in self.frontier:
            rx = p[0]*CELL
            ry = MARGIN + p[1]*CELL
            rect = pygame.Rect(rx+2, ry+2, CELL-4, CELL-4)
            pygame.draw.rect(self.screen, FRONTIER_COLOR, rect)
        # visited
        for p in self.visited:
            rx = p[0]*CELL
            ry = MARGIN + p[1]*CELL
            rect = pygame.Rect(rx+4, ry+4, CELL-8, CELL-8)
            pygame.draw.rect(self.screen, VISITED_COLOR, rect)
        # path
        if self.path:
            for p in self.path:
                rx = p[0]*CELL
                ry = MARGIN + p[1]*CELL
                rect = pygame.Rect(rx+6, ry+6, CELL-12, CELL-12)
                pygame.draw.rect(self.screen, PATH_COLOR, rect)

        # draw start and goal sprites (Pac-Man and ghost-ish)
        sx, sy = self.start
        gx, gy = self.goal
        # Pac-Man (start)
        pac_rect = pygame.Rect(sx*CELL+2, MARGIN + sy*CELL+2, CELL-4, CELL-4)
        pygame.draw.ellipse(self.screen, PACMAN_COLOR, pac_rect)
        # Goal (red circle)
        goal_rect = pygame.Rect(gx*CELL+4, MARGIN + gy*CELL+4, CELL-8, CELL-8)
        pygame.draw.ellipse(self.screen, GOAL_COLOR, goal_rect)

        # highlight current
        if self.current:
            cx, cy = self.current
            r = pygame.Rect(cx*CELL+1, MARGIN + cy*CELL+1, CELL-2, CELL-2)
            pygame.draw.rect(self.screen, (255,255,255), r, 2)

        # status text
        def compute_path_cost(path: Optional[List[Pos]]) -> Optional[float]:
            if not path:
                return None
            total = 0.0
            # cost to enter each cell after start
            for p in path[1:]:
                total += float(self.weights.get(p, 1.0))
            return total

        path_len = len(self.path) if self.path else 'N/A'
        path_cost = compute_path_cost(self.path)
        status_lines = [
            f"Frontier: {len(self.frontier)}",
            f"Expanded: {len(self.visited)}",
            f"Path len: {path_len}",
            f"Path cost: {round(path_cost,2) if path_cost is not None else 'N/A'}",
            f"Running: {self.running}"
        ]
        for i, line in enumerate(status_lines):
            surf = self.font.render(line, True, TEXT_COLOR)
            self.screen.blit(surf, (6 + i*160, HEIGHT - 22))

        # top HUD text
        txt = (
            f"Algorithm: {self.algorithm_name}  |  Select: B/D/A/U  |  Space: Start/Pause  |  S/G set start/goal  |  Speed: {self.anim_speed}  |  Mode: {self.paint_mode.upper()}  |  Weight: {int(self.current_weight)}  |  X toggle, 1-9 set, C clear"
        )
        surf = self.font.render(txt, True, TEXT_COLOR)
        self.screen.blit(surf, (6, 12))

    def run(self):
        while True:
            self.handle_events()
            if self.running:
                self.step_algorithm()
            self.draw_grid()
            pygame.display.flip()
            self.clock.tick(FPS)
