import chess
from copy import copy
import typing


class Node:
    def __init__(self, board: chess.Board, positions: list):
        self.board = board
        self.positions = positions
        piece_map = piece_map_by_color(self.board, chess.WHITE)
        assert len(piece_map) == 1

        cur_position = chess.square_name(piece_map.popitem()[0])  # square of one white piece
        self.positions.append(cur_position)
        self.children = []

    def add_child(self, board: chess.Board):
        self.children.append(Node(board, copy(self.positions)))

    def safe_captures(self):
        moves = self.board.generate_legal_captures()
        moves = list(filter(lambda move: not self.board.is_attacked_by(chess.BLACK, move.to_square), moves))
        return moves

    def is_end(self):
        return len(self.board.piece_map()) == 1  # only one white piece should remain

    @staticmethod
    def push_switch(board, move):
        new_board = board.copy()
        new_board.push(move)
        new_board.push(chess.Move.null())  # skipping black's turn
        return new_board


class Tree:
    def __init__(self, root_board: chess.Board):
        self.root = Node(root_board, [])

    def start_traverse(self):
        self.traverse(self.root)

    def traverse(self, node):
        if node.is_end():
            print(node.positions)
            return

        Tree.add_children(node)
        for child in node.children:
            self.traverse(child)

    @staticmethod
    def add_children(node):
        moves = node.safe_captures()
        for move in moves:
            node.add_child(Node.push_switch(node.board, move))


def piece_map_by_color(board: chess.Board, color: chess.Color):
    """
    Gets a dictionary of :class:`pieces <chess.Piece>` by square index.
    """
    result = {}
    for square in chess.scan_reversed(board.occupied_co[color]):
        result[square] = typing.cast(chess.Piece, board.piece_at(square))
    return result


def main(fen):
    board = chess.Board(fen)
    tree = Tree(board)
    tree.start_traverse()


if __name__ == '__main__':
    fen = '8/n1pp2Rp/n2p3n/b6p/n1n4n/3n3b/2b4n/8 w - - 0 1'
    main(fen)
