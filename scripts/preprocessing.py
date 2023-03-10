import re
import spacy
import string

from nltk.stem.snowball import SnowballStemmer

stopwordlist = ['a', 'about', 'above', 'after', 'again', 'ain', 'all', 'am', 'an',
                'and', 'any', 'are', 'as', 'at', 'be', 'because', 'been', 'before',
                'being', 'below', 'between', 'both', 'by', 'can', 'd', 'did', 'do',
                'does', 'doing', 'down', 'during', 'each', 'few', 'for', 'from',
                'further', 'had', 'has', 'have', 'having', 'he', 'her', 'here',
                'hers', 'herself', 'him', 'himself', 'his', 'how', 'i', 'if', 'in',
                'into', 'is', 'it', 'its', 'itself', 'just', 'll', 'm', 'ma',
                'me', 'more', 'most', 'my', 'myself', 'now', 'o', 'of', 'on', 'once',
                'only', 'or', 'other', 'our', 'ours', 'ourselves', 'out', 'own',
                're', 's', 'same', 'she', "shes", 'should', "shouldve", 'so', 'some', 'such',
                't', 'than', 'that', "thatll", 'the', 'their', 'theirs', 'them',
                'themselves', 'then', 'there', 'these', 'they', 'this', 'those',
                'through', 'to', 'too', 'under', 'until', 'up', 've', 'very', 'was',
                'we', 'were', 'what', 'when', 'where', 'which', 'while', 'who', 'whom',
                'why', 'will', 'with', 'won', 'y', 'you', "youd", "youll", "youre",
                "youve", 'your', 'yours', 'yourself', 'yourselves']


class preprocess:
    def __init__(self, text, auto=True):
        self.stemmed_tokens = None
        self.lemmatized_tokens = None
        self.text = text
        self.punct_list = string.punctuation
        self.nlp = spacy.load("en_core_web_sm")
        self.stemmer = SnowballStemmer("english")
        self.emoji_pattern = re.compile("["
                                        u"\U0001F600-\U0001F64F"  # emoticons
                                        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                        u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                        "]+", flags=re.UNICODE)

        if auto:
            self.set_lower()
            self.cleaning_URLs()
            self.cleaning_emojis()
            self.cleaning_numbers()
            # self.stopword_remover()
            self.clean_punct()
            self.remove_newline_char()
            self.redundant_spaces()
            # self.cleaning_repeating_char()
            self.tokenize_and_stem()
            self.lemmatize_tokens()

    def set_lower(self):
        self.text = self.text.lower()
        return self.text

    def stopword_remover(self):
        return " ".join([word for word in str(self.text).split() if word not in stopwordlist])

    def clean_punct(self):
        translator = str.maketrans('', '', self.punct_list)
        self.text = self.text.translate(translator)
        return self.text

    def cleaning_repeating_char(self):
        self.text = re.sub(r'(.)\1{2,}', r'\1', self.text)
        return self.text

    def cleaning_URLs(self):
        self.text = re.sub(r'http\S+', '', self.text, flags=re.MULTILINE)
        return self.text

    def cleaning_numbers(self):
        self.text = re.sub('[0-9]+', '', self.text)
        return self.text

    def cleaning_emojis(self):
        self.text = self.emoji_pattern.sub(r'', self.text)
        return self.text

    def redundant_spaces(self):
        self.text = re.sub(' +', ' ', self.text)
        return self.text

    def remove_newline_char(self):
        self.text = ''.join(self.text.splitlines())
        return self.text

    def tokenize_and_stem(self):
        doc = self.nlp(self.text)
        tokens = [token.text.lower() for token in doc if not token.is_stop and token.is_alpha]
        self.stemmed_tokens = [self.stemmer.stem(token) for token in tokens]
        return self.stemmed_tokens

    # Define a function to lemmatize text
    def lemmatize_tokens(self):
        doc = self.nlp(" ".join(self.stemmed_tokens))
        self.lemmatized_tokens = [token.lemma_ for token in doc]
        return self.lemmatized_tokens

    def get_result(self):
        return self.text

    def get_stemmed_tokens(self):
        return self.stemmed_tokens

    def get_lemmatized_tokens(self):
        return self.lemmatized_tokens
