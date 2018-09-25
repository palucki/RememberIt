class Observable:
    def __init__(self, initial={}):
        self.data = initial
        self.callbacks = {}
        
    def addCallback(self, func):
        self.callbacks[func] = 1;
        
    def delCallback(self, func):
        del self.callbacks[func];

    def doCallbacks(self):
        for func in self.callbacks:
            func(self.data)
            
    def setData(self, data):
        self.data = data
        self.doCallbacks()
        
    def getData(self):
        return self.data

