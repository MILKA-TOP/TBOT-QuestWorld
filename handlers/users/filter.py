from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import CallbackQuery, Message

from data import default_params_quest_filter, category_filter_dict, type_filter_list, quest_difficult_filter, \
    FORMAT_OUTPUT_QUEST_RANDOM, ONE_PAGE_CATEGORY_TEXT, MORE_PAGES_CATEGORY_TEXT, more_pages_category_dict, filter_type, \
    one_page_category_dict, SUBCATEGORIES_TELEGRAM_PAGE_COUNT, quest_difficult_demonstrate, all_category_dict_value, \
    more_pages_subcategory_list_str, now_params_quest_filter_str, media_message_str, page_number_dict_str, \
    now_quest_str, new_params_str, FORMAT_OUTPUT_QUEST, quest_dict_str, index_str, difficulty_str, ZERO_RESULTS_FILTER, \
    ERROR_MESSAGE, QUESTS_BY_FILTER_BUTTON, MAX_MESSAGE_LENGTH
from data.Texts import now_quest_page_str
from handlers.users.start import update_data_user, bot_start
from keyboards.inline.Filter_inline_keyboard import categories_keyboard, subcategories_one_page_keyboard, \
    subcategories_more_page_keyboards, quest_keyboard, quest_add_params_keyboard, back_quest_menu_inline_markup, \
    filter_cd, quest_cd, back_menu_filter_markup
from loader import dp
from utils.parse import get_text_now_choose, get_category_list, add_params_to_link
from utils.parse.ParseCitySite import get_quests
from utils.parse.ParseQuestSite import get_quest_params


async def delete_filter_mes(data: dict):
    try:
        filter_message = data.get("filter_message")
        if filter_message is not None:
            await filter_message.delete()
            await delete_media_message(data, media_message_str)
    except Exception:
        pass


async def delete_media_message(data: dict, media_message_type):
    if media_message_type in data:
        media_message_list = data.get(media_message_type)
        try:
            for i in range(len(media_message_list)):
                await media_message_list[i].delete()
        except Exception:
            pass


async def delete_new_params_from_quest(data: dict) -> dict:
    new_params = data.get(new_params_str)
    all_params = data.get(now_quest_str)

    for element_key in list(new_params.keys()):
        del all_params[element_key]
    return all_params


def get_more_page_dict(data: dict) -> dict:
    more_params_dict = dict()
    more_subcategory_pages_dict = data.get(more_pages_subcategory_list_str)
    for element in list(more_pages_category_dict.keys()):

        if more_subcategory_pages_dict is None:
            more_params_dict[element] = dict()
            continue
        more_params_dict[element] = more_subcategory_pages_dict.get(more_pages_category_dict.get(element))

    return more_params_dict


