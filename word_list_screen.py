from kivy.uix.screenmanager import Screen
from utilities import load_words

class WordListScreen(Screen):
    def on_pre_enter(self):
        # Clear the list before reloading it
        self.ids.rv_list.data = []
        words = load_words()
        for word in words:
            self.ids.rv_list.data.append({
                'text': word['word'] + "    /    " + word['hiragana_katakana'],
                'on_press': lambda word_id=word['id']: self.view_word_details(word_id),
                'is_learned': word.get('learned', False)  # Add this line
            })

    def view_word_details(self, word_id):
        self.manager.get_screen('word_details').show_details(word_id)
        self.manager.current = 'word_details'
        
    def search_word(self, search_term):
        self.ids.rv_list.data = []
        words = load_words()
        matching_words = []
        
        search_term = search_term.lower()
        for word in words:
            word_lower = word['word'].lower()
            romaji_lower = word['romaji'].lower()
            hiragana_katakana_lower = word['hiragana_katakana'].lower()
            kanji_lower = word['kanji'].lower() if word['kanji'] else ''
            
            if (search_term in word_lower or 
                search_term in romaji_lower or
                search_term in hiragana_katakana_lower or 
                search_term in kanji_lower):
                # If the search term is contained in any field, add it with a high score
                matching_words.append((word, 1.0))
            else:
                # Calculate similarity for subwords of the same length as the search term
                for field in [word_lower, romaji_lower, hiragana_katakana_lower, kanji_lower]:
                    for i in range(len(field) - len(search_term) + 1):
                        subword = field[i:i+len(search_term)]
                        similarity_score = self.calculate_similarity(search_term, subword)
                        if similarity_score > 0.5:  # Adjust this threshold as needed
                            matching_words.append((word, similarity_score))
                            break  # Only add the word once with its highest similarity score
                    if matching_words and matching_words[-1][0] == word:
                        break  # Stop checking other fields if we've already added this word
        
        # Sort by similarity score, highest first
        matching_words.sort(key=lambda x: x[1], reverse=True)
        
        for word, _ in matching_words:
            self.ids.rv_list.data.append({
                'text': f"{word['word']} / {word['romaji']} / {word['hiragana_katakana']} / {word['kanji']}",
                'on_press': lambda w=word['id']: self.view_word_details(w),
                'is_learned': word.get('learned', False)  # Add this line
            })
    
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
