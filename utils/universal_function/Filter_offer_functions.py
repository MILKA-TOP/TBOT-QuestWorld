from datetime import datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from data import MAX_MESSAGE_LENGTH, FILTER_MEDIA_MESSAGE, NEW_PARAMS, NOW_QUEST, MORE_PAGES_SUBCATEGORY_LIST, \
    more_pages_category_dict, ERROR_MESSAGE, log_command_format
from handlers.users.start import bot_start


async def error_func(message: Message, state: FSMContext):
    await message.answer(ERROR_MESSAGE)
    await state.reset_data()
    await bot_start(message=message, state=state)


async def show_add_quest_params(call: CallbackQuery, value: str, quest_value: dict, markup):
    link = quest_value.get("link") + "#{}".format(value)
    message_text = (quest_value.get(value) + "\n" + link)
    if len(message_text) >= MAX_MESSAGE_LENGTH:
        message_text = message_text[:MAX_MESSAGE_LENGTH]
    await call.message.edit_text(text=message_text,
                                 reply_markup=markup)


async def delete_media_message(data: dict, media_message_type):
    if media_message_type in data:
        media_message_list = data.get(media_message_type)
        try:
            for i in range(len(media_message_list)):
                await media_message_list[i].delete()
        except Exception:
            pass


async def delete_category_messages(data: dict, message_type: str, media_message_type: str):
    try:
        message = data.get(message_type)
        if message is not None:
            await message.delete()
            await delete_media_message(data, media_message_type)
    except Exception:
        pass


async def delete_new_params_from_quest(data: dict) -> dict:
    new_params = data.get(NEW_PARAMS)
    all_params = data.get(NOW_QUEST)

    for element_key in list(new_params.keys()):
        del all_params[element_key]
    return all_params


def get_more_page_dict(data: dict) -> dict:
    more_params_dict = dict()
    more_subcategory_pages_dict = data.get(MORE_PAGES_SUBCATEGORY_LIST)
    for element in list(more_pages_category_dict.keys()):

        if more_subcategory_pages_dict is None:
            more_params_dict[element] = dict()
            continue
        more_params_dict[element] = more_subcategory_pages_dict.get(more_pages_category_dict.get(element))

    return more_params_dict


def get_info_person_logging(message: Message, command: str):
    contacts_user = message.chat
    id = contacts_user.id
    username = contacts_user.username
    first_name = contacts_user.first_name
    time = datetime.now()
    return log_command_format.format(id=id, time=time, username=username, first_name=first_name, command=command)
