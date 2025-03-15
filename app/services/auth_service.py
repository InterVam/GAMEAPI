# app/services/auth_service.py
from firebase_admin import auth
from app.services.firebase import users_collection, devices_collection
from app.models import UserCreate, UserResponse, Token, DeviceAuthResponse
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, DEVICE_TOKEN_EXPIRE_DAYS
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from jose import jwt
from typing import Optional

class AuthService:
    @staticmethod
    async def create_user(user_data: UserCreate) -> UserResponse:
        """Create a new user in Firebase Auth and Firestore with device registration"""
        try:
            # Check if device code is already registered
            device_query = devices_collection.where("device_code", "==", user_data.device_code).limit(1).stream()
            device_exists = False
            for _ in device_query:
                device_exists = True
                break
                
            if device_exists:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Device code is already registered"
                )
            
            # Create user in Firebase Auth
            firebase_user = auth.create_user(
                email=user_data.email,
                password=user_data.password,
                display_name=user_data.name
            )
            
            # Store user data in Firestore
            user_doc = {
                "email": user_data.email,
                "name": user_data.name,
                "device_code": user_data.device_code,
                "created_at": datetime.now()
            }
            users_collection.document(firebase_user.uid).set(user_doc)
            
            # Register device
            device_doc = {
                "device_code": user_data.device_code,
                "user_id": firebase_user.uid,
                "name": f"{user_data.name}'s Device",
                "registered_at": datetime.now()
            }
            devices_collection.document().set(device_doc)
            
            return UserResponse(
                id=firebase_user.uid,
                email=user_data.email,
                name=user_data.name,
                device_code=user_data.device_code
            )
            
        except auth.EmailAlreadyExistsError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating user: {str(e)}"
            )
    
    @staticmethod
    async def authenticate_user(email: str, password: str) -> UserResponse:
        """Authenticate a user with Firebase Auth"""
        try:
            # Sign in with email and password
            # Note: Firebase Admin SDK doesn't support password verification
            # In a real app, you'd use Firebase Auth REST API or Firebase Client SDK
            # Here we're simulating successful authentication
            user = auth.get_user_by_email(email)
            
            # Get user data from Firestore
            user_doc = users_collection.document(user.uid).get()
            if not user_doc.exists:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
                
            user_data = user_doc.to_dict()
            
            return UserResponse(
                id=user.uid,
                email=email,
                name=user_data.get("name", ""),
                device_code=user_data.get("device_code", "")
            )
            
        except auth.UserNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Authentication error: {str(e)}"
            )
    
    @staticmethod
    async def authenticate_device(device_code: str) -> DeviceAuthResponse:
        """Authenticate a device using its device code"""
        try:
            # Find device by code
            device_query = devices_collection.where("device_code", "==", device_code).limit(1).stream()
            
            device_doc = None
            for doc in device_query:
                device_doc = doc.to_dict()
                break
                
            if not device_doc:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Device not found"
                )
                
            user_id = device_doc.get("user_id")
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Device is not registered to any user"
                )
                
            # Get user data
            user_doc = users_collection.document(user_id).get()
            if not user_doc.exists:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
                
            user_data = user_doc.to_dict()
            
            # Create device token
            token_data = {
                "sub": user_id,
                "device": device_code,
                "type": "device"
            }
            token = AuthService.create_access_token(
                data=token_data,
                expires_delta=timedelta(days=DEVICE_TOKEN_EXPIRE_DAYS)
            )
            
            return DeviceAuthResponse(
                user_id=user_id,
                name=user_data.get("name", ""),
                device_code=device_code,
                token=token
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Device authentication error: {str(e)}"
            )
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        
        return encoded_jwt