import logging
from aiogram import Bot, Dispatcher
from aiogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from sqlalchemy import select

from app.core.config import settings
from app.models import TgProfile
from app.db.database import get_async_session
from app.models import User, Note
from app.utils.password import hash_password, verify_password
from app.services import NoteService

from bot.formater import format_note
import bot.logging_config

logger = logging.getLogger(__name__)

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher()


class RegistrationStates(StatesGroup):
    email = State()
    password = State()


class LinkProfileStates(StatesGroup):
    email = State()
    password = State()


class AddNoteState(StatesGroup):
    title = State()
    description = State()
    tags = State()


@dp.message(CommandStart())
async def start_command(message: Message):
    tg_id: int = message.from_user.id
    logger.info(f"Пользователь {tg_id} выбрал команду /start")

    async for session in get_async_session():
        query = select(TgProfile).where(TgProfile.tg_id == tg_id)
        result = await session.execute(query)
        profile_db = result.scalar_one_or_none()
        if profile_db is not None:
            await message.answer(
                f"Привет, {profile_db.username}! Я бот для заметок. Чтобы посмотреть свои заметки, отправь мне команду /notes"
            )
        else:
            await message.answer(
                "Вас нет в базе данных. Пожалуйста, зарегистрируйтесь, отправив команду /register.\n"
                "Вы также может подключить свой телеграм профиль, отправив команду /link_profile"
            )


@dp.message(Command("register"))
async def register_command(message: Message, state: FSMContext):
    tg_id: int = message.from_user.id
    async for session in get_async_session():
        query = select(User).join(TgProfile).where(TgProfile.tg_id == tg_id)
        result = await session.execute(query)
        user_db = result.scalar_one_or_none()
        if user_db is not None:
            await message.answer(
                "Вы уже зарегистрированы. Чтобы добавить заметку, отправьте команду /add_note"
            )
            return
    await message.answer("Пожалуйста, введите ваш email:")
    await state.set_state(RegistrationStates.email)


@dp.message(Command("notes"))
async def notes_command(message: Message):
    tg_id: int = message.from_user.id
    async for session in get_async_session():
        query = select(User).join(TgProfile).where(TgProfile.tg_id == tg_id)
        result = await session.execute(query)
        user_db = result.scalar_one_or_none()
        if user_db is None:
            await message.answer(
                "Вы не зарегистрированы. Пожалуйста, зарегистрируйтесь, отправив команду /register"
            )
            return
        notes: list[Note] = user_db.notes
        if not notes:
            await message.answer(
                "У вас нет заметок. Чтобы добавить заметку, отправьте команду /add_note"
            )
            return

        message_text = "Список ваших заметок:\n\n"
        for note in notes:
            message_text += (
                f"Название: {note.title}\n"
                f"Описание: {note.description}\n"
                f"Теги: {', '.join(tag.name for tag in note.tags)}\n"
                "----------------------------------\n"
            )
        await message.answer(message_text)


@dp.message(Command("add_note"))
async def add_note(message: Message, state: FSMContext):
    await message.answer("Как будет называться заметка?")
    await state.set_state(AddNoteState.title)


@dp.message(AddNoteState.title)
async def note_title_process(message: Message, state: FSMContext):
    title = message.text.strip()

    if len(title) < 3:
        await message.answer(
            "Слишком короткое название. Минимальная длина - 3 символа."
        )
        return

    if len(title) > 100:
        await message.answer(
            "Слишком длинное название. Максимальная длина - 100 символов."
        )
        return

    if title.isdigit():
        await message.answer("Название не может состоять только из цифр.")
        return

    await state.update_data(title=title)
    await message.answer("Добавь описание своей заметке")
    await state.set_state(AddNoteState.description)


@dp.message(AddNoteState.description)
async def note_description_process(message: Message, state: FSMContext):
    description = message.text.strip()

    if len(description) < 5:
        await message.answer(
            "Слишком короткое описание. Минимальная длина - 5 символов."
        )
        return

    if len(description) > 500:
        await message.answer(
            "Слишком длинное описание. Максимальная длина - 500 символов."
        )
        return

    if description.isdigit():
        await message.answer("Описание не может состоять только из цифр.")
        return

    await state.update_data(description=description)
    await message.answer("Добавь теги через запятую")
    await state.set_state(AddNoteState.tags)


@dp.message(AddNoteState.tags)
async def note_tags_process(message: Message, state: FSMContext):
    tags = [tag.strip() for tag in message.text.split(",") if tag.strip()]

    if not tags:
        await message.answer("Пожалуйста, введите хотя бы один тег.")
        return

    if len(tags) > 5:
        await message.answer(
            "Слишком много тегов. Пожалуйста, введите не более 5 тегов."
        )
        return

    if any(len(tag) > 20 for tag in tags):
        await message.answer(
            "Слишком длинный тег. Максимальная длина тега - 20 символов."
        )
        return

    await state.update_data(tags=tags)
    formatted_note = format_note(**await state.get_data())

    async for session in get_async_session():
        query = select(TgProfile).where(TgProfile.tg_id == message.from_user.id)
        result = await session.execute(query)
        tg_profile: TgProfile = result.scalar_one_or_none()
        note_service = NoteService(session)
        try:
            await note_service.create_note_by_user_id(
                tg_profile.user_id, formatted_note
            )
            await message.answer("Заметка успешно создана")
        except Exception as e:
            logger.error(f"Ошибка при создании заметки: {e}")
            await message.answer(
                "Произошла ошибка при создании заметки. Пожалуйста, попробуйте снова."
            )

    await state.clear()


