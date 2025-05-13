# Monte-Carlo-Tree-Search
### Process
1. select
2. expansion
3. simulation
4. back-propagation

To make efficiently We use parallelization or introduce heuristic function, etc...

# Class

### Agent
- player_id
- select_move()

### GameState
- board
- whose_turn
- get_legal_moves()
- apply_move()
- get_winner()
- is_terminated()

### MCTS
- root
- run()
- select()
- simulation()
- backpropagate()

### Node
- parent
- children
- visits
- value
- GameState
- select()
- expand()
- update() (=backpropagate)
