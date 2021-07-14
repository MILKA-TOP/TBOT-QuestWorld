from bs4 import BeautifulSoup
import requests


def get_quests(now_url_part, check_main_site):
    quests_base = dict()  # Наш словарь с названием квеста и его характеристиками

    req = requests.get(check_main_site)
    quest_default_number_position = 0

    data = BeautifulSoup(req.text, 'html.parser')

    # Взятие main части html станицы, т.к именно в ней находятся все необходимые нам вещи
    main_code = data.main

    # Получение массива всех квестов (их тег "li" и класс "quest-tile-1")
    quest_soup_array = main_code.find_all('li', class_="quest-tile-1")

    # Оброботка квестов
    for quest_soup in quest_soup_array:

        # Получение супа
        quest_name_html = quest_soup.find('h4', class_="quest-tile-1__title")

        # Возможно костыль. Смотрит, есть ли надпись "ЗАКРЫТО". Реализовано через проверку, пустой ли массив.
        boolean = (len(quest_name_html.find_all('span', class_="badge badge-red-dark")) == 0)

        if boolean:
            # Ниже приложено просто получение основных характеристик квеста из его информационного табло

            params_soup = quest_soup.find('p', class_="quest_params features")

            quest_age = params_soup.find('span', class_="quest-age").text

            quest_people_count = params_soup.find('span', class_="quest-participants-count").text

            difficulty_soup = params_soup.find('span', class_="quest-difficulty")
            quest_difficulty = len(difficulty_soup.find_all('i', class_="fa fa-key"))

            quest_link_img_part = quest_soup.find('img')['data-original']

            quest_id = quest_link_img_part.split('/')[3]

            quest_link = check_main_site + quest_name_html.find('a').get('href')

            quest_type = quest_soup.find('span', class_="game-type").text

            # Строка имеет вид: "Рейтинг по\xa0отзывам: (РЕЙТИНГ)/(НЕТ ДАННЫХ)"
            quest_rating = quest_soup.find('p', class_="rating").text.replace("Рейтинг по\xa0отзывам:", "")

            quest_name = quest_name_html.text

            tag_array = [quest_name, quest_age, quest_people_count, quest_difficulty, quest_link, quest_type,
                         quest_rating, quest_default_number_position, quest_link_img_part]

            quest_default_number_position += 1

            quests_base[quest_id] = tag_array
#            print(quest_id + " ==== " + str(tag_array))
    return quests_base