@dp.message_handler(Command("filter") | Text(QUESTS_BY_FILTER_BUTTON))
async def show_menu(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if len(data) == 0:
        await update_data_user(state)

    data = await state.get_data()
    if data.get(now_params_quest_filter_str) is None:
        await state.update_data(now_params_quest_filter=default_params_quest_filter)

    await delete_filter_mes(data)
    await filter_categories_menu(message, state)


@dp.callback_query_handler(filter_cd.filter())
async def navigate_filter(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=1)
    """
    :param call: Тип объекта CallbackQuery, который прилетает в хендлер
    :param callback_data: Словарь с данными, которые хранятся в нажатой кнопке
    :param state: параметр state, хранящий пользовательскую информацию
    """

    # "type_callback", "category", "value_callback", "subcategory_page"

    type_callback = callback_data.get("type_callback")

    category = callback_data.get("category")

    value = callback_data.get("value_callback")

    levels = {
        "menu_filter": filter_categories_menu,  # Отдаем категории
        ONE_PAGE_CATEGORY_TEXT: list_one_page_subcategory,  # Отдаем подкатегории
        MORE_PAGES_CATEGORY_TEXT: list_more_page_subcategory,  # Отдаем товары
        "page_sub": update_more_subcategory_keyboard,
        "upd_val": update_filter_information,
        "show_quest": show_filtered_quests
    }

    # Забираем нужную функцию для выбранного уровня
    current_level_function = levels[type_callback]
    try:
        # Выполняем нужную функцию и передаем туда параметры, полученные из кнопки
        await current_level_function(
            call, state,
            category=category,
            value=value)
    except Exception:
        await call.message.answer(ERROR_MESSAGE)
        await state.reset_data()
        await bot_start(message=call.message, state=state)


# Та самая функция, которая отдает категории. Она может принимать как CallbackQuery, так и Message
# Помимо этого, мы в нее можем отправить и другие параметры - category, subcategory, item_id,
# Поэтому ловим все остальное в **kwargs
async def filter_categories_menu(message: Union[CallbackQuery, Message], state: FSMContext, **kwargs):
    # Клавиатуру формируем с помощью следующей функции (где делается запрос в базу данных)
    markup = await categories_keyboard()
    data = await state.get_data()

    more_page_dict = get_more_page_dict(data)

    now_params_quest_filter = data.get(now_params_quest_filter_str)
    message_text = get_text_now_choose(now_params_quest_filter, more_page_dict)

    if isinstance(message, Message):

        filter_message = await message.answer(text=message_text, reply_markup=markup)
        await state.update_data(filter_message=filter_message)

    elif isinstance(message, CallbackQuery):

        call = message
        await delete_media_message(data, media_message_str)
        await call.message.edit_text(text=message_text, reply_markup=markup)


async def list_one_page_subcategory(callback: CallbackQuery, state: FSMContext, category: str, **kwargs):
    data = await state.get_data()
    now_value = data.get(now_params_quest_filter_str).get(one_page_category_dict.get(category))
    markup = await subcategories_one_page_keyboard(category, now_value)

    await callback.message.edit_reply_markup(markup)


async def list_more_page_subcategory(callback: CallbackQuery, state: FSMContext, category: str, **kwargs):
    data = await state.get_data()

    page_dict = dict()
    for elements in list(more_pages_category_dict.values()):
        page_dict[elements] = 0
    await state.update_data(page_number_dict=page_dict)

    category_name_value = more_pages_category_dict.get(category)

    now_value_param = data.get(now_params_quest_filter_str)[category_name_value]

    more_pages_parse_func = {
        "category_sub": get_category_list
    }

    more_pages_now_func = more_pages_parse_func[category_name_value]

    subcategory_dict = more_pages_now_func(data.get("main_city_link"))

    subcategory_dict_values = dict()
    if more_pages_subcategory_list_str not in data:
        for element in list(more_pages_category_dict.values()):
            subcategory_dict_values[element] = dict()
    else:
        subcategory_dict_values = data.get(more_pages_subcategory_list_str)
    subcategory_dict_values[category_name_value] = subcategory_dict

    await state.update_data(more_pages_subcategory_list=subcategory_dict_values)
    markup = await subcategories_more_page_keyboards(category, now_value_param, subcategory_dict, 0,
                                                     SUBCATEGORIES_TELEGRAM_PAGE_COUNT)

    await callback.message.edit_reply_markup(markup)
    await callback.answer()


async def update_more_subcategory_keyboard(call: CallbackQuery, state: FSMContext, category, value, **kwargs):
    data = await state.get_data()
    value_page_dict = data.get(page_number_dict_str)
    category_name_val = more_pages_category_dict.get(category)
    page_number = value_page_dict.get(category_name_val)
    now_value_param = data.get(now_params_quest_filter_str)

    if value == "next":
        page_number += 1
    else:
        page_number -= 1
    value_page_dict[category_name_val] = page_number
    await state.update_data(page_number_dict=value_page_dict)

    markup = await subcategories_more_page_keyboards(category, now_value_param.get(category_name_val),
                                                     data.get(more_pages_subcategory_list_str).get(category_name_val),
                                                     page_number * SUBCATEGORIES_TELEGRAM_PAGE_COUNT,
                                                     SUBCATEGORIES_TELEGRAM_PAGE_COUNT)

    await call.message.edit_reply_markup(markup)


async def update_filter_information(call: CallbackQuery, state: FSMContext, category, value, **kwargs):
    data = await state.get_data()
    now_value_param = data.get(now_params_quest_filter_str)
    all_category_name_dict = all_category_dict_value
    category_name_param = all_category_name_dict.get(category)
    checked_param = now_value_param.get(category_name_param)

    keyboard = str()
    if category in one_page_category_dict:
        keyboard = "one_page_keyboard"
    elif category in more_pages_category_dict:
        keyboard = "more_pages_keyboard"

    if isinstance(checked_param, list):
        if value not in checked_param:
            checked_param.append(value)
        else:
            checked_param.remove(value)
    else:
        if checked_param == value:
            checked_param = default_params_quest_filter.get(all_category_name_dict[category])
        else:
            checked_param = value

    now_value_param[category_name_param] = checked_param

    markup = None
    if keyboard == "one_page_keyboard":
        markup = await subcategories_one_page_keyboard(category, checked_param)
    elif keyboard == "more_pages_keyboard":
        telegram_page_number = data.get(page_number_dict_str).get(category_name_param)

        markup = await subcategories_more_page_keyboards(category, checked_param,
                                                         data.get(more_pages_subcategory_list_str).get(
                                                             category_name_param),
                                                         telegram_page_number * SUBCATEGORIES_TELEGRAM_PAGE_COUNT,
                                                         SUBCATEGORIES_TELEGRAM_PAGE_COUNT)

    text = get_text_now_choose(data.get(now_params_quest_filter_str), get_more_page_dict(data))
    await state.update_data(now_params_quest_filter=now_value_param)
    await call.message.edit_text(text=text, reply_markup=markup)


async def show_filtered_quests(callback: CallbackQuery, state: FSMContext, category, **kwargs):
    data = await state.get_data()
    now_value = data.get(now_params_quest_filter_str)
    search_link = data.get("filtered_link")
    main_link = data.get("main_city_link")
    link = add_params_to_link(now_value, search_link) + "&page="
    first_page_link = link + "1"
    start_quest_page = 0
    filtered_quests = get_quests(main_link, first_page_link)

    await state.update_data(checked_link_page=link)
    await state.update_data(quest_dict=filtered_quests)
    await state.update_data(now_quest_page=start_quest_page)
    markup, media_group_array, text = await quest_keyboard(filtered_quests, start_quest_page)

    await callback.message.delete()

    if len(media_group_array) == 0:
        await callback.message.answer(ZERO_RESULTS_FILTER.format(city=data.get("pretty_city_name")),
                                      reply_markup=back_menu_filter_markup)
    else:
        media_message = await callback.message.answer_media_group(media_group_array)
        await state.update_data(media_message=media_message)
        filter_message = await callback.message.answer(first_page_link, reply_markup=markup,
                                                       disable_web_page_preview=True)
        await state.update_data(filter_message=filter_message)


@dp.callback_query_handler(quest_cd.filter())
async def navigate_quests(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=1)
    type_callback = callback_data.get("type_callback")
    value = callback_data.get("value")
    levels = {
        "open_quest": show_quest,
        "open_add_info": answer_add_quest_params,
        "back_quest": back_to_quest_info,
        "page_quests": update_keyboard_page,
        "back_list": back_quest_list
    }

    current_level_function = levels[type_callback]
    try:
        await current_level_function(
            call, state,
            value=value
        )
    except Exception:
        await call.message.answer(ERROR_MESSAGE)
        await state.reset_data()
        await bot_start(message=call.message, state=state)


async def show_quest(call: CallbackQuery, state: FSMContext, value):
    data = await state.get_data()
    quest_index = value
    all_quests_dict = data.get(quest_dict_str)
    quest_value = all_quests_dict.get(quest_index)

    difficulty = quest_difficult_demonstrate[quest_value[difficulty_str] - 1]
    line = FORMAT_OUTPUT_QUEST_RANDOM.format(dif_text=difficulty, **quest_value)

    await call.message.delete()
    await delete_media_message(data, media_message_str)

    message = await call.message.answer(line + "\n\nЗагрузка...")
    add_params_quest = get_quest_params(quest_value["link"])
    quest_value.update(add_params_quest)
    all_quests_dict[quest_index] = quest_value

    await state.update_data(new_params=add_params_quest)
    await state.update_data(now_quest=quest_value)

    new_line = FORMAT_OUTPUT_QUEST.format(dif_text=difficulty, **quest_value)
    markup = await quest_add_params_keyboard(add_params_quest)

    await message.edit_text(new_line)
    await message.edit_reply_markup(markup)
    await state.update_data(filter_message=message)


async def answer_add_quest_params(call: CallbackQuery, state: FSMContext, value, **kwargs):
    data = await state.get_data()
    link = data.get(now_quest_str).get("link") + "#{}".format(value)
    message_text = (data.get(now_quest_str).get(value) + "\n" + link)
    if len(message_text) >= MAX_MESSAGE_LENGTH:
        message_text = message_text[:MAX_MESSAGE_LENGTH]
    await call.message.edit_text(text=message_text,
                                 reply_markup=back_quest_menu_inline_markup)


async def back_to_quest_info(call: CallbackQuery, state: FSMContext, **kwargs):
    data = await state.get_data()
    quest_value = data.get(now_quest_str)
    difficulty = quest_difficult_demonstrate[quest_value[difficulty_str] - 1]
    line = FORMAT_OUTPUT_QUEST.format(dif_text=difficulty, **quest_value)

    await call.message.edit_text(text=line, reply_markup=(await quest_add_params_keyboard(quest_value)))


async def update_keyboard_page(call: CallbackQuery, state: FSMContext, value):
    data = await state.get_data()

    quests = data.get(quest_dict_str)
    page_number = data.get(now_quest_page_str)
    link = data.get("checked_link_page")
    main_link = data.get("main_city_link")

    if value == "next":
        if page_number % 2 != 0:
            link = link + str(page_number // 2 + 2)
            quests = get_quests(main_link, link)
            await state.update_data(quest_dict=quests)

        page_number += 1
    else:
        if page_number % 2 == 0:
            link = link + str(page_number // 2)
            quests = get_quests(main_link, link)
            await state.update_data(quest_dict=quests)
        page_number -= 1

    await state.update_data(now_quest_page=page_number)

    markup, media, text = await quest_keyboard(quests, page_number * 6)
    await call.message.delete()
    await delete_media_message(data, media_message_str)
    if media:
        await state.update_data(media_message=(await call.message.answer_media_group(media)))
    filter_message = await call.message.answer("Выберите квест из списка:", reply_markup=markup)
    await state.update_data(filter_message=filter_message)


async def back_quest_list(call: CallbackQuery, state: FSMContext, **kwargs):
    data = await state.get_data()
    await call.message.delete()

    quests = data.get(quest_dict_str)
    page_number = data.get(now_quest_page_str)
    markup, media, text = await quest_keyboard(quests, page_number * 6)

    await state.update_data(now_quest=(await delete_new_params_from_quest(data)))
    await state.update_data(media_message=(await call.message.answer_media_group(media)))
    filter_message = await call.message.answer("Выберите квест из списка:", reply_markup=markup)
    await state.update_data(filter_message=filter_message)
