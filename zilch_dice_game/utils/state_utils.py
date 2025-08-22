from typing import List, Tuple
import numpy as np

# Simple, initial action space scaffold:
#  - 0: keep nothing (placeholder/no-op)
#  - 1: keep first die (index 0) if any dice exist
# We'll expand this to enumerate valid scoring keeps later.

class ActionSpace:
    def __init__(self):
        # Static mapping for now; expand later
        self._actions: List[List[int]] = [
            [],      # keep nothing
            [0],     # keep first die
        ]

    def size(self) -> int:
        return len(self._actions)

    def all_actions(self) -> List[List[int]]:
        return list(self._actions)

    def index_to_action(self, idx: int) -> List[int]:
        if 0 <= idx < len(self._actions):
            return self._actions[idx]
        # Default to no-op if out of range
        return []


def encode_state(dice: List[int], turn_score: int, p0_score: int, p1_score: int, current_player: int) -> np.ndarray:
    """
    Encode the minimal observable game state into a fixed-size numeric vector.

    Args:
        dice: list of 6 ints (values 0-6 where 0 can represent 'no die')
        turn_score: current accumulated turn score
        p0_score: player 0 total score
        p1_score: player 1 total score
        current_player: 0 or 1
    Returns:
        np.ndarray[float32] of shape (10,)
    """
    dice_vec = list(dice)
    # Ensure fixed length of 6
    if len(dice_vec) < 6:
        dice_vec += [0] * (6 - len(dice_vec))
    else:
        dice_vec = dice_vec[:6]

    obs = [
        *dice_vec,
        int(turn_score),
        int(p0_score),
        int(p1_score),
        int(current_player),
    ]
    return np.array(obs, dtype=np.float32)


def basic_valid_actions(dice: List[int]) -> List[List[int]]:
    """
    Return a minimal set of candidate actions based on the current dice.
    For now, we expose two actions only: keep nothing, keep first die if present.
    This is a placeholder to be expanded with proper scoring-aware keeps.
    """
    actions = [[]]
    if len(dice) > 0:
        actions.append([0])
    return actions
