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

    def __init__(self, text):
        self.text = text
        self.meanings = []
        
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

class MongoDbProxy:
    """Proxy for MongoDB"""
    
    def __init__(self, url, dbName, tableName):
        self.client = MongoClient(url)
        self.db = self.client[dbName]
        self.table = tableName
        
    def get_db(self):
        return self.db
        
    def add_phrase(self, record):
        self.db[self.table].insert(record)

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

db = MongoDbProxy("mongodb://localhost:27017/", "RepeatItDb", "phrases")

mydb = db.get_db()
translator = GlosbeTranslator()
decision = 1

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
        word = input("translate: ")
        
        phrase = translator.translate(word)
        print(phrase)
        
        chosen_meaning_idx = int(input("Which meaning do you want to add to db? [0-%d] " % (len(phrase.meanings)-1)))
        eng = word
        pl = phrase.meanings[chosen_meaning_idx]
        
        if eng != "" and pl != "":
            print(eng, "means", pl)
            
            if record_exists(mydb, "phrases", eng):
                if input("Record already exists! Update? [y/n] ") == "y":
                    print("to be implemented")
                
            else:
                db.add_phrase([{ "english": eng, "polish" : pl}])
        else:
            print("data validation error")

    elif decision == "4":
        if "y" == input("Are you sure? [y/n] "):
            print("Dropping")
            mydb.phrases.drop()

    elif decision == "0":
        os.system("clear")
        break

