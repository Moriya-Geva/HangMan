# Hangman - Python Client-Server Game

## Project Overview  
This project presents a classic Hangman game designed with a client-server architecture using Python. The client offers a simple and user-friendly console interface, enabling players to register, log in, and enjoy the game experience. On the backend, a Flask server manages all user data, game logic, word selection, and maintains persistent storage for player profiles and gameplay history.

## Key Components  
The project includes a backend server implemented as a Flask REST API which supports user authentication, manages the game’s core logic, distributes words for guessing, and handles data persistence. The client application is a Python console-based program that interacts with the server to facilitate gameplay, handle user input, and display game results. All user data and game statistics are stored in JSON files, ensuring persistence between sessions. Gameplay mechanics allow players to make up to seven incorrect guesses, visually represented by a progressively drawn hangman. Correct guesses reveal letters in the word, and the system updates player statistics accordingly.

## Project Structure  
```
Hangman/
├── client.py # Console client handling game interaction and user input
├── server.py # Flask server managing API endpoints, game logic, and data persistence
├── user.py # User class definition and serialization helpers
├── users.json # Persistent storage of user profiles and statistics in JSON format
├── word_bank/ # Directory containing word lists used for the game
└── README.md # Project documentation and instructions (this file)
```

## Setup and Running  
To set up the project, ensure you have Python 3 installed along with the Flask and Requests libraries. After cloning the repository, install dependencies using pip:  
```bash
pip install flask requests
```
Start the server by running the server script:
```bash
python server.py
```
Then launch the client application in a separate terminal window:
```bash
python client.py
```
The client guides users through registration or login, then initiates the Hangman game where players guess letters until they solve the word or exhaust their allowed attempts.

## Usage  
Users enter their ID and password to authenticate. Each game begins by selecting a random word based on user input. As players guess letters, correct guesses reveal those letters within the word, while incorrect guesses advance the hangman drawing. The game tracks and updates statistics like the number of games played and wins automatically.

## License  
This project is intended for educational and personal use only. Unauthorized copying, distribution, or modification of the source code is prohibited without prior consent.
