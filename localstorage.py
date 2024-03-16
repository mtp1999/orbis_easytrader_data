import json
from driver import Driver


class LocalStorage(Driver):
    __localstorage_json_file_address = "json/localstorage.json"

    def __get_localstorage_using_webdriver(self):
        """
        Get the contents of the browser's local storage using a webdriver object.

        Returns:
            str: JSON string representing the contents of the local storage.
        """
        driver = self.logged_in_driver()
        local_storage_data = driver.execute_script("return JSON.stringify(window.localStorage);")
        return local_storage_data

    def write_localstorage_in_json_file(self):
        """
        Write the contents of the browser's local storage into a JSON file.

        1-get the local storage data using a webdriver object.
        2-then writes the data into a JSON file.

        Returns:
            None
        """
        local_storage_data = self.__get_localstorage_using_webdriver()
        with open(self.__localstorage_json_file_address, 'w') as json_file:
            json_file.write(local_storage_data)

    def get_localstorage_from_json_file(self):
        """
        Load local storage data from a JSON file.

        Raises:
            Exception: If there is no JSON file or the file is empty.

        Returns:
            dict: A dictionary containing the local storage data.
        """
        try:
            with open(self.__localstorage_json_file_address, 'r') as json_file:
                localstorage_dictionary = json.load(json_file)
            return localstorage_dictionary
        except:
            raise "ERROR: There is no JSON file or the file is empty!"


if __name__ == '__main__':
    object1 = LocalStorage()
