from app.exceptions.exceptions import UserNotFoundException
from app.services import UserService
from app.schemas import UserEntity, UserResponse, TokenInfo
from app.utils.password import verify_password
from app.utils.utils import create_access_token, create_refresh_token
from app.core.config import settings
from app.exceptions import InvalidAuthEmailException, InvalidAuthPasswordException


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    async def login(self, user: UserEntity) -> TokenInfo:
        try:
            user_db = await self.user_service.get_user_by_email(email=user.email)
        except UserNotFoundException:
            raise InvalidAuthEmailException()
        if verify_password(
            plain_password=user.password, hashed_password=user_db.hashed_password
        ):
            access_token = await create_access_token(user=user_db)
            refresh_token = await create_refresh_token(user=user_db)
            return TokenInfo(
                access_token=access_token,
                refresh_token=refresh_token,
                token_type=settings.authjwt.token_type,
            )
        else:
            raise InvalidAuthPasswordException()

    async def refresh_token(self, user: UserResponse) -> TokenInfo:
        access_token = await create_access_token(user=user)
        return TokenInfo(
            access_token=access_token,
            token_type=settings.authjwt.token_type,
        )
