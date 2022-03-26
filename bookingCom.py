import time

import numpy as np
from selenium import webdriver
import commonFunctions as cf

driver = webdriver.Firefox()


def search_city(city):
    time.sleep(2)
    driver.find_element(by="id", value="ss").send_keys(city)


def search():
    time.sleep(2)
    driver.find_element(by="class name", value="sb-searchbox__button ").click()


def get_by_xpath(xpath):
    return driver.find_element(by="xpath",
                               value=xpath)


def accept_cookies():
    time.sleep(2)
    driver.find_element(by="id", value="onetrust-accept-btn-handler").click()


def set_good_month_year(month, year):
    # we can choose the correct month but we need the calendar open
    is_good_month_shows = False
    while not is_good_month_shows:
        time.sleep(2)
        xpath_calendar = "//div[contains(@aria-live, 'polite')]"
        current_date = get_by_xpath(xpath_calendar).text
        if len(current_date) == 0:
            current_date = driver.find_element(by="xpath", value="//*[contains(@class, 'bui-calendar__wrapper')]")
            current_date = current_date.text.split(" ")[0:2]
            current_date[1] = str(''.join(i for i in current_date[1] if i.isdigit()))

        if month in current_date and year in current_date:
            is_good_month_shows = True
        else:
            try:
                get_by_xpath("//button[contains(@class, 'd40f3b0d6d f5ea4b08ab')]").click()
            except:
                get_by_xpath(
                    "//*[local-name()='div' and contains(@class, 'bui-calendar__control bui-calendar__control--next')]").click()


def show_calendar():
    try:
        driver.find_element(by="xpath", value="//div[contains(@class, 'sb-date-field__display')]").click()
    except:
        driver.find_element(by="xpath", value="//button[contains(@data-testid, 'date-display-field-end')]").click()


def select_day(day):
    # permet de scroller quand on n'a pas le bon mois affiché
    xpathDay = "//span[contains(@aria-hidden, 'true') and contains(text(), '{}')]".format(day)
    get_by_xpath(xpathDay).click()


def set_date(start_date, end_date):
    """
    :param end_date:
    :param start_date:
    """
    start_day, start_month, start_year = cf.separateDate(start_date)
    end_day, end_month, end_year = cf.separateDate(end_date)

    set_good_month_year(start_month, start_year)

    select_day(start_day)

    show_calendar()

    set_good_month_year(end_month, end_year)

    select_day(end_day)


def get_names_and_links_in_cards():
    return driver.find_elements(by="class name", value="fb01724e5b")


def get_names():
    return list(
        map(lambda hotel: hotel.text.split("\n")[0] if hotel is not None else np.nan, get_names_and_links_in_cards()))


def get_links():
    return list(map(lambda hotel: hotel.get_attribute("href"), get_names_and_links_in_cards()))


def get_grades():
    grades = []
    cards = get_cards()
    for card in cards:
        try:
            grade = card.find_element(by="xpath", value="./*//div[contains(@class, '_9c5f726ff bd528f9ea6')]")
            grades.append(grade.text if not None else np.nan)
        except:
            grades.append(np.nan)

    return grades


def get_prices():
    return list(map(lambda price: price.text.split(" ")[1] if price is not None else np.nan,
                    driver.find_elements(by="xpath", value="//span[contains(@class, 'fde444d7ef _e885fdc12')]")))


def get_addresses():
    return list(map(lambda address: address.text if address is not None else np.nan,
                    driver.find_elements(by="xpath", value="//span[contains(@data-testid, 'address')]")))


def get_gps():
    return list(
        map(lambda address: cf.getLocalisationFromAdd(address) if address is not None else np.nan, get_addresses()))


def get_cards():
    return driver.find_elements(by="xpath", value="//div[contains(@class, '_7192d3184')]")


def get_stars():
    stars = []
    for i in get_cards():
        nbr_stars = i.find_elements(by="xpath", value='./*//div[contains(@data-testid, "rating-stars")]/span')
        stars.append(len(nbr_stars) if nbr_stars else np.nan)

    return stars


def get_hotels():
    time.sleep(2)

    return [get_names(), get_grades(), get_stars(), get_prices(), get_addresses(), get_gps(), get_links()]


