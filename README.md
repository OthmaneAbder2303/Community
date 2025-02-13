# Chat App

## Overview
This is a simple real-time chat application built using Flask for the backend and Bootstrap for the frontend. The application allows users to register, log in, and engage in real-time conversations.

## Features
- User authentication (registration & login)
- Real-time chat functionality
- Responsive UI with Bootstrap
- Secure password handling
- Lightweight SQLite database

## Technologies Used
- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS (Bootstrap), JavaScript
- **Database:** SQLite

## Installation
### Prerequisites
Make sure you have **Python 3.x** installed on your machine.

### Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/OthmaneAbder2303/Community.git
   cd community
   ```
2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Run the application:
   ```sh
   python server.py
   ```
5. Open your browser and go to:
   ```
   http://127.0.0.1:5000
   ```

## Project Structure
```
COMMUNITY/
│-- static/
│   ├── css/
│   │   ├── register.css
│   │   ├── login.css
│   │   ├── chat.css
│   ├── js/
│   │   ├── script.js
│-- templates/
│   ├── login.html
│   ├── register.html
│   ├── chat.html
│-- app.py
│-- db_conn.py
│-- models.py
│-- server.py
│-- requirements.txt
│-- README.md
```

## Usage
- Open the **register page** (`/register`) to create an account.
- Log in to access the **chat room**.
- Start chatting in real time with other users.

