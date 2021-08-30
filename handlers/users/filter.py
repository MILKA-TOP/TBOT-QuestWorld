from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import CallbackQuery, Message

from data import default_params_quest_filter, FORMAT_OUTPUT_QUEST_RANDOM, ONE_PAGE_CATEGORY, \
    MORE_PAGES_CATEGORY, more_pages_category_dict, one_page_category_dict, SUBCATEGORIES_TELEGRAM_PAGE_COUNT, \
    quest_difficult_demonstrate, all_category_dict_value, MORE_PAGES_SUBCATEGORY_LIST, NOW_PARAMS_QUEST_FILTER, \
    FILTER_MEDIA_MESSAGE, MORE_PAGE_NUMBER_DICT, NOW_QUEST, FORMAT_OUTPUT_QUEST, QUEST_DICT, DIFFICULTY, \
    ZERO_RESULTS_FILTER, QUESTS_BY_FILTER_BUTTON, QUEST_DESCRIBE, FILTER_MESSAGE, QUEST_TELEGRAM_PAGE_COUNT, \
    NOW_QUEST_PAGE, MAIN_CITY_LINK, MENU_FILTER, PAGE_SUB, UPD_VAL, CATEGORY, TYPE_CALLBACK, SHOW_QUEST, VALUE_CALLBACK, \
    NEXT_VALUE, BACK_VALUE, FILTERED_LINK, PAGE_POSTFIX_LINK, PRETTY_CITY_NAME, VALUE, loading_postfix_message, LINK, \
    show_quest_list_message, OPEN_ADD_INFO, BACK_QUEST, PAGE, BACK_LIST, OPEN_QUEST, CHECKED_LINK_PAGE, QUEST, \
    DEFAULT_PARAM, SEARCH_LIST_QUEST_COUNT, subcategory_info_message
from handlers.users.start import update_data_user
from keyboards.inline import categories_keyboard, subcategories_one_page_keyboard, subcategories_more_page_keyboards, \
    filter_cd, back_menu_filter_markup, main_universal_keyboard, quest_add_params_keyboard, \
    get_main_quest_info_keyboard, quest_cd
from loader import dp
from utils.parse import get_text_now_choose, get_category_list, add_params_to_link, get_quests, get_quest_params
from utils.parse.Filter_Parse import get_text_category
from utils.universal_function import show_add_quest_params, delete_category_messages, \
    delete_media_message, get_more_page_dict, delete_new_params_from_quest, error_func


@dp.message_handler(Command("filter") | Text(QUESTS_BY_FILTER_BUTTON))
async def show_menu(message: types.Message, state: FSMContext):
    data = await state.get_data()
    main_city_link = data.get(MAIN_CITY_LINK)
    from utils.universal_function import get_info_person_logging
    print(get_info_person_logging(message, "filter"))
    if main_city_link is None:
        await update_data_user(state)
        data = await state.get_data()

    if data.get(NOW_PARAMS_QUEST_FILTER) is None:
        await state.update_data(now_params_quest_filter=default_params_quest_filter)

    try:
        await delete_category_messages(data, FILTER_MESSAGE, FILTER_MEDIA_MESSAGE)
        await filter_categories_menu(message, state)
    except Exception as e:
        print("ERROR:", message.date, message.from_user, e, "show_menu")
        await error_func(message, state)


