from pydantic import BaseModel


class UserDTO(BaseModel):
    id: int
    username: str
    email: str
    hashed_password: str
    is_active: bool