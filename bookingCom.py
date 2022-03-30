import time

import numpy as np
from selenium import webdriver
import commonFunctions as cf


class NbrChildrenNotEqualToLenAgesOfChildren(ValueError):
    def __init__(self):
        super(NbrChildrenNotEqualToLenAgesOfChildren, self).__init__()

    def __str__(self):
        return "the number of children must be equal to the length of the array of their ages"


class NotTheCorrectTypeForAgesOfChildren(ValueError):
    def __init__(self):
        super(NotTheCorrectTypeForAgesOfChildren, self).__init__()

    def __str__(self):
        return "ages of children must be an array"


class Booking:
    def __init__(self, city, filename, start_date,
                 end_date, nbr_adults=None,
                 nbr_children=None, ages_of_children=None, nbr_room=None):
        """
        :param city: string
        :param filename: string
        :param start_date: MM-dd-yyyy
        :param end_date: MM-dd-yyyy
        :param nbr_adults: int
        :param nbr_children: int
        :param ages_of_children: array with len equal to number of children
        :param nbr_room: int
        """
        self.start_date = start_date
        self.nbr_adults = nbr_adults
        self.end_date = end_date
        self.nbr_children = nbr_children
        self.ages_of_children = ages_of_children
        self.nbr_room = nbr_room
        self.city = city
        self.filename = filename
        self.iCanWork = True

        if type(ages_of_children) is not list:
            raise NotTheCorrectTypeForAgesOfChildren()

        if len(self.ages_of_children) != self.nbr_children:
            raise NbrChildrenNotEqualToLenAgesOfChildren()

        self.driver = webdriver.Firefox()
        self.driver.delete_all_cookies()

    def search_city(self, city):
        time.sleep(2)
        self.driver.find_element(by="id", value="ss").send_keys(city)

    def search(self):
        time.sleep(2)
        self.driver.find_element(by="class name", value="sb-searchbox__button ").click()

    def get_by_xpath(self, xpath):
        return self.driver.find_element(by="xpath",
                                        value=xpath)

    def accept_cookies(self):
        time.sleep(2)
        try:
            self.driver.find_element(by="id", value="onetrust-accept-btn-handler").click()
        except:
            ...

    def set_good_month_year(self, month, year):
        # we can choose the correct month but we need the calendar open
        is_good_month_shows = False
        while not is_good_month_shows:
            time.sleep(2)
            xpath_calendar = "//div[contains(@aria-live, 'polite')]"
            current_date = self.get_by_xpath(xpath_calendar).text
            if len(current_date) == 0:
                current_date = self.driver.find_element(by="xpath",
                                                        value="//*[contains(@class, 'bui-calendar__wrapper')]")
                current_date = current_date.text.split(" ")[0:2]
                current_date[1] = str(''.join(i for i in current_date[1] if i.isdigit()))

            if month in current_date and year in current_date:
                is_good_month_shows = True
            else:
                try:
                    self.get_by_xpath("//button[contains(@class, 'c9fa5fc96d be298b15fa')]").click()
                except:
                    self.get_by_xpath(
                        "//*[local-name()='div' and contains(@class, 'bui-calendar__control bui-calendar__control--next')]").click()

    def show_calendar(self):
        try:
            self.driver.find_element(by="xpath", value="//div[contains(@class, 'sb-date-field__display')]").click()
        except:
            self.driver.find_element(by="xpath",
                                     value="//button[contains(@data-testid, 'date-display-field-end')]").click()

    def select_day(self, day):
        # permet de scroller quand on n'a pas le bon mois affiché
        xpathDay = "//span[contains(@aria-hidden, 'true') and contains(text(), '{}')]".format(int(day))
        self.get_by_xpath(xpathDay).click()

    def set_date(self, start_date, end_date):
        """
        :param end_date: MM-dd-yyyy
        :param start_date: MM-dd-yyyy
        """
        start_day, start_month, start_year = cf.separateAmericanDate(start_date)
        end_day, end_month, end_year = cf.separateAmericanDate(end_date)

        start_month = cf.monthCorrespondances[start_month]
        end_month = cf.monthCorrespondances[end_month]

        self.set_good_month_year(start_month, start_year)

        self.select_day(start_day)

        self.show_calendar()

        self.set_good_month_year(end_month, end_year)

        self.select_day(end_day)

    def get_names_and_links_in_cards(self):
        return self.driver.find_elements(by="xpath", value="//a[contains(@class, 'e13098a59f')]")

    def get_names(self):
        return list(
            map(lambda hotel: hotel.text.split("\n")[0] if hotel is not None else np.nan,
                self.get_names_and_links_in_cards()))

    def get_links(self):
        return list(map(lambda hotel: hotel.get_attribute("href"), self.get_names_and_links_in_cards()))

    def get_grades(self):
        grades = []
        cards = self.get_cards()
        for card in cards:
            try:
                grade = card.find_element(by="xpath", value="./*//div[contains(@class, 'b5cd09854e d10a6220b4')]")
                grades.append(grade.text if not None else np.nan)
            except:
                grades.append(np.nan)

        return grades

    def get_prices(self):
        return list(map(lambda price: price.text.split(" ")[1] if price is not None else np.nan,
                        self.driver.find_elements(by="xpath",
                                                  value="//span[contains(@class, 'fcab3ed991 bd73d13072')]")))

    def get_addresses(self):
        return list(map(lambda address: address.text if address is not None else np.nan,
                        self.driver.find_elements(by="xpath", value="//span[contains(@data-testid, 'address')]")))

    def get_gps(self):
        return list(
            map(lambda address: cf.getLocalisationFromAdd(address),
                self.get_addresses()))

    def get_cards(self):
        return self.driver.find_elements(by="xpath", value="//div[contains(@class, 'b978843432')]")

    def get_stars(self):
        stars = []
        for i in self.get_cards():
            nbr_stars = i.find_elements(by="xpath", value='./*//div[contains(@data-testid, "rating-stars")]/span')
            stars.append(len(nbr_stars) if nbr_stars else np.nan)

        return stars

    def get_hotels(self):
        time.sleep(2)

        return [self.get_names(),
                self.get_grades(),
                self.get_stars(),
                self.get_prices(),
                self.get_addresses(),
                self.get_gps(),
                self.get_links()]

    def applyFamilyAndDate(self):
        try:
            self.driver.find_element(by="xpath", value="//button[contains(@class, 'sb-searchbox__button')]").click()
        except:
            self.driver.find_element(by="xpath", value="//button[contains(@type, 'submit')]").click()

    def changePage(self):
        time.sleep(2)
        self.driver.find_element(by="xpath", value="//button[contains(@aria-label, 'Page suivante')]").click()

    def get_current_nbr_adults_children_rooms(self):
        return list(map(lambda nbr: int(nbr.text),
                        self.driver.find_elements(by="xpath",
                                                  value="//span[contains(@class, 'bui-stepper__display')]")))

    def get_nbr_adults(self):
        return self.get_current_nbr_adults_children_rooms()[0]

    def get_nbr_children(self):
        return self.get_current_nbr_adults_children_rooms()[1]

    def get_nbr_rooms(self):
        return self.get_current_nbr_adults_children_rooms()[2]

    def set_nbr(self, btn, current_nbr, nbr_wanted):
        """
        :param btn: the button we want to click
        :param current_nbr: fonction to get the current number
        :param nbr_wanted: the number wanted by customer
        :return: None
        """
        while current_nbr() < nbr_wanted:
            time.sleep(0.5)
            btn.click()

    def set_family_and_room(self, nbr_adults, nbr_children, nbr_room, ages_of_children):
        """
        :param nbr_adults: int
        :param nbr_children: int
        :param nbr_room: int
        :param ages_of_children: []
        :return: None
        """
        time.sleep(2)
        self.driver.find_element(by="id", value="xp__guests__toggle").click()

        btn_adults, btn_children, btn_room = self.driver.find_elements(by="xpath",
                                                                       value="//button[contains(@class, 'bui-button bui-button--secondary bui-stepper__add-button')]")

        self.set_nbr(btn_adults, self.get_nbr_adults, nbr_adults)

        self.set_nbr(btn_children, self.get_nbr_children, nbr_children)

        self.set_nbr(btn_room, self.get_nbr_rooms, nbr_room)

        selects = self.driver.find_elements(by="xpath", value="//select[contains(@name, 'age')]")

        for i in range(len(selects)):
            selects[i].find_element(by="xpath", value="./option[contains(@value, '{}')]".format(ages_of_children[i])) \
                .click()

    def get_current_page(self):
        return int(self.driver.find_element(by="xpath", value="//li[contains(@class, 'f32a99c8d1 ebd02eda9e')]").text)

    def get_last_page(self):
        return int(self.driver.find_elements(by="xpath", value="//li[contains(@class, 'f32a99c8d1')]")[-1].text)

    def process_search_results(self):
        try:
            self.driver.get(
                "https://www.booking.com/index.fr.html?label=gen173nr-1BCAEoggI46AdIM1gEaE2IAQGYAQ24ARfIAQzYAQHoAQGIAgGoAgO4Arf4yJEGwAIB0gIkNmMwYWYwNGUtNGY3Ni00ZTk3LThjOGUtZWQ0OTEwMDZkZGMw2AIF4AIB;sid=4870985d274b91999c83d2a5d6f77393;keep_landing=1&sb_price_type=total&")
            self.accept_cookies()

            self.search_city(self.city)
            self.set_family_and_room(self.nbr_adults, self.nbr_children, self.nbr_room, self.ages_of_children)
            self.search()

            self.set_date(self.start_date, self.end_date)
            self.applyFamilyAndDate()
        except:
            self.driver.close()

    def main(self):
        if self.iCanWork:
            try:
                current_page = self.get_current_page()
                last_page = self.get_last_page()
                while current_page < last_page:
                    time.sleep(3)
                    cf.addRows(
                        names=self.get_names(),
                        stars=self.get_stars(),
                        prices=self.get_prices(),
                        gps=self.get_gps(),
                        addresses=self.get_addresses(),
                        links=self.get_links(),
                        grades=self.get_grades(),
                        filename=self.filename,
                        start_date=[self.start_date for _ in range(25)],
                        end_date=[self.end_date for _ in range(25)],
                        nb_adults=[self.nbr_adults for _ in range(25)],
                        nb_children=[self.nbr_children for _ in range(25)],
                        nb_room=[self.nbr_room for _ in range(25)],
                        is_head=current_page == 1)
                    self.changePage()
                    current_page += 1

                self.driver.close()
            except:
                self.driver.close()


if __name__ == '__main__':
    book = Booking(city="paris",
                   start_date="05-20-2022",
                   end_date="05-23-2022",
                   nbr_adults=2,
                   nbr_children=2,
                   nbr_room=2,
                   ages_of_children=[5, 9],
                   filename="bookingCom.csv")
    book.main()
