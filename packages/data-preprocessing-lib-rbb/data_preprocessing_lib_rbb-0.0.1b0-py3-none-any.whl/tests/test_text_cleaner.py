import unittest
from dataPreprocessing.text_cleaner import TextCleaner

class TestTextCleaner(unittest.TestCase):

    """
    TestTextCleaner is a test class for the TextCleaner class, ensuring the correct functionality of text cleaning operations.

    Methods:
        setUp():
            Initializes an instance of TextCleaner for testing.

        test_lowercase_conversion():
            Tests the conversion of text to lowercase.

        test_remove_short_words():
            Tests the removal of short words from the text.

        test_remove_punctuation():
            Tests the removal of punctuation from the text.

        test_split_into_words():
            Tests the splitting of text into words.

        test_remove_stopwords():
            Tests the removal of stopwords from the text.

        test_lemmatization():
            Tests the lemmatization of words in the text.
    """

    def setUp(self):
        self.cleaner = TextCleaner()

    def test_lowercase_conversion(self):
        text = "This IS A SamPle TexT"
        expected = "sample text"
        cleaned_text = self.cleaner.clean(text)
        self.assertEqual(cleaned_text, expected)

    def test_remove_short_words(self):
        text = "This is a sample text with some short words like 'a', 'is', and 'the'"
        expected = "sample text short word like"
        cleaned_text = self.cleaner.clean(text)
        self.assertEqual(cleaned_text, expected)

    def test_remove_punctuation(self):
        text = "This, is. a sample! text?"
        expected = "sample text"
        cleaned_text = self.cleaner.clean(text)
        self.assertEqual(cleaned_text, expected)

    def test_numbers_in_text(self):
        text = "This is a sample text with numbers 123 and 456"
        expected = "sample text number 123 456"
        cleaned_text = self.cleaner.clean(text)
        self.assertEqual(cleaned_text, expected)

    def test_special_characters(self):
        text = "Text with special characters: @#&$%"
        expected = "text special character"
        cleaned_text = self.cleaner.clean(text)
        self.assertEqual(cleaned_text, expected)

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

    def test_empty_string(self):
        text = ""
        expected = ""
        cleaned_text = self.cleaner.clean(text)
        self.assertEqual(cleaned_text, expected)

if __name__ == '__main__':
    unittest.main()
