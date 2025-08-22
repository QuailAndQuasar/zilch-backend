from dataclasses import dataclass


@dataclass
class RLConfig:
    # Q-learning hyperparameters
    alpha: float = 0.1           # learning rate
    gamma: float = 0.9           # discount factor
    epsilon_start: float = 1.0   # initial exploration
    epsilon_min: float = 0.01    # minimum exploration
    epsilon_decay: float = 0.999 # decay per step

    # Training settings
    episodes: int = 1000
    max_steps_per_episode: int = 200

    # Persistence
    model_path: str = "./q_table.json"


default_config = RLConfig()

