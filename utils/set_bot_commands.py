from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("help", "Вывести справку"),
            types.BotCommand("get_location", "Нынешнее положение"),
            types.BotCommand("location", "Положение"),
            types.BotCommand("random", "Выбирает случайный квест в вашем городе"),
        ]
    )
