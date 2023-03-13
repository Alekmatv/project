import random

from aiogram import Bot, Dispatcher
from aiogram.filters import Command, Text
from aiogram.types import Message

with open('bot_token.txt', encoding='utf-8') as file:
    TG_TOKEN = file.read().strip()

bot: Bot = Bot(token=TG_TOKEN)
dp: Dispatcher = Dispatcher()

user: dict = {'in_game': False,
              'secret_num': None,
              'attemps': None,
              'total_games': 0,
              'wins': 0}

attemps: int = 5


def get_secret():
    return random.choice(range(1, 101))


@dp.message(Command(commands=['start']))
async def process_start_comand(message: Message):
    await message.answer(f'Привет! Давай сыграем в игру угадайку?\n'
                         f'Когда будешь готов, скажи "да".\n'
                         f'Если хочешь узнать правила, введи /help.')


@dp.message(Command(commands=['help']))
async def process_help_comand(message: Message):
    await message.answer(f'Я загадываю число от 1 до 100,'
                         f'у тебя есть {attemps} попыток угадать его.\n'
                         f'Хочешь сыграть?')


@dp.message(Command(commands=['cancel']))
async def process_cancel_comand(message: Message):
    if user['in_game']:
        await message.answer(f'Очень жаль! '
                             f'Мое число было {user["secret_num"]}.')
        user['in_game'] = False
        user['total_games'] += 1
    else:
        await message.answer('А мы и так не играем\n\
                             Хотите сыграть?')


@dp.message(Command(commands=['stat']))
async def process_stat_comand(message: Message):
    await message.answer(f'Количество игр: {user["total_games"]}\n'
                         f'Количество побед: {user["wins"]}')


@dp.message(Text(text=['да', 'давай', 'го', 'гоу', 'хочу еще', 'играем',
                       'ок', 'окей'], ignore_case=True))
async def process_positive_answer(message: Message):
    if not user['in_game']:
        await message.answer('Ура! Я загадал число!\n\
                             Если хочешь закончить, введи /cancel.')
        user['in_game'] = True
        user['secret_num'] = get_secret()
        user['total_games'] += 1
        user['attemps'] = attemps
    else:
        await message.answer('Мы уже играем. \
                             Если хочешь прекратить, введи /cancel.')


@dp.message(Text(text=['не', 'нет',
                       'не хочу', 'отказываюсь'], ignore_case=True))
async def process_negative_answer(message: Message):
    if not user['in_game']:
        await message.answer('Очень жаль! :(\n\
                             Когда захотите - сообщите об этом.')
    else:
        await message.answer('Мы уже с вами играем.\n\
                             Если хочешь прекратить, введи /cancel.')


@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers_answer(message: Message):
    if user['in_game']:
        num = int(message.text)
        if num == user['secret_num']:
            await message.answer('Ура! Вы выиграли!!!')
            user['in_game'] = False
            user['wins'] += 1
        elif num < user['secret_num']:
            await message.answer('Мое число больше :)')
            user['attemps'] -= 1
        elif num > user['secret_num']:
            await message.answer('Мое число меньше :)')
            user['attemps'] -= 1

        if user['attemps'] == 0:
            await message.answer(f'К сожалению, у вас больше не осталось '
                                 f'попыток. Вы проиграли :(\n\nМое число '
                                 f'было {user["secret_num"]}\n\nДавайте '
                                 f'сыграем еще? А?')
            user['in_game'] = False
    else:
        await message.answer('Мы еще не играем :)\n\
                             Хотите сыграть?')


@dp.message()
async def process_another_message(message: Message):
    if user['in_game']:
        await message.answer('Мы же сейчас с вами играем. '
                             'Присылайте, пожалуйста, числа от 1 до 100')
    else:
        await message.answer('Пока что я не умею многого, может сыграем?')


if __name__ == '__main__':
    dp.run_polling(bot)
