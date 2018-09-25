import requests

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
