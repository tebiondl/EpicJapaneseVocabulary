from kivy.uix.screenmanager import Screen
from utilities import load_words, save_words, load_tags
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.recycleview import RecycleView

class WordDetailsScreen(Screen):
    is_learned = BooleanProperty(False)
    current_word = ObjectProperty(None)

    def show_details(self, word_id):
        self.current_word_id = word_id
        words = load_words()
        for w in words:
            if w['id'] == word_id:
                self.current_word = w
                self.ids.input_word.text = w['word']
                self.ids.input_romaji.text = w['romaji']
                self.ids.input_hiragana_katakana.text = w['hiragana_katakana']
                self.ids.input_kanji.text = w['kanji']
                self.is_learned = w.get('learned', False)
                break

    def show_tag_popup(self):
        popup = TagSelectionPopup(word=self.current_word)
        popup.open()

    def toggle_tag(self, tag_id, active):
        if 'tags' not in self.current_word:
            self.current_word['tags'] = []
        if active and tag_id not in self.current_word['tags']:
            self.current_word['tags'].append(tag_id)
        elif not active and tag_id in self.current_word['tags']:
            self.current_word['tags'].remove(tag_id)

    def save_changes(self):
        word = self.ids.input_word.text
        romaji = self.ids.input_romaji.text
        hiragana_katakana = self.ids.input_hiragana_katakana.text
        kanji = self.ids.input_kanji.text

        if word:
            words = load_words()
            for i, w in enumerate(words):
                if w['id'] == self.current_word_id:
                    words[i] = {
                        'id': self.current_word_id,
                        'word': word,
                        'romaji': romaji,
                        'hiragana_katakana': hiragana_katakana,
                        'kanji': kanji,
                        'learned': self.is_learned,
                        'tags': self.current_word.get('tags', [])
                    }
                    break
            save_words(words)
            self.manager.current = 'word_list'

    def delete_word(self):
        words = load_words()
        words = [w for w in words if w['id'] != self.current_word_id]
        save_words(words)
        self.manager.current = 'word_list'

    def toggle_learned(self):
        self.is_learned = not self.is_learned
        self.save_changes()

class TagSelectionPopup(Popup):
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
        # The tags are already updated in the current_word object of WordDetailsScreen
        # You might want to call save_changes() here if you want to save immediately
        # self.parent.save_changes()
