import tkinter

class Controller:
    """Controler responsible for interactions between data and views"""
    def __init__(self, views, model):
        
        self.initializeRootWindow()
    
        self.model = model
        self.model.phrases.addCallback(self.updateWords)
        
        self.views = views
        
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
        
    def get_actions_for(self, view_name):
        if view_name == "main_menu":
            return self.get_main_menu_actions()
        elif view_name == "show_words":
            return self.get_words_actions()
        else:
            print("No actions found")
            exit(1)

    def get_main_menu_actions(self):
        return  [("Browse words", lambda: (self.views["main_menu"].hide(), self.views["show_words"].show())),
                  ("Add new word", self.addWord),
                 #("Translate phrase", lambda: translator.translate("error")),
                  ("Quit", self.root.destroy)
                 ##("Add phrase to dictionary",
                  ##("Clear dictionary",
                ]

    def get_words_actions(self):
        return [("Go back", lambda: (self.views["show_words"].hide(), self.views["main_menu"].show())),
                ("Quit", self.root.destroy)]

    def updateWords(self, data):
        print("will update words database")    
        self.views["show_words"].set_words(self.model.getAllWords())
        
    def addWord(self):
        print("will add word: bee to model")
        self.model.addWord("bee", "polish", "pszczoła")
        
    def run(self):
        self.root.mainloop() 
