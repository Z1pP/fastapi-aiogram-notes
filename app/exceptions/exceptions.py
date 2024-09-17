class UserAlreadyExistsException(Exception):
    def __init__(self, email: str):
        self.email = email
        self.message = f"User with email {email} already exists"

    def __str__(self):
        return self.message


class UserNotFoundException(Exception):
    def __init__(self):
        self.message = f"User not found"

    def __str__(self):
        return self.message
    

class NoteNotFoundException(Exception):
    def __init__(self) -> None:
        self.message = f"Note not found"

    def __str__(self):
        return self.message