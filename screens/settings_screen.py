from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
import json
import os
from datetime import datetime

class SettingsScreen(Screen):
    def show_data_options(self):
        self.manager.current = 'data_settings'

    def show_app_options(self):
        popup = Popup(title='App Options',
                      content=Label(text='App options will be implemented soon.'),
                      size_hint=(0.8, 0.4))
        popup.open()

class DataSettingsScreen(Screen):
    def create_backup(self):
        content = BoxLayout(orientation='vertical')
        file_chooser = FileChooserListView(path=os.path.expanduser('~'), filters=['*.epic'])
        content.add_widget(file_chooser)
        
        save_button = Button(text='Save', size_hint_y=None, height='48dp')
        save_button.bind(on_press=lambda x: self.save_backup(file_chooser.path, file_chooser.selection))
        content.add_widget(save_button)
        
        popup = Popup(title='Choose Backup Location', content=content, size_hint=(0.9, 0.9))
        popup.open()

    def save_backup(self, path, selection):
        if selection:
            backup_file = os.path.join(path, f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.epic")
        else:
            backup_file = os.path.join(path, f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.epic")
        
        data = {}
        for file in ['saved_info/tags.json', 'saved_info/words.json']:
            if os.path.exists(file):
                with open(file, 'r') as f:
                    data[file] = json.load(f)
        
        with open(backup_file, 'w') as f:
            json.dump(data, f)
        
        self.show_message(f"Backup created: {backup_file}")

    def restore_backup(self):
        content = BoxLayout(orientation='vertical')
        file_chooser = FileChooserListView(path=os.path.expanduser('~'), filters=['*.epic'])
        content.add_widget(file_chooser)
        
        restore_button = Button(text='Restore', size_hint_y=None, height='48dp')
        restore_button.bind(on_press=lambda x: self.show_restore_options(file_chooser.selection))
        content.add_widget(restore_button)
        
        popup = Popup(title='Choose Backup File', content=content, size_hint=(0.9, 0.9))
        popup.open()

    def show_restore_options(self, selection):
        if not selection:
            self.show_message("No file selected")
            return
        
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text='How do you want to restore the backup?'))
        merge_btn = Button(text='Merge with current data')
        replace_btn = Button(text='Replace current data')
        
        merge_btn.bind(on_press=lambda x: self.perform_restore(selection[0], merge=True))
        replace_btn.bind(on_press=lambda x: self.perform_restore(selection[0], merge=False))
        
        content.add_widget(merge_btn)
        content.add_widget(replace_btn)
        
        popup = Popup(title='Restore Options', content=content, size_hint=(0.8, 0.4))
        popup.open()

    def perform_restore(self, backup_file, merge=False):
        if os.path.exists(backup_file):
            with open(backup_file, 'r') as f:
                backup_data = json.load(f)
            
            for file, data in backup_data.items():
                if merge and os.path.exists(file):
                    with open(file, 'r') as f:
                        current_data = json.load(f)
                    current_data.update(data)  # Merge data
                    data = current_data
                
                with open(file, 'w') as f:
                    json.dump(data, f)
            
            self.show_message("Backup restored successfully")
        else:
            self.show_message("Backup file not found")

    def show_message(self, message):
        popup = Popup(title='Message', content=Label(text=message), size_hint=(0.8, 0.4))
        popup.open()
