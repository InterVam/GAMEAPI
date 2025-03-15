# app/routes/player.py
from fastapi import APIRouter, Depends, HTTPException, status
from app.models import Game, GameList
from app.services.game_service import GameService
from app.dependencies import validate_device_token

router = APIRouter(prefix="/player", tags=["player"])

@router.get("/games", response_model=GameList)
async def get_playable_games(device_info: dict = Depends(validate_device_token)):
    """Player endpoint to get only playable games"""
    games = await GameService.get_playable_games()
    return {"games": games}

@router.get("/games/{game_id}", response_model=Game)
async def get_playable_game(game_id: str, device_info: dict = Depends(validate_device_token)):
    """Player endpoint to get a specific playable game"""
    game = await GameService.get_game_by_id(game_id)
    
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game with ID {game_id} not found"
        )
        
    if not game.is_playable:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Game with ID {game_id} is not available for play"
        )
        
    return game