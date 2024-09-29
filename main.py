from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screens.word_list_screen import WordListScreen
from screens.add_word_screen import AddWordScreen
from screens.word_info_screen import WordDetailsScreen
from screens.settings_screen import SettingsScreen, DataSettingsScreen  # Add this import
from screens.tag_management_screen import TagManagementScreen
import os
from kivy.lang import Builder

# Try to import android module
try:
    import android
except ImportError:
    android = None

# Load the common widgets and styles
Builder.load_file('kv/common.kv')

# Load individual screen layouts
Builder.load_file('kv/word_list_screen.kv')
Builder.load_file('kv/add_word_screen.kv')
Builder.load_file('kv/word_details_screen.kv')
Builder.load_file('kv/settings_screen.kv')
Builder.load_file('kv/tag_management_screen.kv')

Builder.load_file('kv/add_word_tag_popup.kv')
Builder.load_file('kv/word_details_tag_popup.kv')

class MainApp(App):
    def build(self):
        # Check if running on Android and request permissions
        if android:
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])

        sm = ScreenManager()

        # Main screen (List of words)
        word_list_screen = WordListScreen(name='word_list')
        sm.add_widget(word_list_screen)

        # Add word screen
        add_word_screen = AddWordScreen(name='add_word')
        sm.add_widget(add_word_screen)

        # Word details screen
        word_details_screen = WordDetailsScreen(name='word_details')
        sm.add_widget(word_details_screen)

        # Settings screen
        settings_screen = SettingsScreen(name='settings')
        sm.add_widget(settings_screen)

        # Data settings screen
        data_settings_screen = DataSettingsScreen(name='data_settings')
        sm.add_widget(data_settings_screen)

        # Tag management screen
        tag_management_screen = TagManagementScreen(name='tag_management')
        sm.add_widget(tag_management_screen)

        return sm

if __name__ == '__main__':
    MainApp().run()
