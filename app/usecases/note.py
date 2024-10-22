from app.services import NoteService, TagService
from app.schemas import NoteEntity, NoteResponse


class CreateNoteForUserUseCase:
    def __init__(self, note_service: NoteService, tag_service: TagService):
        self.note_service = note_service
        self.tag_service = tag_service

    async def execute(self, user_id: int, note: NoteEntity) -> NoteResponse:
        """
        Create a note for a user and return the created note
        """
        tags = []
        for tag in note.tags:
            tags.append(await self.tag_service.get_or_create(tag_name=tag.name))

        note.tags = tags
        created_note = await self.note_service.create_note_by_user_id(
            user_id=user_id, note=note
        )

        return created_note.to_response()


class GetUserNotesUseCase:
    def __init__(self, note_service: NoteService):
        self.note_service = note_service

    async def execute(self, user_id: int) -> list[NoteResponse]:
        """
        Get all notes by user id
        """
        notes = await self.note_service.get_notes_by_user_id(user_id=user_id)
        return [note.to_response() for note in notes] if notes else []


class DeleteNoteForUserUseCase:
    def __init__(self, note_service: NoteService):
        self.note_service = note_service

    async def execute(self, user_id: int, note_id: int) -> None:
        """
        Delete a note by user id and note id
        """
        await self.note_service.delete_note_by_user_id_and_note_id(
            user_id=user_id, note_id=note_id
        )


class UpdateNoteForUserUseCase:
    def __init__(self, note_service: NoteService, tag_service: TagService):
        self.note_service = note_service
        self.tag_service = tag_service

    async def execute(
        self, user_id: int, note_id: int, note: NoteEntity
    ) -> NoteResponse:
        """
        Update a note by user id and note id
        """
        tags = []
        for tag in note.tags:
            tags.append(await self.tag_service.get_or_create(tag_name=tag.name))

        note.tags = tags
        updated_note = await self.note_service.update_note_by_user_id_and_note_id(
            user_id=user_id, note_id=note_id, note=note
        )

        return updated_note.to_response()


class GetNotesByTagsUseCase:
    def __init__(self, note_service: NoteService, tag_service: TagService):
        self.note_service = note_service
        self.tag_service = tag_service

    async def execute(self, user_id: int, tags: list[str]) -> list[NoteResponse]:
        """
        Get notes by user id and tags
        """
        normalized_tags = [
            await self.tag_service._normalize_tag_name(tag) for tag in tags
        ]
        notes = await self.note_service.get_notes_by_user_id_and_tags(
            user_id=user_id, tags=normalized_tags
        )
        return [note.to_response() for note in notes] if notes else []
