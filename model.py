import random
from pymongo import MongoClient

from observable import Observable

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

class Model:
    """That needs a table of pairs - eng and its meanings"""
    def __init__(self):
        self.phrases = Observable({})
        self.db = MongoDbProxy("mongodb://localhost:27017/", "RepeatItDb", "phrases")
        
        data = self.db.get_all()
        self.phrases.setData(data)
        
    def addWord(self, key, lang, meanings):
        newData = self.phrases.getData()
        newData[key] = meanings
        self.phrases.setData(newData)
    
    def getAllWords(self):
        return self.phrases.getData()
    
    def removeWord(self, key):
        newData = self.phrases.getData()
        newData.pop(key)
        self.phrases.setData(newData)
        
    def saveWord(self, wordAndMeaning):
        word = wordAndMeaning[0]
        meaning = wordAndMeaning[1]
        self.addWord(word, "pl", meaning)
        
    def saveDb(self):
        dbData = self.db.get_all()
        modelData = self.getAllWords()
        
        # we need to replace "meanings" (list) with single meaning.
        # to avoid "unhashable type list" error 
        
        print(set(dbData.keys()))
        print(set(modelData.keys()))
        set(dbData.values())
        set(modelData.values())
