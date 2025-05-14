# Monte-Carlo-Tree-Search
## Process
1. select
2. expansion
3. simulation
4. back-propagation

To make efficiently We use parallelization or introduce heuristic function, etc...

### Selection
Start from root R and select successive child nodes until a leaf node L is reached. The root is the current game state and a leaf is any node that has a potential child from which no simulation (playout) has yet been initiated.

### Expansion
Unless L ends the game decisively (e.g. win/loss/draw) for either player, create one (or more) child nodes and choose node C from one of them. Child nodes are any valid moves from the game position defined by L.

### Simulation
Complete one random playout from node C. This step is sometimes also called playout or rollout.

### Backpropagation
Use the result of the playout to update information in the nodes on the path from C to R.

## Policy & Strategy

### Tree policy (in Selection)
Determine how children are selected.

- UCB (Upper Confidence Bound)
- Progressive Bias: add heuristic to UCT

### Expansion strategy (in Expansion)
Determines how actions are selected. Also known as Untried-action selector.

- Uniform random
- Progressive Widening: heuristic-ranked

### Rollout policy (in Simulation)
Determines how to choose next move in simulation. Also known as Playout policy or Default policy.

- Uniform random

### Evaluation policy (in Simulation)
Determines when and how to perform value evaluation at the leat nodes instead of running full simulations.

- Value leaf
- Early cutoff
- Fixed-depth evaluation
- Progressive bias

### Backup strategy (in Backpropagation)
Determines how the result of the simulation is applied to the nodes.

(1) win-rate: A reward in [0, 1]
(2) zero-sum value: A reward in [-1, 1] 

To avoid a high probability of loss for the current player and favor safe, then (2) zero-sum value is the appropriate starategy.

# Class

For Game and UI.

## Game

### Agent
- player_id
- select_move()

### GameState
- board
- current_player
- get_legal_moves()
- apply_move()
- get_winner()
- is_terminated()

차후 최적화를 위해 bitset을 사용할 예정. (empty_cells 및 board)

### MCTS
- root
- time_limit
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
- expand()

## UI

### console_renderer
- draw()