import pygame
import sys
from typing import List, Optional, Tuple


ROWS, COLS = 6, 7
EMPTY, HUMAN, AI = 0, 1, 2

Board = List[List[int]]


def create_board() -> Board:
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]


def copy_board(board: Board) -> Board:
    return [row[:] for row in board]


def valid_moves(board: Board) -> List[int]:
    return [c for c in range(COLS) if board[0][c] == EMPTY]


def drop_piece(board: Board, col: int, player: int) -> bool:
    if col < 0 or col >= COLS or board[0][col] != EMPTY:
        return False
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == EMPTY:
            board[r][col] = player
            return True
    return False


def check_winner(board: Board) -> Optional[int]:
    # horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            line = board[r][c:c+4]
            if line[0] != EMPTY and all(x == line[0] for x in line):
                return line[0]
    # vertical
    for c in range(COLS):
        for r in range(ROWS - 3):
            line = [board[r+i][c] for i in range(4)]
            if line[0] != EMPTY and all(x == line[0] for x in line):
                return line[0]
    # diag down-right
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            line = [board[r+i][c+i] for i in range(4)]
            if line[0] != EMPTY and all(x == line[0] for x in line):
                return line[0]
    # diag up-right
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            line = [board[r-i][c+i] for i in range(4)]
            if line[0] != EMPTY and all(x == line[0] for x in line):
                return line[0]
    return None


def is_full(board: Board) -> bool:
    return all(board[0][c] != EMPTY for c in range(COLS))

def evaluate_window(window: List[int], player: int) -> int:
    opp = HUMAN if player == AI else AI
    score = 0
    count_p = window.count(player)
    count_e = window.count(EMPTY)
    count_o = window.count(opp)
    if count_p == 4:
        score += 10_000
    elif count_p == 3 and count_e == 1:
        score += 100
    elif count_p == 2 and count_e == 2:
        score += 10
    if count_o == 3 and count_e == 1:
        score -= 120
    if count_o == 2 and count_e == 2:
        score -= 10
    return score


def evaluate_board(board: Board, player: int) -> int:
    winner = check_winner(board)
    if winner == AI:
        return 1_000_000
    if winner == HUMAN:
        return -1_000_000

    score = 0
    # center preference
    center_col = COLS // 2
    center_count = sum(1 for r in range(ROWS) if board[r][center_col] == player)
    score += center_count * 6

    # horizontal
    for r in range(ROWS):
        row = board[r]
        for c in range(COLS - 3):
            window = row[c:c+4]
            score += evaluate_window(window, player)
    # vertical
    for c in range(COLS):
        col = [board[r][c] for r in range(ROWS)]
        for r in range(ROWS - 3):
            window = col[r:r+4]
            score += evaluate_window(window, player)
    # diag down-right
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window = [board[r+i][c+i] for i in range(4)]
            score += evaluate_window(window, player)
    # diag up-right
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            window = [board[r-i][c+i] for i in range(4)]
            score += evaluate_window(window, player)
    return score


def minimax(board: Board, depth: int, alpha: int, beta: int, maximizing: bool) -> Tuple[int, Optional[int]]:
    winner = check_winner(board)
    if depth == 0 or winner is not None or is_full(board):
        return evaluate_board(board, AI), None

    best_col: Optional[int] = None

    if maximizing:
        value = -10**9
        for col in order_moves(valid_moves(board)):
            b2 = copy_board(board)
            drop_piece(b2, col, AI)
            child_val, _ = minimax(b2, depth - 1, alpha, beta, False)
            if child_val > value:
                value = child_val
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value, best_col
    else:
        value = 10**9
        for col in order_moves(valid_moves(board)):
            b2 = copy_board(board)
            drop_piece(b2, col, HUMAN)
            child_val, _ = minimax(b2, depth - 1, alpha, beta, True)
            if child_val < value:
                value = child_val
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value, best_col


def order_moves(moves: List[int]) -> List[int]:
    # prefer center columns first for better pruning
    center = COLS // 2
    return sorted(moves, key=lambda c: abs(c - center))


def best_ai_move(board: Board, search_depth: int = 5) -> Optional[int]:
    _, col = minimax(board, search_depth, -10**9, 10**9, True)
    return col


