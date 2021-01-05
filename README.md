To run the Bot use following instructions:

1. Clone project from this repo by running in terminal (git clone https://github.com/Kryzhanivskyi/globalt.git)
2. Set up virtual environment by running in terminal (python3 -m venv yourvenvname)
3. Activate virtual environment by running in terminal (source yourvenvname/bin/activate)
4. Open project folder by running in terminal (cd globalt)
5. Install requirements by running in terminal (pip install -r requirements.txt)
6. Setup HUNTER_API_KEY and CLEARBIT_API_KEY in .env file
7. Setup NUMBERS_OF_USERS, MAX_POSTS_PER_USER and MAX_LIKES_PER_USER in automated_bot_config.ini file
8. Create database by running in terminal (python3 manage.py migrate)
9. Run server by running in terminal (python3 manage.py runserver)
10. Run bot by running in other opened terminal (python3 automated_bot.py)

