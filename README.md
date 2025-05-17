# Beta-Gomoku

**Beta-Gomoku** is a Gomoku (Five-in-a-row) game featuring AI opponents powered by Monte Carlo Tree Search (MCTS). It provides simpler AI gameplay on Gomoku.
The name "Beta-Gomoku" is inspired by AlphaGo, emphasizing its simpler, "beta-level" AI and its focus on the game Gomoku.

## Features

* Play against AI or watch AI vs AI matches.
* Monte Carlo Tree Search algorithm.
* Configurable parallelism (`n_worker`) via command-line arguments.
* Console-based gameplay and visualization.

## Installation

```bash
git clone https://github.com/Yonaim/Beta-Gomoku.git
cd Beta-Gomoku
pip install -r requirements.txt
```

## Usage

```bash
make run    # single Thread
make root   # root parallelization
```
## License

MIT License. See `LICENSE` for details.
