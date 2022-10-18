from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
 
BTN_PC = InlineKeyboardButton('PC', callback_data='catalog_pc')
BTN_XBOX = InlineKeyboardButton('Xbox', callback_data='catalog_xbox')
BTN_PS = InlineKeyboardButton('PlayStation', callback_data='catalog_ps')
BTN_SWITCH = InlineKeyboardButton('Switch', callback_data='catalog_switch')
BTN_BACK = InlineKeyboardButton('Назад', callback_data='start')
BTN_QUERY = InlineKeyboardButton('Запрос', callback_data="user_query")

MAIN = InlineKeyboardMarkup()
MAIN.add(BTN_PS, BTN_XBOX, BTN_SWITCH, BTN_PC)

HELP = InlineKeyboardMarkup()
HELP.add(BTN_BACK)

SUB_MAIN = InlineKeyboardMarkup()
SUB_MAIN.add(BTN_QUERY, BTN_BACK)