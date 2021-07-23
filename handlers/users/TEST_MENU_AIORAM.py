from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, Message

from data import default_params_quest_filter, type_filter, type_filter_list
from handlers.users.start import update_data_user
from keyboards.inline.TEST_AIOGRAM_INLINE_STRUCT import menu_cd, categories_keyboard, subcategories_keyboard, \
    update_value, more_keyboards, page_checking, quest_keyboard, quest_page_checking
from loader import dp
from middlewares import get_filter_quests_list, get_category_list


# Хендлер на команду /menu
@dp.message_handler(Command("filter"))
async def show_menu(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if len(data) == 0:
        await update_data_user(state)

    data = await state.get_data()
    if data.get("now_params_quest_filter") is None:
        await state.update_data(now_params_quest_filter=default_params_quest_filter)

    await list_categories(message, state)


# Та самая функция, которая отдает категории. Она может принимать как CallbackQuery, так и Message
# Помимо этого, мы в нее можем отправить и другие параметры - category, subcategory, item_id,
# Поэтому ловим все остальное в **kwargs
async def list_categories(message: Union[CallbackQuery, Message], state: FSMContext, **kwargs):
    # Клавиатуру формируем с помощью следующей функции (где делается запрос в базу данных)
    markup = await categories_keyboard()

    # Проверяем, что за тип апдейта. Если Message - отправляем новое сообщение
    if isinstance(message, Message):
        await message.answer(f"Смотри, что у нас есть\n\n{(await state.get_data()).get('now_params_quest_filter')}",
                             reply_markup=markup)

    # Если CallbackQuery - изменяем это сообщение
    elif isinstance(message, CallbackQuery):
        call = message
        await call.message.delete_reply_markup()
        await call.message.delete()
        await call.message.answer(
            f"Смотри, что у нас есть\n\n{(await state.get_data()).get('now_params_quest_filter')}",
            reply_markup=markup)


async def list_one(callback: CallbackQuery, state: FSMContext, category, **kwargs):
    data = await state.get_data()
    now_value = data.get("now_params_quest_filter")[type_filter_list.index(category)]
    markup = await subcategories_keyboard(category, now_value)

    # Изменяем сообщение, и отправляем новые кнопки с подкатегориями
    await callback.message.edit_reply_markup(markup)


async def list_more(callback: CallbackQuery, state, category, **kwargs):
    data = await state.get_data()
    await state.update_data(category_count=0)
    now_value = data.get("now_params_quest_filter")[type_filter_list.index(category)]
    text_list, values_list = get_category_list(data.get("main_city_link"))
    await state.update_data(category_lists=[text_list, values_list])
    markup = await more_keyboards(category, now_value, text_list, values_list, 0)

    # Изменяем сообщение, и отправляем новые кнопки с подкатегориями
    await callback.message.edit_reply_markup(markup)


async def show(callback: CallbackQuery, state: FSMContext, category, **kwargs):
    data = await state.get_data()
    now_value = data.get("now_params_quest_filter")
    search_link = data.get("filtered_link")
    main_link = data.get("main_city_link")

    # Изменяем сообщение, и отправляем новые кнопки с подкатегориями
    filtered_quests = get_filter_quests_list(now_value, search_link, main_link)
    await state.update_data(quest_dict=filtered_quests)
    await state.update_data(quest_page=0)
    markup = await quest_keyboard(filtered_quests, 0)
    await callback.message.edit_text(
        "Здесь указан список квестов по вашим фильтрам")
    await callback.message.edit_reply_markup(markup)


@dp.callback_query_handler(quest_page_checking.filter())
async def update_keyboard_page(call: CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()

    quests = data.get("quest_dict")
    value_page = data.get("quest_page")
    if callback_data.get("orientation") == "next":
        value_page += 7
    else:
        value_page -= 7

    await state.update_data(quest_page=value_page)

    markup = await quest_keyboard(quests, value_page * 7)

    await call.message.edit_reply_markup(markup)


@dp.callback_query_handler(page_checking.filter())
async def update_keyboard_page(call: CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()

    value_page = data.get("category_count")
    now_value = data.get("now_params_quest_filter")
    array_check = data.get("category_lists")
    text_list = array_check[0]
    values_list = array_check[1]

    if callback_data.get("orientation") == "next":
        value_page += 8
    else:
        value_page -= 8
    await state.update_data(category_count=value_page)
    markup = await more_keyboards("Жанр", now_value, text_list, values_list, value_page)

    await call.message.edit_reply_markup(markup)


@dp.callback_query_handler(update_value.filter())
async def update_filter_information(call: CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()
    now_list = data.get("now_params_quest_filter")
    category = callback_data.get("category")
    value = callback_data.get("value")
    keyboard = callback_data.get("type_keyboard")
    temp_index = list(type_filter.keys()).index(category)

    if isinstance(now_list[temp_index], list):
        if value not in now_list[temp_index]:
            now_list[temp_index].append(value)
        else:
            now_list[temp_index].remove(value)
    else:
        now_list[temp_index] = value

    levels = {
        "subcategories": subcategories_keyboard,  # Отдаем категории
        "more": more_keyboards
    }

    # Забираем нужную функцию для выбранного уровня
    if keyboard == "subcategories":
        markup = await subcategories_keyboard(category, now_list[temp_index])
    else:
        value_page = data.get("category_count")
        now_value = data.get("now_params_quest_filter")
        array_check = data.get("category_lists")
        text_list = array_check[0]
        values_list = array_check[1]

        markup = await more_keyboards("Жанр", now_value, text_list, values_list, value_page)
    await state.update_data(now_params_quest_filter=now_list)
    await call.message.delete_reply_markup()
    await call.message.delete()
    await call.message.answer(
        f"Смотри, что у нас есть\n\n{(await state.get_data()).get('now_params_quest_filter')}",
        reply_markup=markup)
    # Функция, которая обрабатывает ВСЕ нажатия на кнопки в этой менюшке


@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: CallbackQuery, callback_data: dict, state: FSMContext):
    """
    :param call: Тип объекта CallbackQuery, который прилетает в хендлер
    :param callback_data: Словарь с данными, которые хранятся в нажатой кнопке
    """

    # "level", "category", "value", "not_one_result"

    # Получаем текущий уровень меню, который запросил пользователь
    current_level = callback_data.get("level")

    # Получаем категорию, которую выбрал пользователь (Передается всегда)
    category = callback_data.get("category")

    # Получаем подкатегорию, которую выбрал пользователь (Передается НЕ ВСЕГДА - может быть 0)
    subcategory = callback_data.get("subcategory")

    # Получаем айди товара, который выбрал пользователь (Передается НЕ ВСЕГДА - может быть 0)
    value = callback_data.get("value")

    # Прописываем "уровни" в которых будут отправляться новые кнопки пользователю
    levels = {
        "menu": list_categories,  # Отдаем категории
        "one_choice": list_one,  # Отдаем подкатегории
        "more_choice": list_more,  # Отдаем товары
        "level_check": list_categories,  # Предлагаем купить товар
        "show": show  # Предлагаем купить товар
    }

    # Забираем нужную функцию для выбранного уровня
    current_level_function = levels[current_level]

    # Выполняем нужную функцию и передаем туда параметры, полученные из кнопки
    await current_level_function(
        call, state,
        category=category,
        subcategory=subcategory,
        value=value
    )
