import json
from localstorage import LocalStorage
from scrape import Scrape


class OrbisData(LocalStorage, Scrape):
    __special_sectors_json_file_address = "./json/special_sectors.json"
    __extra_symbols_json_file_address = "./json/extra_symbols.json"

    def get_sectors_from_localstorage(self):
        """
        Retrieve the sector list from local storage data loaded from a JSON file.

        1-loads local storage data from a JSON file.
        2-extracts the sector list and returns it.

        Returns:
            list: A list containing the sectors:
            [
            {'code': '46', 'name': 'تجارت عمده فروشی به جز وسایل نقلیه موتور'},
            {'code': '01', 'name': 'زراعت و خدمات وابسته'},
            ...
            ]
        """
        localstorage_dictionary = self.get_localstorage_from_json_file()
        sector_list = json.loads(localstorage_dictionary['sectors'])
        sector_list = [{'code': i['code'], 'name': i['name']} for i in sector_list]
        return sector_list

    def get_symbols_from_localstorage(self, sector_code=None):
        """
        Retrieve the symbol list from local storage data loaded from a JSON file.

        1-loads local storage data from a JSON file.
        2-extracts the symbol list, and optionally filters it by sector code, then returns it.

        Args:
            sector_code (str, optional): The sector code used for filtering the symbol list.

        Returns:
            list: A list containing the symbols retrieved from the JSON file, optionally filtered by sector.
        """
        localstorage_dictionary = self.get_localstorage_from_json_file()
        symbol_list = json.loads(localstorage_dictionary['symbols'])['symbols']
        for i in range(len(symbol_list)):
            symbol_list[i]['sector'] = symbol_list[i]['sector'].strip()
            symbol_list[i]['symbolName'] = symbol_list[i]['symbolName'].strip()
        if sector_code is not None:
            new_symbol_list = []
            for i in symbol_list:
                if i['sector'] == sector_code:
                    new_symbol_list.append(i)
            return new_symbol_list
        return symbol_list

    def __get_special_sectors(self):
        """
        Get sector list from both scraped data and local storage.

        This function get the sector lists from both scraped data and local storage.
        It then merges the sector names from local storage into the scraped sector list
        and returns the combined sector list.

        Returns:
            list: A list containing dictionaries with sector information.

            [
                {'code': '27', 'short_name': 'فلزات', 'name': 'فلزات اساسی'},
                {'code': '34', 'short_name': 'خودرویی', 'name': 'خودرو و ساخت قطعات'},
                ...
            ]
        """
        scraped_sector_list = self.scraping_sectors()
        localstorage_sector_list = self.get_sectors_from_localstorage()
        for i in scraped_sector_list:
            for j in localstorage_sector_list:
                if i['code'] == j['code']:
                    i['name'] = j['name']
        return scraped_sector_list

    def write_special_sectors_in_json_file(self):
        """
        Write sector list to a JSON file.

        1-retrieves the sector list.
        2-constructs a dictionary with the sector list as value and the 'sectors' key.
        3-converts the dictionary to a JSON string and writes it to a JSON file.

        Returns:
            None
        """
        sector_list = self.__get_special_sectors()
        sector_dictionary = {
            'sectors': sector_list
        }
        json_string = json.dumps(sector_dictionary)
        with open(self.__special_sectors_json_file_address, "w") as json_file:
            json_file.write(json_string)

    def get_special_sectors_from_json_file(self):
        """
        Load sector list from a JSON file.

        This function attempts to read the sector list from a JSON file.
        If the file is found and contains data, it returns the sector list.

        Returns:
            list: A list containing sector information.

            [
                {'code': '27', 'short_name': 'فلزات', 'name': 'فلزات اساسی'},
                {'code': '34', 'short_name': 'خودرویی', 'name': 'خودرو و ساخت قطعات'},
                ...
            ]

        Raises:
            Exception: If there is no JSON file or the file is empty.
        """
        try:
            with open(self.__special_sectors_json_file_address, 'r') as json_file:
                data_dict = json.load(json_file)
            sector_list = data_dict['sectors']
            return sector_list
        except:
            raise "ERROR: There is no JSON file or the file is empty!"

    def get_extra_sectors(self):
        localstorage_sectors = self.get_sectors_from_localstorage()
        special_sectors = [i['code'] for i in self.get_special_sectors_from_json_file()]
        extra_sectors = []
        for i in localstorage_sectors:
            if i['code'] not in special_sectors:
                extra_sectors.append(i)
        return extra_sectors

    def get_symbols_of_extra_sectors(self):
        extra_sectors = [i['code'] for i in self.get_extra_sectors()]
        localstorage_symbols = self.get_symbols_from_localstorage()
        symbols = []
        for i in extra_sectors:
            for j in localstorage_symbols:
                if j['sector'] == i:
                    symbols.append(j)
        return symbols

    def compare_symbols(self, sector_code):
        _, scraped_symbol_list = self.scraping_symbols_by_sector(sector_code)
        localstorage_symbol_list = self.get_symbols_from_localstorage(sector_code)
        extra_localstorage_symbol_list = [i['symbolName'] for i in localstorage_symbol_list]
        extra_scraped_symbol_list = []
        for i in scraped_symbol_list:
            if i in extra_localstorage_symbol_list:
                extra_localstorage_symbol_list.remove(i)
            else:
                extra_scraped_symbol_list.append(i)

        return {'sector': sector_code, 'extra_scraped': extra_scraped_symbol_list, 'extra_localstorage': extra_localstorage_symbol_list}

    def compare_symbols_for_all_special_sectors(self):
        sector_code_list = [i['code'] for i in self.get_special_sectors_from_json_file()]

        extra_symbols = []
        for code in sector_code_list:
            while True:
                try:
                    d = self.compare_symbols(code)
                    break
                except:
                    pass
            extra_symbols.append(d)

        extra_symbols_dict = {'extra_symbols': extra_symbols}
        json_string = json.dumps(extra_symbols_dict)
        with open(self.__extra_symbols_json_file_address, "w") as json_file:
            json_file.write(json_string)

    def get_extra_symbols_from_json_file(self):
        try:
            with open(self.__extra_symbols_json_file_address, 'r') as json_file:
                data_dict = json.load(json_file)
            extra_symbol_list = data_dict['extra_symbols']
            return extra_symbol_list
        except:
            raise "ERROR: There is no JSON file or the file is empty!"


if __name__ == '__main__':
    object1 = OrbisData()
