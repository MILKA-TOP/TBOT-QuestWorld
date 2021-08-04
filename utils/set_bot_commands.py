from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("help", "Список команд"),
            types.BotCommand("filter", "Список квестов по фильтрам "),
            types.BotCommand("get_location", "Запрос нынешнего положени"),
            types.BotCommand("location", "Изменение положения"),
            types.BotCommand("random", "Случайный квест в вашем городе"),
            types.BotCommand("menu", "Открытие/Закрытие меню с командами бота"),
            types.BotCommand("offers", "Акции в вашем городе"),
            types.BotCommand("contacts", "Ссылка на наши социальные сети"),
        ]
    )
