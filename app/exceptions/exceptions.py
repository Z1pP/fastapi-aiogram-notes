class UserAlreadyExistsException(Exception):
    def __init__(self, email: str):
        self.email = email
        self.message = f"User with email {email} already exists"
        self.status_code = 400

    def __str__(self):
        return self.message


class UserNotFoundException(Exception):
    def __init__(self):
        self.message = "User not found"
        self.status_code = 404

    def __str__(self):
        return self.message


class NoteNotFoundException(Exception):
    def __init__(self) -> None:
        self.message = "Note not found"
        self.status_code = 404

    def __str__(self):
        return self.message


class TgProfileAlreadyExistsException(Exception):
    def __init__(self):
        self.message = "The profile is already linked to another user"
        self.status_code = 400

    def __str__(self):
        return self.message


class TgProfileNotFoundException(Exception):
    def __init__(self):
        self.message = "Tg profile not found"
        self.status_code = 404

    def __str__(self):
        return self.message
