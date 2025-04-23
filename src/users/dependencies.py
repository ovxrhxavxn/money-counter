from .services import UsersService
from .repositories import UserRepository


def get_user_service() -> UsersService:
    return UsersService(UserRepository)