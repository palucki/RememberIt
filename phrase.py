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
