chess_board = [
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    [' ', '.', ' ', '.', ' ', '.', ' ', '.'],
    ['.', ' ', '.', ' ', '.', ' ', '.', ' '],
    [' ', '.', ' ', '.', ' ', '.', ' ', '.'],
    ['.', ' ', '.', ' ', '.', ' ', '.', ' '],
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
]

pieces = {
    'P': 'Pawn',
    'N': 'Knight',
    'B': 'Bishop',
    'R': 'Rook',
    'Q': 'Queen',
    'K': 'King'
}

# Define the rules for each piece
def pawn_moves(start_pos, end_pos, is_white):
    # Check if the pawn is moving forward
    if end_pos[0] == start_pos[0]:
        if is_white:
            # Check if the pawn is moving one or two squares forward
            if end_pos[1] == start_pos[1] + 1 or end_pos[1] == start_pos[1] + 2:
                return True
        else:
            # Check if the pawn is moving one or two squares forward
            if end_pos[1] == start_pos[1] - 1 or end_pos[1] == start_pos[1] - 2:
                return True
    # Check if the pawn is capturing a piece diagonally
    elif abs(end_pos[0] - start_pos[0]) == 1:
        if is_white:
            # Check if the pawn is capturing a black piece diagonally
            if end_pos[1] == start_pos[1] + 1:
                return True
        else:
            # Check if the pawn is capturing a white piece diagonally
            if end_pos[1] == start_pos[1] - 1:
                return True
    return False

def knight_moves(start_pos, end_pos):
    # Check if the knight is moving in an L-shape
    if abs(end_pos[0] - start_pos[0]) == 2 and abs(end_pos[1] - start_pos[1]) == 1:
        return True
    elif abs(end_pos[0] - start_pos[0]) == 1 and abs(end_pos[1] - start_pos[1]) == 2:
        return True
    return False


def bishop_moves(start_pos, end_pos):
    # Check if the bishop is moving diagonally
    if abs(end_pos[0] - start_pos[0]) == abs(end_pos[1] - start_pos[1]):
        # Check if there are any pieces in the way
        x_dir = 1 if end_pos[0] > start_pos[0] else -1
        y_dir = 1 if end_pos[1] > start_pos[1] else -1
        x = start_pos[0] + x_dir
        y = start_pos[1] + y_dir
        while x != end_pos[0] and y != end_pos[1]:
            if chess_board[x][y] != ' ':
                return False
            x += x_dir
            y += y_dir
        return True
    return False

def rook_moves(start_pos, end_pos):
    # Check if the rook is moving horizontally or vertically
    if end_pos[0] == start_pos[0] or end_pos[1] == start_pos[1]:
        # Check if there are any pieces in the way
        if end_pos[0] == start_pos[0]:
            x_dir = 0
            y_dir = 1 if end_pos[1] > start_pos[1] else -1
        else:
            x_dir = 1 if end_pos[0] > start_pos[0] else -1
            y_dir = 0
        x = start_pos[0] + x_dir
        y = start_pos[1] + y_dir
        while x != end_pos[0] or y != end_pos[1]:
            if chess_board[x][y] != ' ':
                return False
            x += x_dir
            y += y_dir
        return True
    return False

def queen_moves(start_pos, end_pos):
    # Check if the queen is moving horizontally, vertically, or diagonally
    if start_pos[0] == end_pos[0] or start_pos[1] == end_pos[1] or abs(end_pos[0] - start_pos[0]) == abs(end_pos[1] - start_pos[1]):
        # Check if there are any pieces in the way
        if start_pos[0] == end_pos[0]:
            x_dir = 0
        else:
            x_dir = 1 if end_pos[0] > start_pos[0] else -1
        if start_pos[1] == end_pos[1]:
            y_dir = 0
        else:
            y_dir = 1 if end_pos[1] > start_pos[1] else -1
        x = start_pos[0] + x_dir
        y = start_pos[1] + y_dir
        while x != end_pos[0] or y != end_pos[1]:
            if chess_board[x][y] != ' ':
                return False
            x += x_dir
            y += y_dir
        return True
    return False

