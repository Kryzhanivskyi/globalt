To run the Bot use following instructions:

1. Clone project from this repo by running in terminal (git clone https://github.com/Kryzhanivskyi/globalt.git)
2. Setup HUNTER_API_KEY and CLEARBIT_API_KEY in .env file
3. Setup NUMBERS_OF_USERS, MAX_POSTS_PER_USER and MAX_LIKES_PER_USER in automated_bot_config.ini file
4. Setup containers by running in terminal(sudo docker-compose up -d --build)
5. Get django CONTEINER_ID by running in terminal(sudo docker ps -a) and copy it
6. Paste your CONTEINER_ID to the command in terminal (docker exec -it CONTAINER_ID sh)
7. Run test by entering in terminal(python manage.py test)
8. Run bot by entering in terminal(python automated_bot.py)

