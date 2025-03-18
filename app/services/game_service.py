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
                category=game_data.get('category', ''),
                is_playable=game_data.get('is_playable', False)  # Changed to is_playable
            )
            games.append(game)
            
        return games
    
    @staticmethod
    async def get_playable_games() -> List[Game]:
        """Get only playable games from Firebase"""
        games_ref = games_collection.where('is_playable', '==', True).stream()  # Changed to is_playable
        games = []
        
        for game_doc in games_ref:
            game_data = game_doc.to_dict()
            game = Game(
                id=game_doc.id,
                name=game_data.get('name'),
                url=game_data.get('url'),
                description=game_data.get('description', ''),
                image_url=game_data.get('image_url'),
                category=game_data.get('category', ''),
                is_playable=game_data.get('is_playable', True)  # Changed to is_playable
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
            category=game_data.get('category', ''),
            is_playable=game_data.get('is_playable', False)  # Changed to is_playable
        )
    
    @staticmethod
    async def create_game(game: GameCreate) -> Game:
        """Create a new game in Firebase"""
        # Convert from model
        game_dict = game.dict()
        
        # Rename is_active to is_playable if needed
        if 'is_active' in game_dict and 'is_playable' not in game_dict:
            game_dict['is_playable'] = game_dict.pop('is_active')
            
        new_game_ref = games_collection.document()
        new_game_ref.set(game_dict)
        
        # Get the created game
        created_game = new_game_ref.get().to_dict()
        return Game(
            id=new_game_ref.id,
            name=created_game.get('name'),
            url=created_game.get('url'),
            description=created_game.get('description', ''),
            image_url=created_game.get('image_url'),
            category=created_game.get('category', ''),
            is_playable=created_game.get('is_playable', False)  # Changed to is_playable
        )
    
    @staticmethod
    async def update_game(game_id: str, game_update: GameUpdate) -> Optional[Game]:
        """Update an existing game"""
        game_ref = games_collection.document(game_id)
        game_doc = game_ref.get()
        
        if not game_doc.exists:
            return None
            
        # Convert from model
        update_data = {k: v for k, v in game_update.dict().items() if v is not None}
        
        # Rename is_active to is_playable if needed
        if 'is_active' in update_data and 'is_playable' not in update_data:
            update_data['is_playable'] = update_data.pop('is_active')
        
        if update_data:
            game_ref.update(update_data)
            
        # Get the updated game
        updated_game = game_ref.get().to_dict()
        return Game(
            id=game_id,
            name=updated_game.get('name'),
            url=updated_game.get('url'),
            description=updated_game.get('description', ''),
            image_url=updated_game.get('image_url'),
            category=updated_game.get('category', ''),
            is_playable=updated_game.get('is_playable', False)  # Changed to is_playable
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
        """Toggle the is_playable status of a game"""
        game_ref = games_collection.document(game_id)
        game_doc = game_ref.get()
        
        if not game_doc.exists:
            return None
            
        game_data = game_doc.to_dict()
        current_status = game_data.get('is_playable', False)  # Changed to is_playable
        
        # Toggle the status
        game_ref.update({'is_playable': not current_status})  # Changed to is_playable
        
        # Get the updated game
        updated_game = game_ref.get().to_dict()
        return Game(
            id=game_id,
            name=updated_game.get('name'),
            url=updated_game.get('url'),
            description=updated_game.get('description', ''),
            image_url=updated_game.get('image_url'),
            category=updated_game.get('category', ''),
            is_playable=updated_game.get('is_playable', False)  # Changed to is_playable
        )