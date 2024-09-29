from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from plyer import filechooser
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
    def get_app_dir(self):
        # Go up one level from the 'screens' directory to reach the main app directory
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def create_backup(self):
        app_dir = self.get_app_dir()
        default_path = os.path.join(app_dir, 'backup.epic')
        original_dir = os.getcwd()
        try:
            filechooser.save_file(on_selection=self.save_backup, 
                                  filters=['*.epic'],
                                  path=default_path)
        finally:
            os.chdir(original_dir)

    def save_backup(self, path):
        if not path:
            return
        
        original_dir = os.getcwd()
        app_dir = self.get_app_dir()
        
        try:
            backup_file = path[0]
            if not backup_file.endswith('.epic'):
                backup_file += '.epic'
            
            data = {}
            for file in ['tags.json', 'words.json']:
                file_path = os.path.join(app_dir, file)
                if os.path.exists(file_path):
                    with open(file_path, 'r') as f:
                        data[file] = json.load(f)
            
            with open(backup_file, 'w') as f:
                json.dump(data, f)
            
            self.show_message(f"Backup created: {backup_file}")
        finally:
            os.chdir(app_dir)  # Always return to the main app directory

    def restore_backup(self):
        app_dir = self.get_app_dir()
        original_dir = os.getcwd()
        try:
            filechooser.open_file(on_selection=self.show_restore_options, 
                                  filters=['*.epic'],
                                  path=app_dir)
        finally:
            os.chdir(original_dir)

    def show_restore_options(self, selection):
        if not selection:
            return
        
        backup_file = selection[0]
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text='How do you want to restore the backup?'))
        merge_btn = Button(text='Merge with current data')
        replace_btn = Button(text='Replace current data')
        
        merge_btn.bind(on_press=lambda x: self.perform_restore(backup_file, merge=True))
        replace_btn.bind(on_press=lambda x: self.perform_restore(backup_file, merge=False))
        
        content.add_widget(merge_btn)
        content.add_widget(replace_btn)
        
        self.restore_popup = Popup(title='Restore Options', content=content, size_hint=(0.8, 0.4))
        self.restore_popup.open()

    def perform_restore(self, backup_file, merge=False):
        print(f"Starting restore process. Current directory: {os.getcwd()}")
        print(f"Backup file: {backup_file}")
        
        original_dir = os.getcwd()
        app_dir = self.get_app_dir()
        
        print(f"Original directory: {original_dir}")
        print(f"App directory: {app_dir}")
        
        try:
            if os.path.exists(backup_file):
                print(f"Backup file exists. Opening file.")
                with open(backup_file, 'r') as f:
                    backup_data = json.load(f)
                
                print(f"Backup data loaded. Files to restore: {list(backup_data.keys())}")
                
                for file, data in backup_data.items():
                    file_path = os.path.join(app_dir, file)
                    print(f"Processing file: {file_path}")
                    
                    if merge and os.path.exists(file_path):
                        print(f"Merging data for {file}")
                        with open(file_path, 'r') as f:
                            current_data = json.load(f)
                        current_data.update(data)  # Merge data
                        data = current_data
                    
                    print(f"Writing data to {file_path}")
                    with open(file_path, 'w') as f:
                        json.dump(data, f)
                
                self.show_message("Backup restored successfully")
            else:
                print(f"Backup file not found: {backup_file}")
                self.show_message("Backup file not found")
        except Exception as e:
            print(f"Error during restore: {str(e)}")
            self.show_message(f"Error during restore: {str(e)}")
        finally:
            print(f"Changing directory back to: {app_dir}")
            os.chdir(app_dir)  # Always return to the main app directory
            print(f"Final current directory: {os.getcwd()}")
        
        if hasattr(self, 'restore_popup') and self.restore_popup:
            self.restore_popup.dismiss()

    def show_message(self, message):
        popup = Popup(title='Message', content=Label(text=message), size_hint=(0.8, 0.4))
        popup.open()
