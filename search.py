import requests
from bs4 import BeautifulSoup
import os


def crawl_pikabu(start_url, max_urls=100):
  visited_urls = set()
  urls_to_visit = [start_url]
  count_url = 0
  i = 0

  with open('index.txt', 'w', encoding='utf-8') as index_file:
    while i <= max_urls:
      current_url = urls_to_visit.pop(0)
      print(f"{count_url + 1} - Посещение {current_url}")

      response = requests.get(current_url)
      if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        visited_urls.add(current_url)
        count_url += 1

        # Сбор ссылок со страницы
        links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('https://pikabu.ru')]

        # Добавление новых ссылок в список для посещения
        for link in links:
          if link not in visited_urls and link not in urls_to_visit:
            urls_to_visit.append(link)

        if 'story' in current_url and ('#comments' and '?cid=') not in current_url:
          i += 1

          # Сохранение HTML-данных в файл
          filename = f"downloaded_pages/page_{i}.html"
          with open(filename, 'w', encoding='utf-8') as file:
            file.write(response.text)

          # Запись собранных ссылок в файл downloaded_pages
          index_file.write(f"{current_url}\n")

  print("Выполнено.")


# Начальная страница для поиска ссылок
start_url = "https://pikabu.ru/"

# Запуск паука
crawl_pikabu(start_url, max_urls=100)