def draw_board(screen, board: Board, status_text: str, hover_col: Optional[int]):
    screen.fill((24, 26, 32))
    W, H = screen.get_size()
    margin = 80
    grid_h = H - margin - 30
    grid_w = min(W - 40, int(grid_h * (COLS / ROWS)))
    grid_h = int(grid_w * (ROWS / COLS))
    cell = grid_w // COLS
    origin_x = (W - grid_w) // 2
    origin_y = (H - margin - grid_h) // 2 + margin

    # Title and status
    font_title = pygame.font.SysFont(None, 36)
    font_status = pygame.font.SysFont(None, 24)
    title = font_title.render("Connect Four - You: Red  |  AI: Yellow", True, (230, 230, 240))
    screen.blit(title, (origin_x, 24))
    status = font_status.render(status_text, True, (200, 200, 210))
    screen.blit(status, (origin_x, 56))

    # Grid background
    board_color = (40, 80, 160)
    pygame.draw.rect(screen, board_color, (origin_x, origin_y, grid_w, grid_h))

    # Hover highlight for column
    if hover_col is not None and 0 <= hover_col < COLS:
        hx = origin_x + hover_col * cell
        pygame.draw.rect(screen, (50, 90, 180), (hx, origin_y, cell, grid_h))

    # Draw slots
    r_color = (220, 60, 60)
    y_color = (240, 210, 70)
    empty_color = (24, 26, 32)
    for r in range(ROWS):
        for c in range(COLS):
            cx = origin_x + c * cell + cell // 2
            cy = origin_y + r * cell + cell // 2
            rad = cell // 2 - 6
            if board[r][c] == HUMAN:
                color = r_color
            elif board[r][c] == AI:
                color = y_color
            else:
                color = empty_color
            pygame.draw.circle(screen, color, (cx, cy), rad)

    # Footer controls
    font_foot = pygame.font.SysFont(None, 22)
    footer = font_foot.render("Click a column. R: restart  |  H: human first  |  A: AI first  |  ESC: quit", True, (180, 190, 205))
    screen.blit(footer, (origin_x, origin_y + grid_h + 12))


def get_col_from_mouse(pos: Tuple[int, int], screen_size: Tuple[int, int]) -> Optional[int]:
    W, H = screen_size
    margin = 80
    grid_h = H - margin - 30
    grid_w = W - 40
    cell = grid_w // COLS
    origin_x = (W - grid_w) // 2
    origin_y = (H - margin - (cell * ROWS)) // 2 + margin
    mx, my = pos
    if not (origin_x <= mx < origin_x + cell * COLS and origin_y <= my < origin_y + cell * ROWS):
        return None
    return int((mx - origin_x) // cell)


def main():
    pygame.init()
    screen = pygame.display.set_mode((720, 680))
    pygame.display.set_caption("Connect Four (Minimax with Alpha-Beta)")
    clock = pygame.time.Clock()

    board: Board = create_board()
    human_turn = True
    game_over = False
    status_text = "Your turn"
    hover_col: Optional[int] = None
    depth = 5  # balanced depth for performance and strength

    def reset(start_human: bool):
        nonlocal board, human_turn, game_over, status_text
        board = create_board()
        human_turn = start_human
        game_over = False
        status_text = ("Your turn" if human_turn else "AI thinking...")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                elif event.key == pygame.K_r:
                    reset(True)
                elif event.key == pygame.K_h:
                    reset(True)
                elif event.key == pygame.K_a:
                    reset(False)
            elif event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                hover_col = get_col_from_mouse(pos, screen.get_size())
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game_over or not human_turn:
                    continue
                col = get_col_from_mouse(pygame.mouse.get_pos(), screen.get_size())
                if col is None:
                    continue
                if drop_piece(board, col, HUMAN):
                    w = check_winner(board)
                    if w or is_full(board):
                        game_over = True
                        status_text = ("You win!" if w == HUMAN else ("AI wins!" if w == AI else "Draw!")) + " Press R/H/A to restart."
                    else:
                        human_turn = False
                        status_text = "AI thinking..."

        if not game_over and not human_turn:
            col = best_ai_move(board, depth)
            if col is not None:
                drop_piece(board, col, AI)
            w = check_winner(board)
            if w or is_full(board):
                game_over = True
                status_text = ("You win!" if w == HUMAN else ("AI wins!" if w == AI else "Draw!")) + " Press R/H/A to restart."
            else:
                human_turn = True
                status_text = "Your turn"

        draw_board(screen, board, status_text, hover_col)
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()


