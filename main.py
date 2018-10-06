# coding: utf-8

# [] for list
# () for tuple
# {} for dictionary

#standard modules
import os

#my modules
from controller import Controller

from views import MainMenuView, ShowWordView, EditWordView, NewWordView
from translator import GlosbeTranslator
from phrase import Phrase
from model import Model



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

app = Controller({"main_menu" : MainMenuView(), 
                  "show_words": ShowWordView(),
                  "edit_word": EditWordView(),
                  "new_word": NewWordView()},
                  dictionary,
                  translator)
app.run()
#currentView.root.mainloop()
