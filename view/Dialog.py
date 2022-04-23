from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown

from view.Table import TableScreen

Builder.load_file("kv/OpenDialog.kv")
Builder.load_file("kv/AddRecordDialog.kv")
Builder.load_file("kv/SelectModeDialog.kv")
Builder.load_file("kv/SearchDialog.kv")
Builder.load_file("kv/DeleteDialog.kv")


class OpenDialog(FloatLayout):
    open = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SelectModeDialog(BoxLayout):
    cancel = ObjectProperty(None)
    selectNameAndGroup=ObjectProperty(None)
    selectYearAndLanguage=ObjectProperty(None)
    selectTotalAndDoneWorks=ObjectProperty(None)
    selectUncomplitedWorks=ObjectProperty(None)


class AddRecordDialog(FloatLayout):
    add = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SearchDialog(BoxLayout):
    cancel = ObjectProperty(None)
    search = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        content = SelectModeDialog(cancel=self.cancel,
                                   selectNameAndGroup=self.searchByNameAndGroup,
                                   selectYearAndLanguage=self.searchByYearAndLanguage,
                                   selectTotalAndDoneWorks=self.searchByTotalAndDoneWorks,
                                   selectUncomplitedWorks=self.searchByUncomplitedWorks)
        
        self.add_widget(content)

    def searchByNameAndGroup(self):
        self.clear_widgets()
        grid = GridLayout(cols=2, spacing=15)

        textInputName = TextInput()
        textInputGroup = TextInput()
        cancelButton = Button(text="Cancel")
        cancelButton.bind(on_press=self.cancel)
        searchButton = Button(text="Search")
        searchButton.bind(on_press=lambda start: self.startSearch({"name": textInputName.text, 
                                                                   "group": textInputGroup.text}))

        grid.add_widget(Label(text="Name"))
        grid.add_widget(textInputName)
        grid.add_widget(Label(text="Group"))
        grid.add_widget(textInputGroup)
        grid.add_widget(cancelButton)
        grid.add_widget(searchButton)

        self.add_widget(grid)

    def searchByYearAndLanguage(self):
        self.clear_widgets()
        grid = GridLayout(cols=2, spacing=10)
        TextInputYear = TextInput()

        LanguageMenu=DropDown()
        for language in ["C","C++","Java","Javascript","C#","Python"]:
            btn=Button(text=language, size_hint_y=None, height=50)
            btn.bind(on_release=lambda btn: LanguageMenu.select(btn.text))
            LanguageMenu.add_widget(btn)
        ButtonMenu=Button(text="Choose language")
        ButtonMenu.bind(on_release = LanguageMenu.open)
        LanguageMenu.bind(on_select=lambda instance, x: setattr(ButtonMenu, 'text', x))

        cancelButton = Button(text="Cancel")
        cancelButton.bind(on_press=self.cancel)
        searchButton = Button(text="Search")
        searchButton.bind(
            on_press=lambda start: self.startSearch({"year": TextInputYear.text, "language": ButtonMenu.text}))

        grid.add_widget(Label(text="language"))
        grid.add_widget(ButtonMenu)
        grid.add_widget(Label(text="Year"))
        grid.add_widget(TextInputYear)
        grid.add_widget(cancelButton)
        grid.add_widget(searchButton)
        self.add_widget(grid)

    def searchByTotalAndDoneWorks(self):
        self.clear_widgets()
        grid = GridLayout(cols=2, spacing=15)
        TextInputTotal = TextInput()
        TextInputDone = TextInput()
        cancelButton = Button(text="Cancel")
        cancelButton.bind(on_press=self.cancel)
        searchButton = Button(text="Search")
        searchButton.bind(
            on_press=lambda start: self.startSearch({"total": TextInputTotal.text, "done": TextInputDone.text}))
        grid.add_widget(Label(text="Total"))
        grid.add_widget(TextInputTotal)
        grid.add_widget(Label(text="Done"))
        grid.add_widget(TextInputDone)
        grid.add_widget(cancelButton)
        grid.add_widget(searchButton)
        self.add_widget(grid)

    def searchByUncomplitedWorks(self):
        self.clear_widgets()
        grid = GridLayout(cols=2, spacing=15)
        TextInputUncomplited = TextInput()
        cancelButton = Button(text="Cancel")
        cancelButton.bind(on_press=self.cancel)
        searchButton = Button(text="Search")
        searchButton.bind(
            on_press=lambda start: self.startSearch({"uncomplited": TextInputUncomplited.text}))
        grid.add_widget(Label(text="Uncomplited"))
        grid.add_widget(TextInputUncomplited)
        grid.add_widget(cancelButton)
        grid.add_widget(searchButton)
        self.add_widget(grid)

    def startSearch(self, searchData: dict):
        self.clear_widgets()
        table = TableScreen(self.search(searchData))
        closeButton = Button(text="Close", size_hint=(1, 0.1))
        closeButton.bind(on_press=self.cancel)
        box = BoxLayout(orientation="vertical")
        box.add_widget(table)
        box.add_widget(closeButton)

        self.add_widget(box)


