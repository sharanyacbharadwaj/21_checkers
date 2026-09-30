from board import SIZE, in_bounds

KING_DIRS = [(-1, -1), (-1, 1), (1, -1), (1, 1)]


def owner(piece):
    """'R' or 'B' for a piece, None for an empty square."""
    return None if piece == "." else piece[0]


def is_king(piece):
    return piece.endswith("K")


def opponent(player):
    return "B" if player == "R" else "R"


def move_directions(piece):
    """Kings move both ways; men move forward only (Red up, Black down)."""
    if is_king(piece):
        return KING_DIRS
    dr = -1 if owner(piece) == "R" else 1
    return [(dr, -1), (dr, 1)]


def simple_move(board, player, start, end):
    sr, sc = start
    er, ec = end
    piece = board[sr][sc]
    if owner(piece) != player or not in_bounds(er, ec) or board[er][ec] != ".":
        return False
    return (er - sr, ec - sc) in move_directions(piece)


def capture_move(board, player, start, end):
    sr, sc = start
    er, ec = end
    piece = board[sr][sc]
    if owner(piece) != player or not in_bounds(er, ec) or board[er][ec] != ".":
        return False
    dr, dc = er - sr, ec - sc
    if abs(dr) != 2 or abs(dc) != 2:
        return False
    if (dr // 2, dc // 2) not in move_directions(piece):
        return False
    jumped = board[sr + dr // 2][sc + dc // 2]
    return owner(jumped) == opponent(player)   # never your own piece or king


def jumped_square(start, end):
    return ((start[0] + end[0]) // 2, (start[1] + end[1]) // 2)


def captures_from(board, player, start):
    sr, sc = start
    piece = board[sr][sc]
    if owner(piece) != player:
        return []
    return [(sr + 2 * dr, sc + 2 * dc) for dr, dc in move_directions(piece)
            if capture_move(board, player, start, (sr + 2 * dr, sc + 2 * dc))]


def simple_moves_from(board, player, start):
    sr, sc = start
    piece = board[sr][sc]
    if owner(piece) != player:
        return []
    return [(sr + dr, sc + dc) for dr, dc in move_directions(piece)
            if simple_move(board, player, start, (sr + dr, sc + dc))]


def all_captures(board, player):
    return [((r, c), end)
            for r in range(SIZE) for c in range(SIZE)
            for end in captures_from(board, player, (r, c))]


def legal_moves(board, player):
    """Forced capture: if any capture exists, only captures are legal."""
    captures = all_captures(board, player)
    if captures:
        return captures
    return [((r, c), end)
            for r in range(SIZE) for c in range(SIZE)
            for end in simple_moves_from(board, player, (r, c))]


def promote(board, pos):
    """Promote the piece at pos if it reached its back row. Returns True if promoted."""
    r, c = pos
    piece = board[r][c]
    if piece == "R" and r == 0:
        board[r][c] = "RK"
        return True
    if piece == "B" and r == SIZE - 1:
        board[r][c] = "BK"
        return True
    return False
