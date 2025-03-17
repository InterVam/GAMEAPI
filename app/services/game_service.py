# app/services/game_service.py
from app.services.firebase import games_collection
from app.models import Game, GameCreate, GameUpdate
from typing import List, Optional
from datetime import datetime

class GameService:
    @staticmethod
    async def get_all_games() -> List[Game]:
        """Get all games from Firebase"""
        games_ref = games_collection.stream()
        games = []
        
        for game_doc in games_ref:
            game_data = game_doc.to_dict()
            game = Game(
                id=game_doc.id,
                name=game_data.get('name'),
                url=game_data.get('url'),
                description=game_data.get('description', ''),
                image_url=game_data.get('image_url'),
                is_active=game_data.get('is_active', False)
            )
            games.append(game)
            
        return games
    
    @staticmethod
    async def get_playable_games() -> List[Game]:
        """Get only playable games from Firebase"""
        games_ref = games_collection.where('is_active', '==', True).stream()
        games = []
        
        for game_doc in games_ref:
            game_data = game_doc.to_dict()
            game = Game(
                id=game_doc.id,
                name=game_data.get('name'),
                url=game_data.get('url'),
                description=game_data.get('description', ''),
                image_url=game_data.get('image_url'),
                is_active=game_data.get('is_active', True)
            )
            games.append(game)
            
        return games
    
    @staticmethod
    async def get_game_by_id(game_id: str) -> Optional[Game]:
        """Get a specific game by ID"""
        game_doc = games_collection.document(game_id).get()
        
        if not game_doc.exists:
            return None
            
        game_data = game_doc.to_dict()
        return Game(
            id=game_doc.id,
            name=game_data.get('name'),
            url=game_data.get('url'),
            description=game_data.get('description', ''),
            image_url=game_data.get('image_url'),
            is_active=game_data.get('is_active', False)
        )
    
    @staticmethod
    async def create_game(game: GameCreate) -> Game:
        """Create a new game in Firebase"""
        game_dict = game.dict()
        new_game_ref = games_collection.document()
        new_game_ref.set(game_dict)
        
        return Game(
            id=new_game_ref.id,
            **game_dict
        )
    
    @staticmethod
    async def update_game(game_id: str, game_update: GameUpdate) -> Optional[Game]:
        """Update an existing game"""
        game_ref = games_collection.document(game_id)
        game_doc = game_ref.get()
        
        if not game_doc.exists:
            return None
            
        update_data = {k: v for k, v in game_update.dict().items() if v is not None}
        
        if update_data:
            game_ref.update(update_data)
            
        updated_game = game_ref.get().to_dict()
        return Game(
            id=game_id,
            **updated_game
        )
    
    @staticmethod
    async def delete_game(game_id: str) -> bool:
        """Delete a game from Firebase"""
        game_ref = games_collection.document(game_id)
        game_doc = game_ref.get()
        
        if not game_doc.exists:
            return False
            
        game_ref.delete()
        return True
    
    @staticmethod
    async def toggle_game_playability(game_id: str) -> Optional[Game]:
        """Toggle the is_active status of a game"""
        game_ref = games_collection.document(game_id)
        game_doc = game_ref.get()
        
        if not game_doc.exists:
            return None
            
        game_data = game_doc.to_dict()
        current_status = game_data.get('is_active', False)
        
        # Toggle the status
        game_ref.update({'is_active': not current_status})
        
        # Get the updated game
        updated_game = game_ref.get().to_dict()
        return Game(
            id=game_id,
            **updated_game
        )