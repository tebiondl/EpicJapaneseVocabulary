from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from plyer import filechooser
from kivy.uix.filechooser import FileChooserIconView
import json
import os
from kivy.utils import platform
from datetime import datetime
from android.storage import primary_external_storage_path
from jnius import autoclass

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

    def get_android_base_dir(self):
        if platform == 'android':     
            return primary_external_storage_path()
        else:
            return os.path.expanduser('~')

    def create_backup(self):
        base_dir = self.get_android_base_dir()
        new_dir = os.path.join(base_dir, "JapaneseVocabulary", "backups")
        
        if not self.has_manage_storage_permission():
            self.request_manage_storage_permission()
            return
        
        try:
            # Create a folder called JapaneseVocabulary on the base path
            os.makedirs(new_dir, exist_ok=True)
            self.save_backup(new_dir)
        except Exception as e:
            popup = Popup(title="Error",
                          content=Label(text=str("You have not given file permissions to the app"), font_size='8sp'),
                          size_hint=(0.8, 0.4))
            popup.open()
            
    def selected_folder(self, selection):
        if selection:
            folder_path = selection[0]
            print(f"Carpeta seleccionada: {folder_path}")
            self.save_backup(folder_path)
        else:
            popup = Popup(title="Error",
                          content=Label(text="No folder has been selected"),
                          size_hint=(0.8, 0.4))
            popup.open()

    def save_backup(self, path):
        backup_folder = os.path.join(path, 'auto_backup')
        date = datetime.now()
        date = date.strftime("%d-%m-%Y")

        if not path:
            default_backup_file = os.path.join(path, 'auto_backup/auto_backup_' + date + '.epic')
            os.makedirs(backup_folder, exist_ok=True)
            backup_file = default_backup_file
        else:
            backup_file = path + "/backup_" + date + '.epic'
        
        this_path = os.path.dirname(os.path.abspath(__file__))
        
        try:
            data = {}
            for file in [this_path + '/../tags.json', this_path + '/../words.json']:
                file_path = os.path.join(path, file)
                if os.path.exists(file_path):
                    with open(file_path, 'r') as f:
                        data[file] = json.load(f)
            
            # Ensure the directory exists
            os.makedirs(os.path.dirname(backup_file), exist_ok=True)
            
            with open(backup_file, 'w') as f:
                json.dump(data, f)
            
            self.show_message(f"Backup created in:\n{backup_file}")
        except Exception as e:
            print(f"Error al cargar los archivos: {e}")
        finally:
            os.chdir(path)  # Always return to the main app directory

    def restore_backup(self):
        base_dir = self.get_android_base_dir()
        original_dir = os.getcwd()
        try:
            filechooser.open_file(on_selection=self.show_restore_options, 
                                  filters=['*.epic'],
                                  path=base_dir)
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
        
    def has_manage_storage_permission(self):
        # En Android 11+, verifica si tenemos MANAGE_EXTERNAL_STORAGE
        Environment = autoclass('android.os.Environment')
        return Environment.isExternalStorageManager()
        
    def request_manage_storage_permission(self):
        # Redirige al usuario a la configuración de permisos de la aplicación
        Intent = autoclass('android.content.Intent')
        Uri = autoclass('android.net.Uri')
        Settings = autoclass('android.provider.Settings')
        
        intent = Intent(Settings.ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION)
        uri = Uri.fromParts("package", autoclass("org.kivy.android.PythonActivity").mActivity.getPackageName(), None)
        intent.setData(uri)
        autoclass("org.kivy.android.PythonActivity").mActivity.startActivity(intent)
        print("Redirigiendo a configuración de permisos para MANAGE_EXTERNAL_STORAGE")
