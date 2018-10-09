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


dictionary = Model()
translator = GlosbeTranslator()

app = Controller({"main_menu" : MainMenuView(), 
                  "show_words": ShowWordView(),
                  "edit_word": EditWordView(),
                  "new_word": NewWordView()},
                  dictionary,
                  translator)
app.run()