class DeleteDialog(FloatLayout):
    cancel = ObjectProperty(None)
    delete = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        content = SelectModeDialog(cancel=self.cancel, 
                                   selectNameAndGroup=self.deleteByNameAndGroup,
                                   selectYearAndLanguage=self.deleteByYearAndLanguage,
                                   selectTotalAndDoneWorks=self.deleteByTotalAndDoneWorks,
                                   selectUncomplitedWorks=self.deleteByUncomplitedWorks)
        self.add_widget(content)
    def deleteByNameAndGroup(self):
        self.clear_widgets()
        grid = GridLayout(cols=2, spacing=15)

        textInputName = TextInput()
        textInputGroup = TextInput()
        cancelButton = Button(text="Cancel")
        cancelButton.bind(on_press=self.cancel)
        searchButton = Button(text="Delete")
        searchButton.bind(on_press=lambda start: self.startDelete({"name": textInputName.text, 
                                                                   "group": textInputGroup.text}))

        grid.add_widget(Label(text="Name"))
        grid.add_widget(textInputName)
        grid.add_widget(Label(text="Group"))
        grid.add_widget(textInputGroup)
        grid.add_widget(cancelButton)
        grid.add_widget(searchButton)

        self.add_widget(grid)

    def deleteByYearAndLanguage(self):
        self.clear_widgets()
        grid = GridLayout(cols=2, spacing=15)
        TextInputYear = TextInput()
        TextInputLanguage = TextInput()
        cancelButton = Button(text="Cancel")
        cancelButton.bind(on_press=self.cancel)
        searchButton = Button(text="Delete")
        searchButton.bind(
            on_press=lambda start: self.startDelete({"year": TextInputYear.text, "language": TextInputLanguage.text}))
        grid.add_widget(Label(text="Year"))
        grid.add_widget(TextInputYear)
        grid.add_widget(Label(text="language"))
        grid.add_widget(TextInputLanguage)
        grid.add_widget(cancelButton)
        grid.add_widget(searchButton)
        self.add_widget(grid)

    def deleteByTotalAndDoneWorks(self):
        self.clear_widgets()
        grid = GridLayout(cols=2, spacing=15)
        TextInputTotal = TextInput()
        TextInputDone = TextInput()
        cancelButton = Button(text="Cancel")
        cancelButton.bind(on_press=self.cancel)
        searchButton = Button(text="Delete")
        searchButton.bind(
            on_press=lambda start: self.startDelete({"total": TextInputTotal.text, "done": TextInputDone.text}))
        grid.add_widget(Label(text="Total"))
        grid.add_widget(TextInputTotal)
        grid.add_widget(Label(text="Done"))
        grid.add_widget(TextInputDone)
        grid.add_widget(cancelButton)
        grid.add_widget(searchButton)
        self.add_widget(grid)

    def deleteByUncomplitedWorks(self):
        self.clear_widgets()
        grid = GridLayout(cols=2, spacing=15)
        TextInputUncomplited = TextInput()
        cancelButton = Button(text="Cancel")
        cancelButton.bind(on_press=self.cancel)
        searchButton = Button(text="Delete")
        searchButton.bind(
            on_press=lambda start: self.startDelete({"uncomplited": TextInputUncomplited.text}))
        grid.add_widget(Label(text="Uncomplited"))
        grid.add_widget(TextInputUncomplited)
        grid.add_widget(cancelButton)
        grid.add_widget(searchButton)
        self.add_widget(grid)

    def startDelete(self, deleteData: dict):
        self.clear_widgets()
        label = Label(text="You delete " + str(self.delete(deleteData)) + " records")
        closeButton = Button(text="Close", size_hint=(1, 0.1))
        closeButton.bind(on_press=self.cancel)
        box = BoxLayout(orientation="vertical")
        box.add_widget(label)
        box.add_widget(closeButton)

        self.add_widget(box)
