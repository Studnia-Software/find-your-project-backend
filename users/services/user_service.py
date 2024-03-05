from ..dtos import UserDTO
from ..models import User


class UserService:
    def create_user(self, user_dto: UserDTO) -> User or None:
        try:
            instance = User(
                first_name=user_dto.first_name,
                last_name=user_dto.last_name,
                email=user_dto.email,
            )

            if user_dto.password is not None:
                instance.set_password(user_dto.password)

            instance.save()

            return instance
        except Exception as e:
            return None





        
