from pathlib import Path

from dotenv import load_dotenv
import os

from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import F

from app.parsing_vacancies import ApiHh, ApiHabr

BASE_DIR = Path(__file__).parent.parent
dot_env = Path(BASE_DIR, '.env')

load_dotenv(dotenv_path=dot_env)

bot_token = os.getenv('BOT_TOKEN')

bot = Bot(bot_token)
dp = Dispatcher()

hh_parser = ApiHh()
habr_parser = ApiHabr()


@dp.message(Command('start'))
async def start(message: Message):
    await message.reply(
        "Привет! Я подбираю вакансии, но я еще тупой. Поэтому не злись.\nВведи команду /find, чтобы начать поиск.")


@dp.message(Command('find'))
async def find_vacancy(message: Message):
    await message.answer("Введите название вакансии, которую вы хотите найти:")

@dp.message()
async def process_job_search(message: types.Message):
    job_title = message.text
    await message.answer(f"Ищу вакансии для: {job_title}...")

    try:
        # Получение данных с hh.ru
        hh_vacancies = await hh_parser.get_vacancy_from_api([job_title])
        print("Полученные вакансии с hh.ru:", hh_vacancies)  # Отладка
        hh_cleaned = hh_parser.clean_vacancies_list(hh_vacancies)
        print(hh_cleaned)

        if not hh_cleaned:
            await message.answer("К сожалению, вакансий по вашему запросу не найдено.")
            return

        # Отправка результатов пользователю
        response = "\n\n".join(
            [
                f"📌 {vacancy['name_vacancy']}\n"
                f"💼 Компания: {vacancy['company']}\n"
                f"🌍 Локация: {vacancy['location']}\n"
                f"💰 Зарплата: от {vacancy['salary_from']} до {vacancy['salary_to']}\n"
                f"🔗 [Ссылка на вакансию]({vacancy['url']})"
                for vacancy in hh_cleaned[:10]  # Отправляем первые 5 вакансий
            ]
        )
        await message.answer(response, disable_web_page_preview=True)
    except Exception as e:
        await message.answer("Произошла ошибка при поиске вакансий. Попробуйте позже.")
        print(e)


async def main():
    try:
        print("Запуск бота...")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
