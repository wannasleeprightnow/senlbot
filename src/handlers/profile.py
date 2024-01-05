from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from database import Database
from handlers.states import UserDeskmate, UserGrade, UserNoticetime
from keyboards.profile import builder as profile_keyboard


profile_router = Router()


@profile_router.message(F.text == "Профиль")
async def command_profile_handler(message: Message):
    await message.answer(
        "Ваш профиль",
        reply_markup=profile_keyboard.as_markup(resize_keyboard=True))


@profile_router.callback_query(F.data == "Изменить класс")
async def change_grade(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите класс, в котором Вы учитесь")
    await state.set_state(UserGrade.grade)


@profile_router.message(UserGrade.grade)
async def grade_choosen(message: Message, state: FSMContext):
    await state.update_data(grade=message.text)
    await state.update_data(telegram_id=message.from_user.id)
    to_update = await state.get_data()
    db = Database()
    await db.update_user_grade(**to_update)
    await message.answer("Ваш класс обновлен")
    await state.clear()


@profile_router.callback_query(F.data == "Изменить соседа по парте")
async def change_deskmate(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите username Вашего соседа по парте")
    await state.set_state(UserDeskmate.deskmate)


@profile_router.message(UserDeskmate.deskmate)
async def deskmate_choosen(message: Message, state: FSMContext):
    await state.update_data(deskmate=message.text)
    await state.update_data(telegram_id=message.from_user.id)
    to_update = await state.get_data()
    db = Database()
    await db.update_user_deskmate(**to_update)
    await message.answer("Ваш сосед по парте обновлен")
    await state.clear()


@profile_router.callback_query(F.data == "Изменить время напоминаний")
async def change_notice_time(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите время напоминаний")
    await state.set_state(UserNoticetime.notice_time)


@profile_router.message(UserNoticetime.notice_time)
async def notice_time_choosen(message: Message, state: FSMContext):
    await state.update_data(notice_time=message.text)
    await state.update_data(telegram_id=message.from_user.id)
    to_update = await state.get_data()
    db = Database()
    await db.update_user_notice_time(**to_update)
    await message.answer("Ваше время напоминаний обновлено")
    await state.clear()
