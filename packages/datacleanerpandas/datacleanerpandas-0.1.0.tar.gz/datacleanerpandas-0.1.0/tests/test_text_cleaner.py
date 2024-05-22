import unittest
from dataPreprocessing.text_cleaner import TextCleaner

class TestTextCleaner(unittest.TestCase):
    def setUp(self):
        self.cleaner = TextCleaner()

    def test_lowercase_conversion(self):
        text = "This IS A SamPle TexT"
        expected = "sample text"
        cleaned_text = self.cleaner.clean(text)
        self.assertEqual(cleaned_text, expected)



    def test_remove_punctuation(self):
        text = "This, is. a sample! text?"
        expected = "sample text"
        cleaned_text = self.cleaner.clean(text)
        self.assertEqual(cleaned_text, expected)

    def test_split_into_words(self):
        text = "This is a sample text"
        expected_words = "sample text"
        cleaned_text = self.cleaner.clean(text)
        self.assertEqual(cleaned_text, expected_words)

    def test_remove_stopwords(self):
        text = "This is a sample text with some stopwords like 'the' and 'is'"
        expected = "sample text stopwords like"
        cleaned_text = self.cleaner.clean(text)
        self.assertEqual(cleaned_text, expected)

    def test_lemmatization(self):
        text = "This is a sample text with some different forms of words"
        expected = "sample text different form word"
        cleaned_text = self.cleaner.clean(text)
        self.assertEqual(cleaned_text, expected)

if __name__ == '__main__':
    unittest.main()
