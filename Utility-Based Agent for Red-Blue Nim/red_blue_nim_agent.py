import sys

class GameState:
    def __init__(self, red, blue):
        self.red = red
        self.blue = blue

    def is_game_over(self):
        return self.red == 0 or self.blue == 0

    def calculate_score(self):
        return 2 * self.red + 3 * self.blue

    def possible_moves(self, standard=True):
        moves = []
        if standard:
            if self.red >= 2:
                moves.append(('red', 2))
            if self.blue >= 2:
                moves.append(('blue', 2))
            if self.red >= 1:
                moves.append(('red', 1))
            if self.blue >= 1:
                moves.append(('blue', 1))
        else:
            if self.blue >= 1:
                moves.append(('blue', 1))
            if self.red >= 1:
                moves.append(('red', 1))
            if self.blue >= 2:
                moves.append(('blue', 2))
            if self.red >= 2:
                moves.append(('red', 2))
        return moves

    def make_move(self, move):
        color, count = move
        new_state = GameState(self.red, self.blue)
        if color == 'red':
            new_state.red -= count
        else:
            new_state.blue -= count
        return new_state

def evaluate_state(state, standard):
    if state.is_game_over():
        score = (state.red * 2) + (state.blue * 3)
        return score if standard else -score
    score = (state.red * 2) + (state.blue * 3)

    move_factor = len(state.possible_moves(standard))
    evaluation = score + (move_factor * 1) 
    return evaluation if standard else -evaluation

def minimax(state, depth, alpha, beta, is_maximizing, standard, limit_depth):
    if state.is_game_over():
        return None, state.calculate_score() if standard else -state.calculate_score()

    if limit_depth and depth == 0:
        return None, evaluate_state(state, standard)

    best_move = None
    moves = state.possible_moves(standard)

    if is_maximizing:
        max_eval = float('-inf')
        for move in moves:
            new_state = state.make_move(move)
            eval_value = minimax(new_state, depth - 1 if limit_depth else depth, alpha, beta, False, standard, limit_depth)[1]
            if eval_value > max_eval:
                max_eval = eval_value
                best_move = move
            alpha = max(alpha, eval_value)
            if beta <= alpha:
                break
        return best_move, max_eval
    else:
        min_eval = float('inf')
        for move in moves:
            new_state = state.make_move(move)
            eval_value = minimax(new_state, depth - 1 if limit_depth else depth, alpha, beta, True, standard, limit_depth)[1]
            if eval_value < min_eval:
                min_eval = eval_value
                best_move = move
            beta = min(beta, eval_value)
            if beta <= alpha:
                break
        return best_move, min_eval

def human_move(state):
    while True:
        try:
            # print(f"Current pile - Red: {state.red}, Blue: {state.blue}")
            user_input = input("Enter marbles to be removed e.g., 'red 1' or 'blue 2': ").lower().split()
            
            if len(user_input) != 2:
                print("Invalid format.")
                continue
                
            color, count = user_input[0], int(user_input[1])
            if color not in ['red', 'blue'] or count not in [1, 2]:
                print("Invalid input. Use 'red' or 'blue' with count 1 or 2.")
                continue

            current_count = state.red if color == 'red' else state.blue
            if count > current_count:
                print(f"Not enough {color} marbles.")
                continue

            return (color, count)

        except ValueError:
            print("Invalid input. Please try again.")

def main():
    if len(sys.argv) < 3:
        print("Usage: game.py <red-count> <blue-count> [mode] [first] [depth]")
        sys.exit(1)

    initial_red = int(sys.argv[1])
    initial_blue = int(sys.argv[2])
    
    mode = "standard" if len(sys.argv) <= 3 else sys.argv[3].lower()
    first_player = "computer" if len(sys.argv) <= 4 else sys.argv[4].lower()
    depth_limit = int(sys.argv[5]) if len(sys.argv) > 5 else None

    is_standard = mode == "standard"
    computer_starts = first_player == "computer"
    depth_restriction = depth_limit is not None

    game_state = GameState(initial_red, initial_blue)
    is_computer_turn = computer_starts

    while not game_state.is_game_over():
        print(f"\nCurrent pile: Red: {game_state.red}, Blue: {game_state.blue}")
        
        if is_computer_turn:
            print("\nComputer's turn...")
            best_move, _ = minimax(game_state, depth_limit if depth_restriction else float('inf'), float('-inf'), float('inf'), True, is_standard, depth_restriction)
            print(f"Computer takes {best_move[1]} {best_move[0]}")
            game_state = game_state.make_move(best_move)
        else:
            print("\nHuman's turn...")
            # Print available moves for the human player
            available_moves = game_state.possible_moves(is_standard)
            print("Available moves:")
            for move in available_moves:
                print(f"{move[0]} {move[1]}")

            user_move = human_move(game_state)
            game_state = game_state.make_move(user_move)
        
        is_computer_turn = not is_computer_turn

    final_score = game_state.calculate_score()
    print("\n" + "=" * 50)
    print("Game Over!")
    print(f"Final Pile: Red: {game_state.red}, Blue: {game_state.blue}")

    if is_computer_turn:
        print(f"{'Human' if is_standard else 'Computer'} wins! Score: {final_score}")
    else:
        print(f"{'Computer' if is_standard else 'Human'} wins! Score: {final_score}")

if __name__ == "__main__":
    main()
