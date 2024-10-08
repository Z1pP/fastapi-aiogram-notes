import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from sqlalchemy import select

from app.core.config import settings
from app.models import TgProfile
from app.db.database import get_async_session
from app.models import User
from app.utils.password import hash_password, verify_password

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
        notes = user_db.notes
        if not notes:
            await message.answer(
                "У вас нет заметок. Чтобы добавить заметку, отправьте команду /add_note"
            )
            return

        message_text = "Список ваших заметок:\n"
        for num, note in enumerate(notes, 1):
            message_text += f"{num}. {note.title}\n" f"{note.description}\n\n"
        await message.answer(message_text)


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
async def process_password(message: Message, state: FSMContext):
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
async def process_email(message: Message, state: FSMContext):
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
async def process_password(message: Message, state: FSMContext):
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
    await message.answer(message.text)


if __name__ == "__main__":
    try:
        logger.info("Bot started")
        dp.run_polling(bot)
    except KeyboardInterrupt:
        logger.info("Bot stopped")
