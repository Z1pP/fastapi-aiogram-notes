from app.services import UserService
from app.schemas import UserCreate, UserResponse, TokenInfo
from app.utils.password import verify_password
from app.utils.utils import create_access_token, create_refresh_token
from app.core.config import settings
from app.exceptions import InvalidEmailException, InvalidPasswordException


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    async def login(self, user: UserCreate) -> TokenInfo:
        user_db = await self.user_service.get_user_by_email(user.email)
        if user_db is not None:
            if verify_password(user.password, user_db.hashed_password):
                access_token = await create_access_token(user_db)
                refresh_token = await create_refresh_token(user_db)
                return TokenInfo(
                    access_token=access_token,
                    refresh_token=refresh_token,
                    token_type=settings.authjwt.token_type,
                )
            else:
                raise InvalidPasswordException()
        raise InvalidEmailException()

    async def refresh_token(self, user: UserResponse) -> TokenInfo:
        access_token = await create_access_token(user)
        return TokenInfo(
            access_token=access_token,
            token_type=settings.authjwt.token_type,
        )
