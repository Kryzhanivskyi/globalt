import configparser
import random
import string
import requests
import json

from datetime import datetime, timedelta
from typing import Union, Dict, Any, Optional, Callable, Tuple

settings = configparser.ConfigParser()
settings.read('automated_bot_config.ini')

NUMBERS_OF_USERS: int = int(settings.get('CONFIG', 'NUMBERS_OF_USERS'))
MAX_POSTS_PER_USER: int = int(settings.get('CONFIG', 'MAX_POSTS_PER_USER'))
MAX_LIKES_PER_USER: int = int(settings.get('CONFIG', 'MAX_LIKES_PER_USER'))

USERNAME_LENGTH: int = int(settings.get('USER', 'USERNAME_LENGTH'))
PASSWORD_LENGTH: int = int(settings.get('USER', 'PASSWORD_LENGTH'))


class User:

    def __init__(
            self,
            username: str,
            email: str,
            password: str
    ):
        self.username: str = username
        self.email: str = email
        self.password: str = password
        self.likes_countdown: int = MAX_LIKES_PER_USER
        self.__access_token: Union[str, None] = None
        self.__refresh_token: Union[str, None] = None
        self.__posts_id_list: list = list()

    @property
    def access_token(self) -> str:
        return self.__access_token

    @access_token.setter
    def access_token(self, access_token: str) -> None:
        self.__access_token = access_token

    @property
    def refresh_token(self) -> str:
        return self.__refresh_token

    @refresh_token.setter
    def refresh_token(self, refresh_token: str) -> None:
        self.__refresh_token = refresh_token

    @property
    def posts_id_list(self) -> list:
        return self.__posts_id_list

    @posts_id_list.setter
    def posts_id_list(self, posts_id_list: list) -> None:
        self.__posts_id_list = posts_id_list

    def receive_tokens(self):
        tokens: Union[dict, None] = get_user_tokens(self)
        if tokens:
            self.access_token = tokens['access']
            self.refresh_token = tokens['refresh']
            return True
        return False

    def get_fresh_token(self):
        token = send_token_refresh_request(self)
        if token:
            self.access_token = token['access']
            return True
        return False

    def create_post(self):
        post_data = send_post_creation_request(self)
        if post_data:
            self.posts_id_list.append(post_data['id'])
            return True
        return False

    def like_post(self, post: dict):
        post_id: int = post['id']
        if send_post_like_request(self, post_id):
            self.likes_countdown -= 1


def benchmark(func: Callable[[Any], Tuple[Any, timedelta]]):
    """
    Decorator for function runtime measurement.
    """
    def wrapper(*args, **kwargs):
        start_ts: datetime = datetime.now()
        result: Any = func(*args, **kwargs)
        finish_ts: datetime = datetime.now()
        _runtime: timedelta = finish_ts - start_ts
        return result, _runtime
    return wrapper


@benchmark
def run_bot() -> dict:
    """
    Running bot to make an api activity
    """
    print('Bot has started')
    result: dict = {
        'result_message': '',
        'posts_num': 0
    }
    users_list: Optional[list, None] = signup_users()
    if users_list:
        if not create_posts(users_list):
            result['result_message'] = 'Function run_bot: error in func "create_posts"!'
            return result
    else:
        result['result_message'] = 'Function run_bot: error in func "signup_users"!'
        return result
    sort_list_by_num_posts(users_list)
    for _user in users_list:
        while _user.likes_countdown != 0:
            full_posts_list: list = get_posts_list(_user)
            posts_list: list = remove_own_and_liked_posts(_user, full_posts_list)
            if not posts_list:
                break
            user_set: set = get_users_set_with_no_likes(full_posts_list)
            if not user_set:
                _full_posts_list: list = get_posts_list(users_list[0])
                result['result_message'] = 'Bot stopped because there is no posts with 0 likes'
                result['posts_num'] = len(_full_posts_list)
                return result
            posts_list: list = remove_posts_from_fully_liked_users(posts_list, user_set)
            if not posts_list:
                break
            post = random.choice(posts_list)
            _user.like_post(post)

    _full_posts_list: list = get_posts_list(users_list[0])
    result['result_message'] = 'Bot correctly finished'
    result['posts_num'] = len(_full_posts_list)
    return result


def generate_user() -> User:
    """
    Generate required user data for signing up
    """
    username: str = ''.join(random.choice(string.ascii_lowercase) for _ in range(USERNAME_LENGTH))
    password: str = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(PASSWORD_LENGTH))
    user: User = User(
        username=username,
        email=''.join((username, '@gmail.com')),
        password=password
    )
    return user


def signup_users() -> Union[list, None]:
    """
    Signing up users
    """
    users_list = list()
    for _ in range(NUMBERS_OF_USERS):
        user: User = generate_user()
        try:
            response = send_request(
                address='http://127.0.0.1:8000/api/user/',
                headers={'Content-type': 'application/json'},
                payload={
                    'username': user.username,
                    'email': user.email,
                    'password': user.password
                },
                method='POST'
            )
        except Exception:
            # DO CARE ABOUT EXCEPTION HANDLING
            return None
        if response.status_code == 201:
            users_list.append(user)
    return users_list


