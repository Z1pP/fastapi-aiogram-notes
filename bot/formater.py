from app.schemas import NoteCreate, TagCreate


def format_note(title: str, description: str, tags: list[str]) -> NoteCreate:
    return NoteCreate(
        title=title, description=description, tags=[TagCreate(name=tag) for tag in tags]
    )
