from webapp.main.infra.persistence.user_repository import UserRepository
from uuid import uuid4
from passlib.context import CryptContext


class AuthService:
    def __init__(self, users_repository: UserRepository):
        self.users_repo: UserRepository = users_repository

    def get_users(self):
        return self.users_repo.get_all_users()

    def user_by_id(self, id):
        print("in service by id", id)
        return self.users_repo.get_by_id(id)

    def create_user(self):
        uid = uuid4()
        self.users_repo.add_user(f"{uid}@email.com", "pwd")

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def authenticate_user(self, username: str, password: str):
        user = self.users_repo.get_by_username(username)
        if not user:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False
        return user
