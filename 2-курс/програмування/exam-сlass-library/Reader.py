from Validation import Validation as V


class Reader:
    ID = 0

    def __init__(self, name=None, surname=None):
        self.__name = name
        self.__surname = surname
        self.__id = Reader.ID
        Reader.ID += 1

        self.set_empty_values()

    def set_empty_values(self):
        for key, value in vars(self).items():
            if value == None:
                getattr(self, f"set_{key[9:]}")(None)

    def set_valid_data(self, set_func):
        value = self.get_data_from_keyboard(
            f"{set_func.__name__} (id:{self.get_id()})")
        getattr(self, f"{set_func.__name__}")(value)

    def get_data_from_keyboard(self, message):
        print(f"Incorrect {message}")
        return input()

    def get_name(self):
        print(self.__name)
        return self.__name

    def get_surname(self):
        return self.__surname

    def get_id(self):
        return self.__id

    @V.isInSpecificFormat(r'^[a-zA-Z]{2,}$')
    def set_name(self, name):
        self.__name = name

    @V.isInSpecificFormat(r'^[a-zA-Z]{2,}$')
    def set_surname(self, surname):
        self.__surname = surname


r = Reader('Levi', )
print(r.get_name(), r.get_surname(), r.get_id())