import pygame
import sys
from typing import List, Optional, Tuple


# Board uses: 'X' (human), 'O' (AI), '' (empty)
Board = List[List[str]]


def check_winner(board: Board) -> Optional[str]:
    lines = []
    # rows and cols
    for i in range(3):
        lines.append(board[i])
        lines.append([board[0][i], board[1][i], board[2][i]])
    # diagonals
    lines.append([board[0][0], board[1][1], board[2][2]])
    lines.append([board[0][2], board[1][1], board[2][0]])
    for line in lines:
        if line[0] and line[0] == line[1] == line[2]:
            return line[0]
    return None


def is_full(board: Board) -> bool:
    for r in range(3):
        for c in range(3):
            if board[r][c] == "":
                return False
    return True


def evaluate(board: Board) -> int:
    winner = check_winner(board)
    if winner == 'O':
        return 10
    if winner == 'X':
        return -10
    return 0


def minimax(board: Board, depth: int, alpha: int, beta: int, maximizing: bool) -> Tuple[int, Optional[Tuple[int, int]]]:
    score = evaluate(board)
    if score == 10:
        return score - depth, None  # prefer quicker wins
    if score == -10:
        return score + depth, None  # prefer slower losses
    if is_full(board):
        return 0, None

    best_move: Optional[Tuple[int, int]] = None

    if maximizing:
        best_val = -10_000
        for r in range(3):
            for c in range(3):
                if board[r][c] == "":
                    board[r][c] = 'O'
                    val, _ = minimax(board, depth + 1, alpha, beta, False)
                    board[r][c] = ""
                    if val > best_val:
                        best_val = val
                        best_move = (r, c)
                    # print(f'Maximizer: {maximizing} {(r, c)} [{alpha} & {beta}]')
                    alpha = max(alpha, best_val)
                    if beta <= alpha:
                        return best_val, best_move
        return best_val, best_move
    else:
        best_val = 10_000
        for r in range(3):
            for c in range(3):
                if board[r][c] == "":
                    board[r][c] = 'X'
                    val, _ = minimax(board, depth + 1, alpha, beta, True)
                    board[r][c] = ""
                    if val < best_val:
                        best_val = val
                        best_move = (r, c)
                    beta = min(beta, best_val)
                    if beta <= alpha:
                        return best_val, best_move
        return best_val, best_move


def best_ai_move(board: Board) -> Optional[Tuple[int, int]]:
    _, move = minimax(board, 0, -10_000, 10_000, True)
    return move


def draw_board(screen, board: Board, status_text: str, hover: Optional[Tuple[int, int]]):
    screen.fill((24, 26, 32))
    W, H = screen.get_size()
    margin = 80
    grid = min(W, H - margin)
    cell = grid // 3
    origin_x = (W - grid) // 2
    origin_y = (H - margin - grid) // 2 + margin

    # Title and status
    font_title = pygame.font.SysFont(None, 36)
    font_status = pygame.font.SysFont(None, 24)
    title = font_title.render("Tic-Tac-Toe - You: X  |  AI: O", True, (230, 230, 240))
    screen.blit(title, (origin_x, 24))
    status = font_status.render(status_text, True, (200, 200, 210))
    screen.blit(status, (origin_x, 56))

    # Grid lines
    line_color = (70, 80, 100)
    for i in range(1, 3):
        # vertical
        x = origin_x + i * cell
        pygame.draw.line(screen, line_color, (x, origin_y), (x, origin_y + 3 * cell), 3)
        # horizontal
        y = origin_y + i * cell
        pygame.draw.line(screen, line_color, (origin_x, y), (origin_x + 3 * cell, y), 3)

    font_cell = pygame.font.SysFont(None, 100)

    # Hover highlight
    if hover is not None:
        hr, hc = hover
        if 0 <= hr < 3 and 0 <= hc < 3 and board[hr][hc] == "":
            rect = pygame.Rect(origin_x + hc * cell + 2, origin_y + hr * cell + 2, cell - 4, cell - 4)
            pygame.draw.rect(screen, (40, 50, 65), rect)

    # Draw marks
    for r in range(3):
        for c in range(3):
            mark = board[r][c]
            if mark:
                text = font_cell.render(mark, True, (240, 240, 255))
                tr = text.get_rect(center=(origin_x + c * cell + cell // 2, origin_y + r * cell + cell // 2))
                screen.blit(text, tr)

    # Footer controls
    font_foot = pygame.font.SysFont(None, 22)
    footer = font_foot.render("Click to play. R: restart  |  H: human first  |  A: AI first  |  ESC: quit", True, (180, 190, 205))
    screen.blit(footer, (origin_x, origin_y + 3 * cell + 16))


def get_cell_from_mouse(pos: Tuple[int, int], screen_size: Tuple[int, int]) -> Optional[Tuple[int, int]]:
    W, H = screen_size
    margin = 80
    grid = min(W, H - margin)
    cell = grid // 3
    origin_x = (W - grid) // 2
    origin_y = (H - margin - grid) // 2 + margin
    mx, my = pos
    if not (origin_x <= mx < origin_x + grid and origin_y <= my < origin_y + grid):
        return None
    c = (mx - origin_x) // cell
    r = (my - origin_y) // cell
    return int(r), int(c)


def main():
    pygame.init()
    screen = pygame.display.set_mode((520, 600))
    pygame.display.set_caption("Tic-Tac-Toe (Minimax with Alpha-Beta)")
    clock = pygame.time.Clock()

    board: Board = [["" for _ in range(3)] for _ in range(3)]
    human = 'X'
    ai = 'O'
    human_turn = True  # human starts by default
    game_over = False
    status_text = "Your turn"
    hover_cell: Optional[Tuple[int, int]] = None

    def reset(start_human: bool):
        nonlocal board, human_turn, game_over, status_text
        board = [["" for _ in range(3)] for _ in range(3)]
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
                hover_cell = get_cell_from_mouse(pygame.mouse.get_pos(), screen.get_size())
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game_over or not human_turn:
                    continue
                cell = get_cell_from_mouse(pygame.mouse.get_pos(), screen.get_size())
                if cell is None:
                    continue
                r, c = cell
                if board[r][c] == "":
                    board[r][c] = human
                    winner = check_winner(board)
                    if winner or is_full(board):
                        game_over = True
                        if winner == human:
                            status_text = "You win! Press R/H/A to restart."
                        elif winner == ai:
                            status_text = "AI wins! Press R/H/A to restart."
                        else:
                            status_text = "Draw! Press R/H/A to restart."
                    else:
                        human_turn = False
                        status_text = "AI thinking..."

        if not game_over and not human_turn:
            move = best_ai_move(board)
            if move is not None:
                r, c = move
                board[r][c] = ai
            winner = check_winner(board)
            if winner or is_full(board):
                game_over = True
                if winner == human:
                    status_text = "You win! Press R/H/A to restart."
                elif winner == ai:
                    status_text = "AI wins! Press R/H/A to restart."
                else:
                    status_text = "Draw! Press R/H/A to restart."
            else:
                human_turn = True
                status_text = "Your turn"

        draw_board(screen, board, status_text, hover_cell)
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()