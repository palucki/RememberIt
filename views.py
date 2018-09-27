import tkinter
from tkinter import ttk

class BaseView:
    """Base class for all screens"""
    def set_button_commands(self, actions):
        self.actions = actions
        
    def createFrame(self, root, params={}):
        self.frame = tkinter.Frame(root)
        self.frame.configure(background='white') 
        
    def show(self):
        self.frame.pack()
        
    def hide(self):
        self.frame.pack_forget()


class MainMenuView(BaseView):
    """Main menu"""

    def build_into(self, root):
        self.createFrame(root)
        
        self.mainLabel = tkinter.Label(self.frame, 
                                       text="Repeat It - learn new english words easily & efficently",
                                       bg="#339999")
        self.buttons = []

        for (label, cmd) in self.actions:
            self.buttons.append(tkinter.Button(self.frame, 
                                text=label, 
                                fg="black",
                                bg="#33996E",
                                command=cmd))

        self.mainLabel.pack(fill=tkinter.X, ipady=20, padx=10)
        for but in self.buttons:
            but.pack(fill=tkinter.X, pady=10, padx=50)
        
class ShowWordView(BaseView):
    """Showing words menu"""
    
    def build_into(self, root):
        self.createFrame(root)
        
        self.mainLabel = tkinter.Label(self.frame, text="Browse dictionary", bg="#339999")
        
        self.strvariable = tkinter.StringVar()
        
        self.combo = ttk.Combobox(self.frame, textvariable=self.strvariable, width=15)
        self.combo["values"] = ()
        self.combo["state"] = 'readonly'
        self.combo.bind('<<ComboboxSelected>>', self.updateCurrentlyDisplayed)
        
        self.means_label = tkinter.Label(self.frame, text="means", bg="#339999")
        self.meaning = tkinter.Label(self.frame, text="", bg="lightgray")
        
        self.buttons = []

        for (label, cmd) in self.actions:
            self.buttons.append(tkinter.Button(self.frame, 
                                text=label, 
                                fg="black",
                                command=cmd))

        self.mainLabel.pack(fill=tkinter.X, ipady=20, padx=10)
        self.combo.pack()
        
        self.means_label.pack(ipady=5, padx=10)
        self.meaning.pack(ipady=10, padx=10)
        
        self.combo["values"] = ()
        
        for but in self.buttons:
            but.pack(side=tkinter.LEFT, pady=35, padx=10)

    def updateCurrentlyDisplayed(self, event):
        self.meaning["text"] = self.words[self.combo["values"][self.combo.current()]]

    def set_words(self, words):
        self.words = words
        self.updateComboboxList()

    def updateComboboxList(self):
        self.combo["values"] = ()
        for key in self.words.keys():
            print("adding", key)
            self.combo["values"] = self.combo["values"] + (key, )
        
        if len(self.combo["values"]) > 0:
            self.combo.current(0)
            
        self.updateCurrentlyDisplayed(None)
