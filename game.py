from board import initial_board, move_piece, remove_piece, count_pieces, SIZE
from rules import (simple_move, capture_move, captures_from, all_captures,
                   legal_moves, jumped_square, promote, opponent, owner)

NAMES = {"R": "Red", "B": "Black"}


def fmt(pos):
    return f"({pos[0]},{pos[1]})"


class Checkers:
    def __init__(self):
        self.board = initial_board()
        self.player = "R"
        self.chain_piece = None   # piece that must keep jumping in a multi-capture

    def print_board(self):
        print("\n    " + "  ".join(str(c) for c in range(SIZE)))
        for r, row in enumerate(self.board):
            print(f"{r}   " + " ".join(cell.ljust(2) for cell in row))

    def game_over_message(self):
        name, other = NAMES[self.player], NAMES[opponent(self.player)]
        if count_pieces(self.board, self.player) == 0:
            return f"{name} has no pieces left. {other} wins!"
        if not legal_moves(self.board, self.player):
            return f"{name} has no legal moves. {other} wins!"
        return None

    def read_move(self):
        """Returns ((sr, sc), (er, ec)), 'quit', or None on bad input."""
        prompt = f"{self.player}> "
        if self.chain_piece:
            prompt = f"{self.player} (continue from {self.chain_piece[0]} {self.chain_piece[1]})> "
        try:
            raw = input(prompt).strip().lower().split()
        except (EOFError, KeyboardInterrupt):
            print()
            return "quit"
        if raw in (["q"], ["quit"]):
            return "quit"
        if len(raw) != 4:
            print("Enter four coordinates: sr sc er ec (or q to quit).")
            return None
        try:
            sr, sc, er, ec = map(int, raw)
        except ValueError:
            print("Coordinates must be numbers.")
            return None
        if not all(0 <= x < SIZE for x in (sr, sc, er, ec)):
            print(f"Outside board. Use 0-{SIZE - 1}.")
            return None
        return (sr, sc), (er, ec)

    def validate(self, start, end):
        """Returns an error message, or None if the move is legal."""
        if owner(self.board[start[0]][start[1]]) != self.player:
            return "That is not your piece."
        if self.chain_piece and start != self.chain_piece:
            return f"You must continue capturing with the piece at {fmt(self.chain_piece)}."
        if capture_move(self.board, self.player, start, end):
            return None
        if all_captures(self.board, self.player):
            return "A capture is available - you must jump."
        if simple_move(self.board, self.player, start, end):
            return None
        return "Invalid move."

    def apply_move(self, start, end):
        """Performs a validated move and returns one feedback line."""
        name = NAMES[self.player]
        if capture_move(self.board, self.player, start, end):
            mid = jumped_square(start, end)
            move_piece(self.board, start, end)
            remove_piece(self.board, mid)
            msg = f"{name} captured {fmt(mid)}: {fmt(start)} -> {fmt(end)}."
            if promote(self.board, end):
                msg += " Promoted to king!"            # promotion ends the turn
            elif captures_from(self.board, self.player, end):
                self.chain_piece = end
                return msg + f" Jump again from {fmt(end)}."
        else:
            move_piece(self.board, start, end)
            msg = f"{name} moved {fmt(start)} -> {fmt(end)}."
            if promote(self.board, end):
                msg += " Promoted to king!"
        self.chain_piece = None
        self.player = opponent(self.player)
        return msg

    def run(self):
        print("Checkers - move: sr sc er ec  |  q to quit")
        while True:
            if self.chain_piece is None:
                result = self.game_over_message()
                if result:
                    self.print_board()
                    print(result)
                    return
            self.print_board()
            move = self.read_move()
            if move == "quit":
                print("Game ended by player.")
                return
            if move is None:
                continue
            start, end = move
            error = self.validate(start, end)
            if error:
                print(error)
                continue
            print(self.apply_move(start, end))
