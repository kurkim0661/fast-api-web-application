from passlib.context import CryptContext

from webapp.main.infra.persistence.user_repository import UserRepository
from uuid import uuid4


class UserService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def __init__(self, users_repository: UserRepository):
        self.users_repo: UserRepository = users_repository

    def get_users(self):
        return self.users_repo.get_all_users()

    def user_by_id(self, id):
        print("in service by id", id)
        return self.users_repo.get_by_id(id)

    def create_user(self, username, email, password):
        hashed_password = self.get_password_hash(password)
        return self.users_repo.add_user(username, email, hashed_password)
