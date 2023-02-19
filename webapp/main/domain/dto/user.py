from typing import Optional

from pydantic import BaseModel


class UserDTO(BaseModel):
    username: str
    email: str
    hashed_password: str
    is_active: Optional[bool]
