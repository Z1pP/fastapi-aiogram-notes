class UserAlreadyExistsException(Exception):
    def __init__(self, email: str):
        self.email = email
        self.message = f"User with email {email} already exists"
        self.status_code = 400

    def __str__(self):
        return self.message


class UserNotFoundException(Exception):
    def __init__(self):
        self.message = f"User not found"
        self.status_code = 404

    def __str__(self):
        return self.message
    

class NoteNotFoundException(Exception):
    def __init__(self) -> None:
        self.message = f"Note not found"
        self.status_code = 404

    def __str__(self):
        return self.message
    

class TgProfileAlreadyExistsException(Exception):
    def __init__(self):
        self.message = f"The profile is already linked to another user"
        self.status_code = 400

    def __str__(self):
        return self.message