@dp.callback_query_handler(filter_cd.filter())
async def navigate_filter(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer()
    """
    :param call: Тип объекта CallbackQuery, который прилетает в хендлер
    :param callback_data: Словарь с данными, которые хранятся в нажатой кнопке
    :param state: параметр state, хранящий пользовательскую информацию
    """

    # "type_callback", "category", "value_callback", "subcategory_page"

    type_callback = callback_data.get(TYPE_CALLBACK)

    category = callback_data.get(CATEGORY)

    value = callback_data.get(VALUE_CALLBACK)

    levels = {
        MENU_FILTER: filter_categories_menu,  # Показываем список возможных запросов для фильтрации
        ONE_PAGE_CATEGORY: list_one_page_subcategory,  # Отдаем одностраничную подкатегории
        MORE_PAGES_CATEGORY: list_more_page_subcategory,  # Отдаем многостраничные подкатегории
        PAGE_SUB: update_more_subcategory_keyboard,  # Обновление клавиатуру из многостраничной подкатегории
        UPD_VAL: update_filter_information,  # Изменение значения пользователя для последующей фильттрации
        SHOW_QUEST: show_filtered_quests,  # Показать список квестов по фильтрации пользователя
        DEFAULT_PARAM: use_default_params
    }

    current_level_function = levels[type_callback]
    from utils.universal_function import get_info_person_logging
    print(get_info_person_logging(call.message, value))
    try:
        await current_level_function(
            call, state,
            category=category,
            value=value)

    except Exception as e:
        print("ERROR:", call.message.date, call.message.from_user, e, "navigate_filter")
        await error_func(call.message, state)


async def filter_categories_menu(message: Union[CallbackQuery, Message], state: FSMContext, **kwargs):
    markup = await categories_keyboard()
    data = await state.get_data()

    more_page_category_dict = get_more_page_dict(data)

    now_params_quest_filter = data.get(NOW_PARAMS_QUEST_FILTER)
    message_text = get_text_now_choose(now_params_quest_filter, more_page_category_dict, data.get(PRETTY_CITY_NAME))

    if isinstance(message, Message):

        filter_message = await message.answer(text=message_text, reply_markup=markup)
        await state.update_data(filter_message=filter_message)

    elif isinstance(message, CallbackQuery):

        call = message
        await delete_media_message(data, FILTER_MEDIA_MESSAGE)
        await call.message.edit_text(text=message_text, reply_markup=markup)


async def list_one_page_subcategory(callback: CallbackQuery, state: FSMContext, category: str, **kwargs):
    data = await state.get_data()
    now_value = data.get(NOW_PARAMS_QUEST_FILTER).get(one_page_category_dict.get(category))
    markup = await subcategories_one_page_keyboard(category, now_value)
    message_text = subcategory_info_message.format(
        information=get_text_category(data.get(NOW_PARAMS_QUEST_FILTER), get_more_page_dict(data), category))
    await callback.message.edit_text(text=message_text, reply_markup=markup)


async def list_more_page_subcategory(callback: CallbackQuery, state: FSMContext, category: str, **kwargs):
    data = await state.get_data()

    page_dict = dict()
    for elements in list(more_pages_category_dict.values()):
        page_dict[elements] = 0
    await state.update_data(more_page_number_dict=page_dict)

    category_name_value = more_pages_category_dict.get(category)

    now_value_param = data.get(NOW_PARAMS_QUEST_FILTER)[category_name_value]

    more_pages_parse_func = {
        "category_sub": get_category_list
    }

    more_pages_now_func = more_pages_parse_func[category_name_value]

    subcategory_dict = more_pages_now_func(data.get(MAIN_CITY_LINK))

    subcategory_dict_values = dict()
    if MORE_PAGES_SUBCATEGORY_LIST not in data:
        for element in list(more_pages_category_dict.values()):
            subcategory_dict_values[element] = dict()
    else:
        subcategory_dict_values = data.get(MORE_PAGES_SUBCATEGORY_LIST)
    subcategory_dict_values[category_name_value] = subcategory_dict

    await state.update_data(more_pages_subcategory_list=subcategory_dict_values)
    markup = await subcategories_more_page_keyboards(category, now_value_param, subcategory_dict, 0,
                                                     SUBCATEGORIES_TELEGRAM_PAGE_COUNT)

    message_text = subcategory_info_message.format(
        information=get_text_category(data.get(NOW_PARAMS_QUEST_FILTER), get_more_page_dict(data), category))
    await callback.message.edit_text(text=message_text, reply_markup=markup)
    await callback.answer()


async def update_more_subcategory_keyboard(call: CallbackQuery, state: FSMContext, category, value, **kwargs):
    data = await state.get_data()
    value_page_dict = data.get(MORE_PAGE_NUMBER_DICT)
    category_name_val = more_pages_category_dict.get(category)
    page_number = value_page_dict.get(category_name_val)
    now_value_param = data.get(NOW_PARAMS_QUEST_FILTER)

    if value == NEXT_VALUE:
        page_number += 1
    elif value == BACK_VALUE:
        page_number -= 1
    else:
        pass

    value_page_dict[category_name_val] = page_number
    await state.update_data(more_page_number_dict=value_page_dict)

    markup = await subcategories_more_page_keyboards(category, now_value_param.get(category_name_val),
                                                     data.get(MORE_PAGES_SUBCATEGORY_LIST).get(category_name_val),
                                                     page_number * SUBCATEGORIES_TELEGRAM_PAGE_COUNT,
                                                     SUBCATEGORIES_TELEGRAM_PAGE_COUNT)

    await call.message.edit_reply_markup(markup)


async def update_filter_information(call: CallbackQuery, state: FSMContext, category, value, **kwargs):
    data = await state.get_data()
    now_value_param = data.get(NOW_PARAMS_QUEST_FILTER)
    all_category_name_dict = all_category_dict_value
    category_name_param = all_category_name_dict.get(category)
    checked_param = now_value_param.get(all_category_name_dict.get(category))

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
    if category in one_page_category_dict:
        markup = await subcategories_one_page_keyboard(category, checked_param)
    elif category in more_pages_category_dict:
        telegram_page_number = data.get(MORE_PAGE_NUMBER_DICT).get(category_name_param)

        markup = await subcategories_more_page_keyboards(category, checked_param,
                                                         data.get(MORE_PAGES_SUBCATEGORY_LIST).get(
                                                             category_name_param),
                                                         telegram_page_number * SUBCATEGORIES_TELEGRAM_PAGE_COUNT,
                                                         SUBCATEGORIES_TELEGRAM_PAGE_COUNT)

    text = subcategory_info_message.format(
        information=get_text_category(data.get(NOW_PARAMS_QUEST_FILTER), get_more_page_dict(data), category))
    await state.update_data(now_params_quest_filter=now_value_param)
    await call.message.edit_text(text=text, reply_markup=markup)


async def show_filtered_quests(callback: CallbackQuery, state: FSMContext, **kwargs):
    data = await state.get_data()
    now_value = data.get(NOW_PARAMS_QUEST_FILTER)
    search_link = data.get(FILTERED_LINK)
    main_link = data.get(MAIN_CITY_LINK)
    link = add_params_to_link(now_value, search_link) + PAGE_POSTFIX_LINK
    first_page_link = link + "1"
    start_quest_page = 0
    filtered_quests = get_quests(main_link, first_page_link)

    await state.update_data(checked_link_page=link)
    await state.update_data(quest_dict=filtered_quests)
    await state.update_data(now_quest_page=start_quest_page)
    markup, media_group_array = await main_universal_keyboard(filtered_quests, start_quest_page * 6, QUEST_DESCRIBE,
                                                              QUEST, mod_value=12)

    await callback.message.delete()

    if len(media_group_array) == 0:
        await callback.message.answer(ZERO_RESULTS_FILTER.format(city=data.get(PRETTY_CITY_NAME)),
                                      reply_markup=back_menu_filter_markup)
    else:
        media_message = await callback.message.answer_media_group(media_group_array)
        await state.update_data(filer_media_message=media_message)
        filter_message = await callback.message.answer(show_quest_list_message.format(link=first_page_link,
                                                                                      city=data.get(PRETTY_CITY_NAME)),
                                                       reply_markup=markup,
                                                       disable_web_page_preview=True)
        await state.update_data(filter_message=filter_message)
        await state.update_data(filter_link=first_page_link)


async def use_default_params(callback: CallbackQuery, state: FSMContext, **kwargs):
    data = await state.get_data()
    if data.get(NOW_PARAMS_QUEST_FILTER) != default_params_quest_filter:
        await state.update_data(now_params_quest_filter=default_params_quest_filter)
        await filter_categories_menu(callback, state)


@dp.callback_query_handler(quest_cd.filter())
async def navigate_quests(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=1)
    type_callback = callback_data.get(TYPE_CALLBACK)
    value = callback_data.get(VALUE)
    levels = {
        OPEN_QUEST: show_quest,
        OPEN_ADD_INFO: answer_add_quest_params,
        BACK_QUEST: back_to_quest_info,
        PAGE: update_keyboard_page,
        BACK_LIST: back_quest_list
    }
    from utils.universal_function import get_info_person_logging
    print(get_info_person_logging(call.message, value))
    current_level_function = levels[type_callback]
    try:
        await current_level_function(
            call, state,
            value=value
        )
    except Exception as e:
        await error_func(call.message, state)
        print("ERROR:", call.message.date, call.message.from_user, e, "navigate_quests")


async def show_quest(call: CallbackQuery, state: FSMContext, value):
    data = await state.get_data()
    quest_index = value
    all_quests_dict = data.get(QUEST_DICT)
    quest_value = all_quests_dict.get(quest_index)

    difficulty = quest_difficult_demonstrate[quest_value[DIFFICULTY] - 1]
    line = FORMAT_OUTPUT_QUEST_RANDOM.format(dif_text=difficulty, **quest_value, city=data.get(PRETTY_CITY_NAME))

    await call.message.delete()
    await delete_media_message(data, FILTER_MEDIA_MESSAGE)

    message = await call.message.answer(line + loading_postfix_message)
    add_params_quest = get_quest_params(quest_value[LINK])
    quest_value.update(add_params_quest)
    all_quests_dict[quest_index] = quest_value

    await state.update_data(new_params=add_params_quest, now_quest=quest_value)

    new_line = FORMAT_OUTPUT_QUEST.format(dif_text=difficulty, **quest_value)
    markup = await quest_add_params_keyboard(add_params_quest)

    await message.edit_text(new_line)
    await message.edit_reply_markup(markup)
    await state.update_data(filter_message=message)


async def answer_add_quest_params(call: CallbackQuery, state: FSMContext, value, **kwargs):
    data = await state.get_data()
    quest_value = data.get(NOW_QUEST)
    markup = await get_main_quest_info_keyboard(QUEST)
    await show_add_quest_params(call, value, quest_value, markup)


async def back_to_quest_info(call: CallbackQuery, state: FSMContext, **kwargs):
    data = await state.get_data()
    quest_value = data.get(NOW_QUEST)
    difficulty = quest_difficult_demonstrate[quest_value[DIFFICULTY] - 1]
    line = FORMAT_OUTPUT_QUEST.format(dif_text=difficulty, **quest_value)

    await call.message.edit_text(text=line, reply_markup=(await quest_add_params_keyboard(quest_value)))


async def update_keyboard_page(call: CallbackQuery, state: FSMContext, value):
    data = await state.get_data()

    quests = data.get(QUEST_DICT)
    page_number = data.get(NOW_QUEST_PAGE)
    link = data.get(CHECKED_LINK_PAGE)
    main_link = data.get(MAIN_CITY_LINK)

    if value == NEXT_VALUE:
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

    markup, media = await main_universal_keyboard(quests, page_number * QUEST_TELEGRAM_PAGE_COUNT, QUEST_DESCRIBE,
                                                  QUEST, mod_value=SEARCH_LIST_QUEST_COUNT)
    await call.message.delete()
    await delete_media_message(data, FILTER_MEDIA_MESSAGE)
    if media:
        await state.update_data(filer_media_message=(await call.message.answer_media_group(media)))

    filter_link = data.get("filter_link")
    filter_message = await call.message.answer(
        show_quest_list_message.format(link=filter_link, city=data.get(PRETTY_CITY_NAME)), reply_markup=markup,
        disable_web_page_preview=True)
    await state.update_data(filter_message=filter_message)


async def back_quest_list(call: CallbackQuery, state: FSMContext, **kwargs):
    data = await state.get_data()
    await call.message.delete()

    quests = data.get(QUEST_DICT)
    page_number = data.get(NOW_QUEST_PAGE)
    markup, media = await main_universal_keyboard(quests, page_number * QUEST_TELEGRAM_PAGE_COUNT, QUEST_DESCRIBE,
                                                  QUEST, mod_value=SEARCH_LIST_QUEST_COUNT)

    await state.update_data(now_quest=(await delete_new_params_from_quest(data)))
    await state.update_data(filer_media_message=(await call.message.answer_media_group(media)))
    link = data.get("filter_link")
    filter_message = await call.message.answer(
        show_quest_list_message.format(link=link, city=data.get(PRETTY_CITY_NAME)), reply_markup=markup,
        disable_web_page_preview=True)
    await state.update_data(filter_message=filter_message)
