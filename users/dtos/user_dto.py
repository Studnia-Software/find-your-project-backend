import dataclasses
from ..models import User


@dataclasses.dataclass
class UserDTO:
    first_name: str
    last_name: str
    email: str
    password: str = None
    id: int = None

    @classmethod
    def from_instance(cls, user_instance: User) -> "UserDTO":
        return cls(
            first_name=user_instance.first_name,
            last_name=user_instance.last_name,
            email=user_instance.email,
            id=user_instance.id,
        )
