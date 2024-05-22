import pandas as pd
import string
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer, PorterStemmer
from bs4 import BeautifulSoup
import contractions
import emoji
from spellchecker import SpellChecker

class TextCleaner:
    @staticmethod
    def clean_text(text):
        stop_words = set(stopwords.words('english'))
        lemmatizer = WordNetLemmatizer()
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        words = word_tokenize(text)
        words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
        return ' '.join(words)

    @staticmethod
    def clean_column(df, column):
        df[column] = df[column].apply(TextCleaner.clean_text)
        return df

    @staticmethod
    def remove_stopwords(text):
        stop_words = set(stopwords.words('english'))
        words = text.split()
        cleaned_text = " ".join([word for word in words if word.lower() not in stop_words])
        return cleaned_text

    @staticmethod
    def to_lowercase(text):
        return text.lower()

    @staticmethod
    def remove_punctuation(text):
        return re.sub(r'[^\w\s]', '', text)

    @staticmethod
    def lemmatize(text):
        lemmatizer = WordNetLemmatizer()
        words = text.split()
        lemmatized_text = " ".join([lemmatizer.lemmatize(word) for word in words])
        return lemmatized_text

    @staticmethod
    def remove_numbers(text):
        return re.sub(r'\d+', '', text)

    @staticmethod
    def remove_extra_whitespace(text):
        return re.sub(r'\s+', ' ', text).strip()

    @staticmethod
    def stem_words(text):
        stemmer = PorterStemmer()
        words = text.split()
        stemmed_text = " ".join([stemmer.stem(word) for word in words])
        return stemmed_text

    @staticmethod
    def remove_html_tags(text):
        return BeautifulSoup(text, "html.parser").get_text()

    @staticmethod
    def replace_contractions(text):
        return contractions.fix(text)

    @staticmethod
    def expand_abbreviations(text):
        abbreviations = {
            "u": "you",
            "r": "are",
            "ur": "your",
            "lol": "laughing out loud",
            "idk": "I don't know"
            # Add more abbreviations as needed
        }
        words = text.split()
        expanded_text = " ".join([abbreviations[word] if word in abbreviations else word for word in words])
        return expanded_text

    @staticmethod
    def remove_special_characters(text):
        return re.sub(r'[^a-zA-Z0-9\s]', '', text)

    @staticmethod
    def remove_urls(text):
        return re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)

    @staticmethod
    def remove_emojis(text):
        emoji_pattern = re.compile(
            "[" 
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\U00002702-\U000027B0"  # Dingbats
            u"\U000024C2-\U0001F251" 
            "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', text)

    @staticmethod
    def spell_check(text):
        spell = SpellChecker()
        words = text.split()
        corrected_text = " ".join([spell.correction(word) if spell.correction(word) is not None else word for word in words])
        return corrected_text

# Test kodu
if __name__ == "__main__":
    data = {
        'text': [
            "Hello World! This is a test.",
            "Check out this link: https://example.com",
            "U r amazing! LOL",
            "Text with numbers 12345 and punctuations!!!",
            "<html>HTML content</html>",
            "   Extra   whitespace   ",
            "Spellng mistkes are cmmon",
            "Emojis are fun 😊😂👍",
            "Here's a contraction: don't",
            "Abbreviations like idk and lol"
        ]
    }
    df = pd.DataFrame(data)

    cleaner = TextCleaner()

    # clean_text test
    print("Clean Text:")
    for text in df['text']:
        print(cleaner.clean_text(text))

    # clean_column test
    df_clean = cleaner.clean_column(df.copy(), 'text')
    print("\nClean Column:")
    print(df_clean)

    # remove_stopwords test
    print("\nRemove Stopwords:")
    for text in df['text']:
        print(cleaner.remove_stopwords(text))

    # to_lowercase test
    print("\nTo Lowercase:")
    for text in df['text']:
        print(cleaner.to_lowercase(text))

    # remove_punctuation test
    print("\nRemove Punctuation:")
    for text in df['text']:
        print(cleaner.remove_punctuation(text))

    # lemmatize test
    print("\nLemmatize:")
    for text in df['text']:
        print(cleaner.lemmatize(text))

    # remove_numbers test
    print("\nRemove Numbers:")
    for text in df['text']:
        print(cleaner.remove_numbers(text))

    # remove_extra_whitespace test
    print("\nRemove Extra Whitespace:")
    for text in df['text']:
        print(cleaner.remove_extra_whitespace(text))

    # stem_words test
    print("\nStem Words:")
    for text in df['text']:
        print(cleaner.stem_words(text))

    # remove_html_tags test
    print("\nRemove HTML Tags:")
    for text in df['text']:
        print(cleaner.remove_html_tags(text))

    # replace_contractions test
    print("\nReplace Contractions:")
    for text in df['text']:
        print(cleaner.replace_contractions(text))

    # expand_abbreviations test
    print("\nExpand Abbreviations:")
    for text in df['text']:
        print(cleaner.expand_abbreviations(text))

    # remove_special_characters test
    print("\nRemove Special Characters:")
    for text in df['text']:
        print(cleaner.remove_special_characters(text))

    # remove_urls test
    print("\nRemove URLs:")
    for text in df['text']:
        print(cleaner.remove_urls(text))

    # remove_emojis test
    print("\nRemove Emojis:")
    for text in df['text']:
        print(cleaner.remove_emojis(text))

    # spell_check test
    print("\nSpell Check:")
    for text in df['text']:
        print(cleaner.spell_check(text))
