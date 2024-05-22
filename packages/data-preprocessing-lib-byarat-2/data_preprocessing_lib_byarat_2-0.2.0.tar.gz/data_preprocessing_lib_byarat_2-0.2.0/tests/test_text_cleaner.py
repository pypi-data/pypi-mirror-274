import unittest
import pandas as pd
from data_preprocessing_lib_byarat import TextCleaner

class TestTextCleaner(unittest.TestCase):

    def setUp(self):
        self.text = "This is a TEST text, with punctuations! And some <b>HTML</b> tags, URLs like https://example.com, and emojis 😊."
        self.df = pd.DataFrame({
            'text_column': [
                "This is a TEST text, with punctuations!",
                "Another text with <b>HTML</b> tags.",
                "Text with URLs https://example.com and emojis 😊."
            ]
        })

    def test_clean_text(self):
        cleaned_text = TextCleaner.clean_text(self.text)
        self.assertIsInstance(cleaned_text, str)
        self.assertNotIn('<', cleaned_text)
        self.assertNotIn('😊', cleaned_text)

    def test_clean_column(self):
        df_result = TextCleaner.clean_column(self.df.copy(), 'text_column')
        self.assertIsInstance(df_result, pd.DataFrame)
        self.assertNotIn('<', df_result['text_column'].iloc[0])
        self.assertNotIn('😊', df_result['text_column'].iloc[2])

    def test_remove_stopwords(self):
        cleaned_text = TextCleaner.remove_stopwords(self.text)
        self.assertIsInstance(cleaned_text, str)
        self.assertNotIn('is', cleaned_text)
        self.assertNotIn('a', cleaned_text)

    def test_to_lowercase(self):
        lowered_text = TextCleaner.to_lowercase(self.text)
        self.assertIsInstance(lowered_text, str)
        self.assertTrue(lowered_text.islower())

    def test_remove_punctuation(self):
        cleaned_text = TextCleaner.remove_punctuation(self.text)
        self.assertIsInstance(cleaned_text, str)
        self.assertNotIn('!', cleaned_text)
        self.assertNotIn(',', cleaned_text)

    def test_lemmatize(self):
        lemmatized_text = TextCleaner.lemmatize(self.text)
        self.assertIsInstance(lemmatized_text, str)

    def test_remove_numbers(self):
        text_with_numbers = "This is text with numbers 12345."
        cleaned_text = TextCleaner.remove_numbers(text_with_numbers)
        self.assertIsInstance(cleaned_text, str)
        self.assertNotIn('12345', cleaned_text)

    def test_remove_extra_whitespace(self):
        text_with_whitespace = "This  is   text    with     extra      whitespace."
        cleaned_text = TextCleaner.remove_extra_whitespace(text_with_whitespace)
        self.assertIsInstance(cleaned_text, str)
        self.assertNotIn('  ', cleaned_text)

    def test_stem_words(self):
        stemmed_text = TextCleaner.stem_words(self.text)
        self.assertIsInstance(stemmed_text, str)

    def test_remove_html_tags(self):
        cleaned_text = TextCleaner.remove_html_tags(self.text)
        self.assertIsInstance(cleaned_text, str)
        self.assertNotIn('<', cleaned_text)

    def test_replace_contractions(self):
        text_with_contractions = "I'm not sure if it's going to work."
        expanded_text = TextCleaner.replace_contractions(text_with_contractions)
        self.assertIsInstance(expanded_text, str)
        self.assertNotIn("I'm", expanded_text)

    def test_expand_abbreviations(self):
        text_with_abbreviations = "u r awesome!"
        expanded_text = TextCleaner.expand_abbreviations(text_with_abbreviations)
        self.assertIsInstance(expanded_text, str)
        self.assertIn("you are awesome!", expanded_text)

    def test_remove_special_characters(self):
        text_with_special_characters = "This @#& text *&^% has special $$# characters."
        cleaned_text = TextCleaner.remove_special_characters(text_with_special_characters)
        self.assertIsInstance(cleaned_text, str)
        self.assertNotIn('@', cleaned_text)
        self.assertNotIn('#', cleaned_text)

    def test_remove_urls(self):
        text_with_urls = "Visit https://example.com for more info."
        cleaned_text = TextCleaner.remove_urls(text_with_urls)
        self.assertIsInstance(cleaned_text, str)
        self.assertNotIn('https://example.com', cleaned_text)

    def test_remove_emojis(self):
        text_with_emojis = "This text has emojis 😊👍."
        cleaned_text = TextCleaner.remove_emojis(text_with_emojis)
        self.assertIsInstance(cleaned_text, str)
        self.assertNotIn('😊', cleaned_text)
        self.assertNotIn('👍', cleaned_text)

    def test_spell_check(self):
        text_with_typos = "Ths is a txt with sme typos."
        corrected_text = TextCleaner.spell_check(text_with_typos)
        self.assertIsInstance(corrected_text, str)
        self.assertIn('This is a text with some typos', corrected_text)

if __name__ == '__main__':
    unittest.main()
