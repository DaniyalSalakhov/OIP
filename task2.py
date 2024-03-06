from bs4 import BeautifulSoup
import re
import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pymorphy2
import nltk

nltk.download('stopwords')
nltk.download('punkt')

# Очистка токена от непечатаемых символов и спецсимволов
def clean_token(token):
    return re.sub("[^а-яА-ЯёЁ-]", '', token)

# Загрузка списка стоп-слов
stop_words = set(stopwords.words('russian'))

def get_clean_tokens(file_path, stop_words):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        # Извлечение текста из HTML
        text = soup.get_text()

        # Токенизация текста
        tokens = word_tokenize(text)

        # Очистка токенов и фильтрация
        cleaned_tokens = [clean_token(token.lower()) for token in tokens]
        cleaned_tokens = [token for token in cleaned_tokens if token not in stop_words and len(token) > 1]

        return cleaned_tokens

def get_tokens(directory, stop_words):
    # Получение списка файлов в директории
    html_files = [file for file in os.listdir(directory) if file.endswith('.html')]
    all_tokens = []
    for file_name in html_files:
        file_path = os.path.join(directory, file_name)
        tokens = get_clean_tokens(file_path, stop_words)
        all_tokens.extend(tokens)
    return set(all_tokens)  # Удаление дубликатов

tokens = get_tokens('content/downloaded_pages', stop_words)
with open('content/tokens.txt', 'w') as token_file:
  for token in tokens:
    token_file.write(token +'\n')


# Создание объекта для морфологического анализа
morph = pymorphy2.MorphAnalyzer

def group_tokens_by_lemmas(tokens):
    morph = pymorphy2.MorphAnalyzer()
    lemmas = {}
    for token in tokens:
        # Лемматизация каждого токена
        lemma = morph.parse(token)[0].normal_form
        # Группировка токенов по леммам
        if lemma not in lemmas:
            lemmas[lemma] = []
        lemmas[lemma].append(token)
    return lemmas

def read_tokens_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        tokens = file.read().split()
    return tokens

tokens = read_tokens_from_file('content/tokens.txt')
grouped_tokens = group_tokens_by_lemmas(tokens)
with open('content/lemmas.txt', 'w') as lemma_file:
  for lemma, token_list in grouped_tokens.items():
    lemma_file.write(lemma + ' ' + ' '.join(token_list) + '\n')
