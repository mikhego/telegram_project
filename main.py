import telebot
import pandas as pd
import os
import sys
import asyncio

from src.tg_bot.tg_auth_data import TOKEN
from src.tg_bot import tg_client_kb

from telegraph.aio import Telegraph

module_path = os.path.abspath(os.path.join('.'))
if module_path not in sys.path:
    sys.path.append(module_path)

MODULE_PATH = module_path

data = pd.read_csv(MODULE_PATH + '/data/raw/data_games_list.csv')
count_pc = data[data['platform'] == 'PC']['link'].nunique()
count_ps = data[data['platform'].str.contains('PS')]['link'].nunique()
count_xbox = data[data['platform'].str.contains('Xbox')]['link'].nunique()
count_switch = data[data['platform'].str.contains('Switch')]['link'].nunique()



async def create_telegraph(title, content):
    telegraph = Telegraph()
    await telegraph.create_account(short_name='kwis')

    response = await telegraph.create_page(f'{title}', html_content=f'<p>{content}</p>')
    return response['url']




def telegram_bot(TOKEN):
    bot = telebot.TeleBot(TOKEN, parse_mode=None)

    @bot.message_handler(commands=['start'])
    def catalog_inline(message):
        photo_menu = 'https://vhx.imgix.net/vivaladirtleague/assets/2237b15e-2e27-413b-8073-5a255834405e-fea12d36.jpg?auto=format%2Ccompress&fit=crop&h=720&q=75&w=1280'
        bot.send_photo(message.from_user.id, photo_menu, caption='Hello, adventurer! Nice day for fishing! (c)')
        main_menu = telebot.types.InlineKeyboardMarkup()
        catalog_pc = telebot.types.InlineKeyboardButton(text="PC", callback_data="catalog_pc")
        catalog_xbox = telebot.types.InlineKeyboardButton(text="XBox", callback_data="catalog_xbox")
        catalog_ps = telebot.types.InlineKeyboardButton(text="PS", callback_data="catalog_ps")
        catalog_switch = telebot.types.InlineKeyboardButton(text="Switch", callback_data="catalog_switch")
        main_menu.add(catalog_xbox, catalog_ps, catalog_switch, catalog_pc)
        bot.send_message(message.chat.id, "Выберите платформу", reply_markup=main_menu)


    @bot.callback_query_handler(func=lambda x:True)
    def inline_button(button):
        if button.data == 'catalog_pc':
            bot.send_photo(button.message.chat.id, 'https://www.tecnogeek.com/wp-content/uploads/2022/01/pc-market.jpg?auto=format%2Ccompress&fit=crop&h=720&q=75&w=1280')
            bot.send_message(button.message.chat.id, f'Всего игр в БД PC: {count_pc}')
            menu_catalog= telebot.types.InlineKeyboardMarkup()
            text_query = telebot.types.InlineKeyboardButton(text="Ввести запрос", callback_data="text_query")
            backinmainmenu = telebot.types.InlineKeyboardButton(text="Назад", callback_data="backinmainmenu")
            menu_catalog.add(text_query, backinmainmenu)
            bot.send_message(button.message.chat.id, 'Готовы сделать запрос?', reply_markup=menu_catalog)
        elif button.data == 'catalog_ps':
            bot.send_photo(button.message.chat.id, 'https://wallpaper.dog/large/10840928.jpg?auto=format%2Ccompress&fit=crop&h=720&q=75&w=1280')
            bot.send_message(button.message.chat.id, f'Всего игр в БД PS: {count_ps}')
            menu_catalog = telebot.types.InlineKeyboardMarkup()
            text_query = telebot.types.InlineKeyboardButton(text="Ввести запрос", callback_data="text_query")
            backinmainmenu = telebot.types.InlineKeyboardButton(text="Назад", callback_data="backinmainmenu")
            menu_catalog.add(text_query, backinmainmenu)
            bot.send_message(button.message.chat.id, 'Готовы сделать запрос?', reply_markup=menu_catalog)
        elif button.data == 'catalog_xbox':
            bot.send_photo(button.message.chat.id, 'https://www.ultimaficha.com.br/wp-content/uploads/2021/05/xbox-hd-wallpapers-33922-6759894.jpg?auto=format%2Ccompress&fit=crop&h=720&q=75&w=1280')
            bot.send_message(button.message.chat.id, f'Всего игр в БД Xbox: {count_xbox}')
            menu_catalog = telebot.types.InlineKeyboardMarkup()
            text_query = telebot.types.InlineKeyboardButton(text="Ввести запрос", callback_data="text_query")
            backinmainmenu = telebot.types.InlineKeyboardButton(text="Назад", callback_data="backinmainmenu")
            menu_catalog.add(text_query, backinmainmenu)
            bot.send_message(button.message.chat.id, 'Готовы сделать запрос?', reply_markup=menu_catalog)
        elif button.data == 'catalog_switch':
            bot.send_photo(button.message.chat.id, 'https://wallpaperaccess.com/full/749930.png?auto=format%2Ccompress&fit=crop&h=720&q=75&w=1280')
            bot.send_message(button.message.chat.id, f'Всего игр в БД Switch: {count_switch}')
            menu_catalog = telebot.types.InlineKeyboardMarkup()
            text_query = telebot.types.InlineKeyboardButton(text="Ввести запрос", callback_data="text_query")
            backinmainmenu = telebot.types.InlineKeyboardButton(text="Назад", callback_data="backinmainmenu")
            menu_catalog.add(text_query, backinmainmenu)
            bot.send_message(button.message.chat.id, 'Готовы сделать запрос?', reply_markup=menu_catalog)
        elif button.data == 'backinmainmenu':
            return catalog_inline(button.message)
        elif button.data == 'text_query':
            bot.send_message(button.message.chat.id, 'Введите текстовый запрос описания игры и наша модель создаст схожую по контексту подборку.')
            @bot.message_handler(content_types=['text'])
            def after_text(message):
                input = message.text
                telegraph_link = asyncio.run(create_telegraph(title='Подборка игр:', content=f'{input}'))
                print(telegraph_link)
                text_link = f'Результаты обработки запроса: {telegraph_link}'
                bot.send_message(message.chat.id, text_link, disable_web_page_preview=True)


    bot.polling()

if __name__ == '__main__':
    telegram_bot(TOKEN)
