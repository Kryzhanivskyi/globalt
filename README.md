To run the Bot use following instructions:

1. Clone project from this repo by entering in terminal (git clone https://github.com/Kryzhanivskyi/globalt.git)
2. Open project directory by entering in terminal (cd globalt)
3. Setup HUNTER_API_KEY and CLEARBIT_API_KEY in .env file
4. Setup NUMBERS_OF_USERS, MAX_POSTS_PER_USER and MAX_LIKES_PER_USER in automated_bot_config.ini file
5. Setup containers by entering in terminal(sudo docker-compose up -d --build)
6. Get django CONTEINER_ID by entering in terminal(sudo docker ps -a) and copy it
7. Paste your CONTEINER_ID to the command in terminal (sudo docker exec -it CONTAINER_ID sh)
8. Run test by entering in terminal(python manage.py test)
9. Run bot by entering in terminal(python automated_bot.py)

