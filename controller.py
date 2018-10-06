import tkinter

class Controller:
    """Controler responsible for interactions between data and views"""
    def __init__(self, views, model, translator):
        
        self.initializeRootWindow()
    
        self.model = model
        self.model.phrases.addCallback(self.updateWords)
        
        self.views = views
        self.translator = translator
        
        for name in self.views.keys():
            self.views[name].set_button_commands(self.get_actions_for(name))
            self.views[name].build_into(self.root)
        
        #add observer or something similiar. Now do it here
        self.views["show_words"].set_words(self.model.getAllWords())
        self.views["main_menu"].show()
    
    def initializeRootWindow(self):
        self.root = tkinter.Tk()
        self.root.configure(background="#339999")
        self.root.title("Repeat It")
        self.root.geometry("350x300")
        
        self.quit_button = tkinter.Button(self.root, 
                                          text="Quit", 
                                          fg="red",
                                          command=self.root.destroy)
        
        self.quit_button.pack(side=tkinter.BOTTOM, pady=10)
        
    def get_actions_for(self, view_name):
        if view_name == "main_menu":
            return self.get_main_menu_actions()
        elif view_name == "show_words":
            return self.get_words_actions()
        elif view_name == "edit_word":
            return self.getEditWordActions()
        elif view_name == "new_word":
            return self.getNewWordActions()
        else:
            print("No actions found")
            exit(1)

    def get_main_menu_actions(self):
        return  [("Browse words", lambda: (self.views["main_menu"].hide(), 
                                           self.views["show_words"].show()
                                           )),
                  ("Add new word", lambda: (self.views["main_menu"].hide(), 
                                            self.views["new_word"].show()
                                            )),
                 #("Translate phrase", lambda: translator.translate("error")),
                  #("Quit", self.root.destroy)
                 ##("Add phrase to dictionary",
                  ##("Clear dictionary",
                ]

    def get_words_actions(self):
        return [("Go back", lambda: (self.views["show_words"].hide(), self.views["main_menu"].show())),
                ("Delete word", lambda: self.removeWord(self.views["show_words"].getDisplayedWordAndMeaning())),
                ("Edit word", lambda: (self.views["show_words"].hide(), self.views["edit_word"].setWord(self.views["show_words"].getDisplayedWordAndMeaning()) ,self.views["edit_word"].show())),
                #("Quit", self.root.destroy)
                ]

    def getEditWordActions(self):
        return [("Go back", lambda: (self.views["edit_word"].hide(), self.views["show_words"].show())),
                ("Save", lambda: (self.views["edit_word"].saveNewMeaning(),
                                  self.model.saveWord(self.views["edit_word"].getWordAndMeaning()))),
                ]

    def getNewWordActions(self):
        return [("Go back", lambda: (self.views["new_word"].hide(), self.views["main_menu"].show())),
                ("Translate in Glosbe", lambda: self.model.addWord(*self.translate(self.views["new_word"].getWord()))),
                ]

    def updateWords(self, data):
        print("will update words database")    
        self.views["show_words"].set_words(self.model.getAllWords())
        
    def addWord(self):
        print("will add word: bee to model")
        self.model.addWord("bee", "polish", "pszczoła")
        
    def removeWord(self, wordMeaningTuple):
        self.model.removeWord(wordMeaningTuple[0])
        
    def translate(self, word):
        #return ("ball", "pol", "piłka")
        
        try:
            print(self.translator.translate(word))
        except:
            print("Unable to connect to translator. Check your Internet connection")
        
        
    
    def run(self):
        self.root.mainloop() 
