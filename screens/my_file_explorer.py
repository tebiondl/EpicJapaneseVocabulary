from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
import os

class MyFileExplorer(BoxLayout):
    def __init__(self, start_path, on_file_selected, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.current_path = start_path
        self.on_file_selected = on_file_selected
        self.create_file_view()

    def create_file_view(self):
        """Create the view for displaying files and directories."""
        self.clear_widgets()

        # Display the current path label (responsive height)
        path_label = Label(
            text=f"Current Path: {self.current_path}",
            size_hint_y=None,
            height=50,
            text_size=(self.width * 0.95, None),  # Ajustar el área de texto al ancho del Label
            halign='left',
            valign='middle',
            padding=(10, 10)
        )
        path_label.bind(size=path_label.setter('text_size'))
        self.add_widget(path_label)

        # Layout for file and folder buttons (responsive size)
        file_layout = GridLayout(
            cols=1,
            size_hint_y=None,
            padding=[10, 10, 10, 10],  # Padding para dejar espacio alrededor
            spacing=10
        )
        file_layout.bind(minimum_height=file_layout.setter('height'))

        # Button to navigate up one directory (only if not at the root)
        if os.path.dirname(self.current_path) != self.current_path:
            up_button = Button(
                text=".. (Up)",
                size_hint_y=None,
                height=self.height * 0.05,
                halign='left',
                valign='middle',
                padding=(10, 10)
            )
            up_button.bind(on_release=self.go_up)
            file_layout.add_widget(up_button)

        # Create buttons for each file and folder in the current directory
        for item in os.listdir(self.current_path):
            item_path = os.path.join(self.current_path, item)
            if os.path.isdir(item_path):
                # Button for directories
                btn = Button(
                    text=f"[Folder] {item}",
                    size_hint_y=None,
                    height=self.height * 0.05,
                    halign='left',
                    valign='middle',
                    padding=(10, 10)
                )
                btn.bind(on_release=lambda x, p=item_path: self.open_folder(p))
            elif item.endswith(".epic"):
                # Button for .epic files
                btn = Button(
                    text=item,
                    size_hint_y=None,
                    height=self.height * 0.05,
                    halign='left',
                    valign='middle',
                    padding=(10, 10)
                )
                btn.bind(on_release=lambda x, p=item_path: self.select_file(p))
            else:
                continue  # Ignore files that do not have the .epic extension

            file_layout.add_widget(btn)

        # ScrollView to handle large lists of files (responsive height)
        scroll_view = ScrollView(size_hint=(1, 0.8))  # Reducir la altura para dejar espacio para el Label
        scroll_view.add_widget(file_layout)
        self.add_widget(scroll_view)

    def go_up(self, instance):
        """Navigate to the parent directory."""
        self.current_path = os.path.dirname(self.current_path)
        self.create_file_view()

    def open_folder(self, path):
        """Open a folder and update the view."""
        self.current_path = path
        self.create_file_view()

    def select_file(self, path):
        """Select a file and trigger the callback with the selected file path."""
        self.on_file_selected([path])
