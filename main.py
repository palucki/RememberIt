# coding: utf-8

# [] for list
# () for tuple
# {} for dictionary

import os
import random
from pymongo import MongoClient
import requests
import tkinter
from tkinter import ttk

class Phrase:
    """Class representing single entry in model (database)"""

    def __init__(self, eng, lang, meanings):
        self.eng = eng
        self.lang = lang
        self.meanings = meanings

    def __str__(self):
        output = "Word: " + self.eng + "in " + lang + "\n";
        for idx, meaning in enumerate(self.meanings):
            output += "%3d. %s\n" % (idx, meaning)
            
        return output

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

class Observable:
    def __init__(self, initial={}):
        self.data = initial
        self.callbacks = {}
        
    def addCallback(self, func):
        self.callbacks[func] = 1;
        
    def delCallback(self, func):
        del self.callbacks[func];

    def doCallbacks(self):
        for func in self.callbacks:
            func(self.data)
            
    def setData(self, data):
        self.data = data
        self.doCallbacks()
        
    def getData(self):
        return self.data



class Model:
    """That needs a table of pairs - eng and its meanings"""
    def __init__(self):
        self.phrases = Observable({})
        self.db = MongoDbProxy("mongodb://localhost:27017/", "RepeatItDb", "phrases")
        
        data = self.db.get_all()
        self.phrases.setData(data)
        
        #for key in db_phrases.keys():            
            #self.addWord(Phrase(key, "polish", db_phrases[key]))
            
        #fetch all the data and save it in self.phrases then
        
    def addWord(self, key, lang, meanings):
        newData = self.phrases.getData()
        newData[key] = meanings
        self.phrases.setData(newData)
    
    def getAllWords(self):
        return self.phrases.getData()
    
    def removeWord(self, phrase):
        print("Model::removeWord TO BE IMPLEMENTED")

#create concrete Observable (Words or similiar)
#add callback to view
        
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
        #define your data struct here
        words = {}
        for i, phrase in enumerate(self.db[self.table].find()):
            eng = phrase["english"]
            lang = phrase["lang"]
            meanings = phrase[lang]
            
            words[eng] = meanings

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


dictionary = Model()
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

class BaseView:
    """Base class for all screens"""
    def __init__(self):
        print("Base ctor")
        
    def set_actions(self, actions):
        print("setting actions")
        self.actions = actions

class MainMenuView(BaseView):
    """Main menu"""
    def __init__(self):
        BaseView.__init__(self)
        print("MainMenu ctor")
     
    def build_into(self, frame):
        self.mainLabel = tkinter.Label(frame, 
                                       text="Repeat It - learn new english words easily & efficently",
                                       bg="#339999")
        self.buttons = []

        for (label, cmd) in self.actions:
            self.buttons.append(tkinter.Button(frame, 
                                text=label, 
                                fg="black",
                                bg="#33996E",
                                command=cmd))

    def show(self):
        self.mainLabel.pack(fill=tkinter.X, ipady=20, padx=10)
        for but in self.buttons:
            but.pack(fill=tkinter.X, pady=10, padx=50)
            
    def hide(self):
        self.mainLabel.pack_forget()
        for but in self.buttons:
            but.pack_forget()
        
class ShowWordView(BaseView):
    """Showing words menu"""
    def __init__(self):
        BaseView.__init__(self)
        print("Show Words ctor")
    
    def build_into(self, frame):    
        self.mainLabel = tkinter.Label(frame, text="Browse dictionary")
        
        self.strvariable = tkinter.StringVar()
        
        self.combo = ttk.Combobox(frame, textvariable=self.strvariable)
        self.combo["values"] = ()
        self.combo["state"] = 'readonly'
        self.combo.bind('<<ComboboxSelected>>', self.updateCurrenttlyDisplayed)
        
        self.means_label = tkinter.Label(frame, text="means")
        self.meaning = tkinter.Label(frame, text="")
        
        self.buttons = []

        for (label, cmd) in self.actions:
            self.buttons.append(tkinter.Button(frame, 
                                text=label, 
                                fg="black",
                                command=cmd))

    def updateCurrenttlyDisplayed(self, event):
        #print (self.strvariable)
        self.meaning["text"] = self.words[self.combo["values"][self.combo.current()]]

    def set_words(self, words):
        self.words = words

    def show(self):
        self.mainLabel.pack(fill=tkinter.X, ipady=20, padx=10)
        self.combo.pack(fill = tkinter.X)
        
        self.means_label.pack(fill=tkinter.X, ipady=20, padx=10)
        self.meaning.pack(fill=tkinter.X, ipady=20, padx=10)
        
        #It should be somewhere else
        self.combo["values"] = ()
        for key in self.words.keys():
            self.combo["values"] = self.combo["values"] + (key, )
        
        if len(self.combo["values"]) > 0:
            self.combo.current(0)
            
        self.updateCurrenttlyDisplayed(None)
        
        for but in self.buttons:
            but.pack(fill=tkinter.X, pady=10, padx=50)
            
    def hide(self):
        self.mainLabel.pack_forget()
        self.combo.pack_forget()
        self.means_label.pack_forget()
        self.meaning.pack_forget()
        for but in self.buttons:
            but.pack_forget()

class Controller:
    """Controler responsible for interactions between data and views"""
    def __init__(self, views, model):
        self.root = tkinter.Tk()
        self.root.configure(background="#339999")
        self.init_root()
    
        self.model = model
        self.model.phrases.addCallback(self.updateWords)
        
        self.views = views

        for name in self.views.keys():
            self.views[name].set_actions(self.get_actions_for(name))
            self.views[name].build_into(self.frame)
        
        self.currentView = self.views["main_menu"]
        self.currentView.show()
    
    def init_root(self):
        self.root.title("Repeat It")
        self.root.geometry("350x300")
        self.frame = tkinter.Frame(self.root)
        self.frame.configure(background='#339999') 
        self.frame.pack()
        
    def get_actions_for(self, view_name):
        if view_name == "main_menu":
            return self.get_main_menu_actions()
        elif view_name == "show_words":
            return self.get_words_actions()
        else:
            print("No actions found")
            exit(1)

    def get_main_menu_actions(self):
        return  [("Browse words", self.show_words),
                  ("add word", self.addWord),
                 #("Translate phrase", lambda: translator.translate("error")),
                  ("Quit", self.root.destroy)
                 ##("Add phrase to dictionary",
                  ##("Clear dictionary",
                ]

    def get_words_actions(self):
        return [("Go back", self.show_main),
                ("Quit", self.root.destroy)]
        
    def show_words(self):
        self.currentView.hide()
        self.currentView = self.views["show_words"]
        
        #add observer or something similiar. Now do it here
        self.currentView.set_words(self.model.getAllWords())
        
        
        
        self.currentView.show()
        
    def updateWords(self, data):
        print("will update words database")    
        self.views["show_words"].set_words(self.model.getAllWords())
        
    def addWord(self):
        print("will add word: bee to model")
        self.model.addWord("bee", "polish", "pszczoła")
        
    def show_main(self):
        self.currentView.hide()
        self.currentView = self.views["main_menu"]
        self.currentView.show()
        
    def run(self):
        self.root.mainloop() 


app = Controller({"main_menu" : MainMenuView(), 
                  "show_words": ShowWordView()},
                  dictionary)
app.run()
#currentView.root.mainloop()
