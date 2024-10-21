from g4f.client import Client
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

# Переменная для хранения истории чата
chat_history = []


# Функция для общения с GPT через gpt4free
async def get_gpt_response(prompt: str):
    # Создаем клиента GPT
    client = Client()

    # Отправляем запрос к GPT модели
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


@router.message(F.text)
async def gpt_chat(message: Message):
    # Добавляем сообщение пользователя в историю
    chat_history.append({"role": "user", "content": message.text})

    # Создаем текст запроса для GPT, включая всю историю чата
    prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_history])

    # Получаем ответ от GPT
    gpt_response = await get_gpt_response(prompt)

    # Добавляем ответ GPT в историю чата
    chat_history.append({"role": "assistant", "content": gpt_response})

    # Отправляем ответ пользователю
    await message.answer(gpt_response)
