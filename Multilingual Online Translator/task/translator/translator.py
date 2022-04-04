import requests
from bs4 import BeautifulSoup
import argparse


arr_languages = ["Arabic", "German", "English", "Spanish", "French", "Hebrew", "Japanese", "Dutch", "Polish",
    "Portuguese",
    "Romanian",
    "Russian",
    "Turkish"]

headers = {'User-Agent': 'Mozilla/5.0'}

parser = argparse.ArgumentParser()
parser.add_argument("lang_from")
parser.add_argument("lang_to")
parser.add_argument("word")
args = parser.parse_args()


lang_from = args.lang_from
lang_to = args.lang_to
word = args.word


soup = None


def save_to_file(word: str, text: str) -> str:
    with open(f"{word}.txt", "a") as file:
        file.write(text)
    return text


def strip_file(word):
    file_text = ""
    with open(f"{word}.txt", "r", encoding="utf-8") as file:
        file_text = file.read().strip()

    with open(f"{word}.txt", "w", encoding="utf-8") as file:
        file.write(file_text)


def translated_words() -> list:
    arr_words = []
    words_html = soup.find_all("a", {"class": ["rtl", "ltr"]})
    for a in words_html:
        arr_words.append(a.text.strip())

    return arr_words


def translated_phrases() -> list:
    arr_phrases = []
    words_html = soup.find_all("div", {"class": ["src", "trg"]})
    for a in words_html:
        arr_phrases.append(a.text.strip())

    return arr_phrases


def show_text(lang: str):
    global soup
    translation_text = f"{lang} Translations:"

    examples_text = f"{lang} Examples:"
    headers = {'User-Agent': 'Mozilla/5.0'}

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')

    if not r.ok:
        print(save_to_file(word, 'Something wrong with your internet connection'), end="")
        return

    if lang_from.title() not in arr_languages:
        print(save_to_file(word, f"Sorry, the program doesn't support {lang_from}"), end="")
        exit(-1)

    if lang_to.title() not in arr_languages and lang_to != "all":
        print(save_to_file(word, f"Sorry, the program doesn't support {lang_to}"), end="")
        exit(-1)

    arr_words = translated_words()
    if len(arr_words) < 1:
        print(save_to_file(word, f'Sorry, unable to find {word}'), end="")
        return

    print(save_to_file(word, translation_text + "\n"), end="")
    for i in arr_words:
        print(save_to_file(word, i + "\n"), end="")

    print(save_to_file(word, examples_text + "\n"), end="")
    arr_pha = translated_phrases()
    for i in arr_pha:
        print(save_to_file(word, i + "\n"), end="")


if lang_to == "all":
    for lang in arr_languages:
        if lang == lang_from:
            continue
        url = f"https://context.reverso.net/translation/{lang_from.lower()}-{lang.lower()}/{word}"
        show_text(lang)
else:
    url = f"https://context.reverso.net/translation/{lang_from.lower()}-{lang_to.lower()}/{word}"
    show_text(lang_to)

strip_file(word)
