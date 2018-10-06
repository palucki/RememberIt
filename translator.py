import requests
from phrase import Phrase

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
            
            contents = resp["tuc"]

            for entry in contents:
                if "phrase" in entry and "text" in entry["phrase"]:
                    meaning = entry["phrase"]["text"]
                    break 
                    # if in the future we would like to add multiple meanings:
                    #phrase.add_meaning(meaning)
            phrase = Phrase(word, "pol", meaning)

            return phrase
        else:
            print("Request failed!!!")
