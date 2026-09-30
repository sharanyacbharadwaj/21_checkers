SIZE = 8


def initial_board():
    board = [["."] * SIZE for _ in range(SIZE)]
    for r in range(3):
        for c in range(SIZE):
            if (r + c) % 2 == 1:
                board[r][c] = "B"
    for r in range(5, 8):
        for c in range(SIZE):
            if (r + c) % 2 == 1:
                board[r][c] = "R"
    return board


def in_bounds(r, c):
    return 0 <= r < SIZE and 0 <= c < SIZE


def move_piece(board, start, end):
    board[end[0]][end[1]] = board[start[0]][start[1]]
    board[start[0]][start[1]] = "."


def remove_piece(board, pos):
    board[pos[0]][pos[1]] = "."


def count_pieces(board, player):
    return sum(1 for row in board for cell in row if cell != "." and cell[0] == player)
