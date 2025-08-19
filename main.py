from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
import uuid
import random

app = FastAPI()

# --- Player State Model ---
class PlayerState(BaseModel):
    name: str
    total_score: int = 0

# --- Game State Model ---
class GameState(BaseModel):
    game_id: str
    players: List[PlayerState]  # [0] = human, [1] = AI
    current_player: int         # 0 = human, 1 = AI
    dice: List[int] = []        # Current dice values
    kept: List[int] = []        # Dice kept for scoring
    turn_score: int = 0         # Score for current turn
    finished: bool = False
    winner: Optional[int] = None  # 0 = human, 1 = AI

# In-memory store for games (for demo; use DB for production)
games: Dict[str, GameState] = {}

# --- Endpoint: Create New Game ---
@app.post('/game/new')
def create_game():
    game_id = str(uuid.uuid4())
    players = [PlayerState(name='Human'), PlayerState(name='AI')]
    game = GameState(
        game_id=game_id,
        players=players,
        current_player=0,  # Human starts
        dice=[0]*6,
        kept=[],
        turn_score=0,
        finished=False,
        winner=None
    )
    games[game_id] = game
    return {'game_id': game_id, 'game': game}

# --- Endpoint: Get Game State ---
@app.get('/game/{game_id}')
def get_game(game_id: str):
    game = games.get(game_id)
    if not game:
        raise HTTPException(status_code=404, detail='Game not found')
    return game

# --- Endpoint: Roll Dice ---
@app.post('/game/{game_id}/roll')
def roll_dice(game_id: str):
    game = games.get(game_id)
    if not game:
        raise HTTPException(status_code=404, detail='Game not found')
    if game.finished:
        raise HTTPException(status_code=400, detail='Game is finished')
    # Only allow rolling if it's the human's turn
    if game.current_player != 0:
        raise HTTPException(status_code=400, detail="It's not your turn")
    num_to_roll = 6 if len(game.dice) == 0 or all(d == 0 for d in game.dice) else game.dice.count(0)
    if num_to_roll == 0:
        num_to_roll = 6  # Hot dice: all dice scored, roll all 6 again
    new_dice = []
    for d in game.dice:
        if d == 0:
            new_dice.append(random.randint(1, 6))
        else:
            new_dice.append(d)
    if len(new_dice) < 6:
        new_dice += [random.randint(1, 6) for _ in range(6 - len(new_dice))]
    game.dice = new_dice
    return game

# --- Endpoint: Keep Dice ---
class KeepRequest(BaseModel):
    indices: List[int]  # Indices of dice to keep from the current roll

@app.post('/game/{game_id}/keep')
def keep_dice(game_id: str, req: KeepRequest):
    game = games.get(game_id)
    if not game:
        raise HTTPException(status_code=404, detail='Game not found')
    if game.finished:
        raise HTTPException(status_code=400, detail='Game is finished')
    if game.current_player != 0:
        raise HTTPException(status_code=400, detail="It's not your turn")
    if any(i < 0 or i >= len(game.dice) for i in req.indices):
        raise HTTPException(status_code=400, detail='Invalid dice indices')
    for i in req.indices:
        if game.dice[i] == 0:
            continue  # Already kept
        game.kept.append(game.dice[i])
        # Add to turn score (simple: 1=100, 5=50, 3 of a kind, etc. - scoring logic can be improved)
        if game.dice[i] == 1:
            game.turn_score += 100
        elif game.dice[i] == 5:
            game.turn_score += 50
        # (TODO: Add full scoring logic for triples, straights, etc.)
        game.dice[i] = 0
    return game

# --- Endpoint: Bank Points ---
@app.post('/game/{game_id}/bank')
def bank_points(game_id: str):
    game = games.get(game_id)
    if not game:
        raise HTTPException(status_code=404, detail='Game not found')
    if game.finished:
        raise HTTPException(status_code=400, detail='Game is finished')
    if game.current_player != 0:
        raise HTTPException(status_code=400, detail="It's not your turn")
    # Add turn score to current player's total
    game.players[game.current_player].total_score += game.turn_score
    # Check for win (e.g., 10,000 points)
    if game.players[game.current_player].total_score >= 10000:
        game.finished = True
        game.winner = game.current_player
    else:
        # Switch to AI turn (1)
        game.current_player = 1
        game.turn_score = 0
        game.kept = []
        game.dice = [0]*6
    return game

@app.get('/')
def read_root():
    return {'message': 'Welcome to the Zilch Dice Game API!'}