@dp.message(Command("delete_note"))
async def delete_note(message: Message):
    tg_id: int = message.from_user.id
    async for session in get_async_session():
        query = select(User).join(TgProfile).where(TgProfile.tg_id == tg_id)
        result = await session.execute(query)
        user_db = result.scalar_one_or_none()
        if user_db is not None:
            notes: list[Note] = user_db.notes
            if not notes:
                await message.answer(
                    "У вас нет заметок. Чтобы добавить заметку, отправьте команду /add_note"
                )
                return
            kb_buttons = []
            for note in notes:
                kb_buttons.append(
                    InlineKeyboardButton(
                        text=note.title,
                        callback_data=f"delete-note-id-{note.id}-user-id-{user_db.id}",
                    )
                )
            await message.answer(
                "Выберите заметку, которую хотите удалить",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[kb_buttons]),
            )
        else:
            await message.answer(
                "Вы не зарегистрированы. Пожалуйста, зарегистрируйтесь, отправив команду /register"
            )


@dp.callback_query(lambda text: text.data.startswith("delete-note-id-"))
async def delete_note_callback(callback: CallbackQuery):
    note_id = int(callback.data.split("-")[3])
    user_id = int(callback.data.split("-")[-1])
    async for session in get_async_session():
        note_service = NoteService(session)
        try:
            await note_service.delete_note_by_user_id_and_note_id(user_id, note_id)
            await callback.message.delete()
            await callback.message.answer("Заметка успешно удалена")
        except Exception as e:
            logger.error(f"Ошибка при удалении заметки: {e}")
            await callback.message.delete()
            await callback.message.answer(
                "Произошла ошибка при удалении заметки. Пожалуйста, попробуйте снова."
            )


@dp.message(Command("link_profile"))
async def link_profile_command(message: Message, state: FSMContext):
    tg_id: int = message.from_user.id

    async for session in get_async_session():
        query = select(TgProfile).where(TgProfile.tg_id == tg_id)
        result = await session.execute(query)
        profile_db = result.scalar_one_or_none()
        if profile_db is not None:
            await message.answer(
                "Ваш профиль уже связан с Telegram. Вы можете использовать бот для управления своими заметками."
            )
        else:
            await message.answer("Пожалуйста, введите ваш email:")
            await state.set_state(LinkProfileStates.email)


@dp.message(LinkProfileStates.email)
async def process_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer("Пожалуйста, введите ваш пароль:")
    await state.set_state(LinkProfileStates.password)


@dp.message(LinkProfileStates.password)
async def process_link_password(message: Message, state: FSMContext):
    await state.update_data(password=message.text)

    data = await state.get_data()
    email = data.get("email")
    password = data.get("password")

    async for session in get_async_session():
        query = select(User).where(User.email == email)
        result = await session.execute(query)
        user_db = result.scalar_one_or_none()
        if user_db is not None:
            if verify_password(password, user_db.hashed_password):
                new_tg_profile = TgProfile(
                    tg_id=message.from_user.id, username=message.from_user.username
                )
                user_db.tg_profile = new_tg_profile
                await session.commit()
                await message.answer(
                    f"Здравствуйте {user_db.tg_profile.username}\n"
                    "Профиль успешно связан с Telegram. Вы можете использовать бот для управления своими заметками."
                )
                await state.clear()
            else:
                await message.answer("Неверный пароль. Пожалуйста, попробуйте снова.")
        else:
            await message.answer(
                "Пользователь с таким email не найден. Пожалуйста, проверьте правильность введенного email."
            )


@dp.message(Command("delete_profile"))
async def delete_profile_command(message: Message):
    tg_id: int = message.from_user.id
    async for session in get_async_session():
        query = select(TgProfile).where(TgProfile.tg_id == tg_id)
        result = await session.execute(query)
        profile_db = result.scalar_one_or_none()
        if profile_db is not None:
            await session.delete(profile_db)
            await session.commit()
            await message.answer(
                "Ваш профиль удален. Вы можете зарегистрироваться снова, отправив команду /register"
            )
        else:
            await message.answer(
                "Вы не зарегистрированы. Пожалуйста, зарегистрируйтесь, отправив команду /register"
            )


@dp.message(RegistrationStates.email)
async def process_register_email(message: Message, state: FSMContext):
    async for session in get_async_session():
        query = select(User).where(User.email == message.text)
        result = await session.execute(query)
        user_db = result.scalar_one_or_none()
        if user_db is not None:
            await message.answer(
                "Пользователь с таким email уже зарегистрирован. Пожалуйста, введите другой email."
            )
            return
        else:
            await state.update_data(email=message.text)
            await message.answer("Пожалуйста, введите ваш пароль:")
    await state.set_state(RegistrationStates.password)


@dp.message(RegistrationStates.password)
async def process_register_password(message: Message, state: FSMContext):
    await state.update_data(password=message.text)

    data = await state.get_data()
    email = data.get("email")
    password = data.get("password")

    async for session in get_async_session():
        new_user = User(email=email, hashed_password=hash_password(password))
        session.add(new_user)
        new_tg_profile = TgProfile(
            tg_id=message.from_user.id, username=message.from_user.username
        )
        new_user.tg_profile = new_tg_profile
        await session.commit()
    await message.answer(
        "Регистрация завершена. Теперь вы можете использовать бот для управления своими заметками."
    )
    await state.clear()


@dp.message(lambda message: message.text)
async def echo_message(message: Message):
    await message.reply("Нет такой команды!")


if __name__ == "__main__":
    try:
        logger.info("Bot started")
        dp.run_polling(bot)
    except KeyboardInterrupt:
        logger.info("Bot stopped")
