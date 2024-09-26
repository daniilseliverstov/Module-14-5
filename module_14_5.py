from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from crud_functions import *


with open("teg_api") as file:
    api = file.read()

bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = KeyboardButton(text='Рассчитать')
button_2 = KeyboardButton(text='Информация')
button_3 = KeyboardButton(text='Купить')
button_4 = KeyboardButton(text='Регистрация')
kb.add(button_1)
kb.add(button_2)
kb.add(button_3)
kb.add(button_4)

in_kb = InlineKeyboardMarkup()
in_button_1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
in_button_2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
in_kb.add(in_button_1)
in_kb.add(in_button_2)
in_menu = InlineKeyboardMarkup()
butt_1 = InlineKeyboardButton(text='Product1', callback_data="product_buying")
butt_2 = InlineKeyboardButton(text='Product2', callback_data="product_buying")
butt_3 = InlineKeyboardButton(text='Product3', callback_data="product_buying")
butt_4 = InlineKeyboardButton(text='Product4', callback_data="product_buying")
in_menu.add(butt_1)
in_menu.add(butt_2)
in_menu.add(butt_3)
in_menu.add(butt_4)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()


@dp.message_handler(text='Регистрация')
async def sing_up(message):
    await message.answer('Введите имя пользователя (только латинский алфавит): ')
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    if is_included(message.text):
        await message.answer("Пользователь существует, введите другое имя")
        await RegistrationState.username.set()
    else:
        await state.update_data(username=message.text)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    add_user(data['username'], data['email'], data['age'])
    await message.answer("Регистрация прошла успешно")
    await state.finish()


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    base = get_all_products()
    for i in range(1, 5):
        await message.answer(f'Название: {base[i][0]} | Описание: {base[i][1]}| Цена: {base[i][2]}')
        with open(f'{i}.png', 'rb') as img:
            await message.answer_photo(img)
    await message.answer('Выберите продукт для покупки:', reply_markup=in_menu)


@dp.callback_query_handler(text="product_buying")
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer(text='Выберите опцию:', reply_markup=in_kb)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) -161')
    await call.answer()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer(text='Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.callback_query_handler(text='calories')
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    # 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161
    norma_calories = 10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * int(data['age']) - 161
    await message.answer(f'Ваша норма калорий: {norma_calories}')
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
