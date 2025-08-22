from typing import Dict, List, Tuple, Optional, Any, Union
import numpy as np
from ..models import GameState, PlayerState
from ..main import app  # We'll use the FastAPI app for game logic
from fastapi.testclient import TestClient
from ..utils.state_utils import encode_state, ActionSpace

class ZilchEnv:
    """
    A Gym-like environment for the Zilch dice game.
    This provides a clean interface for reinforcement learning.
    """
    
    def __init__(self):
        self.client = TestClient(app)
        self.action_space = ActionSpace()
        self.reset()
        
    def reset(self) -> np.ndarray:
        """Reset the environment to start a new game."""
        response = self.client.post("/new-game/")
        self.game_state = GameState(**response.json())
        response = self.client.post("/start/")
        self.game_state = GameState(**response.json())
        return self._get_observation()
    
    def step(self, action: Union[int, List[int]]) -> Tuple[np.ndarray, float, bool, Dict]:
        """Take an action in the environment."""
        if isinstance(action, int):
            dice_to_keep = self._decode_action(action)
        else:
            dice_to_keep = action
            
        try:
            response = self.client.post(
                "/keep/",
                json={"dice_indices": dice_to_keep}
            )
            self.game_state = GameState(**response.json())
            
            # Simplified reward and done logic
            reward = 0
            done = self.game_state.winner is not None
            
            return self._get_observation(), reward, done, {}
            
        except Exception as e:
            return self._get_observation(), -10, True, {"error": str(e)}
    
    def _get_observation(self) -> np.ndarray:
        """Convert the game state to a numerical observation."""
        return encode_state(
            dice=self.game_state.dice,
            turn_score=self.game_state.turn_score,
            p0_score=self.game_state.players[0].total_score,
            p1_score=self.game_state.players[1].total_score,
            current_player=self.game_state.current_player,
        )
    
    def _decode_action(self, action_idx: int) -> List[int]:
        """Convert an action index to dice indices to keep using ActionSpace."""
        return self.action_space.index_to_action(action_idx)
    
    def render(self, mode: str = 'human') -> None:
        """Render the current game state."""
        if mode == 'human':
            print(f"\n--- Turn {self.game_state.turn_count} ---")
            print(f"Dice: {self.game_state.dice}")
            print(f"Current player: {self.game_state.current_player}")
            print(f"Turn score: {self.game_state.turn_score}")
