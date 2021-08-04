import requests
from bs4 import BeautifulSoup

from data import FULL_QUESTS_POSTFIX


def get_quest_information(quest_soup: BeautifulSoup, main_city_link: str):
    img_soup = quest_soup.find('img')
    quest_link_img_part = img_soup.get('data-original')

    quest_link_img = main_city_link + quest_link_img_part
    quest_id = quest_link_img_part.split('/')[3]
    quest_link = main_city_link + FULL_QUESTS_POSTFIX + "/" + str(quest_id)
    offer_name = quest_soup.find('div',
                                 class_="item-box-desc quest-tile-1__content").find('h4',
                                                                                    class_="quest-tile-1__title").find(
        'a').text
    offer_description = quest_soup.find('p', class_="offer-description").text

    return {"name": offer_name, "link": quest_link, "description": offer_description, "link_img": quest_link_img,
            "offer_type": "quest"}


def get_offer_information(offer_soup: BeautifulSoup, main_city_link):
    img_soup = offer_soup.find('img')
    quest_link_img = main_city_link + img_soup.get('src')
    # quest_link_img = main_city_link + quest_link_img_part

    info_soup = offer_soup.find('div', class_="item-box-desc")
    name = info_soup.find('a').text
    description = info_soup.find('p').text
    link = main_city_link + info_soup.find('a').get('href')
    return {"link_img": quest_link_img, "name": name, "link": link, "description": description, "offer_type": "offer"}


def get_offers_parse(link_offers: str, main_city_link: str):
    soup = BeautifulSoup(requests.get(link_offers).text, 'html.parser')

    quest_offers_dict = dict()
    another_offers_dict = dict()
    offer_id = 0
    all_h2 = soup.find_all('h2')
    for elements in all_h2:

        if "Прошедшие акции" in elements.text:
            pass
        elif "Действующие акции" in elements.text:
            try:
                quest_offers_soup = elements.find_next('ul')
                quest_soup_list = quest_offers_soup.find_all('li')

                for quest_soup in quest_soup_list:
                    quest_offers_dict[offer_id] = get_quest_information(quest_soup, main_city_link)
                    offer_id += 1
            except Exception:
                pass
        elif "Описание действующих" in elements.text:
            try:
                another_offers_all_soup = elements.find_next('div')
                another_offers_list_soup = another_offers_all_soup.find_all('div', class_="offer-1")

                for offer_soup in another_offers_list_soup:
                    another_offers_dict[offer_id] = get_offer_information(offer_soup, main_city_link)
                    offer_id += 1
            except Exception:
                pass
        else:
            pass

    quest_offers_dict.update(another_offers_dict)
    return quest_offers_dict


def get_full_offer_info(offer_link) -> dict:
    soup = BeautifulSoup(requests.get(offer_link).text, 'html.parser')
    information_part = soup.find('div', class_="row").find('div')

    header_name = information_part.find('header').text[:-1]

    try:
        all_information_soup = information_part.find('article')
        all_information_text = str(all_information_soup).replace('<article>', '')
        all_information_text = all_information_text.replace('</article>', '')
        all_information_text = all_information_text.replace('<p>', '<a>')
        all_information_text = all_information_text.replace('</p>', '</a>\n\n')
    except Exception:
        all_information_text = information_part.text
    all_information_text_sec = information_part.text

    return {"head": header_name, "body": all_information_text, "body_text": all_information_text_sec}
