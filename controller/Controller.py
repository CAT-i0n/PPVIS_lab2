from datetime import date

from model.database import Database


class Controller:
    def __init__(self):
        self.data = Database()
        self.filepath = ""

    def openFile(self, filepath: str):
        self.filepath = filepath
        self.data.load(self.filepath)
        return self.data.getData()

    def saveFile(self):
        if self.filepath == "": return
        self.data.save(self.filepath)

    def addRecord(self, record: dict):
        try:
            self.data.addRecord(record)
        except ValueError:
            pass

    def searchByNameAndGroup(self, name: str, group: str):
        return self.data.searchByNameAndGroup(name, group)

    def searchByYearAndLanguage(self, year: str, language: str) -> list:
        return self.data.searchByYearAndLanguage(year, language)

    def searchByTotalAndDoneWorks(self, total: str, done: str) -> list:
        return self.data.searchByTotalAndDoneWorks(total, done)

    def searchByUncomplitedWorks(self, uncomplited: str) -> list:
        return self.data.searchByUncomplitedWorks(uncomplited)


    def deleteByNameAndGroup(self, name: str, group: str):
        return self.data.deleteByNameAndGroup(name, group)

    def deleteByYearAndLanguage(self, year: str, language: str):
        return self.data.deleteByYearAndLanguage(year, language)

    def deleteByTotalAndDoneWorks(self, total: str, done: str):
        return self.data.deleteByTotalAndDoneWorks(total, done)

    def deleteByUncomplitedWorks(self, uncomplited: str):
        return self.data.deleteByUncomplitedWorks(uncomplited)

    def getData(self):
        return self.data.getData()
