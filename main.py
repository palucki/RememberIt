# coding: utf-8

# [] for list
# () for tuple
# {} for dictionary

import os
import random
from pymongo import MongoClient
import requests


class EnglishPhrase:
    """Class representing single entry in dictionary"""
    text = ""
    meanings = []

    def __init__(self, text):
        self.text = text
        
    def __str__(self):
        output = "Word: " + self.text + "\n";
        for idx, meaning in enumerate(self.meanings):
            output += "%3d. %s\n" % (idx, meaning)
            
        return output
        
    def show(self):        
        print("Word:", self.text)
        print("Meanings:")        
        for idx, meaning in enumerate(self.meanings):
            print("%3d. %s" % (idx, meaning))
            
    def add_meaning(self, phrase):
        self.meanings.append(phrase)

class GlosbeTranslator:
    """Client class of Glosbe translator API"""
    base_url = "https://glosbe.com/gapi/translate"
    payload = {'from': 'eng', 'dest': 'pol', "format" : "json", "phrase" : "", "pretty" : "true"}
    
    def translate(self, word):
        self.payload["phrase"] = word
        raw_resp = requests.get(self.base_url, params=self.payload)
        #print (raw_resp.text)
        resp = raw_resp.json()

        if resp["result"] == "ok":
            print("Successfully translated")
            
            phrase = EnglishPhrase(word)
            contents = resp["tuc"]
            
            for entry in contents:
                if "phrase" in entry and "text" in entry["phrase"]:
                    meaning = entry["phrase"]["text"]
                    #print(meaning)
                    phrase.add_meaning(meaning)

            return phrase
        else:
            print("Request failed!!!")

def init_db():
    client = MongoClient('mongodb://localhost:27017/')
    mydb = client.myFirstMB
    return mydb

def add_to_db(db, table, record):
    db[table].insert(record)

def iterate_over_db(db, table):
    for i, phrase in enumerate(db[table].find()):
        print("%d. eng: \'%s\' pol: \'%s\'" % (i, phrase["english"], phrase["polish"]))

def get_rendom_entry(db, table):
    entries = db[table].find()
    count = entries.count()
    print(entries[random.randrange(count)])

def record_exists(db, table, eng):
    if db[table].find_one({"english" : eng}):
        return True
    else:
        return False




mydb = init_db()
decision = 1
word = "speaker"
translator = GlosbeTranslator()
phrase = translator.translate(word)

while True:
    os.system("clear")
    print("""\
*************************************
*                                   *
*   1. Browse the whole dictionary  *
*   2. Show random word             *
*   3. Add phrase to dictionary     *
*   4. Clear dictionary             *
*   0. Exit                         *
*                                   *
*************************************
""")
    decision = input(">> ")

    if decision == "1":
        iterate_over_db(mydb, "phrases")
        input()
        
    elif decision == "2":
        get_rendom_entry(mydb, "phrases")
        input()
        
    elif decision == "3":
        eng = input("english:")
        pl = input("polish: ")

        if eng != "" and pl != "":
            print(eng, "means", pl)
            
            if record_exists(mydb, "phrases", eng):
                if input("Record already exists! Update? [y/n] ") == "y":
                    print("to be implemented")
                
            else:
                print("adding to database...")
                add_to_db(mydb, "phrases", [{
                                            "english": eng,
                                            "polish" : pl
                                            }])
                print("...added successfully")
        else:
            print("data validation error")

    elif decision == "4":
        if "y" == input("Are you sure? [y/n] "):
            print("Dropping")
            mydb.phrases.drop()

    elif decision == "0":
        os.system("clear")
        break

