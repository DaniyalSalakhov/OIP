from os import listdir
from bs4 import BeautifulSoup
from os.path import isfile, join
import pymorphy2
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

morph = pymorphy2.MorphAnalyzer()
nltk.download('stopwords')
nltk.download('punkt')

# Загрузка списка стоп-слов
stop_words = set(stopwords.words('russian'))

# Очистка токена от непечатаемых символов и спецсимволов
def clean_token(token):
    return re.sub("[^а-яА-ЯёЁ-]", '', token)

# Получение преобразованных токенов из текста

def get_clean_tokens(text):

  # Токенизация текста
  tokens = word_tokenize(text)

  # Очистка токенов и фильтрация
  cleaned_tokens = [clean_token(token.lower()) for token in tokens]
  cleaned_tokens = [token for token in cleaned_tokens if token not in stop_words and len(token) > 1]

  return set(cleaned_tokens)

def create_inverted_index_file():
  lemmas_file = open('content/lemmas.txt')
  indices = {}
  for line in lemmas_file:
    lemma = line.split(' ')[0]
    indices[lemma] = []

  filenames = listdir('content/downloaded_pages/')
  filenames.sort(key=lambda x: int(x.replace('.html', '')))

  # Получаем текст со всех html

  texts = [BeautifulSoup(open('content/downloaded_pages/' + f).read(), 'html.parser').get_text().lower() for f in filenames if isfile(join('content/downloaded_pages/', f))]

  # Просчитываем, какая лемма находится в каком документе

  for i, text in enumerate(texts):
    tokens = get_clean_tokens(text)
    for token in tokens:
      normal_form = morph.parse(token)[0].normal_form
      if normal_form in indices:
        indices[normal_form].append(i)

  # Запись инвертированного индекса в файл

  with open('content/inverted_index.txt', 'w') as inverted_index_file:
    for i in indices:
      inverted_index_file.write(i + ': ' + ' '.join(set(map(lambda file_number: str(file_number), indices[i]))) + '\n')


create_inverted_index_file()
# Окончили создавать инвертированный индекс



# Создание булева поиска по инвертированному индексу с операторами AND, OR, NOT

def boolean_search (operation):

  # Считываем файл inverted_index.txt

  inverted_indices = {}
  inverted_index_file = open('content/inverted_index.txt')
  for index in inverted_index_file.read().splitlines():
    items = index.split(': ')
    inverted_indices[items[0]] = items[1].split()

  parts = operation.split()

  normal_form = morph.parse(parts[0])[0].normal_form

  # Смотрим пересечения по операторам и выводим результат

  if normal_form in inverted_indices:
    print(inverted_indices[normal_form])
    result = set(inverted_indices[normal_form])
  else:
    result = set

  for i in range(2, len(parts), 2):
    normal_form = morph.parse(parts[i])[0].normal_form
    if normal_form in inverted_indices:
      if parts[i - 1] == 'and':
        result = result.intersection(inverted_indices[normal_form])
      else:
        result = result.union(inverted_indices[normal_form])

  print(result)

while True:
  operation = input('Write operation:\n')
  operation.lower()
  if operation == 'exit':
    break
  boolean_search(operation)