def applyFamilyAndDate():
    try:
        driver.find_element(by="xpath", value="//button[contains(@class, 'sb-searchbox__button')]").click()
    except:
        driver.find_element(by="xpath", value="//button[contains(@type, 'submit')]").click()


def changePage():
    time.sleep(2)
    driver.find_element(by="xpath", value="//button[contains(@aria-label, 'Page suivante')]").click()


def get_current_nbr_adults_children_rooms():
    return list(map(lambda nbr: int(nbr.text),
                    driver.find_elements(by="xpath", value="//span[contains(@class, 'bui-stepper__display')]")))


def get_nbr_adults():
    return get_current_nbr_adults_children_rooms()[0]


def get_nbr_children():
    return get_current_nbr_adults_children_rooms()[1]


def get_nbr_rooms():
    return get_current_nbr_adults_children_rooms()[2]


def set_nbr(btn, current_nbr, nbr_wanted):
    """
    :param btn: the button we want to click
    :param current_nbr: fonction to get the current number
    :param nbr_wanted: the number wanted by customer
    :return: None
    """
    while current_nbr() < nbr_wanted:
        time.sleep(0.5)
        btn.click()


def set_family_and_room(nbr_adults, nbr_children, nbr_room, ages_of_children):
    """
    :param nbr_adults: int
    :param nbr_children: int
    :param nbr_room: int
    :param ages_of_children: []
    :return: None
    """
    time.sleep(2)
    driver.find_element(by="id", value="xp__guests__toggle").click()

    btn_adults, btn_children, btn_room = driver.find_elements(by="xpath",
                                                              value="//button[contains(@class, 'bui-button bui-button--secondary bui-stepper__add-button')]")

    set_nbr(btn_adults, get_nbr_adults, nbr_adults)

    set_nbr(btn_children, get_nbr_children, nbr_children)

    set_nbr(btn_room, get_nbr_rooms, nbr_room)

    selects = driver.find_elements(by="xpath", value="//select[contains(@name, 'age')]")

    for i in range(len(selects)):
        selects[i].find_element(by="xpath", value="./option[contains(@value, '{}')]".format(ages_of_children[i])) \
            .click()


def get_current_page():
    return int(driver.find_element(by="xpath", value="//li[contains(@class, 'ce83a38554 f38c6bbd53')]").text)


def get_last_page():
    return int(driver.find_elements(by="xpath", value="//li[contains(@class, 'ce83a38554')]")[-1].text)


def main(infos, filename):
    """
    :param filename: example.csv
    :param infos: [city, start_date, end_date, nbr_adults, nbr_children, nbr_room, [age_children] ]
    :return:
    """
    city, start_date, end_date = infos[0], infos[1], infos[2]
    nbr_adults, nbr_children, nbr_room, ages_of_children = infos[3], infos[4], infos[5], infos[6]

    driver.get(
        "https://www.booking.com/index.fr.html?label=gen173nr-1BCAEoggI46AdIM1gEaE2IAQGYAQ24ARfIAQzYAQHoAQGIAgGoAgO4Arf4yJEGwAIB0gIkNmMwYWYwNGUtNGY3Ni00ZTk3LThjOGUtZWQ0OTEwMDZkZGMw2AIF4AIB;sid=4870985d274b91999c83d2a5d6f77393;keep_landing=1&sb_price_type=total&")
    accept_cookies()

    search_city(city)
    set_family_and_room(nbr_adults, nbr_children, nbr_room, ages_of_children)
    search()

    set_date(start_date, end_date)
    applyFamilyAndDate()

    current_page = get_current_page()
    last_page = get_last_page()

    while current_page < last_page:
        time.sleep(3)
        cf.addRows(
            names=get_names(),
            stars=get_stars(),
            gps=get_gps(),
            addresses=get_addresses(),
            links=get_links(),
            grades=get_grades(),
            filename=filename,
            is_head=current_page == 1)
        changePage()
        current_page += 1

    driver.close()

if __name__ == '__main__':
    main(["paris", "20/05/2022", "23/05/2022", 2, 2, 2, [5, 6]], "bookingCom.csv")
