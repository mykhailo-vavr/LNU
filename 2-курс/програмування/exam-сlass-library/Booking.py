import Validation as V


class Booking:
    def __init__(self, date=None, id=None, author=None, title=None):
        self.__date = date
        self.__id = id
        self.__author = author
        self.__title = title
        self.set_empty_values()

    def set_empty_values(self):
        for key, value in vars(self).items():
            if value == None:
                getattr(self, f"set_{key[10:]}")(None)

    def set_valid_data(self, set_func):
        value = self.get_data_from_keyboard(
            f"{set_func.__name__} (id:{self.get_id()})")
        getattr(self, f"{set_func.__name__}")(value)

    def get_data_from_keyboard(self, message):
        print(f"Incorrect {message}")
        return input()

    def get_date(self):
        return self.__date

    def get_id(self):
        return self.__id

    def get_author(self):
        return self.__author

    def get_title(self):
        return self.__title

    @V.isValidDate
    def set_date(self, date):
        self.__date = date

    @V.isInSpecificFormat(r'^[a-zA-Z]{2,}$')
    def set_author(self, author):
        self.__author = author

    def set_title(self, title):
        self.__title = title
