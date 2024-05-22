import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


class TextCleaner:
    @staticmethod
    def clean_text(text, tokenize=True):
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(text)

        filtered_words = [word for word in word_tokens if word not in stop_words]
        lemmatizer = WordNetLemmatizer()
        cleaned_text = ' '.join([lemmatizer.lemmatize(word) for word in filtered_words])
        return cleaned_text

