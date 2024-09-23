import random
import numpy as np

# Make an empty board
board = [' ' for _ in range(10)]  # index 0 is ignored for simplicity

# Initialize Q-table as a dictionary
Q = {}  # Key: state (tuple of board), Value: list of Q-values for each action

# Define Q-learning parameters
learning_rate = 0.1  # α
discount_factor = 0.9  # γ
exploration_rate = 1.0  # ε (starts at 100% exploration)
exploration_decay = 0.995  # Decay ε after each episode
min_exploration_rate = 0.01  # Minimum value for ε

# Set to value of rewards for win, draw, and loss
reward_win = 1
reward_loss = -1
reward_draw = 0.5

def reset_board():
    return [' ' for _ in range(10)]

def get_state(board):
    # Convert the board into a tuple that can be used as a key in Q-table
    return tuple(board[1:])

def choose_action(state, possible_moves):
    # Exploration vs Exploitation
    if random.uniform(0, 1) < exploration_rate:
        # Explore: Choose a random move
        return random.choice(possible_moves)
    else:
        # Exploit:Choose the move with the highest Q-value
        if state in Q:
            q_values = Q[state]
            max_q_value = max([q_values[i] for i in possible_moves])
            best_moves = [i for i in possible_moves if q_values[i] == max_q_value]
            return random.choice(best_moves)
        else:
            # If state not in Q, choose the moves randomly
            return random.choice(possible_moves)

def update_q_table(state, action, reward, next_state):
    if state not in Q:
        Q[state] = [0] * 9  # Initialize Q-values for this state (one for each action)

    if next_state not in Q:
        Q[next_state] = [0] * 9

    # Update Q-value using the Bellman Equation that is most important in this program
    best_future_q = max(Q[next_state])  # Best possible Q-value for the next state
    Q[state][action - 1] = (1 - learning_rate) * Q[state][action - 1] + \
        learning_rate * (reward + discount_factor * best_future_q)

def insertLetter(letter, pos):
    board[pos] = letter

def spaceIsFree(pos):
    return board[pos] == ' '

def printBoard(board):
    rows = [
        f' {board[1]} | {board[2]} | {board[3]} ',
        f' {board[4]} | {board[5]} | {board[6]} ',
        f' {board[7]} | {board[8]} | {board[9]} '
    ]
    
    separator = '-----------'  # Single dashes for uniform alignment
    
    for i in range(3):
        print('   |   |   ')  # Spaced correctly for alignment
        print(rows[i])        # Print the current row
        print('   |   |   ')  # Bottom part of each cell
        if i < 2:  # Avoid printing the separator after the last row
            print(separator)


def isWinner(bo, le):
    # List of all possible winning combinations
    winning_combinations = [
        (7, 8, 9),  # Top row
        (4, 5, 6),  # Middle row
        (1, 2, 3),  # Bottom row
        (1, 4, 7),  # Left column
        (2, 5, 8),  # Middle column
        (3, 6, 9),  # Right column
        (1, 5, 9),  # Diagonal (top-left to bottom-right)
        (3, 5, 7)   # Diagonal (top-right to bottom-left)
    ]
    
    # Check if any of the winning combinations is satisfied
    return any(bo[a] == le and bo[b] == le and bo[c] == le for a, b, c in winning_combinations)


def playerMove():
    run = True
    while run:
        move = input("Please select a position to place an 'X' (1-9): ")
        try:
            move = int(move)
            if move > 0 and move < 10:
                if spaceIsFree(move):
                    run = False
                    insertLetter('X', move)
                else:
                    print("Sorry, this space is occupied!")
            else:
                print("Please type a number within the range!")
        except:
            print("Please type a number!")

def update_q_table(state, action, reward, next_state):
    # Initialize Q-values if state is new
    if state not in Q:
        Q[state] = [0] * 9  # Initialize Q-values for this state

    if next_state not in Q:
        Q[next_state] = [0] * 9

    # Update Q-value using the Bellman Equation
    best_future_q = max(Q[next_state])  # Best possible Q-value for the next state
    Q[state][action - 1] = (1 - learning_rate) * Q[state][action - 1] + \
        learning_rate * (reward + discount_factor * best_future_q)

def compMove():
    state = get_state(board)
    possibleMoves = [x for x, letter in enumerate(board) if letter == ' ' and x != 0]
 # Check if there are no possible moves (i.e., the game is a tie)
    if not possibleMoves:
        return 0 
    # No move possible, return 0 to indicate a tie
  
    # Check for immediate winning move
    for move in possibleMoves:
        board[move] = 'O'  # Simulate AI move
        if isWinner(board, 'O'):
            insertLetter('O', move)
            reward = reward_win
            next_state = get_state(board)
            update_q_table(state, move, reward, next_state)
            return move
        board[move] = ' '  # Undo move

    # Check if player can win and block it
    for move in possibleMoves:
        board[move] = 'X'  # Simulate player move
        if isWinner(board, 'X'):
            insertLetter('O', move)  # Block player
            reward = reward_draw  # Reward for blocking
            next_state = get_state(board)
            update_q_table(state, move, reward, next_state)
            return move
        board[move] = ' '  # Undo move

    # If no immediate win/block, use Q-learning to choose the best move
    move = choose_action(state, possibleMoves)
    insertLetter('O', move)

    # Check the result of the move
    if isWinner(board, 'O'):
        reward = reward_win
    elif isWinner(board, 'X'):
        reward = reward_loss
    elif isBoardFull(board):
        reward = reward_draw
    else:
        reward = 0  # Game is not over yet

    next_state = get_state(board)
    # Update Q-table with the result of the move
    update_q_table(state, move, reward, next_state)
    return move

# Modify the rewards to be more strategic
reward_win = 10      # High reward for winning
reward_loss = -10    # High penalty for losing
reward_draw = 0.5    # Neutral reward for a draw


def isBoardFull(board):
    return board.count(' ') <= 1

def main():
    global board,exploration_rate
    play_again = 'y'
    
    while play_again.lower() == 'y':
        board = reset_board()  # Reset board at the start of each new game
        print("Welcome to Tic Tac Toe!")
        printBoard(board)

        while not isBoardFull(board):
         if not isWinner(board, 'O'):
            playerMove()
            printBoard(board)
         else:
            print("Sorry, Agent won this time!")
            break

         if not isWinner(board, 'X'):
            move =compMove()
            if move == 0:
                print("Tie Game!")
                
            else:
                print(f"Computer placed an 'O' in position {move}:")
                printBoard(board)
         else:
            print("You won this time! Congratulations!")
            break

    if   isBoardFull(board):
        print("Tie game!")

    # Decay exploration rate after each episode
    if exploration_rate > min_exploration_rate:
        exploration_rate *= exploration_decay
        
     # Ask if the player wants to play again
    play_again = True

if __name__ == "__main__":
    main()
1
