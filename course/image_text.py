import re
import time

from aiogram.dispatcher.filters import Command, Text, CommandStart
from aiogram.types import Message, ContentType
from loader import dp, bot, db
from aiogram import types
from aiogram.contrib.middlewares import logging
from aiogram.dispatcher import FSMContext
import easyocr
from states import ImageTranslate
from data.config import ADMINS
import os
from collections import Counter
from loader import translator_ru_en, translator_en_ru, en,ru

reader  = easyocr.Reader(['ru', 'en'])

@dp.message_handler(Command('translate_photo'))
async def doc_mag(message: Message):
    try:
        await message.answer('пришлите фото')
        await ImageTranslate.first()
    except:
        await message.answer('что-то пошло не так :(')

@dp.message_handler(state=ImageTranslate.It1, content_types= ContentType.PHOTO)
async def enter_message(message: types.Message, state: FSMContext):
    try:
        photo = message.photo[-1].file_id
        path = r"C:\Users\VoronkovSergey\PycharmProjects\reminder\Downloads\image.jpg"
        await message.photo[-1].download(path)
        result = reader.readtext(path, detail=0, paragraph=True)
        print(result)
        text = ' '.join(result)
        text_out = re.sub(r"[^a-zA-Zа-яА-Я]", '', text).lower()
        await message.answer(f'Текст с картинки: \n {text}')
        lang = ['en' if i in en else 'ru' for i in text_out]
        dict_count = Counter(lang)
        if dict_count['en'] > dict_count['ru']:
            text_translate = translator_en_ru(text)[0].get('translation_text')
            await message.answer(f'Перевод: \n {text_translate}')
            # os.remove(path)
            await state.finish()
            # print('текст английский')
        elif dict_count['ru'] > dict_count['en']:
            text_translate = translator_ru_en(text)[0].get('translation_text')
            await message.answer(f'Перевод: \n {text_translate}')
            # os.remove(path)
            await state.finish()
            # print('текст русский')

        # await state.finish()
    except:
        await message.answer('что-то пошло не так :(')
        await state.finish()
#
#

# #
# #
async def text_recognition(file):
    reader  = easyocr.Reader(['ru', 'en'])
    # print('f: ',file)
    result = reader.readtext(file, detail=0, paragraph=True)
    return result
# #
# #     return result
# # def main():
# #     file = 's.png'
# #     print(' '.join(text_recognition(file)))
# #
# #
# # if __name__== '__main__':
# #     main()