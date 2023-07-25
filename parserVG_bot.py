import json 
from aiogram import Bot, Dispatcher, executor, types
# from config import token
from aiogram.dispatcher.filters import Text
from func_vg_no import check_update
import asyncio



user_id = 12121212
token = ''
bot = Bot(token=token)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttns = ['All news', 'Fresh news']
    keyboar = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboar.add(*start_buttns)
    await message.answer('News hot line', reply_markup=keyboar)

@dp.message_handler(Text(equals='All news'))
async def get_all_news(message: types.Message):
    with open('vg.json') as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items()):
        news =f'{v["time_news"]}\n{v["url"]}'
        
        await message.answer(news)     

@dp.message_handler(Text(equals='Fresh news'))
async def fresh_VG_news(message: types.Message):
        fresh_news = check_update()
        if len(fresh_news) >= 1:
            for k, v in sorted(fresh_news.items())[-3:]:
                news =f'{v["time_news"]}\n{v["url"]}'
                await message.answer(news)     
        else:
             await message.answer('Have not fresh news...')

async def every_30min_news():
     while True:
        fresh_news = check_update()
        if len(fresh_news) >= 1:
            for k, v in sorted(fresh_news.items())[-3:]:
                news =f'{v["time_news"]}\n{v["url"]}'
                #get your id @userinfobot
                await bot.send_message(user_id, news, disable_notification=True)
        else:
            await bot.send_message(user_id, 'Haven`t new News yet')
        
        await asyncio.sleep(30)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(every_30min_news())
    executor.start_polling(dp)
    