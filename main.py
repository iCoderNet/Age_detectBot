import logging,os

from aiogram import Bot, Dispatcher, executor, types
from sqlalchemy import func
from func import predict_age_and_gender 

API_TOKEN = '5030006982:AAG0zmlXKRbHHdXHt_e1uQ-7tOG-lvykOWk'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN,parse_mode='markdown')
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    folder = f"data/{message.from_user.id}"
    if not os.path.isdir(folder):
        os.mkdir(folder)
    await message.reply("...")


@dp.message_handler(content_types=['photo'])
async def echo(message: types.Message):
    folder = f"data/{message.from_user.id}"
    if not os.path.isdir(folder):
        os.mkdir(folder)
    await message.photo[-1].download(folder+'/input.jpg')
    r = predict_age_and_gender(folder+'/input.jpg',folder+'/output.jpg')
    if r['status'] == 'ok':
        tx, s = "", 0
        for k in r['data']:
            s+=1
            i = '🚹' if k['gender'] == 'Male' else '🚺'
            tx+=f'🛃 {s} Person\n{i}Gender: {k["gender"]}\n🚼Age: {k["age"]}\n\n'
        ph=open(r['photo_path'],'rb')
        await message.answer_photo(ph, f'''*I have been able to clarify the picture*\n\n{tx}''')
    else:
        await message.answer(r['status'])

    os.remove(folder+'/input.jpg')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)