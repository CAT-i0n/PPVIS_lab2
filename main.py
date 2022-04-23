from kivy.app import App

from view.MainWindow import MainWindow


class DatabaseApp(App):
    def build(self):
        return MainWindow()


if __name__ == "__main__":
    DatabaseApp().run()
