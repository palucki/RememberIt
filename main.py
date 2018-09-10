# coding: utf-8

# [] for list
# () for tuple
# {} for dictionary

import os
import random
from pymongo import MongoClient

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
#mydb.phrases.drop()

#add_to_db(mydb, "phrases", record1)
#add_to_db(mydb, "phrases", record2)

#iterate_over_db(mydb, "phrases")

#one_found = mydb.phrases.find_one({"english" : "delve into"})
#all_found = mydb.phrases.find({"english" : "delve into"})

#print(one_found["polish"])

#print("Found %d result(s)" % all_found.count())

#for one in all_found:
    #print(one)

class Phrase:
    """Class representing single entry in dictionary"""
    english = ""
    polish = ""

    def __init__(self, eng, pl):
        self.english = eng
        self.polish = pl

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




import requests

def translate_phrase(phrase, src, dst):
    translated = "nothing"

    return translated

#https://glosbe.com/gapi/translate?from=pol&dest=eng&format=json&phrase=witaj&pretty=true

#print ("translating...", translate_phrase("coś", "pol", "eng"))

payload = {'from': 'eng', 'dest': 'pol', "format" : "json", "phrase" : "speaker", "pretty" : "true"}
resp = requests.get('https://glosbe.com/gapi/translate', params=payload).json()

if resp["result"] == "ok":
    print("Success")
    contents = resp["tuc"]
    print(contents)
   
    translation = contents["phrase"]["text"]
    meaning_from = contents["meanings"][0]["text"]
    meaning_dest = contents["meanings"][1]["text"]
   
    print("\n",translation)
    print("\n",meaning_from)
    print("\n",meaning_dest)


   
   
   
    # meanings = resp["tuc"]
    # print("samochód", "means", meanings[0]["text"])
   
   
# print(r.url)
# print(r.text)
# print(r.json())

# if r.text["result"] == "ok":

    # print(r.text)
#r = requests.get("https://glosbe.com/gapi/translate?from=pol&dest=eng&format=json&phrase=witaj&pretty=true")
#print("received response")

