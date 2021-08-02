from bs4 import BeautifulSoup
import requests


def get_quest_params(quest_link, full_info=False):
    output_params = dict()  # Наш словарь с названием квеста и его характеристиками

    req = requests.get(quest_link)

    data = BeautifulSoup(req.text, 'html.parser')

    up_panel_params = data.find('ul', class_="params-ul").find_all('li')

    quest_time = up_panel_params[1].find('span', class_="td").text
    quest_price = up_panel_params[2].find('span', class_="td").text
    quest_scary_level = up_panel_params[4].find('span', class_="td").text
    if quest_scary_level != "Не страшный":
        quest_scary_level = up_panel_params[4].find('span', class_="td").find('img').get('alt')

    if full_info:
        output_params["age"] = up_panel_params[5].find('span', class_="td").text
        output_params["people_count"] = up_panel_params[0].find('span', class_="td").text
        output_params["difficulty"] = len(up_panel_params[3].find_all('i', class_="fa fa-key"))
        output_params["type"] = data.find('span', class_="game-type").text
        output_params["rating"] = data.find('h2', id="reviews_block").find_next('div').find('span',
                                                                                            style="margin-left: 7px").text
    main = data.find('div', class_="main-info content")

    contacts_soup = main.find('div', class_="contacts").find_all('p', class_="with-bullet-icon-1")
    # quest_location = ""
    # quest_location_description = ""
    # quest_web_site = ""
    # quest_phone = ""
    # for element in contacts_soup:
    #    if element.find('i', class_="fa fa-fw fa-map-marker bullet-icon"):
    #        quest_location = element.text
    #    elif element.find('i', class_="fa fa-fw fa-map-signs bullet-icon"):
    #        quest_location_description = element.text
    #    elif element.find('i', class_="fa fa-fw fa-phone bullet-icon"):
    #        quest_phone = element.text
    #    elif element.find('i', class_="fa fa-laptop fa-fw bullet-icon"):
    #        print(element)
    #        quest_web_site = element.get("data-link")
    # print(quest_time, quest_price, quest_scary_level, "\n" + quest_location, "\n" + quest_location_description,
    #      "\n" + quest_web_site, "\n" + quest_phone)

    output_params.update({"time": quest_time, "price": quest_price, "scary_level": quest_scary_level})
    try:
        price = main.find('div', class_="price").find('p').text
        output_params["price"] = price
    except Exception:
        pass

    try:
        description = main.find('div', class_="description").text
        output_params["description"] = "<b>Описание:</b>\n" + description[8:]
    except Exception:
        pass

    try:
        details = main.find('div', class_="details").text
        output_params["details"] = "<b>Особенности:</b>\n" + details[11:]
    except Exception:
        pass

    return output_params
