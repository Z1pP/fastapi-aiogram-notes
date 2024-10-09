class AppException(Exception):
    status_code: int = 500  # default status code

    def __init__(self, message: str, status_code: int):
        super().__init__(message)
        if status_code is not None:
            self.status_code = status_code


class UserAlreadyExistsException(AppException):
    def __init__(self, email: str):
        self.message = f"User with email {email} already exists"
        super().__init__(self.message, status_code=400)


class UserNotFoundException(AppException):
    def __init__(self):
        self.message = "User not found"
        super().__init__(self.message, status_code=404)


class NoteNotFoundException(AppException):
    def __init__(self) -> None:
        self.message = "Note not found"
        super().__init__(self.message, status_code=404)


class TgProfileAlreadyExistsException(AppException):
    def __init__(self):
        self.message = "The profile is already linked to another user"
        super().__init__(self.message, status_code=400)


class TgProfileNotFoundException(AppException):
    def __init__(self):
        self.message = "Tg profile not found"
        super().__init__(self.message, status_code=404)
