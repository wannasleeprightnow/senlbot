from aiogram.fsm.state import State, StatesGroup


class UserGrade(StatesGroup):
    telegram_id = State()
    grade = State()


class UserDeskmate(StatesGroup):
    telegram_id = State()
    deskmate = State()


class UserNoticetime(StatesGroup):
    telegram_id = State()
    notice_time = State()


class UserInfo(StatesGroup):
    telegram_id = State()
    grade = State()
    deskmate_username = State()
    telegram_username = State()


class WannaGiveBooks(StatesGroup):
    telegram_id = State()
    lessons_date = State()
    books = State()
    deskmate_books = State()
