To run the Bot use following instructions:

1. Clone project from this repo by running in terminal (https://github.com/Kryzhanivskyi/globalt.git)
2. Set up virtual environment by running in terminal (python3 -m venv yourvenvname)
3. Activate virtual environment by running in terminal (source yourvenvname/bin/activate)
4. Install requirements by running in terminal (pip install -r requirements.txt)
5. Setup HUNTER_API_KEY and CLEARBIT_API_KEY in .env file
6. Setup NUMBERS_OF_USERS, MAX_POSTS_PER_USER and MAX_LIKES_PER_USER in automated_bot_config.ini file
7. Create database by running in terminal (python3 manage.py migrate)
8. Run server by running in terminal (python3 manage.py runserver)
9. Run bot by running in other opened terminal (python3 automated_bot.py)

