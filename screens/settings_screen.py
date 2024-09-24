from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label

class SettingsScreen(Screen):
    def show_data_options(self):
        popup = Popup(title='Data Options',
                      content=Label(text='Data options will be implemented soon.'),
                      size_hint=(0.8, 0.4))
        popup.open()

    def show_app_options(self):
        popup = Popup(title='App Options',
                      content=Label(text='App options will be implemented soon.'),
                      size_hint=(0.8, 0.4))
        popup.open()
