from selenium.webdriver.common.by import By
import time
from driver import Driver


class Scrape(Driver):

    def scraping_sectors(self):
        """
        Scrape the sectors from the web page after logging in.

        performs web scraping to extract sector information from the web page
        after logging in and returns it as a list of dictionaries.

        Returns:
            list: A list containing dictionaries with sector information.

            [
            {'code': '27', 'short_name': 'فلزات'},
            {'code': '34', 'short_name': 'خودرویی'},
             ... ]

        Raises:
            Exception: If there is an issue with scraping the data.
        """
        driver = self.logged_in_driver()
        search_button = driver.find_element(By.CLASS_NAME, "mdi-magnify")
        search_button.click()
        time.sleep(2)
        sector_ul = driver.find_element(By.TAG_NAME, "search-panel-sector-container")
        sector_li_list = sector_ul.find_elements(By.TAG_NAME, "li")
        shown_sector_list = []
        for i in sector_li_list:
            dict1 = {}
            if i.text == '' or i.get_attribute('id') == '':
                raise "Somthing wrong with scraping the data!"
            dict1['code'] = i.get_attribute('id')[-2:]
            dict1['short_name'] = i.text
            shown_sector_list.append(dict1)
        return shown_sector_list

    def scraping_symbols_by_sector(self, sector_code):
        """
        Scrape symbols by sector code from the web page after logging in.

        This function performs web scraping to extract symbols by sector code from the web page.
        after logging in extracts symbol data, and returns it as a dictionary and a list.

        Args:
            sector_code (str): The sector code to scrape symbols.

        Returns:
            tuple: A tuple containing a dictionary with categorized symbols and a list of symbols.

            dictionary :
                {'سهام': ['ذوب', 'فملی', 'فسرب', ...], 'حق تقدم': ['فولاژح', 'فجهانح', ...]}
            list :
                ['ذوب', 'فملی', 'فسرب', 'فباهنر', ...]
        """
        driver = self.logged_in_driver()
        search_button = driver.find_element(By.CLASS_NAME, "mdi-magnify")
        search_button.click()
        time.sleep(2)
        sector_button = driver.find_element(By.ID, "search-panel-sector-{}".format(str(sector_code)))
        sector_button.click()
        time.sleep(2)
        parent_element = driver.find_element(By.TAG_NAME, "search-panel-result-list")
        elements = parent_element.find_elements(By.XPATH, "./*")

        # categorized symbols
        symbol_dictionary = {}

        # all found symbols in a list
        symbol_list = []

        key = None
        for i in elements:
            if i.tag_name == 'div':
                symbol_dictionary[i.text] = []
                key = i.text
            else:
                item = i.find_element(By.CLASS_NAME, "text-truncate")
                item = item.find_element(By.TAG_NAME, "b")
                symbol_dictionary[key].append(item.text)
                symbol_list.append(item.text)
        return symbol_dictionary, symbol_list


if __name__ == '__main__':
    object1 = Scrape()