def king_moves(start_pos, end_pos):
    # Check if the king is moving one square in any direction
    if abs(end_pos[0] - start_pos[0]) <= 1 and abs(end_pos[1] - start_pos[1]) <= 1:
        return True
    # Check if the king is castling
    elif abs(end_pos[1] - start_pos[1]) == 2 and start_pos[0] == end_pos[0]:
        # Check if the king and rook have not moved
        if start_pos == (0, 4) and end_pos == (0, 6) and not has_moved['K'] and not has_moved['R1']:
            # Check if the squares between the king and rook are empty
            if chess_board[0][5] == ' ' and chess_board[0][6] == ' ':
                return True
        elif start_pos == (0, 4) and end_pos == (0, 2) and not has_moved['K'] and not has_moved['R2']:
            # Check if the squares between the king and rook are empty
            if chess_board[0][1] == ' ' and chess_board[0][2] == ' ' and chess_board[0][3] == ' ':
                return True
        elif start_pos == (7, 4) and end_pos == (7, 6) and not has_moved['k'] and not has_moved['r1']:
            # Check if the squares between the king and rook are empty
            if chess_board[7][5] == ' ' and chess_board[7][6] == ' ':
                return True
        elif start_pos == (7, 4) and end_pos == (7, 2) and not has_moved['k'] and not has_moved['r2']:
            # Check if the squares between the king and rook are empty
            if chess_board[7][1] == ' ' and chess_board[7][2] == ' ' and chess_board[7][3] == ' ':
                return True
    return False

# Define the rules for the game
def is_valid_move(piece, start_pos, end_pos):
    # Check if the starting and ending positions are on the board
    if start_pos[0] < 0 or start_pos[0] > 7 or start_pos[1] < 0 or start_pos[1] > 7:
        return False
    if end_pos[0] < 0 or end_pos[0] > 7 or end_pos[1] < 0 or end_pos[1] > 7:
        return False
    # Check if the starting position is not the same as the ending position
    if start_pos == end_pos:
        return False
    # Check if the piece is moving to a square occupied by a piece of the same color
    if chess_board[end_pos[0]][end_pos[1]] != ' ' and chess_board[end_pos[0]][end_pos[1]].isupper() == piece.isupper():
        return False
    # Check if the move is valid for the given piece
    if piece == 'P':
        # Check if the pawn is moving one or two squares forward
        if end_pos[1] == start_pos[1] and chess_board[end_pos[0]][end_pos[1]] == ' ':
            if (end_pos[0] - start_pos[0] == 1 and piece.isupper()) or (end_pos[0] - start_pos[0] == -1 and not piece.isupper()):
                # Check if the pawn has reached the opposite end of the board and needs to be promoted
                if end_pos[0] == 0 or end_pos[0] == 7:
                    return True, 'Q'
                else:
                    return True, None
            elif (end_pos[0] - start_pos[0] == 2 and piece.isupper() and start_pos[0] == 1 and chess_board[2][start_pos[1]] == ' ') or (end_pos[0] - start_pos[0] == -2 and not piece.isupper() and start_pos[0] == 6 and chess_board[5][start_pos[1]] == ' '):
                return True, None
        # Check if the pawn is capturing diagonally
        elif abs(end_pos[1] - start_pos[1]) == 1 and chess_board[end_pos[0]][end_pos[1]] != ' ':
            if (end_pos[0] - start_pos[0] == 1 and piece.isupper()) or (end_pos[0] - start_pos[0] == -1 and not piece.isupper()):
                # Check if the pawn has reached the opposite end of the board and needs to be promoted
                if end_pos[0] == 0 or end_pos[0] == 7:
                    return True, 'Q'
                else:
                    return True, None
            # Check if the pawn is capturing en passant
            elif end_pos[0] - start_pos[0] == 1 and piece.isupper() and start_pos[0] == 4 and last_move[1][1] == end_pos[1] and last_move[0][0] == 6 and last_move[1][0] == 4 and chess_board[4][end_pos[1]] == ' ' and chess_board[6][end_pos[1]] == 'p':
                return True, None
            elif end_pos[0] - start_pos[0] == -1 and not piece.isupper() and start_pos[0] == 3 and last_move[1][1] == end_pos[1] and last_move[0][0] == 1 and last_move[1][0] == 3 and chess_board[3][end_pos[1]] == ' ' and chess_board[1][end_pos[1]] == 'P':
                return True, None
    elif piece == 'N':
        return knight_moves(start_pos, end_pos), None
    elif piece == 'B':
        return bishop_moves(start_pos, end_pos), None
    elif piece == 'R':
        return rook_moves(start_pos, end_pos), None
    elif piece == 'Q':
        return queen_moves(start_pos, end_pos), None
    elif piece == 'K':
        # Check if the king is castling
        if abs(end_pos[1] - start_pos[1]) == 2:
            if is_castling_allowed(piece, start_pos, end_pos):
                return True, None
            else:
                return False, None
        else:
            return king_moves(start_pos, end_pos), None
    return False, None

