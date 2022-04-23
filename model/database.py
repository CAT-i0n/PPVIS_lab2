from datetime import date

from model.parserDOM import writeXML
from model.parserSAX import parse


class Database:
    __recordFields = ["name", "year", "group", "total", "done", "language"]

    def __init__(self):
        self.__data = list()

    def load(self, filepath) -> None:
        self.__data = parse(filepath)

    def save(self, filepath) -> None:
        writeXML(filepath, self.__data)

    def getData(self) -> list:
        return self.__data

    def addRecord(self, record: dict) -> None:
        if sorted([*record.keys()]) != sorted(self.__recordFields):
            raise ValueError("Incorrect record!")
        else:
            self.__data.append(record)

    def searchByNameAndGroup(self, name: str, group: str) -> list:
        result: list = list()
        for record in self.__data:
            if name == record["name"] or group == record["group"]:
                result.append(record)
        return result

    def searchByYearAndLanguage(self, year: str, language: str) -> list:
        result: list = list()
        for record in self.__data:
            if year == record["year"] or language == record["language"]:
                result.append(record)
        return result

    def searchByTotalAndDoneWorks(self, total: str, done: str) -> list:
        result: list = list()
        for record in self.__data:
            if total == record["total"] or done == record["done"]:
                result.append(record)
        return result

    def searchByUncomplitedWorks(self, uncomplited: str) -> list:
        result: list = list()
        for record in self.__data:
            if int(uncomplited) == int(record["total"])-int(record["done"]):
                result.append(record)
        return result


    def deleteByNameAndGroup(self, name: str, group: str) -> list:
        delete = self.searchByNameAndGroup(name, group)
        result = len(delete)
        for element in delete:
            self.__data.remove(element)
        return result

    def deleteByYearAndLanguage(self, year: str, language: str) -> list:
        delete = self.searchByYearAndLanguage(year, language)
        result = len(delete)
        for element in delete:
            self.__data.remove(element)
        return result

    def deleteByTotalAndDoneWorks(self, total: str, done: str) -> list:
        delete = self.searchByTotalAndDoneWorks(total, done)
        result = len(delete)
        for element in delete:
            self.__data.remove(element)
        return result

    def deleteByUncomplitedWorks(self, uncomplited: str) -> list:
        delete = self.searchByUncomplitedWorks(uncomplited)
        result = len(delete)
        for element in delete:
            self.__data.remove(element)
        return result