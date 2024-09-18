from .services import UserService
from .repositories import UserRepository


def get_user_service():

    return UserService(UserRepository)