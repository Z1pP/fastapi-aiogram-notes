from abc import ABC, abstractmethod
from typing import List, Optional

from app.models import User, Note, Tag


class IUserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    async def get_all(self) -> List[User]:
        pass

    @abstractmethod
    async def add(self, user: User) -> User:
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        pass

    @abstractmethod
    async def delete(self, user: User) -> None:
        pass


class INoteRepository(ABC):
    @abstractmethod
    async def get_by_id(self, note_id: int) -> Optional[Note]:
        pass

    @abstractmethod
    async def get_by_user_id_and_tags(
        self, user_id: int, tags: List[str]
    ) -> List[Note]:
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> List[Note]:
        pass

    @abstractmethod
    async def get_by_user_id_and_note_id(
        self, user_id: int, note_id: int
    ) -> Optional[Note]:
        pass

    @abstractmethod
    async def get_all(self) -> List[Note]:
        pass

    @abstractmethod
    async def add(self, note: Note) -> Note:
        pass

    @abstractmethod
    async def update(self, note: Note) -> Note:
        pass

    @abstractmethod
    async def delete(self, note: Note) -> None:
        pass


class ITagRepository(ABC):
    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[Tag]:
        pass

    @abstractmethod
    async def add(self, tag: Tag) -> Tag:
        pass

    @abstractmethod
    async def delete(self, tag: Tag) -> None:
        pass
