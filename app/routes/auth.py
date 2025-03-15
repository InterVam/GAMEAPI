# app/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.models import UserCreate, UserResponse, Token, DeviceAuth, DeviceAuthResponse
from app.services.auth_service import AuthService
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate):
    """Register a new user with device registration"""
    return await AuthService.create_user(user_data)

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login and get access token"""
    user = await AuthService.authenticate_user(form_data.username, form_data.password)
    
    access_token_expires = timedelta(minutes=30)
    access_token = AuthService.create_access_token(
        data={"sub": user.id, "type": "user"},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/device", response_model=DeviceAuthResponse)
async def authenticate_device(device_data: DeviceAuth):
    """Authenticate a device using its device code"""
    return await AuthService.authenticate_device(device_data.device_code)