def is_checkmate():
    # Check if the current player is in check
    if is_check():
        # Check if the current player has any valid moves
        for i in range(8):
            for j in range(8):
                if chess_board[i][j] != ' ' and chess_board[i][j].isupper() == is_white_turn:
                    for k in range(8):
                        for l in range(8):
                            if is_valid_move(chess_board[i][j], (i, j), (k, l)):
                                # If the current player has a valid move, the game is not in checkmate
                                return False
        # If the current player has no valid moves, the game is in checkmate
        return True
    # If the current player is not in check, the game is not in checkmate
    return False

def is_stalemate():
    # Check if the current player is not in check
    if not is_check():
        # Check if the current player has any valid moves
        for i in range(8):
            for j in range(8):
                if chess_board[i][j] != ' ' and chess_board[i][j].isupper() == is_white_turn:
                    for k in range(8):
                        for l in range(8):
                            if is_valid_move(chess_board[i][j], (i, j), (k, l)):
                                # If the current player has a valid move, the game is not in stalemate
                                return False
        # If the current player has no valid moves, the game is in stalemate
        return True
    # If the current player is in check, the game is not in stalemate
    return False

def switch_players():
    global is_white_turn
    is_white_turn = not is_white_turn

def display_board():
    print("   A  B  C  D  E  F  G  H")
    print("  ------------------------")
    for i in range(8):
        print(str(8 - i) + " |", end="")
        for j in range(8):
            print(chess_board[i][j] + "|", end="")
        print(" " + str(8 - i))
        print("  ------------------------")
    print("   A  B  C  D  E  F  G  H")

def is_check(color):
    # Find the position of the king of the given color
    for i in range(8):
        for j in range(8):
            if chess_board[i][j] == 'K' and chess_board[i][j].isupper() == color:
                king_pos = (i, j)
                break
    # Check if any of the opponent's pieces can attack the king
    for i in range(8):
        for j in range(8):
            if chess_board[i][j] != ' ' and chess_board[i][j].isupper() != color:
                if is_valid_move(chess_board[i][j], (i, j), king_pos)[0]:
                    return True
    return False

def is_castling_allowed(piece, start_pos, end_pos):
    # Check if the king and rook have not moved
    if piece == 'K' and start_pos == (7, 4) and end_pos == (7, 6) and not has_king_moved and not has_kingside_rook_moved:
        # Check if the squares between the king and rook are empty and not under attack
        if chess_board[7][5] == ' ' and chess_board[7][6] == ' ' and not is_check(True) and not is_check(False):
            return True
    elif piece == 'K' and start_pos == (7, 4) and end_pos == (7, 2) and not has_king_moved and not has_queenside_rook_moved:
        # Check if the squares between the king and rook are empty and not under attack
        if chess_board[7][1] == ' ' and chess_board[7][2] == ' ' and chess_board[7][3] == ' ' and not is_check(True) and not is_check(False):
            return True
    elif piece == 'k' and start_pos == (0, 4) and end_pos == (0, 6) and not has_king_moved and not has_kingside_rook_moved:
        # Check if the squares between the king and rook are empty and not under attack
        if chess_board[0][5] == ' ' and chess_board[0][6] == ' ' and not is_check(True) and not is_check(False):
            return True
    elif piece == 'k' and start_pos == (0, 4) and end_pos == (0, 2) and not has_king_moved and not has_queenside_rook_moved:
        # Check if the squares between the king and rook are empty and not under attack
        if chess_board[0][1] == ' ' and chess_board[0][2] == ' ' and chess_board[0][3] == ' ' and not is_check(True) and not is_check(False):
            return True
    return False