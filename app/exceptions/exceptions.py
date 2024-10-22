from fastapi import status, HTTPException


class BaseAppException(Exception):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR  # default status code
    message: str = "Internal server error"

    def __init__(self, message: str, status_code: int):
        super().__init__(message)
        if status_code is not None:
            self.status_code = status_code


class BaseAuthException(HTTPException):
    def __init__(self, detail: str = None, status_code: int = None):
        self.detail = detail or "Unauthorized user"
        self.headers = {"WWW-Authenticate": "Bearer"}
        self.status_code = status_code or status.HTTP_401_UNAUTHORIZED
        super().__init__(
            status_code=self.status_code, detail=self.detail, headers=self.headers
        )


class UserAlreadyExistsException(BaseAppException):
    def __init__(self, email: str):
        self.message = f"User with email {email} already exists"
        super().__init__(self.message, status_code=status.HTTP_400_BAD_REQUEST)


class UserNotFoundException(BaseAppException):
    def __init__(self):
        self.message = "User not found"
        super().__init__(self.message, status_code=status.HTTP_404_NOT_FOUND)


class NoteNotFoundException(BaseAppException):
    def __init__(self) -> None:
        self.message = "Note not found"
        super().__init__(self.message, status_code=status.HTTP_404_NOT_FOUND)


class TagNotFoundException(BaseAppException):
    def __init__(self, name: str):
        self.message = f"Tag with name {name} not found"
        super().__init__(self.message, status_code=status.HTTP_404_NOT_FOUND)


class TgProfileAlreadyExistsException(BaseAppException):
    def __init__(self):
        self.message = "The profile is already linked to another user"
        super().__init__(self.message, status_code=status.HTTP_400_BAD_REQUEST)


class TgProfileNotFoundException(BaseAppException):
    def __init__(self):
        self.message = "Tg profile not found"
        super().__init__(self.message, status_code=status.HTTP_404_NOT_FOUND)


class InvalidAuthPasswordException(BaseAuthException):
    def __init__(self):
        self.detail = "Invalid auth password"
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=self.detail)


class InvalidAuthEmailException(BaseAuthException):
    def __init__(self):
        self.detail = "Invalid auth email"
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=self.detail)
