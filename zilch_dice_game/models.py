from pydantic import BaseModel
from typing import List, Optional

class PlayerState(BaseModel):
    name: str
    total_score: int = 0

class GameState(BaseModel):
    game_id: str
    players: List[PlayerState]  # [0] = human, [1] = AI
    current_player: int         # 0 = human, 1 = AI
    dice: List[int] = []        # Current dice values
    kept: List[int] = []        # Dice kept for scoring
    turn_score: int = 0         # Score for current turn
    finished: bool = False
    winner: Optional[int] = None  # 0 = human, 1 = AI

class KeepRequest(BaseModel):
    indices: List[int]  # Indices of dice to keep from the current roll