from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

Builder.load_file("kv/MyLabel.kv")
Builder.load_file("kv/TextCell.kv")
Builder.load_file("kv/Table.kv")
Builder.load_file("kv/TableController.kv")


class TextCell(BoxLayout):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.ids.label.text = text

    def setText(self, text):
        self.ids.label.text = text


class Table(GridLayout):
    def __init__(self, data: list, **kwargs):
        super().__init__(**kwargs)
        self.currentPage = 0
        self.totalPage = 0
        self.data = data
        self.maxRows = 36
        self.update(1)

    def clear(self):
        for child in reversed(self.children):
            if type(child) is TextCell:
                self.remove_widget(child)

    def update(self, page):
        self.currentPage = 0 if len(self.data) == 0 else page
        self.totalPage = len(self.data) // (self.rows - 1) + (1 if len(self.data) % (self.rows - 1) != 0 else 0)
        for i in range(self.rows - 1):
            currentRecord = i + (self.rows - 1) * max(0, (self.currentPage - 1))
            self.add_widget(TextCell(str(currentRecord + 1), size_hint=self.ids.num.size_hint))
            if currentRecord < len(self.data) != 0:
                self.add_widget(TextCell(self.data[currentRecord]["name"], size_hint=self.ids.name.size_hint))
                self.add_widget(TextCell(self.data[currentRecord]["year"],
                                         size_hint=self.ids.year.size_hint))
                self.add_widget(TextCell(self.data[currentRecord]["group"],
                                         size_hint=self.ids.group.size_hint))
                self.add_widget(TextCell(self.data[currentRecord]["total"], size_hint=self.ids.all.size_hint))
                self.add_widget(TextCell(self.data[currentRecord]["done"], size_hint=self.ids.done.size_hint))
                self.add_widget(TextCell(self.data[currentRecord]["language"], size_hint=self.ids.language.size_hint))
            else:
                self.add_widget(TextCell("", size_hint=self.ids.name.size_hint))
                self.add_widget(TextCell("", size_hint=self.ids.year.size_hint))
                self.add_widget(TextCell("", size_hint=self.ids.group.size_hint))
                self.add_widget(TextCell("", size_hint=self.ids.all.size_hint))
                self.add_widget(TextCell("", size_hint=self.ids.done.size_hint))
                self.add_widget(TextCell("", size_hint=self.ids.language.size_hint))


class TableController(BoxLayout):
    def __init__(self, table: Table, **kwargs):
        super().__init__(**kwargs)
        self.table = table
        self.update()

    def superLeft(self):
        self.table.clear()
        self.table.update(1)
        self.update()

    def superRight(self):
        self.table.clear()
        self.table.update(self.table.totalPage)
        self.update()

    def left(self):
        self.table.clear()
        self.table.update(max(1, self.table.currentPage - 1))
        self.update()

    def right(self):
        self.table.clear()
        self.table.update(min(self.table.totalPage, self.table.currentPage + 1))
        self.update()

    def textInput(self):
        newCol = self.ids.rowsCol.text
        if newCol.isdigit():
            self.table.clear()
            self.table.rows = min(int(newCol) + 1, self.table.maxRows)
            self.table.update(self.table.currentPage)
            self.update()

    def update(self):
        self.ids.currentPage.text = str(self.table.currentPage)
        self.ids.totalPage.text = str(self.table.totalPage)
        self.ids.rowsCol.text = str(self.table.rows - 1)


class TableScreen(BoxLayout):
    def __init__(self, data: list, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.data = data
        self.table = Table(self.data, size_hint=(1, .9))
        self.tableController = TableController(self.table, size_hint=(1, .1))

        self.add_widget(self.table)
        self.add_widget(self.tableController)

    def update(self, data: list):
        self.data = data
        self.table.data = self.data
        self.table.clear()
        self.table.update(1)
        self.tableController.update()
