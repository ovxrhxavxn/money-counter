from .services import UserService
from .repositories import UserRepository


def get_user_service() -> UserService:
    return UserService(UserRepository)