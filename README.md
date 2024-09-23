# **TicTacToe**

This project involve tictactoe game which is completely based on Q learning algorithm in which player taking moves from q values .

* play against a computer that learns from each game.
- The computer uses Q-learning to improve its strategy over time.
- Simple and intuitive command-line interface.

## Requirements
- **python 3.12.8** 
- **Numpy**

``` def update_q_table(state, action, reward, next_state):
    if state not in Q:
        Q[state] = [0] * 9  # Initialize Q-values for this state
    if next_state not in Q:
        Q[next_state] = [0] * 9
    
    best_future_q = max(Q[next_state])
    Q[state][action - 1] = (1 - learning_rate) * Q[state][action - 1] + \
        learning_rate * (reward + discount_factor * best_future_q)
```
This code has the most crucial function which is known as Bellman Equation and that is used for updating q values.

*The game alternates between the player and the computer.
After every move, the game checks for a winner, updates the Q-table, and decays the exploration rate after each episode.*

### Gameplay Loop:

1. You make your move by entering a valid position number.
2. The game board is displayed after your move.
3. If you win or the board is full, the game ends.
4. If it's the AI's turn, it selects the best move based on its Q-table.
5. Te AI's move is displayed on the board.
6.  The game continues until a winner is declared or the board is full.

### Code Structure

- **main.py:** This is the main entry point as it initializes the board, Q-table, learning parameters, and runs the game loop.
- **q_learning_functions:** This functions helps to determine the q values based on iterations , such as get_state, choose_action, update_q_table, etc., for better organization.
- **tic_tac_toe_functions:** This file consists functions related to game mechanics, such as insertLetter, spaceIsFree, printBoard, isWinner, isBoardFull, etc.

### Learning Parameters

- learning_rate (alpha): Regulats how quickly the AI learns from new experiences.
- discount_factor (gamma): Weights the importance of future rewards.
- exploration_rate (epsilon): Decides how often to explore new moves vs. exploit learned knowledge.
- exploration_decay: As the AI gets more experienced, it gradually reduces exploration.
- min_exploration_rate:This Sets a minimum exploration rate to maintain some level of diversification.
- reward_win: Reward assigned when the AI wins.
- reward_loss: Reward assigned when the AI loses.
- reward_draw: Reward assigned when the game ends in a draw.

### Further Development

- Visualize the Q-table to see how it evolves as the AI learns.
- Train against different human playing styles to improve the AI's adaptability.
- Implement other game variations (e.g., Tic-Tac-Toe with larger boards).
#TicTacToe
