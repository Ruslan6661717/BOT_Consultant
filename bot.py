import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from database import init_db, get_answer, add_answer, delete_answer, list_questions

TOKEN = "6719594903:AAFCZLrj391woSzJwWAKR_A5ncbfjWTp_cc"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()



async def on_startup():
    await init_db()



@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Привет! Я бот-консультант по сантехнике. Задавай вопросы!")



@dp.message(Command("help"))
async def help_cmd(message: types.Message):
    await message.answer("🔹 Отправь мне вопрос, и я постараюсь ответить.\n"
                         "🔹 Добавить новый ответ: `/add Вопрос - Ответ`\n"
                         "🔹 Удалить вопрос: `/delete Вопрос`\n"
                         "🔹 Посмотреть все вопросы: `/list`")



@dp.message(Command("add"))
async def add_multiple_answers_cmd(message: types.Message):
    text = message.text.replace("/add", "").strip()

    if not text:
        await message.answer("Используй формат:\n"
                             "/add\n"
                             "Как выбрать смеситель? - Обрати внимание на материал и тип крепления.\n"
                             "Какие трубы лучше? - Полипропиленовые или металлопластиковые.")
        return

    lines = text.split("\n")
    added_count = 0

    for line in lines:
        if " - " in line:
            question, answer = line.split(" - ", 1)
            question = question.strip().lower()
            answer = answer.strip()

            await add_answer(question, answer)
            added_count += 1

    if added_count > 0:
        await message.answer(f"✅ Добавлено {added_count} вопросов в базу!")
    else:
        await message.answer("❌ Ошибка: не найдено пар 'вопрос - ответ'.")



@dp.message(Command("delete"))
async def delete_answer_cmd(message: types.Message):
    question = message.text.replace("/delete", "").strip().lower()

    if not question:
        await message.answer("❌ Используй команду так:\n`/delete Вопрос который нужно удалить`")
        return

    await delete_answer(question)
    await message.answer(f"✅ Вопрос '{question}' удалён из базы!")



@dp.message(Command("list"))
async def list_questions_cmd(message: types.Message):
    questions = await list_questions()

    if questions:
        text = "📋 Список вопросов:\n" + "\n".join(f"🔹 {q}" for q in questions)
        await message.answer(text)
    else:
        await message.answer("🔹 В базе пока нет вопросов.")



@dp.message()
async def reply_message(message: types.Message):
    question = message.text.lower().strip()
    answer = await get_answer(question)

    if answer:
        await message.answer(answer)
    else:
        await message.answer("❌ Я пока не знаю ответа на этот вопрос.\n"
                             "Добавь его командой `/add Вопрос - Ответ`")



async def main():
    await on_startup()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())