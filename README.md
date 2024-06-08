# Social Networking API

# Overview
This project implements a RESTful API for a social networking application using Django Rest Framework. The API provides endpoints for user authentication, managing friend requests, searching for users, and listing friends and pending friend requests.

## Project Structure
```bash
social_network/
├── db.sqlite3 # SQLite database file
├── manage.py # Django management script
├── requirements.txt # File containing project dependencies
├── api/ # Django app
└── social_network/ # Django project settings
```
## Getting Started
Follow these steps to set up and run the project locally:

### 1.Clone the repository to your local machine:

```bash
git clone https://github.com/your-username/social-networking-api.git
```
### 2.Navigate to the project directory:
```bash
cd social-networking-api
```
### 3.Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac
# Or
.\venv\Scripts\activate  # For Windows
```
### 4.Install the project dependencies:
```bash
pip install -r requirements.txt
```
### 5.Apply database migrations:
```bash
python manage.py migrate
```
### 6.Run the development server:
```bash
python manage.py runserver
```
Access the API at `http://localhost:8000/api/`.


## API Endpoints
### User Authentication:
* `POST /api/login/`: User login with email and password.
* `POST /api/register/`: User signup with email (no OTP verification required).
### Friend Requests:
* `POST /api/send-friend-request/`: Send a friend request to another user.
* `POST /api/respond-friend-request/`: Respond to a friend request (accept/reject).
* `GET /api/list-friends/`: List all friends of the authenticated user.
* `GET /api/list-pending-requests/`: List pending friend requests received by the authenticated user.
### User Search:
* `GET /api/search/?query=<search-term>`: Search for users by email or name.
### Throttling
* The `FriendRequest` endpoints are throttled to limit users to a maximum of 3 requests per minute.
### Authentication
* User authentication is handled using token-based authentication.
* Users can obtain an authentication token by logging in with their email and password.

# Examples for each endpoint

## User Authentication
### User Login
* Endpoint: `POST /api/login/`
* Request Body:
```json
{
    "email": "user@example.com",
    "password": "password123"
}
```
* Response:
```json
{
    "token": "your-authentication-token"
}
```
## User Signup
* Endpoint: `POST /api/register/`
* Request Body:
```json
{
    "email": "newuser@example.com",
    "password": "newpassword123"
}
```
* Response:
```json

{
    "message": "User created successfully"
}
```
## Friend Requests
### Send Friend Request
* Endpoint: `POST /api/send-friend-request/`
* Request Body:
```json

{
    "to_user": 2
}
```
* Response:
```json

{
    "message": "Friend request sent successfully"
}
```
### Respond to Friend Request
* Endpoint: `POST /api/respond-friend-request/`
* Request Body:
```json

{
    "friend_request_id": 1,
    "action": "accept"
}
```
* Response:
```json

{
    "message": "Friend request accepted"
}
```
### List Friends
* Endpoint: `GET /api/list-friends/`
* Response:
```json

[
    {
        "id": 2,
        "username": "friend1",
        "email": "friend1@example.com"
    },
    {
        "id": 3,
        "username": "friend2",
        "email": "friend2@example.com"
    }
]
```
### List Pending Requests
* Endpoint: `GET /api/list-pending-requests/`
* Response:
```json

[
    {
        "id": 1,
        "from_user": {
            "id": 1,
            "username": "user1",
            "email": "user1@example.com"
        },
        "created_at": "2024-06-08T12:23:54Z"
    }
]
```
## User Search
### Search Users
* Endpoint: `GET /api/search/?query=am`
* Response:
```json
[
    {
        "id": 1,
        "username": "Amarendra",
        "email": "amarendra@example.com"
    },
    {
        "id": 2,
        "username": "Amar",
        "email": "amar@example.com"
    }
]
```
