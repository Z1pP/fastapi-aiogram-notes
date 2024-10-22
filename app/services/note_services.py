from app.exceptions.exceptions import NoteNotFoundException
from app.schemas import NoteEntity
from app.models import Note
from app.repositories import INoteRepository


class NoteService:
    def __init__(self, note_repository: INoteRepository) -> None:
        self.note_repository = note_repository

    async def create_note_by_user_id(
        self, user_id: int, note: NoteEntity
    ) -> NoteEntity:
        note_data = note.model_dump(exclude={"tags", "user_id"})
        note_db = Note(**note_data, user_id=user_id)

        note_db.tags = note.tags
        created_note = await self.note_repository.add(note=note_db)
        return created_note.to_entity()

    async def update_note_by_user_id_and_note_id(
        self, user_id: int, note_id: int, note: NoteEntity
    ) -> NoteEntity:
        db_note = await self.note_repository.get_by_user_id_and_note_id(
            user_id=user_id, note_id=note_id
        )

        if not db_note:
            raise NoteNotFoundException()

        updated_data = note.model_dump(
            exclude={"tags"}, exclude_unset=True, exclude_none=True
        )
        for key, value in updated_data.items():
            setattr(db_note, key, value)

        if note.tags:
            db_note.tags = note.tags

        updated_note = await self.note_repository.update(note=db_note)
        return updated_note.to_entity()

    async def get_notes_by_user_id(self, user_id: int) -> list[NoteEntity]:
        notes_db = await self.note_repository.get_by_user_id(user_id=user_id)
        return [note.to_entity() for note in notes_db] if notes_db else []

    async def get_notes(self) -> list[NoteEntity]:
        notes_db = await self.note_repository.get_all()
        return [note.to_entity() for note in notes_db]

    async def get_notes_by_user_id_and_tags(
        self, user_id: int, tags: list[str]
    ) -> list[NoteEntity]:
        notes_db = await self.note_repository.get_by_user_id_and_tags(
            user_id=user_id, tags=tags
        )
        return [note.to_entity() for note in notes_db]

    async def delete_note_by_id(self, note_id: int) -> None:
        note = await self.note_repository.get_by_id(note_id=note_id)
        if note is None:
            raise NoteNotFoundException()
        await self.note_repository.delete(note=note)

    async def delete_note_by_user_id_and_note_id(
        self, user_id: int, note_id: int
    ) -> None:
        note = await self.note_repository.get_by_user_id_and_note_id(
            user_id=user_id, note_id=note_id
        )
        if note is None:
            raise NoteNotFoundException()
        await self.note_repository.delete(note=note)
