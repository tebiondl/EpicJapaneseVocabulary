from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from utilities import load_tags, save_tags
import uuid

class TagManagementScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_edit_tag_id = None
        self.all_tags = {}

    def on_pre_enter(self):
        self.load_tags()

    def load_tags(self):
        self.all_tags = load_tags()
        self.update_tag_list()

    def update_tag_list(self, filter_text=''):
        self.ids.rv_tags.data = []
        matching_tags = []

        filter_text = filter_text.lower()
        for tag_id, tag_info in self.all_tags.items():
            tag_name_lower = tag_info['name'].lower()
            
            if filter_text in tag_name_lower:
                matching_tags.append((tag_id, tag_info, 1.0))
            else:
                for i in range(len(tag_name_lower) - len(filter_text) + 1):
                    subword = tag_name_lower[i:i+len(filter_text)]
                    similarity_score = self.calculate_similarity(filter_text, subword)
                    if similarity_score > 0.5:
                        matching_tags.append((tag_id, tag_info, similarity_score))
                        break

        matching_tags.sort(key=lambda x: x[2], reverse=True)

        for tag_id, tag_info, _ in matching_tags:
            self.ids.rv_tags.data.append({
                'text': tag_info['name'],
                'color': tag_info['color'],
                'tag_id': tag_id,
                'on_press': lambda x=tag_id: self.edit_tag(x)
            })

    def search_tags(self, query):
        self.update_tag_list(query)

    def calculate_similarity(self, s1, s2):
        # Simple Levenshtein distance-based similarity
        m = len(s1)
        n = len(s2)
        d = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(m + 1):
            d[i][0] = i
        for j in range(n + 1):
            d[0][j] = j
        
        for j in range(1, n + 1):
            for i in range(1, m + 1):
                if s1[i - 1] == s2[j - 1]:
                    d[i][j] = d[i - 1][j - 1]
                else:
                    d[i][j] = min(d[i - 1][j], d[i][j - 1], d[i - 1][j - 1]) + 1
        
        max_len = max(m, n)
        return 1 - (d[m][n] / max_len)

    def show_tag_creation_popup(self):
        popup = TagCreationPopup(tag_management_screen=self)
        popup.open()

    def edit_tag(self, tag_id):
        tags = load_tags()
        if tag_id in tags:
            self.current_edit_tag_id = tag_id
            tag_info = tags[tag_id]
            
            edit_popup = TagEditPopup(tag_management_screen=self, tag_info=tag_info)
            edit_popup.open()

    def delete_tag(self, tag_id):
        tags = load_tags()
        if tag_id in tags:
            del tags[tag_id]
            save_tags(tags)
            self.load_tags()

    def confirm_edit_tag(self, new_name, new_color):
        if self.current_edit_tag_id:
            tags = load_tags()
            tags[self.current_edit_tag_id]['name'] = new_name
            tags[self.current_edit_tag_id]['color'] = new_color
            save_tags(tags)
            self.current_edit_tag_id = None
            self.load_tags()

class TagCreationPopup(Popup):
    def __init__(self, tag_management_screen, **kwargs):
        super().__init__(**kwargs)
        self.tag_management_screen = tag_management_screen
        self.chosen_color = [1, 1, 1, 1]

    def show_color_picker(self):
        color_picker = ColorPickerPopup(self.set_color)
        color_picker.open()

    def set_color(self, color):
        self.chosen_color = color
        self.ids.color_preview.background_color = color

    def add_tag(self):
        tag_name = self.ids.input_tag_name.text.strip()
        if tag_name:
            tags = load_tags()
            new_tag_id = str(uuid.uuid4())
            tags[new_tag_id] = {
                'name': tag_name,
                'color': self.chosen_color
            }
            save_tags(tags)
            self.tag_management_screen.load_tags()
            self.dismiss()

class TagEditPopup(Popup):
    def __init__(self, tag_management_screen, tag_info, **kwargs):
        super().__init__(**kwargs)
        self.tag_management_screen = tag_management_screen
        self.tag_info = tag_info
        self.ids.name_input.text = tag_info['name']
        self.chosen_color = tag_info['color']
        self.ids.color_preview.background_color = self.chosen_color

    def show_color_picker(self):
        color_picker = ColorPickerPopup(self.set_color, initial_color=self.chosen_color)
        color_picker.open()

    def set_color(self, color):
        self.chosen_color = color
        self.ids.color_preview.background_color = color

    def confirm_edit_tag(self):
        new_name = self.ids.name_input.text
        self.tag_management_screen.confirm_edit_tag(new_name, self.chosen_color)
        self.dismiss()

class ColorPickerPopup(Popup):
    def __init__(self, on_color_select, initial_color=[1, 1, 1, 1], **kwargs):
        super().__init__(**kwargs)
        self.on_color_select = on_color_select
        self.ids.color_picker.color = initial_color

    def select_color(self):
        self.on_color_select(self.ids.color_picker.color)
        self.dismiss()