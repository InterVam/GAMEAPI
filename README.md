# Game Management API

A backend API for managing web-based games, built with FastAPI and Firebase.

## Features

- 🔐 JWT Authentication for admins and devices
- 🎮 Game management (CRUD operations)
- 📱 Device registration and management
- 🏷️ Game categorization (Educational, Fun, etc.)
- 🌐 RESTful API endpoints
- 🔥 Firebase Firestore integration
- 🐳 Docker support
- ☁️ Azure deployment ready

## Tech Stack

- **Framework**: FastAPI
- **Database**: Firebase Firestore
- **Authentication**: JWT
- **Validation**: Pydantic
- **Server**: Uvicorn
- **Containerization**: Docker

## Installation

### Prerequisites

- Python 3.9+
- Firebase project with Firestore
- Firebase Admin SDK credentials

1. Clone the repository:
```bash
git clone https://github.com/yourusername/game-management-api.git
cd game-management-api
```
2.Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```
3.Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create .env file:
```bash
SECRET_KEY=your_jwt_secret_key
FIREBASE_CREDENTIALS_BASE64=your_base64_encoded_firebase_credentials
```
5. Run the server:
```bash
uvicorn app.main:app --reload
```
API Documentation

Authentication

 Endpoint 
 Method 
 Description 
 /auth/signup 
 POST 
 Register new admin with device code 
 /auth/token 
 POST 
 Get admin JWT token 
 /auth/device 
 POST 
 Authenticate device 

Admin Endpoints

 Endpoint 
 Method 
 Description 
 /admin/games 
 GET 
 List all games 
 /admin/games 
 POST 
 Add new game 
 /admin/games/{id} 
 GET 
 Get specific game 
 /admin/games/{id} 
 PUT 
 Update game 
 /admin/games/{id} 
 DELETE 
 Delete game 
 /admin/games/{id}/toggle 
 PATCH 
 Toggle game availability 

Player Endpoints

 Endpoint 
 Method 
 Description 
 /player/games 
 GET 
 List playable games 
 /player/games/{id} 
 GET 
 Get specific playable game 
