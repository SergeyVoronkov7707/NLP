from aiogram import types
from aiogram.contrib.middlewares import logging
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text, CommandStart
from aiogram.types import Message, ContentType
from loader import dp, bot, db
from data.config import ADMINS
import transformers
import re
from transformers import AutoTokenizer, BertTokenizer
from loader import translator_ru_en, translator_en_ru, en,ru
from states import Translate


from collections import Counter




lang = ['en' if i in en else 'ru' for i in text]
dict_count = Counter(lang)
print(lang)



# print(translator_ru_en("сегодня увидел за окном радугу", max_length=40))
# print(translator_en_ru('hello world')[0].get('translation_text'))

# state, translate

@dp.message_handler(Command('translate'))
async def add_depot(message: types.Message):
      await message.answer(f'Введите текст')
      await Translate.first()

@dp.message_handler(state=Translate.Tt1)
async def enter_message(message: types.Message, state: FSMContext):
    try:
      test_word = message.text
      text = re.sub(r"[^a-zA-Zа-яА-Я]", '', test_word).lower()
      # print(text)
      # lang = ['en' for i in text if i in en ]
      lang = ['en' if i in en else 'ru' for i in text]
      lang = set(lang)
      if len(lang) == 1:
            if 'ru' in lang:
                  text_translate = translator_ru_en(test_word)[0].get('translation_text')
                  await message.answer(f'Перевод: \n {text_translate}')
                  await state.finish()
            elif 'en' in lang:
                  text_translate = translator_en_ru(test_word)[0].get('translation_text')
                  await message.answer(f'Перевод: \n {text_translate}')
                  await state.finish()
      else:
            await message.answer('Пожалуйста введите корректный текст, '
                                 'присутствуют символы разных языков')
            await Translate.Tt1.set()
    except:
        await message.answer('что-то пошло не так :(')

