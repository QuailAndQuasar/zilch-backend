import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_game():
    response = client.post('/game/new')
    assert response.status_code == 200
    data = response.json()
    assert 'game_id' in data
    assert 'game' in data
    game = data['game']
    assert len(game['players']) == 2
    assert game['players'][0]['name'] == 'Human'
    assert game['players'][1]['name'] == 'AI'
    assert game['players'][0]['total_score'] == 0
    assert game['players'][1]['total_score'] == 0
    assert game['current_player'] == 0
    assert game['winner'] is None
    assert len(game['dice']) == 6

def test_roll_dice_human_turn():
    response = client.post('/game/new')
    game_id = response.json()['game_id']
    response = client.post(f'/game/{game_id}/roll')
    assert response.status_code == 200
    game = response.json()
    assert game['current_player'] == 0
    assert len(game['dice']) == 6
    assert all(1 <= d <= 6 for d in game['dice'])

def test_roll_dice_ai_turn_forbidden():
    response = client.post('/game/new')
    game_id = response.json()['game_id']
    # Simulate banking to switch to AI turn
    client.post(f'/game/{game_id}/roll')
    client.post(f'/game/{game_id}/keep', json={'indices': [0]})
    client.post(f'/game/{game_id}/bank')
    # Now it's AI's turn, human cannot roll
    response = client.post(f'/game/{game_id}/roll')
    assert response.status_code == 400
    assert response.json()['detail'] == "It's not your turn"

def test_keep_dice_human_turn():
    response = client.post('/game/new')
    game_id = response.json()['game_id']
    client.post(f'/game/{game_id}/roll')
    response = client.post(f'/game/{game_id}/keep', json={'indices': [0]})
    assert response.status_code == 200
    game = response.json()
    assert game['kept']
    assert game['dice'][0] == 0
    assert game['current_player'] == 0

def test_bank_points_switches_to_ai():
    response = client.post('/game/new')
    game_id = response.json()['game_id']
    client.post(f'/game/{game_id}/roll')
    client.post(f'/game/{game_id}/keep', json={'indices': [0]})
    response = client.post(f'/game/{game_id}/bank')
    assert response.status_code == 200
    game = response.json()
    # After banking, it should be AI's turn
    assert game['current_player'] == 1
    assert game['turn_score'] == 0
    assert game['kept'] == []
    assert game['players'][0]['total_score'] >= 0
    assert game['players'][1]['total_score'] == 0
    assert game['winner'] is None 