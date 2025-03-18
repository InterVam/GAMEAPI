Game Management API



A robust backend API for managing and serving web-based games. Built with FastAPI and Firebase for a responsive, scalable gaming platform.



Overview



This API provides a comprehensive backend solution for managing a library of HTML5/JavaScript games. It supports two types of users:

Admins: Can add, update, delete, and toggle the availability of games

Players: Can access the library of available games through registered devices



The system uses Firebase for data storage and JWT for secure authentication.



Features



User Authentication

Admin login with JWT token generation

Device-based authentication for players

Secure password hashing



Game Management

Add new games with descriptions, URLs, and images

Categorize games (Educational, Fun, etc.)

Toggle game availability

Update game details

Delete games



Device Management

Register devices with unique codes

Associate devices with user accounts

Device-based access to games



Tech Stack



FastAPI: High-performance Python web framework

Firebase/Firestore: NoSQL database for data storage

Pydantic: Data validation and settings management

JWT: Secure authentication tokens

Uvicorn: ASGI server for hosting the API

Python 3.9+: Modern Python features



Installation



Prerequisites



Python 3.9 or higher

Firebase project with Firestore enabled

Firebase Admin SDK credentials



Setup



Clone the repository:

   git clone https://github.com/yourusername/game-management-api.git
   cd game-management-api



Set up a virtual environment:

   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate



Install dependencies:

   pip install -r requirements.txt



Create a .env file with the following variables:

   SECRET_KEY=your_secret_key_for_jwt
   FIREBASE_CREDENTIALS_BASE64=your_base64_encoded_firebase_credentials



   You can generate a base64 encoded version of your Firebase credentials with:

   base64 -w 0 path/to/firebase-credentials.json



Start the server:

   uvicorn app.main:app --reload



API Endpoints



Authentication



POST /auth/signup: Create a new admin user with a device code

POST /auth/token: Obtain an admin JWT token

POST /auth/device: Authenticate a device and get a device token



Admin Game Management



GET /admin/games: Get all games

POST /admin/games: Add a new game

GET /admin/games/{game_id}: Get a specific game

PUT /admin/games/{game_id}: Update a game

DELETE /admin/games/{game_id}: Delete a game

PATCH /admin/games/{game_id}/toggle: Toggle game playability

GET /admin/games/category/{category}: Get games by category



Player Endpoints



GET /player/games: Get all playable games

GET /player/games/{game_id}: Get a specific playable game



Data Models



Game



{
  "id": "string",
  "name": "string",
  "category": "string",
  "description": "string",
  "url": "string",
  "image_url": "string",
  "is_playable": boolean
}



User



{
  "id": "string",
  "email": "string",
  "name": "string"
}



Device



{
  "id": "string",
  "device_code": "string",
  "user_id": "string"
}



Deployment



Docker



A Dockerfile is included for containerized deployment:



docker build -t game-api .
docker run -p 8000:8000 -e SECRET_KEY=your_secret_key -e FIREBASE_CREDENTIALS_BASE64=your_base64_credentials game-api



Azure Deployment



The API can be easily deployed to Azure App Service:



az login
az webapp up --runtime PYTHON:3.9 --sku B1 --name your-app-name



Set the necessary environment variables in the Azure portal or using the Azure CLI:



az webapp config appsettings set --name your-app-name --resource-group your-resource-group --settings SECRET_KEY="your_secret_key" FIREBASE_CREDENTIALS_BASE64="your_base64_credentials"



Development



Running Tests



pytest



Code Quality



flake8 app
black app



Security Considerations



All passwords are hashed before storage

JWT tokens have a limited lifespan

Firebase credentials are never exposed to clients

CORS is configured to allow only specific origins



License



MIT



Contributing



Fork the repository

Create a feature branch: git checkout -b feature-name

Commit your changes: git commit -am 'Add some feature'

Push to the branch: git push origin feature-name

Submit a pull request






Sample Requests



Adding a Game (Admin)



POST /admin/games
Content-Type: application/json
Authorization: Bearer your_admin_token

{
  "name": "Mathivities",
  "category": "Educational",
  "description": "A math-based game for children to learn basic operations.",
  "url": "https://mathivities.netlify.app/category",
  "image_url": "https://example.com/images/mathivities.jpg",
  "is_playable": false
}



Getting Playable Games (Player)



GET /player/games
Authorization: Bearer your_device_token






Built with ❤️ for creating engaging educational gaming experiences.
