START_TEXT = """
Привет! 
Добро пожаловать в <i> тестовый телеграмм бот </i> компании "Мир Квестов"
"""

HELP_TEXT = """
Ниже представлен список команд бота:
    
    /filter - Список квестов по фильтрам 
    /random - Случайный квест в вашем городе
    /offers - Акции в вашем городе
    /location - Изменение положения
    /get_location - Запрос нынешнего положени
    /contacts - Ссылка на наши социальные сети
    /help - Список команд
    /menu - Открытие/Закрытие меню с командами бота
"""

ZERO_RESULTS_FILTER = """В городе {city}  не было найдено ни одного квеста по вашим фильтрам.

Попробуйте изменить параметры фильтров"""

FORMAT_OUTPUT_QUEST_RANDOM = """
<b>Название:</b> {name}
<b>Возрастные ограничения:</b> {age}
<b>Количество человек:</b> {people_count}
<b>Сложность:</b> {dif_text}
<b>Тип игры:</b> {type}
<b>Рейтинг по отзвам:</b>{rating}
<b>Город:</b> {city}
<b>Ссылка:</b> {link}
"""

FORMAT_OUTPUT_QUEST = """
<b>Название:</b> {name}
<b>Возрастные ограничения:</b> {age}
<b>Количество человек:</b> {people_count}
<b>Сложность:</b> {dif_text}
<b>Тип игры:</b> {type}
<b>Рейтинг по отзвам:</b>{rating}
<b>Время:</b> {time}
<b>Уровень страха:</b> {scary_level}
<b>Цены:</b> {price}

<b>Ссылка:</b> {link}

"""

CONTACTS = """Наши социальные сети:

▫️<a href="https://vk.com/mirkvestov_ru"> ВКОНТАКТЕ </a>

▫️<a href="https://www.instagram.com/mirkvestov/"> Instagram </a>

▫️<a href="https://twitter.com/mir_kvestov"> Twitter </a>

▫️<a href="https://www.facebook.com/mirkvestov.ru/"> Facebook </a>

▫️<a href="https://t.me/mirkvestovru"> Telegram-канал  </a>

▫️<a href="https://www.youtube.com/channel/UCzu7XwVL_uiFRF5IWdpcl7w"> YouTube  </a>



"""

FORMAT_OUTPUT_QUEST_ADD = """
Время: {}
Уровень страха: {}
Цены: {}
"""

NOW_CHECK_LOCATION = """Квесты рассматриваются в городе {}."""

CITY_TAKE = """Введите пожалуйста город, в котором вы хотите выбрать квесты.

<i>В случае отмены пропишите /cancel</i>"""

CITY_ERROR = """Данного города нет в базе данных, либо вы опечатались. Пожалуйста, введите другой город.

<i>В случае отмены пропишите /cancel</i>"""

FULL_QUESTS_POSTFIX = "/quests"
FILTER_QUESTS_POSTFIX = "/quests/search?"
OFFERS_QUESTS_POSTFIX = "/offers"
PAGE_POSTFIX_LINK = "&page="

QUEST_DESCRIBE = """{number}) {name}:
Количество человек: {people_count}
Сложность: {difficulty_key} ({difficulty_word})
Рейтинг: {rating_star} {rating_num}

"""

OFFER_DESCRIBE = """{number}) <b>{name}</b>:
{description}

"""

ONE_PAGE_CATEGORY = "one_sub"
MORE_PAGES_CATEGORY = "more_sub"

QUEST_LINE = "{numb}) {name}"

MAIN_CITY_LINK = "main_city_link"
MORE_PAGES_SUBCATEGORY_LIST = "more_pages_subcategory_list"
NOW_PARAMS_QUEST_FILTER = "now_params_quest_filter"
NEW_QUEST_VALUE = "new_quest_value"
QUEST_VALUE = "quest_value"
FILTER_MEDIA_MESSAGE = "filer_media_message"
OFFERS_MEDIA_MESSAGE = "offers_media_message"
MORE_PAGE_NUMBER_DICT = "more_page_number_dict"
NEW_PARAMS = "new_params"
NOW_QUEST = "now_quest"
OFFER = "offer"
QUEST = "quest"
FILTER = "filter"
QUEST_DICT = "quest_dict"
OFFERS_DICT = "offers_dict"
INDEX = "index"
DIFFICULTY = "difficulty"
NOW_QUEST_PAGE = "now_quest_page"
FILTER_MESSAGE = "filter_message"
OFFERS_MESSAGE = "offers_message"
MENU_FILTER = "menu_filter"
PAGE_SUB = "page_sub"
UPD_VAL = "upd_val"
SHOW_QUEST = "show_quest"
CATEGORY = "category"
TYPE_CALLBACK = "type_callback"
VALUE_CALLBACK = "value_callback"
VALUE = "value"
NEXT_VALUE = "next"
BACK_VALUE = "back"
ONE_PAGE_KEYBOARD = "one_page_keyboard"
MORE_PAGES_KEYBOARD = "more_pages_keyboard"
FILTERED_LINK = "filtered_link"
PRETTY_CITY_NAME = "pretty_city_name"
LINK = "link"
OPEN_ADD_INFO = "open_add_info"
BACK_QUEST = "back_quest"
PAGE = "page"
OFFER_PAGE = "offer_page"
BACK_LIST = "back_list"
OPEN_QUEST = "open_quest"
OPEN_OFFER = "open_offer"
CHECKED_LINK_PAGE = "checked_link_page"
DEFAULT_PARAM = "default_param"
OFFER_TYPE = "offer_type"

ERROR_MESSAGE = """
Произошла непредвиденная ошибка в работе бота.

Ваши данные были обновлены до начальных. 
По возможности напишите пожалуйста ваши последние действия следующему контакту @КОНТАКТЫ.
"""

CLOSE_MENU_KEYBOARD_MESSAGE = """Ваша клавиатура была скрыта. 

<i>Для её открытия используйте команду /menu</i>"""

OPEN_MENU_KEYBOARD_MESSAGE = """Ваша клавиатура была открыта. 

<i>Для её закрытия используйте команду /menu</i>"""

QUESTS_BY_FILTER_BUTTON = "🔍 Выбор квеста по фильтрам"
RANDOM_QUEST_BUTTON = "🎲 Случайный квест"
OFFERS_BUTTON = "💸 Акции в вашем городе"
GET_CITY_BUTTON = "🏙 Выбор города"
CONTACTS_BUTTON = "📞 Контакты"
HELP_BUTTON = "💭 Команды бота"
NEXT_PAGE_BUTTON = "➡️"
PREV_PAGE_BUTTON = "⬅️"
TO_INLINE_LIST_BUTTON = "📋 К списку"
MENU_INLINE_BUTTON = "🏠 К меню"
SHOW_QUEST_LIST_BUTTON = "🗝 Показать квесты по фильтру"
QUEST_BACK_INFO_BUTTON = "🗝 К основной информации квеста"
DEFAULT_PARAM_BUTTON = "❇️ Установить настройки по умолчанию"

OFFER_MESSAGE = "<b>{head}:</b>\n\n{body}"
loading_postfix_message = "\n\nЗагрузка..."
show_quest_list_message = """Выберите квест из <a href="{link}"> списка </a> ({city}):"""
show_offer_list_message = "Выберите акцию из списка ({city}):"
zero_offers_message = "В вашем городе не было обнаружено акций"
subcategory_info_message = """{information}
<i>ℹ️ Повторное нажатие убирает выббранный элемент из списка.</i>

"""
log_command_format = "[{time}] id{id} || @{username} ({first_name} {second_name}): {command}()"

cancel_command = "/cancel"
