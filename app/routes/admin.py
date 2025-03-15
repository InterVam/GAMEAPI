# app/routes/admin.py
from fastapi import APIRouter, Depends, HTTPException, status
from app.models import Game, GameCreate, GameUpdate, GameList
from app.services.game_service import GameService
from app.dependencies import get_current_user_id

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/games", response_model=GameList)
async def get_all_games(user_id: str = Depends(get_current_user_id)):
    """Admin endpoint to get all games"""
    games = await GameService.get_all_games()
    return {"games": games}

@router.get("/games/{game_id}", response_model=Game)
async def get_game(game_id: str, user_id: str = Depends(get_current_user_id)):
    """Admin endpoint to get a specific game"""
    game = await GameService.get_game_by_id(game_id)
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game with ID {game_id} not found"
        )
    return game

@router.post("/games", response_model=Game, status_code=status.HTTP_201_CREATED)
async def create_game(game: GameCreate, user_id: str = Depends(get_current_user_id)):
    """Admin endpoint to create a new game"""
    return await GameService.create_game(game)

@router.put("/games/{game_id}", response_model=Game)
async def update_game(game_id: str, game_update: GameUpdate, user_id: str = Depends(get_current_user_id)):
    """Admin endpoint to update a game"""
    updated_game = await GameService.update_game(game_id, game_update)
    if not updated_game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game with ID {game_id} not found"
        )
    return updated_game

@router.delete("/games/{game_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_game(game_id: str, user_id: str = Depends(get_current_user_id)):
    """Admin endpoint to delete a game"""
    success = await GameService.delete_game(game_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game with ID {game_id} not found"
        )
    return None

@router.patch("/games/{game_id}/toggle", response_model=Game)
async def toggle_game_playability(game_id: str, user_id: str = Depends(get_current_user_id)):
    """Admin endpoint to toggle game playability"""
    updated_game = await GameService.toggle_game_playability(game_id)
    if not updated_game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game with ID {game_id} not found"
        )
    return updated_game