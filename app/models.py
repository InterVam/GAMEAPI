# app/models.py
from pydantic import BaseModel, EmailStr, HttpUrl, Field
from typing import List, Optional
from datetime import datetime

# Game Models
class GameBase(BaseModel):
    name: str
    url: HttpUrl
    description: str
    image_url : Optional[HttpUrl] = None
    
class GameCreate(GameBase):
    is_playable: bool = False
    
class Game(GameBase):
    id: str
    is_playable: bool
    
    class Config:
        orm_mode = True
        
class GameUpdate(BaseModel):
    name: Optional[str] = None
    url: Optional[HttpUrl] = None
    description: Optional[str] = None
    image_url: Optional[HttpUrl] = None
    is_playable: Optional[bool] = None
    
class GameList(BaseModel):
    games: List[Game]

# Auth Models
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    device_code: str
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class UserResponse(BaseModel):
    id: str
    email: EmailStr
    name: str
    device_code: str
    
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
# Device Models
class DeviceAuth(BaseModel):
    device_code: str
    
class DeviceAuthResponse(BaseModel):
    user_id: str
    name: str
    device_code: str
    token: str