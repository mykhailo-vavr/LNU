from datetime import datetime
import re


class Validation:
    @staticmethod
    def isInSpecificFormat(regexp):
        def _isInSpecificFormat(func):
            def wrapper(self, value, *args):
                if isinstance(value, str) and re.search(regexp, value):
                    return func(self, value, *args)
                return self.set_valid_data(func, *args)

            return wrapper

        return _isInSpecificFormat

    @staticmethod
    def isValidDate(func):
        def wrapper(self, date, *args):
            dateFormat = "%d.%m.%Y"
            try:
                datetime.strptime(date, dateFormat)
            except:
                return self.set_valid_data(func, *args)
            return func(self, date)

        return wrapper