def create_posts(users_list: list) -> bool:
    """
    Creating user posts
    """
    for user in users_list:
        if user.receive_tokens():
            for _ in range(random.randint(1, MAX_POSTS_PER_USER)):
                if not user.create_post():
                    return False
    return True


def remove_own_and_liked_posts(_user: User, posts_list: list) -> Union[list, None]:
    """
    Removing posts from list, made by user and already liked posts
    """
    posts_list = [post for post in posts_list if post['author_name'] != _user.username and post['is_liked'] is not True]
    if posts_list:
        return posts_list
    return None


def remove_posts_from_fully_liked_users(posts_list: list, users_set: set) -> Union[list, None]:
    """
    Removing posts from users, who have at least one post with 0 likes
    """

    filtered_posts: list = [post for post in posts_list if post['author_name'] in users_set]
    if filtered_posts:
        return filtered_posts
    return None


def get_users_set_with_no_likes(posts_list: list) -> Union[set, None]:
    """
    Getting users, who have at least one post with 0 likes
    """
    users_set_with_no_likes: set = set()
    _posts_with_no_likes: list = [post for post in posts_list if post['total_likes'] == 0]
    if _posts_with_no_likes:
        for post in _posts_with_no_likes:
            users_set_with_no_likes.add(post['author_name'])
        return users_set_with_no_likes
    return None


def sort_list_by_num_posts(users_list: list) -> None:
    """
    Sorting users by number of posts
    """
    users_list.sort(key=lambda x: len(x.posts_id_list), reverse=True)


def get_posts_list(_user: User) -> Union[list, None]:
    """
    Getting list of all posts
    """
    response_data: Union[list, None] = None
    _user.get_fresh_token()
    try:
        response = send_request(
            address='http://127.0.0.1:8000/api/post/',
            headers={
                'Content-type': 'application/json',
                'Authorization': f'Bearer {_user.access_token}'
            },
            method='GET'
        )
    except Exception:
        # DO CARE ABOUT EXCEPTION HANDLING
        return None
    if response.status_code == 200:
        response_data: dict = parse_response_data(response.text)
    return response_data


def get_user_tokens(_user: User) -> Union[dict, None]:
    """
    Getting access and refresh tokens for user
    """
    response_data: Union[dict, None] = None
    try:
        response = send_request(
            address='http://127.0.0.1:8000/api/token/',
            headers={'Content-type': 'application/json'},
            payload={
                "username": _user.username,
                "password": _user.password
            },
            method='POST'
        )
    except Exception:
        # DO CARE ABOUT EXCEPTION HANDLING
        return None
    if response.status_code == 200:
        response_data: dict = parse_response_data(response.text)
    return response_data


def send_token_refresh_request(_user: User) -> Union[dict, None]:
    """
    Getting fresh access token using refresh token
    """
    response_data: Union[dict, None] = None
    try:
        response = send_request(
            address='http://127.0.0.1:8000/api/token/refresh',
            headers={'Content-type': 'application/json'},
            payload={"refresh": _user.refresh_token},
            method='POST'
        )
    except Exception:
        # DO CARE ABOUT EXCEPTION HANDLING
        return None
    if response.status_code == 200:
        response_data: dict = parse_response_data(response.text)
    return response_data


def send_post_creation_request(_user: User) -> Union[dict, None]:
    """
    Sending request to create post
    """
    response_data: Union[dict, None] = None
    try:
        response = send_request(
            address='http://127.0.0.1:8000/api/post/',
            headers={
                'Content-type': 'application/json',
                'Authorization': f'Bearer {_user.access_token}'
            },
            payload={
                "title": f"{_user.username} title",
                "body": f"{_user.username} body"
            },
            method='POST'
        )
    except Exception:
        # DO CARE ABOUT EXCEPTION HANDLING
        return None
    if response.status_code == 201:
        response_data = parse_response_data(response.text)
    return response_data


def send_post_like_request(_user: User, post_id: int) -> bool:
    """
    Sending request to like a post
    """
    try:
        response = send_request(
            address=f'http://127.0.0.1:8000/api/post/{post_id}/like/',
            headers={'Authorization': f'Bearer {_user.access_token}'},
            method='POST'
        )
    except Exception:
        # DO CARE ABOUT EXCEPTION HANDLING
        return False
    if response.status_code == 200:
        return True
    return False


def send_request(
        address: str,
        payload: Union[dict, None] = None,
        headers: Union[dict, None] = None,
        method: str = 'GET',
):
    """
    Common request factory.
    """
    if method == 'POST':
        response: requests.Response = requests.post(
            url=address,
            data=json.dumps(payload),
            headers=headers
        )
    else:
        response: requests.Response = requests.get(
            url=address,
            headers=headers,
        )
    return response


def parse_response_data(response_body: str) -> Dict[str, Any]:
    """
    Getting data from json.
    """
    data: dict = json.loads(response_body)
    return data


if __name__ == '__main__':
    _result, runtime = run_bot()
    print(f'response from bot -- {_result["result_message"]}\n'
          f'created posts -- {_result["posts_num"]}\n'
          f'runtime -- {runtime}')
