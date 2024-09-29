import json
import os
import uuid

DATA_FILE = 'words.json'
TAGS_FILE = 'tags.json'

# Function to load words from the JSON file
def load_words():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            words = json.load(file)
        
        # Define the expected structure with default values
        word_template = {
            'id': '',
            'word': '',
            'romaji': '',
            'hiragana_katakana': '',
            'kanji': '',
            'learned': False,
            'tags': []  # Add this line
        }
        
        # Ensure each word has all required fields
        for word in words:
            for key, default_value in word_template.items():
                if key not in word:
                    word[key] = default_value
        
        return words
    return []

# Function to save words to the JSON file
def save_words(words):
    with open(DATA_FILE, 'w') as file:
        json.dump(words, file, indent=4)

# Function to load tags from the JSON file
def load_tags():
    if os.path.exists(TAGS_FILE):
        with open(TAGS_FILE, 'r') as file:
            tags = json.load(file)
        # Convert old format to new format if necessary
        if tags and isinstance(next(iter(tags.values())), list):
            new_tags = {}
            for tag_name, color in tags.items():
                new_tags[str(uuid.uuid4())] = {'name': tag_name, 'color': color}
            tags = new_tags
            save_tags(tags)
        return tags
    return {}

# Function to save tags to the JSON file
def save_tags(tags):
    with open(TAGS_FILE, 'w') as file:
        json.dump(tags, file, indent=4)
