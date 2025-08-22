from __future__ import annotations
from typing import Dict, Tuple, List
import numpy as np
import json
import os

from ..utils.state_utils import ActionSpace


def _discretize_state(state: np.ndarray) -> Tuple[int, ...]:
    """
    Convert continuous/float observation to a discrete key for the Q-table.
    For now we just cast to int per component.
    """
    return tuple(int(x) for x in state.tolist())


class ZilchRLAgent:
    def __init__(
        self,
        action_space: ActionSpace,
        alpha: float = 0.1,
        gamma: float = 0.9,
        epsilon: float = 1.0,
        epsilon_min: float = 0.01,
        epsilon_decay: float = 0.999,
    ) -> None:
        self.action_space = action_space
        # Learning rate: how strongly we move current Q toward the target
        self.alpha = alpha
        # Discount factor: how much we value future rewards
        self.gamma = gamma
        # Exploration parameters for epsilon-greedy policy
        self.epsilon = epsilon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        # Q-table mapping: state (discrete tuple) -> list of action values
        self.q_table: Dict[Tuple[int, ...], List[float]] = {}

    def _ensure_state(self, state_key: Tuple[int, ...]) -> None:
        if state_key not in self.q_table:
            # Initialize Q-values to zeros for all actions
            self.q_table[state_key] = [0.0 for _ in range(self.action_space.size())]

    def choose_action(self, state: np.ndarray) -> int:
        """Epsilon-greedy action selection."""
        state_key = _discretize_state(state)
        self._ensure_state(state_key)

        # Explore with probability epsilon, otherwise exploit best-known action
        if np.random.rand() < self.epsilon:
            return np.random.randint(0, self.action_space.size())

        q_values = self.q_table[state_key]
        # Argmax over actions to pick the greedy action
        return int(np.argmax(q_values))

    def update(self, state: np.ndarray, action: int, reward: float, next_state: np.ndarray, done: bool) -> None:
        state_key = _discretize_state(state)
        next_key = _discretize_state(next_state)
        self._ensure_state(state_key)
        self._ensure_state(next_key)

        # Q-learning target = r + gamma * max_a' Q(s', a') (0 if terminal)
        q_current = self.q_table[state_key][action]
        max_next = 0.0 if done else max(self.q_table[next_key])
        target = reward + self.gamma * max_next
        # Incremental update toward target
        self.q_table[state_key][action] = q_current + self.alpha * (target - q_current)

        # Decay exploration
        # Gradually shift from exploring to exploiting learned values
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
            if self.epsilon < self.epsilon_min:
                self.epsilon = self.epsilon_min

    def save(self, path: str) -> None:
        # Persist epsilon and Q-table to JSON (simple baseline persistence)
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w") as f:
            json.dump({"epsilon": self.epsilon, "q_table": self.q_table}, f)

    def load(self, path: str) -> None:
        if not os.path.exists(path):
            return
        with open(path, "r") as f:
            data = json.load(f)
        self.epsilon = float(data.get("epsilon", self.epsilon))
        # Keys come back as strings; convert to tuples of ints
        raw_q = data.get("q_table", {})
        parsed: Dict[Tuple[int, ...], List[float]] = {}
        for k, v in raw_q.items():
            # Handle keys serialized by default tuple->string
            if isinstance(k, str):
                parts = k.strip("() ").split(",")
                key_tuple = tuple(int(p) for p in parts if p.strip() != "")
            else:
                key_tuple = tuple(k)
            parsed[key_tuple] = list(v)
        self.q_table = parsed
