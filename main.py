from bs4 import BeautifulSoup
import requests
from random import choice
from pyfiglet import Figlet
import requests
import os
import sqlite3

url = "https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/Korean_5800"
res = requests.get(url)
res.encoding = "utf-8"


soup = BeautifulSoup(res.text, features="html.parser")
list_of_e = soup.select(".Kore")
list_of_words = []


def get_words(words):
    global list_of_words
    with sqlite3.connect("korean.db") as connection:
        c = connection.cursor()
        c.execute("Select * from words;")
        list_of_words = c.fetchall()
        print(type(list_of_words))
        # c.execute("Create table words(word TEXT, href TEXT)")

        # for word in words:
        #     c.execute("INSERT INTO words values (?,?);",
        #               (word["word"], word["href"]))
        # connection.commit()


def get_info(href):
    url = "https://en.wiktionary.org"+href
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    latin = soup.select(".manual-tr")[0].get_text()
    print(latin)
    data = soup.select("ol")  # returns a list
    for word in data:
        meaning = word.find("li").get_text()
        print(meaning+"\n")


for li in list_of_e:
    word = {
        "word": li.find("a")["title"],
        "href": li.find("a")["href"]
    }
    if (word["word"].find("(page does not exist)")) == -1:
        list_of_words.append(word)

f = Figlet(width=100)

print(f.renderText("Korean 5000 Frequency Words"))
get_words(list_of_words)
while True:
    word = choice(list_of_words)

    print(f"Here is one word: {word['word']}")
    get_info(word["href"])
    next = input("Press N for next, anything else to exit:")
    if next.lower() == "n":
        os.system("cls")
        continue
    else:
        break
