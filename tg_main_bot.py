import pandas as pd
import os
import sys
from telegraph import Telegraph

from aiogram import executor, types
from create_tg_bot import dp, bot
from src.tg_bot import tg_client_kb


from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from telegraph.aio import Telegraph


module_path: str = os.path.abspath(os.path.join('.'))
if module_path not in sys.path:
    sys.path.append(module_path)

MODULE_PATH: str = module_path

data: pd.DataFrame = pd.read_csv(MODULE_PATH + '/data/raw/data_games_list.csv')
count_pc: int = data[data['platform'] == 'PC']['link'].nunique()
count_ps: int = data[data['platform'].str.contains('PS')]['link'].nunique()
count_xbox: int = data[data['platform'].str.contains('Xbox')]['link'].nunique()
count_switch: int = data[data['platform'].str.contains('Switch')]['link'].nunique()


class Start(StatesGroup): 
    user_query = State()




async def on_startup(_):
    print('CR_BOT online')


async def create_telegraph(title, content):
    telegraph = Telegraph()
    print(await telegraph.create_account(short_name='kwis'))

    response = await telegraph.create_page(
        f'{title}',
        html_content=f'<p>{content}</p>',
    )
    return response['url']


    


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    photo_main: str = 'https://vhx.imgix.net/vivaladirtleague/assets/2237b15e-2e27-413b-8073-5a255834405e-fea12d36.jpg?auto=format%2Ccompress&fit=crop&h=720&q=75&w=1280'
    await bot.send_photo(message.from_user.id, photo_main, caption='Hello, adventurer! Nice day for fishing! (c)', reply_markup=tg_client_kb.MAIN)

@dp.message_handler(commands=['help'])
async def command_help(message: types.Message):
    await bot.send_message(message.from_user.id, 'Раздел в разработке', reply_markup=tg_client_kb.HELP)

@dp.callback_query_handler(text="start")
async def return_to_start(message: types.CallbackQuery):
    await message.answer()
    return await command_start(message)

@dp.message_handler()
async def echo_message(message: types.Message):
    await bot.send_message(message.from_user.id, 'Неправильная команда')



@dp.message_handler(state=Start.user_query)
async def telepraph_answer(message: types.Message, state: FSMContext):
    input = message.text
    if input == '/cancel':
        await bot.send_message(message.from_user.id, text='Можно вернуться в главное меню - /start', disable_web_page_preview=True)
        await state.finish()
    else:
        telegraph_link = await create_telegraph(title='Подборка игр:', content=f'{input}')
        await bot.send_message(message.from_user.id, text=f'Результат запроса: {telegraph_link}', disable_web_page_preview=True, reply_markup=tg_client_kb.HELP)
        await state.finish()


message_info =  '''Попробуем сделать запрос?

Введите текстовое описание игры и модель создаст схожую по контексту подборку.

p.s.: для отмены запроса - /cancel'''



@dp.callback_query_handler(lambda callback_query: True)
async def btn_pc(callback_query: types.CallbackQuery):
    if callback_query.data == 'catalog_pc':
        photo_pc: str = 'https://www.tecnogeek.com/wp-content/uploads/2022/01/pc-market.jpg?auto=format%2Ccompress&fit=crop&h=720&q=75&w=1280'
        caption_pc: str = f'Ваш выбор - PC. В базе данных {count_pc} игр для этой платформы. ' + message_info
        await callback_query.answer()
        await callback_query.message.answer_photo(photo_pc, caption=caption_pc)
        await Start.user_query.set()

    elif callback_query.data == 'catalog_xbox':
        photo_xbox: str = 'https://www.ultimaficha.com.br/wp-content/uploads/2021/05/xbox-hd-wallpapers-33922-6759894.jpg?auto=format%2Ccompress&fit=crop&h=720&q=75&w=1280'
        caption_xbox: str = f'Ваш выбор - Xbox. В базе данных {count_xbox} игр для этой платформы. ' + message_info
        await callback_query.answer()
        await callback_query.message.answer_photo(photo_xbox, caption=caption_xbox)
        await Start.user_query.set()

    elif callback_query.data == 'catalog_ps':
        photo_ps = 'https://wallpaper.dog/large/10840928.jpg?auto=format%2Ccompress&fit=crop&h=720&q=75&w=1280'
        caption_ps = f'Ваш выбор - PlayStation. В базе данных {count_ps} игр для этой платформы. ' + message_info
        await callback_query.answer()
        await callback_query.message.answer_photo(photo_ps, caption=caption_ps)
        await Start.user_query.set()

    elif callback_query.data == 'catalog_switch':
        photo_switch: str = 'https://wallpaperaccess.com/full/749930.png?auto=format%2Ccompress&fit=crop&h=720&q=75&w=1280'
        caption_switch: str = f'Ваш выбор - Switch. В базе данных {count_switch} игр для этой платформы. ' + message_info
        await callback_query.answer()
        await callback_query.message.answer_photo(photo_switch, caption=caption_switch)
        await Start.user_query.set()

    elif callback_query.data == 'back_menu':
        return await return_to_start(text='start')




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)