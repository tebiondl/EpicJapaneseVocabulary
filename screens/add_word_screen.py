from kivy.uix.screenmanager import Screen
from utilities import save_words, load_words, load_tags
import uuid
from kivy.uix.popup import Popup

class AddWordScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_tags = []

    def show_tag_popup(self):
        popup = AddWordTagSelectionPopup(word={'tags': self.selected_tags})
        popup.open()

    def update_selected_tags(self, instance):
        self.selected_tags = instance.word['tags']

    def toggle_tag(self, tag_id, active):
        if active and tag_id not in self.selected_tags:
            self.selected_tags.append(tag_id)
        elif not active and tag_id in self.selected_tags:
            self.selected_tags.remove(tag_id)

    def save_word(self):
        word = self.ids.input_word.text
        romaji = self.ids.input_romaji.text
        hiragana_katakana = self.ids.input_hiragana_katakana.text
        kanji = self.ids.input_kanji.text

        if word:
            words = load_words()
            new_word = {
                'id': str(uuid.uuid4()),
                'word': word,
                'romaji': romaji,
                'hiragana_katakana': hiragana_katakana,
                'kanji': kanji,
                'tags': self.selected_tags
            }
            words.append(new_word)
            save_words(words)
            self.clear_inputs()
            self.manager.current = 'word_list'

    def clear_inputs(self):
        self.ids.input_word.text = ''
        self.ids.input_romaji.text = ''
        self.ids.input_hiragana_katakana.text = ''
        self.ids.input_kanji.text = ''
        self.selected_tags = []
        
class AddWordTagSelectionPopup(Popup):
    def __init__(self, word, **kwargs):
        super().__init__(**kwargs)
        self.word = word
        self.load_tags()

    def load_tags(self):
        tags = load_tags()
        self.ids.rv_tags.data = [
            {'tag_id': tag_id, 'text': tag_info['name'], 'active': tag_id in self.word.get('tags', [])}
            for tag_id, tag_info in tags.items()
        ]

    def search_tags(self, query):
        tags = load_tags()
        filtered_tags = {tag_id: tag_info for tag_id, tag_info in tags.items() 
                         if query.lower() in tag_info['name'].lower()}
        self.ids.rv_tags.data = [
            {'tag_id': tag_id, 'text': tag_info['name'], 'active': tag_id in self.word.get('tags', [])}
            for tag_id, tag_info in filtered_tags.items()
        ]

    def apply_tags(self):
        self.dismiss()
