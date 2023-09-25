from Validation import Validation as V
import json


class Collection:
    def __init__(self, instance, path=None):
        self.instance = instance
        self.collection = []
        if path:
            self.set_items_from_file(path)

    def set_valid_data(self, set_func, *args):
        value = self.get_data_from_keyboard(
            f"value in {set_func.__name__} method")
        getattr(self, f"{set_func.__name__}")(value, *args)

    def get_data_from_keyboard(self, message):
        print(f"Incorrect {message}")
        return input()

    def find(self, value):
        foundItems = []
        for item in self.collection:
            if str(item).find(str(value)) != -1:
                foundItems.append(item)

        if len(foundItems) > 0:
            return foundItems

        return -1

    def sort(self, value):
        str(value)
        self.collection.sort(key=lambda x: getattr(x, f"get_{value}")(),
                             reverse=False)

    @V.isIntegerInRange(-1)
    def delete(self, id, path=""):
        item = self.find_item_by_ID(id)
        if path:
            self.write_to_file(item, path)
        if item:
            self.collection.remove(item)
        else:
            print(f"There is no item with id: {id}")

    def add(self, inputPath, outputPath=""):
        tempItem = self.instance()
        if tempItem.get_data_from_file(inputPath) == -1:
            print("Invalid path")
            return -1

        tempItem.set_data_from_file(inputPath)

        if outputPath:
            self.write_to_file(tempItem, outputPath)
        self.collection.append(tempItem)

    @V.isIntegerInRange(-1)
    def change(self, id, inputPath, outputPath=""):
        item = self.find_item_by_ID(id)
        if item.get_data_from_file(inputPath) == -1:
            print("Invalid path")
            return -1

        if item:
            item.set_data_from_file(inputPath)
        else:
            print(f"There is no item with id: {id}")
            return -1

        if outputPath:
            self.write_to_file(item, outputPath)

    def find_item_by_ID(self, id):
        for item in self.collection:
            if item.get_ID() == id:
                self.item = item
                return item
        return None

    def write_to_file(self, path, item):
        try:
            with open(path, "w") as file:
                file.write(str(item))
        except:
            return -1

    def set_items_from_file(self, path):
        data = self.instance.get_data_from_file(self.instance, path)

        if data == -1:
            return -1

        for obj in data["items"]:
            tempItem = self.instance()
            for key, value in obj.items():
                getattr(tempItem, f"set_{key}")(value)
            tempItem.set_empty_values()
            self.collection.append(tempItem)

    def show(self):
        print(self)

    def __str__(self):
        return json.dumps([obj.__dict__ for obj in self.collection], indent=2)

    def __len__(self):
        return len(self.collection)

    @V.isIntegerInRange(-1)
    def __getitem__(self, index):
        if index >= len(self.collection):
            return -1
        return self.collection[index]