# coding: utf-8

# [] for list
# () for tuple
# {} for dictionary

import os
import random
from pymongo import MongoClient
import requests
import tkinter

class SimpleEnglishPhrase:
    """Class representing single entry in user database"""

    def __init__(self, eng, pol):
        self.eng = eng
        self.pol = pol


class EnglishPhrase:
    """Class representing single entry from Glosbe"""

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
        self.count = self.db[self.table].find().count()
        
    def get_db(self):
        return self.db
        
    def add_phrase(self, record):
        self.db[self.table].insert(record)
        self.count = self.db[self.table].find().count()
        
    def show_one(self, phrase):
        print("eng: \'%s\' pol: \'%s\'" % (phrase["english"], phrase["polish"]))
        
    def get_all(self):
        words = []
        for i, phrase in enumerate(self.db[self.table].find()):
            words.append(phrase)
        return words
            
    def show_all(self):
        if self.count > 0:
            for i, phrase in enumerate(self.db[self.table].find()):
                print(i, end=" ")
                self.show_one(phrase)
        else:
            print("Database is empty")

    def show_random(self):
        entries = self.db[self.table].find()
        self.count = entries.count()
        if self.count > 0:
            self.show_one(entries[random.randrange(self.count)])
        else:
            print("Database is empty")
        
    def record_exists(self, eng):
        if self.db[self.table].find_one({"english" : eng}):
            return True
        else:
            return False
            
    def drop_db(self):
        print("Dropping")
        self.db.self.table.drop()
        self.count = self.db[self.table].find().count()



mainBanner = """\
*************************************
*                                   *
*   1. Browse the whole dictionary  *
*   2. Show random word             *
*   3. Translate phrase             *
*   4. Add phrase to dictionary     *
*   5. Clear dictionary             *
*   0. Exit                         *
*                                   *
*************************************\
"""

db = MongoDbProxy("mongodb://localhost:27017/", "RepeatItDb", "phrases")

translator = GlosbeTranslator()
#decision = 1

#while True:
    #os.system("clear")
    #print(mainBanner)
    #decision = input(">> ")

    #if decision == "1":
        #db.show_all()
        #input()
        
    #elif decision == "2":
        #db.show_random()
        #input()
    
    #elif decision == "3":
        #word = input("translate: ")
        #phrase = translator.translate(word)
        #print(phrase)
        #input()
    
    #elif decision == "4":
        #word = input("translate: ")
        
        #phrase = translator.translate(word)
        #print(phrase)
        
        #chosen_meaning_idx = int(input("Which meaning do you want to add to db? [0-%d] " % (len(phrase.meanings)-1)))
        #eng = word
        #pl = phrase.meanings[chosen_meaning_idx]
        
        #if eng != "" and pl != "":           
            #if db.record_exists(eng):
                #if input("Record already exists! Update? [y/n] ") == "y":
                    #print("to be implemented")
                
            #else:
                #db.add_phrase([{ "english": eng, "polish" : pl}])
        #else:
            #print("data validation error")

    #elif decision == "4":
        #if "y" == input("Are you sure? [y/n] "):
            #print("Dropping")
            #mydb.phrases.drop()

    #elif decision == "0":
        #os.system("clear")
        #break

#exit(1)

class AppWindow():

    def __init__(self, db):
        self.db = db;
        self.root = tkinter.Tk()
        self.root.title("Repeat It")
        self.root.geometry("350x300")
        self.frame = tkinter.Frame(self.root)
        self.frame.pack()

        self.mainLabel = tkinter.Label(self.frame, text="Repeat It - learn new english words easily & efficently")
        self.mainLabel.pack(fill=tkinter.X, ipady=20, padx=10)

        self.actions = [("Browse the whole dictionary", self.show_all),
                        ("Show random word", db.show_random),
                        ("Translate phrase", lambda: translator.translate("error")),
                        ##("Add phrase to dictionary",
                        ##("Clear dictionary",
                        ("Quit", lambda : quit())
                       ]

        self.buttons = []

        for (label, cmd) in self.actions:
            self.buttons.append(tkinter.Button(self.frame, 
                                text=label, 
                                fg="black",
                                command=cmd))

        self.show_main()

    def show_main(self):
        self.mainLabel.pack(fill=tkinter.X, pady=10, padx=10)
        for but in self.buttons:
            but.pack(fill=tkinter.X, pady=10, padx=50)
    
    def show_all(self):
        #Update view
        for but in self.buttons:
            but.pack_forget()
        
        #get data from db
        phrases = self.db.get_all()
        for i, phrase in enumerate(phrases):
            
            
            
            print("eng: \'%s\' pol: \'%s\'" % (phrase["english"], phrase["polish"]))
    
    def run(self):
        self.root.mainloop()

app = AppWindow(db)
app.run()

