from bs4 import BeautifulSoup
import requests
from random import choice
from pyfiglet import Figlet
import requests
import os
import sqlite3

list_of_words = []


def get_words(words):
    global list_of_words
    with sqlite3.connect("korean.db") as connection:
        c = connection.cursor()
        c.execute("Select * from words;")
        list_of_words = c.fetchall()

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
    i = 1
    for word in data:
        meaning = word.find("li").get_text()
        print(str(i)+". "+meaning+"\n")
        i += 1


def get_list_of_words(list_of_words):

    url = "https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/Korean_5800"
    res = requests.get(url)
    res.encoding = "utf-8"

    soup = BeautifulSoup(res.text, features="html.parser")
    list_of_e = soup.select(".Kore")
    list_of_words = []

    for li in list_of_e:
        word = {
            "word": li.find("a")["title"],
            "href": li.find("a")["href"]
        }
        if (word["word"].find("(page does not exist)")) == -1:
            list_of_words.append(word)


try:
    get_words(list_of_words)
except:
    print("Excpetion while fetching from db, getting from other source!")
    get_list_of_words(list_of_words)
f = Figlet(width=100)

print(f.renderText("Korean 5000 Frequency Words"))


while True:
    word = choice(list_of_words)
    if type(word) == "dict":

        print(f"Here is one word: {word['word']}")
        get_info(word["href"])
    else:
        print(f"Here is one word: {word[0]}")
        get_info(word[1])
    next = input("Press enter to continue, anything else to exit: ")
    if next.lower() == "":
        os.system("cls")
        continue
    else:
        break
