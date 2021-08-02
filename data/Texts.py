START_TEXT = """
Привет! 
Добро пожаловать в <i> тестовый телеграмм бот </i> компании "Мир Квестов"
"""

HELP_TEXT = """
Ниже представлен список команд бота:
    
    /menu - Меню с командами бота
    /random - Случайный вест
    /filter - Список квестов по фильтрам
    /help - Список команд
    /get_location - Запрос нынешнего положени
    /location - Изменение положения
    
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

CITY_TAKE = "Введите пожалуйста город, в котором вы хотите выбрать квесты"

COUNTRY_ERROR = "Данной страны нет в базе данных, либо вы опечатались. Пожалуйста, введите другую страну."
CITY_ERROR = "Данного города нет в базе данных, либо вы опечатались. Пожалуйста, введите другой город."

FULL_QUESTS_POSTFIX = "/quests"
FILTER_QUESTS_POSTFIX = "/quests/search?"
OFFERS_QUESTS_POSTFIX = "/offers"

QUEST_DESCRIBE = """{number}) {name}:
Количество человек: {people_count}
Сложность: {difficulty_key} ({difficulty_word})
Рейтинг: {rating_star} {rating_num}

"""

OFFER_DESCRIBE = """{number}) <b>{name}</b>:
{description}

"""

ONE_PAGE_CATEGORY_TEXT = "one_sub"
MORE_PAGES_CATEGORY_TEXT = "more_sub"

QUEST_LINE = "{numb}) {name}"

more_pages_subcategory_list_str = "more_pages_subcategory_list"
now_params_quest_filter_str = "now_params_quest_filter"
media_message_str = "media_message"
page_number_dict_str = "page_number_dict"
new_params_str = "new_params"
now_quest_str = "now_quest"
quest_dict_str = "quest_dict"
index_str = "index"
difficulty_str = "difficulty"
now_quest_page_str = "now_quest_page"

ERROR_MESSAGE = """
Произошла непредвиденная ошибка в работе бота.

Ваши данные были обновлены до начальных. 
По возможности напишите пожалуйста ваши последние действия следующему контакту @КОНТАКТЫ.
"""

CLOSE_MENU_KEYBOARD_MESSAGE = """Ваша клавиатура была скрыта. 

Для её открытия используйте команду /menu"""

OPEN_MENU_KEYBOARD_MESSAGE = """Ваша клавиатура была открыта. 

Для её закрытия используйте команду /menu"""

QUESTS_BY_FILTER_BUTTON = "Выбор квеста по фильтрам"
RANDOM_QUEST_BUTTON = "Случайный квест"
OFFERS_BUTTON = "Акции в вашем городе"
GET_CITY_BUTTON = "Выбор города"
CONTACTS_BUTTON = "Контакты"
HELP_BUTTON = "Команды бота"

OFFER_MESSAGE = "<b>{head}:</b>\n\n{body}"
