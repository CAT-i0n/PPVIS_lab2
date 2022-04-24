from datetime import date

from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

from controller.Controller import Controller
from view.Dialog import OpenDialog, AddRecordDialog, SearchDialog, DeleteDialog
from view.Table import TableScreen

Builder.load_file("kv/ControllerPanel.kv")


class ControllerPanel(BoxLayout):
    def __init__(self, ScreenWindow, **kwargs):
        super().__init__(**kwargs)
        self.isOpened = False
        self.controller = Controller()
        self.popup = Popup()
        self.ScreenWindow = ScreenWindow

    def openDialog(self):
        content = OpenDialog(open=self.open, cancel=self.dismissPopup)
        self.popup = Popup(title="Open", content=content, size_hint=(0.7, 0.7))
        self.popup.open()

    def addRecordDialog(self):
        if not self.isOpened: return
        content = AddRecordDialog(add=self.addRecord, cancel=self.dismissPopup)
        self.popup = Popup(title="AddRecord", content=content, size_hint=(0.7, 0.7))
        self.popup.open()

    def searchDialog(self):
        
        if not self.isOpened: return
        content = SearchDialog(cancel=self.dismissPopup, search=self.search)
        self.popup = Popup(title="Search", content=content)
        self.popup.open()

    def deleteDialog(self):
        if not self.isOpened: return
        content = DeleteDialog(cancel=self.dismissPopup, delete=self.delete)
        self.popup = Popup(title="Delete", content=content)
        self.popup.open()

    def open(self, filename):
        try:
            self.ScreenWindow.update(self.controller.openFile(filename[0]))
        except:
            pass
        self.dismissPopup()
        self.isOpened = True

    def save(self):
        if not self.isOpened: return
        self.controller.saveFile()

    def addRecord(self, **kwargs):
        if not self.isOpened: return
        self.controller.addRecord(kwargs)
        self.ScreenWindow.update(self.controller.getData())
        self.dismissPopup()

    def search(self, searchData: dict) -> dict:
        if not self.isOpened: return
        try:
            if "name" in searchData.keys() and "group" in searchData.keys():
                return self.controller.searchByNameAndGroup(searchData["name"], searchData["group"])
            elif "year" in searchData.keys() and "language" in searchData.keys():
                return self.controller.searchByYearAndLanguage(searchData["year"], searchData["language"])
            elif "total" in searchData.keys() and "done" in searchData.keys():
                return self.controller.searchByTotalAndDoneWorks(searchData["total"], searchData["done"])
            elif "uncomplited" in searchData.keys():
                return self.controller.searchByUncomplitedWorks(searchData["uncomplited"])
        except:
            return []

    def delete(self, deleteData: dict):
        if not self.isOpened: return
        try:
            if "name" in deleteData.keys() and "group" in deleteData.keys():
                return self.controller.deleteByNameAndGroup(deleteData["name"], deleteData["group"])
            elif "year" in deleteData.keys() and "language" in deleteData.keys():
                return self.controller.deleteByYearAndLanguage(deleteData["year"], deleteData["language"])
            elif "total" in deleteData.keys() and "done" in deleteData.keys():
                return self.controller.deleteByTotalAndDoneWorks(deleteData["total"], deleteData["done"])
            elif "uncomplited" in deleteData.keys():
                return self.controller.deleteByUncomplitedWorks(deleteData["uncomplited"])
        except:
            return 0
        self.ScreenWindow.update(self.controller.getData())

    def dismissPopup(self, *args):
        self.popup.dismiss()


class MainWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.table = TableScreen([])
        self.controller = ControllerPanel(self, size_hint=(1, 0.1))

        self.add_widget(self.table)
        self.add_widget(self.controller)



        '''#load prepared data
        self.update(self.controller.controller.openFile(filepath=r"C:\a\ППВИС\PPvIS_Lab2\data\2.xml"))
        self.controller.isOpened = True'''

    def update(self, data: list):
        self.table.update(data)
