import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Downloading necessary data sets from NLTK
nltk.download('stopwords')
nltk.download('wordnet')


class TextCleaner:
    """
    TextCleaner is a class for performing text cleaning operations such as removing stopwords,
    punctuation, and lemmatizing words.

    Attributes:
        remove_stopwords (bool): Indicates whether to remove stopwords.
        lemmatize (bool): Indicates whether to lemmatize words.
        stopwords (set): A set of stopwords to remove.
        lemmatizer (WordNetLemmatizer): An instance of WordNetLemmatizer for lemmatizing words.

    Methods:
        clean(text):
            Cleans the input text by performing the specified operations.
    """

    def __init__(self, remove_stopwords=True, lemmatize=True):
        self.remove_stopwords = remove_stopwords
        self.lemmatize = lemmatize
        self.stopwords = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()

    def clean(self, text):
        # Convert text to lowercase
        text = text.lower()

        # Remove punctuation
        text = re.sub(r'[^\w\s]', '', text)

        # Remove one or two-letter words
        text = re.sub(r'\b\w{1,2}\b', '', text)

        # Split text into words
        words = text.split()

        # Remove stopwords
        if self.remove_stopwords:
            words = [word for word in words if word not in self.stopwords]

        # Lemmatize words
        if self.lemmatize:
            words = [self.lemmatizer.lemmatize(word) for word in words]

        # Return the cleaned words as a joined string
        return ' '.join(words)
