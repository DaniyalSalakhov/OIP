from bs4 import BeautifulSoup
import nltk
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
import re
import pandas as pd
from os import listdir
from os.path import isfile, join
from pymystem3 import Mystem
from sklearn.feature_extraction.text import TfidfVectorizer


pages = 'content/downloaded_pages/'

filenames = listdir(pages)
filenames.sort(key=lambda x: int(x.replace('.html', '')))

texts = [BeautifulSoup(open(pages + f).read(), 'html.parser').get_text().lower() for f in filenames if isfile(join(pages, f))]

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

stopwords_ru = stopwords.words("russian")
stopwords_en = stopwords.words("english")
stopwords_all = stopwords_en + stopwords_ru

tokens = open('content/tokens.txt').read().splitlines()
lemmas = [word.split(' ')[0] for word in open('content/lemmas.txt').read().splitlines()]

lemmatizer_en = WordNetLemmatizer()
lemmatizer_ru = Mystem()

lemmas_tokens = "content/lemmas_tokens/"


def get_tokens(text: str):
    text_tokens = nltk.word_tokenize(text)
    almost_clean_tokens = set([w for w in text_tokens if not re.search(r"[^a-zA-Zа-яА-ЯёЁ]", w)])
    clean_tokens = [w for w in almost_clean_tokens if w not in stopwords_all and len(w) > 1]
    return clean_tokens


def get_lemmas(text: str):
    text_tokens = get_tokens(text)
    text_lemmas = []
    for token in text_tokens:
        if re.search(r"[a-zA-Z]", token):
            lemma = lemmatizer_en.lemmatize(token)
        else:
            lemma = lemmatizer_ru.lemmatize(token)[0]
        text_lemmas.append(lemma)
    return text_lemmas


tokens_vectorizer = TfidfVectorizer(analyzer=get_tokens, vocabulary=tokens)
lemmas_vectorizer = TfidfVectorizer(analyzer=get_lemmas, vocabulary=lemmas)

tokens_matrix = tokens_vectorizer.fit_transform(texts)
lemmas_matrix = lemmas_vectorizer.fit_transform(texts)

tokens_idf = pd.DataFrame(tokens_vectorizer.idf_, index=tokens, columns=["idf"])
lemmas_idf = pd.DataFrame(lemmas_vectorizer.idf_, index=lemmas, columns=["idf"])

for i in range(100):
    tokens_tfidf = pd.DataFrame(tokens_matrix[i].T.todense(), index=tokens, columns=["tf-idf"])
    lemmas_tfidf = pd.DataFrame(lemmas_matrix[i].T.todense(), index=lemmas, columns=["tf-idf"])

    tokens_result_df = pd.concat([tokens_idf, tokens_tfidf], axis=1)
    lemmas_result_df = pd.concat([lemmas_idf, lemmas_tfidf], axis=1)

    tokens_file = open(f"{lemmas_tokens}tokens{i + 1}.txt", "w")
    lemmas_file = open(f"{lemmas_tokens}lemmas{i + 1}.txt", "w")

    tokens_file.write(tokens_result_df.to_csv(sep=" ", header=False))
    lemmas_file.write(lemmas_result_df.to_csv(sep=" ", header=False))

    tokens_file.close()
    lemmas_file.close()